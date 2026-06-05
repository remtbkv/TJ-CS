#include <opencv2/core.hpp>
#include <opencv2/imgcodecs.hpp>
#include <opencv2/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>

#include <iostream>
#include <stdlib.h>
#include <time.h>

using namespace std;
using namespace cv;

int main(int argc, char *argv[]) {
    Mat img(Size(100, 100), CV_8U, Scalar(255));
    
    long seed = time(NULL);
    // cout << seed << endl;
    srand(seed);

    int x = rand() % 100, y = rand() % 100;
    img.at<uchar>(y, x) = (uchar)0;
    // cout << x << " " << y << endl;
    vector<pair<int, int>> points;
    points.push_back(make_pair(x, y));
    
    int t = 1, j = 1;
    Mat m = img.clone();
    while (t < 9000) {
        for (auto existing_point : points) {
            // if 5 out of 8 surrounding points are black, then dont create new point
            int x = existing_point.first;
            int y = existing_point.second;
            
            int full = 0;
            full += (int)(m.at<uchar>(y - 1, x - 1)==0);
            full += (int)(m.at<uchar>(y, x - 1)==0);
            full += (int)(m.at<uchar>(y + 1, x - 1) == 0);
            full += (int)(m.at<uchar>(y - 1, x + 1) == 0);
            full += (int)(m.at<uchar>(y, x + 1) == 0);
            full += (int)(m.at<uchar>(y + 1, x + 1) == 0);
            full += (int)(m.at<uchar>(y - 1, x) == 0);
            full += (int)(m.at<uchar>(y + 1, x) == 0);

            if (full < 5 && t < 9000) {
                pair<int, int> point = make_pair(rand() % 100, rand() % 100);
                while (find(points.begin(), points.end(), point) != points.end()) {
                    point.first = rand() % 100;
                    point.second = rand() % 100;
                }
                m.at<uchar>(point.second, point.first) = (uchar)0;
                t++;
                points.push_back(point);
            }
        }
        cout << t << endl;
    }
    imwrite("output.png", m);
    return 0;
}