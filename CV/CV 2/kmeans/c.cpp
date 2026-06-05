#include <opencv2/opencv.hpp>

using namespace std;
using namespace cv;

Mat make_templ(Mat templ) {
    Mat mask;
    inRange(templ, Scalar(0, 0, 0), Scalar(254, 254, 254), mask);
    bitwise_not(mask, mask);
    return mask;
}

tuple<double, Point> match_template(Mat scene, const Mat templ) {
    Mat sceneGray, sceneBW, result;
    cvtColor(scene, sceneGray, COLOR_BGR2GRAY);
    double thresholdValue = 240;
    threshold(sceneGray, sceneBW, thresholdValue, 255, THRESH_BINARY);
    int result_cols = scene.cols - templ.cols + 1, result_rows = scene.rows - templ.rows + 1;
    result.create(result_rows, result_cols, CV_32FC1);
    matchTemplate(sceneBW, templ, result, TM_SQDIFF);
    double minVal, maxVal;
    Point minLoc, maxLoc, matchLoc;
    minMaxLoc(result, &minVal, &maxVal, &minLoc, &maxLoc, Mat());
    matchLoc = minLoc;
    return {abs(minVal), matchLoc};
}

tuple<double, Mat, Point> find_match(Mat scene, vector<Mat> templs) {
    vector<tuple<double, Mat, Point>> matches;
    for (Mat templ : templs) {
        auto [score, matchLoc] = match_template(scene, templ);
        matches.push_back({score, templ, matchLoc});
    }
    sort(matches.begin(), matches.end(), [](const auto &a, const auto &b) { return get<0>(a) < get<0>(b); });
    return matches.front();
}

void count_matches(vector<Mat> scenes, vector<Mat> templs) {
    for (Mat scene : scenes) {
        auto [score, templ_match, matchLoc] = find_match(scene, templs);
        Mat combined, templ_full;
        Mat scene_drawn = scene.clone(), scene_check = scene.clone();
        Point match2(matchLoc.x + templ_match.cols, matchLoc.y + templ_match.rows);
        rectangle(scene_drawn, matchLoc, match2, Scalar(255, 0, 0));
        rectangle(scene_check, matchLoc, match2, Scalar(255, 255, 255), -1);
        
        auto [MATCH_WHITE, _] = match_template(imread("blank.png"), templ_match);
        double score_original = score, epsilon_score = 5e7;
        int matches = 1;
        tie(score, matchLoc) = match_template(scene_check, templ_match);
        
        imshow("out", scene_drawn);
        waitKey(0);
        
        while (abs(score - score_original) < epsilon_score && abs(score - MATCH_WHITE)) {
            matches++;
            match2 = Point(matchLoc.x + templ_match.cols, matchLoc.y + templ_match.rows);
            rectangle(scene_drawn, matchLoc, match2, Scalar(255, 0, 0));
            rectangle(scene_check, matchLoc, match2, Scalar(255, 255, 255), -1);
            tie(score, matchLoc) = match_template(scene_check, templ_match);
            imshow("out", scene_drawn);
            waitKey(0);
        }
        cout << "Matched " << matches << " times" << endl;
        int top = (scene.rows - templ_match.rows) / 2;
        int bottom = scene.rows - templ_match.rows - top;
        int left = (scene.cols - templ_match.cols) / 2;
        int right = scene.cols - templ_match.cols - left;
        copyMakeBorder(templ_match, templ_full, top, bottom, left, right, BORDER_CONSTANT, Scalar(255, 255, 255));
        cvtColor(templ_full, templ_full, COLOR_GRAY2BGR);
        hconcat(scene_drawn, templ_full, combined);
        imshow("out", combined);
        waitKey(0);
    }
}

void match_all(vector<Mat> scenes, vector<Mat> templs) {
    for (Mat scene : scenes) {
        vector<tuple<double, Mat, Point>> matches;
        for (Mat templ : templs) {
            auto [score, matchLoc] = match_template(scene, templ);
            matches.push_back({score, templ, matchLoc});
        }
        sort(matches.begin(), matches.end(), [](const auto &a, const auto &b) { return get<0>(a) < get<0>(b); });
        auto [score, templ_match, matchLoc] = matches.front();
        Mat combined, templ_full;
        Mat scene_drawn = scene.clone();
        rectangle(scene_drawn, matchLoc, Point(matchLoc.x + templ_match.cols, matchLoc.y + templ_match.rows), Scalar(255, 0, 0), 1, 8, 0);
        int top = (scene.rows - templ_match.rows) / 2;
        int bottom = scene.rows - templ_match.rows - top;
        int left = (scene.cols - templ_match.cols) / 2;
        int right = scene.cols - templ_match.cols - left;
        copyMakeBorder(templ_match, templ_full, top, bottom, left, right, BORDER_CONSTANT, Scalar(255, 255, 255));
        cvtColor(templ_full, templ_full, COLOR_GRAY2BGR);
        hconcat(scene_drawn, templ_full, combined);
        imshow("out", combined);
        waitKey(0);
    }
}

void make_initial_templs() {
    vector<string> templs_fn = {"t1.png", "t13.png", "t19.png", "t28.png", "t37.png", "t46.png", "t55.png", "t64.png", "t73.png"};
    for (string t : templs_fn) {
        Mat tmp = make_templ(imread("set81/"+t.substr(1)));
        Point tl(97, 18);
        Point br(159, 145);
        Rect roi(tl, br);
        Mat smaller = tmp(roi);
        // imshow(t, smaller);
        // waitKey(0); 
        imwrite(t, smaller);
    }
    
}

void match_color(vector<Mat> scenes) {
    for (Mat scene : scenes) {
        double blue, green, red;
        int count = 0;
        for (int i = 0; i < scene.rows; i++) {
            for (int j = 0; j < scene.cols; j++) {
                Vec3b pix = scene.at<Vec3b>(i, j);
                double dist_color = pow(pix[0]-127, 2) + pow(pix[1]-127, 2) + pow(pix[2]-127, 2);
                double dist_white = pow(pix[0]-255, 2) + pow(pix[1]-255, 2) + pow(pix[2]-255, 2);
                if (dist_color < dist_white) {
                    blue += pix[0], green += pix[1], red += pix[2];
                    count++;
                }
            }
        }
        blue /= count, green /= count, red /= count;
        int mid_col = scene.cols / 2;
        Mat left_color(scene.rows, mid_col, scene.type(), Scalar(blue, green, red));
        Mat right_white(scene.rows, scene.cols - mid_col, scene.type(), Scalar(255, 255, 255));
        Mat filled, out;
        hconcat(left_color, right_white, filled);
        hconcat(scene, filled, out);
        imshow("out", out);
        waitKey(0);
    }
}

int main() {
    int match_everything = 1;
    if (!match_everything)
        make_initial_templs();
    else {
        vector<string> templs_fn = {"t1.png", "t13.png", "t19.png", "t28.png", "t37.png", "t46.png", "t55.png", "t64.png", "t73.png"};
        vector<Mat> templs, scenes;
        for (string t : templs_fn)
            templs.push_back(imread(t, IMREAD_UNCHANGED));
        for (int i = 1; i < 82; i++)
            scenes.push_back(imread("set81/" + to_string(i) + ".png"));
        // count_matches(scenes, templs);
        match_color(scenes);
    }
    return 0;
}