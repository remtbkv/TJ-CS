#include <opencv2/opencv.hpp>
#include <iostream>
#include <vector>
#include <cmath>
#include <tuple>

using namespace std;
using namespace cv;

tuple<double, int, int> my_match(Mat scene, const Mat& templ) {
    int R = templ.rows, C = templ.cols, min_r=0, min_c=0;
    int start_row = 0, end_row =scene.rows/2, start_col = scene.cols*1/4, end_col = scene.cols*3/4;
    // int start_row = 0, end_row =scene.rows-R, start_col = 0, end_col = scene.cols-C;
    double smallest = INFINITY;

    for (int row=start_row; row<end_row; ++row) {
        for (int col=start_col; col<end_col; ++col) {
            double diff = 0;
            for (int r = 0; r < R; ++r) {
                for (int c = 0; c < C; ++c) {
                    Vec4b w_pixel = templ.at<Vec4b>(r, c);
                    Vec3b s_pixel = scene.at<Vec3b>(row + r, col + c);
                    uchar wb = w_pixel[0], wg = w_pixel[1], wr = w_pixel[2], wa = w_pixel[3];
                    uchar sb = s_pixel[0], sg = s_pixel[1], sr = s_pixel[2];
                    if (wa == 255)
                        diff += pow(sb - wb, 2) + pow(sg - wg, 2) + pow(sr - wr, 2);
                }
            }
            if (diff < smallest)
                smallest=diff, min_r=row, min_c=col;
        }
    }
    return make_tuple(smallest, min_r, min_c);
}

tuple<double, int, int> opencv_match(Mat scene, const Mat &templ) {
    const int cols = scene.cols;
    scene = scene(Range(0,scene.rows/2), Range(scene.cols/4, scene.cols*3/4));
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
    return make_tuple(abs(minVal), matchLoc.y, matchLoc.x+cols/4);
}

Mat rotateImg(const Mat &img, int n) {
    Point center = Point(img.cols / 2, img.rows / 2);
    Mat rotated = img;
    for (int i = 0; i < n; ++i) {
        Mat rot_mat = getRotationMatrix2D(center, 90, 1);
        Rect bounding_box = RotatedRect(Point2f(center), rotated.size(), 90).boundingRect();
        Mat temp;
        warpAffine(rotated, temp, rot_mat, bounding_box.size(), INTER_LINEAR, BORDER_CONSTANT, Scalar(255, 255, 255));
        rotated = temp;
    }
    return rotated;
}

void rotate() {
    int scale = 5;
    vector<string> inps = {"a1.png", "a2.png", "a3.png", "a4.png", "a5.png", "a6.png", "a7.png", "a8.png", "a9.png"};
    vector<tuple<Mat, int>> templs;
    int templ_cols=0, templ_rows=0;
    for (int i = 0; i < inps.size(); ++i) {
        Mat templ = imread(inps[i], IMREAD_UNCHANGED);
        Mat templ_small;
        resize(templ, templ_small, Size(), 1.0/scale, 1.0/scale, INTER_AREA);
        if (!templ_cols) templ_cols = templ_small.cols;
        if (!templ_rows) templ_rows = templ_small.rows;
        templs.push_back(make_tuple(templ_small, i+1));
    }

    vector<string> tests = {"in1.png", "in2.png", "in3.png"};
    for (string scene_fn : tests) {
        Mat scene = imread(scene_fn);
        resize(scene, scene, Size(), 1.0 / scale, 1.0 / scale, INTER_AREA);
        vector<tuple<double, int, int, int>> matches;
        string templ_matches = "Matched numbers: ";
        for (int i = 0; i < 4; i++) {
            Mat rot_scene = rotateImg(scene, i);
            vector<tuple<double, int, int, int>> matches;
            for (auto& templ_tuple : templs) {
                auto [templ, templ_n] = templ_tuple;
                auto [score, r, c] = opencv_match(rot_scene, templ);
                matches.push_back(make_tuple(score, r, c, templ_n));
            }
            sort(matches.begin(), matches.end(), [](const auto &a, const auto &b) { return get<0>(a) < get<0>(b); });
            auto [score, row, col, templ_n] = matches.front();
            Point p1(col, row), p2(col + templ_cols, row + templ_rows);
            rectangle(rot_scene, p1, p2, Scalar(255, 0, 0), 2);
            scene = rot_scene;
            templ_matches += to_string(templ_n) + " ";
        }
        cout << templ_matches << endl;
        imshow("out", scene);
        waitKey(0);
    }
}

void single() {
    vector<string> inps = {"a1.png", "a2.png", "a3.png", "a4.png", "a5.png", "a6.png", "a7.png", "a8.png", "a9.png", "a1.png"};
    vector<Mat> templs;
    for (string t : inps)
        templs.push_back(imread(t, IMREAD_UNCHANGED));
    int scale = 10;
    vector<string> tests = {"in1.png", "in2.png", "in3.png"};
    for (string scene_fn : tests) {
        Mat scene = imread(scene_fn);
        Mat scene_small, templ_small;
        resize(scene, scene_small, Size(), 1.0 / scale, 1.0 / scale, INTER_AREA);
        vector<tuple<double, int, int, Mat>> matches;
        for (Mat templ : templs) {
            resize(templ, templ_small, Size(), 0.1, 0.1, INTER_AREA);
            // auto [score, r, c] = my_match(scene_small, templ_small);
            auto [score, r, c] = opencv_match(scene_small, templ_small);
            matches.push_back(make_tuple(score, r, c, templ_small));
        }
        cout << endl;
        sort(matches.begin(), matches.end(), [](const auto &a, const auto &b) { return get<0>(a) < get<0>(b); });
        auto [score, row, col, templ] = matches.front();
        Point p1(col, row), p2(col + templ.cols, row + templ.rows);
        rectangle(scene_small, p1, p2, Scalar(255, 0, 0), 2);
        imshow("out", scene_small);
        waitKey(0);
    }
}

int main() {
    // single();
    rotate();
    return 0;
}