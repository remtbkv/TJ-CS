#include <opencv2/core.hpp>
#include <opencv2/imgcodecs.hpp>
#include <opencv2/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <opencv2/dnn/dnn.hpp>
#include <iostream>

using namespace std;
using namespace cv;
using namespace dnn;        

vector<vector<Mat>> read_digits() {
    Mat img = imread("digits.png");
    vector<vector<Mat>> digits;
    for (int r=0; r<50; r+=5) {
        vector<Mat> temp_digits;
        for (int count=0; count<5; count++) {
            for (int c=0; c<50; c++) {
                int row=20*(r+count), col=c*20;
                Mat digit = img(Rect(col, row, 20, 20));
                resize(digit, digit, Size(28, 28));
                cvtColor(digit, digit, COLOR_BGR2GRAY);
                temp_digits.push_back(digit);
            }
        }
        digits.push_back(temp_digits);
    }
    return digits;
}

vector<pair<float, int>> get_prob_digit(string fn, Mat img=Mat(), string model="lenet") {
    Net nn = readNetFromONNX(model+".onnx");
    if (img.empty()) {
        img = imread(fn);
        cvtColor(img, img, COLOR_BGR2GRAY);
        threshold(img, img, 0, 255, THRESH_BINARY | THRESH_OTSU);
        bitwise_not(img, img);
        resize(img, img, Size(28, 28));
    }
    // imwrite(fn.substr(0,1)+".jpg", img);
    Mat blob = blobFromImage(img, 1.0, Size(28, 28));
    nn.setInput(blob);
    Mat p = nn.forward();

    vector<float> probs;
    for (int i = 0; i < 10; i++)
        probs.push_back(p.at<float>(0, i));
    float max_val = -1.0, sum = 0.0, max_prob = *max_element(probs.begin(), probs.end());
    for (int i = 0; i < 10; i++) {
        probs.at(i) = exp(probs.at(i) - max_prob);
        sum += probs.at(i);
    }
    int max_digit = 0;
    for (int i = 0; i < 10; i++) {
        probs.at(i) = probs.at(i) / sum;
    }
    vector<pair<float, int>> prob_digit;
    for (int i = 0; i < 10; i++)
        prob_digit.push_back(make_pair(probs.at(i), i));
    sort(prob_digit.begin(), prob_digit.end(), greater<pair<float, int>>());
    return prob_digit;
}

int match_digit(string fn, Mat img=Mat(), string model="lenet") {
    auto prob_digit = get_prob_digit(fn, img, model);
    return prob_digit[0].second;
}

void compare_models() {
    vector<vector<Mat>> digits = read_digits();
    int correct=0, disagree=0, agree=0, mwrong=0, lwrong=0;
    vector<int> agree_count(10, 0);
    vector<int> agree_correct_count(10, 0);

    for (int i = 0; i < 10; i++) {
        for (Mat dig : digits[i]) {
            auto m_prob_digit = get_prob_digit("", dig, "mnist-12");
            auto l_prob_digit = get_prob_digit("", dig, "lenet");
            int m = m_prob_digit[0].second, l = l_prob_digit[0].second;
            int mr = m_prob_digit[1].second, lr = l_prob_digit[1].second;
            float ms = m_prob_digit[0].first, ls = l_prob_digit[0].first;
            float mrs = m_prob_digit[1].first, lrs = l_prob_digit[1].first;
            float R = ms / mrs, L = ls / lrs;
            if (m == l) {
                agree++;
                agree_count[i]++;
                if (m==l==i) {
                    correct++;
                    agree_correct_count[i]++;
                }
            }
            else {
                disagree++;
                if (m != i)
                    mwrong++;
                else lwrong++;
                if (m != i && l != i) {
                    // cout << "Digit: " << i << endl;
                    // cout << "MNIST\nIncorrect Winner: " << m << " (softmax = " << ms << ")" << "\nIncorrect runner-up: " << mr << " (softmax = " << mrs << ")" << " Ratio: " << R << endl;
                    // cout << "Lenet\nIncorrect Winner: " << l << " (softmax = " << ls << ")" << "\nIncorrect runner-up: " << lr << " (softmax = " << lrs << ")" << " Ratio: " << L << endl << endl;
                    // imshow("Input Image", dig);
                    // waitKey(0);
                }
            }
        }
    }
    for (int i = 0; i < 10; i++) {
        cout << "Digit: " << i << " Agreed: " << agree_count[i] << " Correct: " << agree_correct_count[i] << endl;
    }
    cout << "Agree: " << agree << endl;
    cout << "Correct: " << correct << endl;
    // cout << "Disagree: " << disagree << endl;
    // cout << "MNIST wrong: " << mwrong << endl;
    // cout << "LeNet wrong: " << lwrong << endl;
}

int main(int argc, char* argv[]) {
    vector<string> files = {"img9_099.png", "4.png", "5.png", "6.png", "7.png"};
    
    for (string fn : files) {
        cout << "File: " << fn << endl;
        compare_models();
        // cout << "Lenet: " << match_digit(fn, Mat(), "lenet") << endl;
        // cout << "Mnist: " << match_digit(fn, Mat(), "mnist-12") << endl << endl;
    }
    return 0;
}
