#include <opencv2/opencv.hpp>
#include <iostream>
#include <vector>
#include <cmath>

using namespace std;
using namespace cv;


vector<Mat> cutup(const Mat& scene) {
    Mat s1 = scene.clone(), s2 = scene.clone(), s3 = scene.clone();
    int rows = scene.rows, cols = scene.cols, rows2 = rows/2, cols2 = cols/2;
    Rect tl = Rect(0, 0, cols2, rows2), tr = Rect(cols2, 0, cols2, rows2), bl = Rect(0, rows2, cols2, rows2), br = Rect(cols2, rows2, cols2, rows2);
    Mat TL = scene(tl).clone(), TR = scene(tr).clone(), BL = scene(bl).clone(), BR = scene(br).clone();
    TR.copyTo(s1(br)); // swap TR and BR
    BR.copyTo(s1(tr));
    TR.copyTo(s2(bl)); // swap TR and BL
    BL.copyTo(s2(tr));
    TL.copyTo(s3(bl)); // swap TL and BL
    BL.copyTo(s3(tl));
    return vector<Mat>{s1, s2, s3};
}

Mat my_match(Mat scene, const Mat& waldo) {
    int R = waldo.rows, C = waldo.cols, min_r=0, min_c=0;
    double smallest = INFINITY;
    for (int row=0; row<scene.rows-R; ++row) {
        for (int col=0; col<scene.cols-C; ++col) {
            double diff = 0;
            for (int r=0; r<R; ++r) {
                const uchar* s_ptr = scene.ptr<uchar>(row+r);
                const uchar* w_ptr = waldo.ptr<uchar>(r);
                for (int c=0; c<C; ++c) {
                    uchar wb = w_ptr[c*4], wg = w_ptr[c*4 + 1], wr = w_ptr[c*4 + 2], wa = w_ptr[c*4 + 3];
                    uchar sb = s_ptr[(col+c)*3], sg = s_ptr[(col+c)*3 + 1], sr = s_ptr[(col+c)*3 + 2];
                    if (wa == 255)
                        diff += pow(sb-wb, 2) + pow(sg-wg, 2) + pow(sr-wr, 2);
                }
            }
            if (diff < smallest)
                smallest=diff, min_r=row, min_c=col;
        }
    }
    cout << min_r << " " << min_c << " " << endl;
    rectangle(scene, Point(min_c, min_r), Point(min_c+C, min_r+R), Scalar(255, 0, 0), 2);
    return scene;
}

Mat opencv_find_waldo(Mat scene, const Mat& templ) {
    Mat sceneGray, templGray, result, alphaChannel, mask;
    cvtColor(scene, sceneGray, COLOR_BGR2RGB);
    cvtColor(templ, templGray, COLOR_BGRA2RGB);

    extractChannel(templ, alphaChannel, 3);
    mask = alphaChannel == 255;

    int result_cols = scene.cols - templ.cols + 1, result_rows = scene.rows - templ.rows + 1;
    result.create(result_rows, result_cols, CV_32FC1);
    matchTemplate(sceneGray, templGray, result, TM_SQDIFF, mask);
    normalize(result, result, 0, 1, NORM_MINMAX, -1, Mat());
    
    double minVal, maxVal;
    Point minLoc, maxLoc, matchLoc;
    minMaxLoc(result, &minVal, &maxVal, &minLoc, &maxLoc, Mat());
    matchLoc = minLoc;
    cout << matchLoc << endl;
    rectangle(scene, matchLoc, Point(matchLoc.x + templ.cols, matchLoc.y + templ.rows), Scalar(255, 0, 0), 2, 8, 0);
    return scene;
}

double getAngle(Point2f a, Point2f b, Point2f c, Point2f d) {
    Point2f AB = b-a, CD = d-c;
    return acos((AB.x*CD.x + AB.y*CD.y) / (norm(b - a) * norm(d - c)));
}

void find_tilted() {
    const Mat &templ = imread("templ_QR_cropped.png", IMREAD_UNCHANGED);
    const Mat &original = imread("waldo_scene_with_QR.png");
    // const Mat &test = imread("waldo_QR_tilted.jpg");
    const Mat &test = imread("test_Me.png");
    Mat squareRect, tiltedRect, scaled, rotated, result;
    
    auto qr = QRCodeDetector();
    qr.detect(original, squareRect);
    qr.detect(test, tiltedRect);
    Point2f a(squareRect.at<float>(0, 0), squareRect.at<float>(0, 1));
    Point2f b(squareRect.at<float>(0, 2), squareRect.at<float>(0, 3));
    Point2f c(tiltedRect.at<float>(0, 0), tiltedRect.at<float>(0, 1));
    Point2f d(tiltedRect.at<float>(0, 2), tiltedRect.at<float>(0, 3));
    double scale = norm(b-a) / norm(d-c); // smaller/bigger
    resize(test, scaled, Size(), scale, scale);

    double angle = getAngle(a, b, c, d);
    Point2f center(scaled.cols * 0.5f, scaled.rows * 0.5f); // make it float so no warnings
    Mat matrix = getRotationMatrix2D(center, angle * 180 / CV_PI, 1);
    warpAffine(scaled, rotated, matrix, scaled.size());

    Mat reference = opencv_find_waldo(original, templ);
    Mat out = opencv_find_waldo(rotated, templ);
    // imwrite("original.png", reference);
    // imwrite("test.png", out);
}

int main(int argc, char *argv[]) {
    find_tilted();
    return 0;
}