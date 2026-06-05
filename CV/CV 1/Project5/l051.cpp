#include <iostream>
#include <fstream>
#include <random>
#include <cmath>
#include <sstream>

using namespace std;

string format;
int width=0, height=0, scale=1;

vector<vector<int>> readPPM() {
    ifstream img("image.ppm");
    img >> format >> width >> height >> scale;
    vector<vector<int>> vvn;
    int r,g,b;
    for (int i=0; i<height; i++) {
        vector<int> vn;
        for (int j=0; j<width; j++) {
            img >> r >> g >> b;
            vn.push_back((int)((r+g+b)/3.0 + 0.5));
        }
        vvn.push_back(vn);
    }
    return vvn;
}

auto vvi = readPPM();

void writeGray(const string& filename) {
    ofstream fout(filename);
    fout<<"P3 "<<width<<" "<<height<<" "<<scale<<endl;
    for (auto& vi : vvi) {
        for (int i : vi)
            fout << i << " "<< i << " "<< i << " ";
        fout << endl;
    }
}

void writeSobell(const string& filename) {
    vector<vector<int>> gx, gy;
    vector<int> tmp(width, 0);
    gx.push_back(tmp), gy.push_back(tmp);
    for (int r=1; r<height-1; r++)
        gx.push_back(vector<int>{0}), gy.push_back(vector<int>{0});
    vector<vector<int>> matx{{-1, 0, 1}, {-2, 0, 2}, {-1, 0, 1}}, maty{{-1, -2, -1}, {0, 0, 0}, {1, 2, 1}};
    for (int r=0; r<height-2; r++) {
        for (int c=0; c < width-2; c++) {
            int nx=0, ny=0;
            for (int i=0; i<9; i++) {
                int row=i/3, col=i%3, val=vvi[r+row][c+col];
                nx+=matx[row][col]*val, ny+=maty[row][col]*val;
            }
            gx[r+1].push_back(nx), gy[r+1].push_back(ny);
        }
        gx[r+1].push_back(0), gy[r+1].push_back(0);
    }
    gx.push_back(tmp), gy.push_back(tmp);
    vector<vector<int>> sobell;
    for (int r=0; r<height; r++) {
        vector<int> vi;
        for (int c=0; c<width; c++) {
            int g = (int)(pow(pow(gx[r][c],2)+pow(gy[r][c],2),0.5)+0.5);
            g>250 ? vi.push_back(1) : vi.push_back(0);
        }
        sobell.push_back(vi);
    }
    
    ofstream fout(filename);
    fout<<"P3 "<<width<<" "<<height<<" "<<1<<endl;
    for (auto& vi : sobell) {
        for (int i : vi)
            fout << i << " "<< i << " "<< i << " ";
        fout << endl;
    }
}

void part1() {
    writeGray("imageg.ppm");
    writeSobell("images.ppm");
}

int main() {
    part1();
}