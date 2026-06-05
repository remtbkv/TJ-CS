#include <iostream>
#include <fstream>
#include <random>
#include <cmath>
using namespace std;

string format;
int width=0, height=0, scale=1;
double epsilon = 1e-6;

vector<vector<int>> readPPM(const string& infile) {
    ifstream img(infile);
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

void writeGray(vector<vector<int>> vvi, const string& filename) {
    ofstream fout(filename);
    fout<<"P3 "<<width<<" "<<height<<" "<<scale<<endl;
    for (auto& vi : vvi) {
        for (int i : vi)
            fout << i << " "<< i << " "<< i << " ";
        fout << endl;
    }
}

void promote(vector<vector<int>>& s, int r, int c) {
    int w=(int)s[0].size(),h=(int)s.size(), ld=c-1, rd=c+1, ud=r-1, dd=r+1;
    if (r>=0 && r<h && c>=0 && c<w) {
        if (s[r][c]==1) {
            if (ld>=0) {
                if (s[r][ld]>=2) // left
                    s[r][c] = 3;
                if (ud>=0 && s[ud][ld]>=2) // up-left
                    s[r][c] = 3;
                if (dd<h && s[dd][ld]>=2) // down-left
                    s[r][c] = 3;
            }
            if (rd<w) {
                if (s[r][rd]>=2) // right
                    s[r][c] = 3;
                if (ud>=0 && s[ud][rd]>=2) // up-right
                    s[r][c] = 3;
                if (dd<h && s[dd][rd]>=2) // down-right
                    s[r][c] = 3;
            }
            if (ud>=0 && s[ud][c]>=2) // up
                s[r][c] = 3;
            if (dd<h && s[dd][c]>=2) // down
                s[r][c] = 3;
        }
        else if (s[r][c]==2)
            s[r][c]=3;
        
        if (ld>=0) { // left
            if (s[r][ld]==2 || s[r][ld]==1)
                promote(s, r, ld);
            if (ud>=0 && (s[ud][ld]==2 || s[ud][ld]==1)) // up-left
                promote(s, ud, ld);
            if (dd<h && (s[dd][ld]==2 || s[dd][ld]==1)) // down-left
                promote(s, dd, ld);
        }
        if (rd<w) { // right
            if (s[r][rd]==2 || s[r][rd]==1)
                promote(s, r, rd);
            if (ud>=0 && (s[ud][rd]==2 || s[ud][rd]==1)) // up-right
                promote(s, ud, rd);
            if (dd<h && (s[dd][rd]==2 || s[dd][rd]==1)) // down-right
                promote(s, dd, rd);
        }
        if (ud>=0 && (s[ud][c]==2 || s[ud][rd]==1)) // up
            promote(s, ud, c);
        if (dd<h && (s[dd][c]==2 || s[dd][rd]==1)) // down
            promote(s, dd, c);
    }
}

void binarize(vector<vector<int>>& downgraded) {
    for (int i=0; i<(int)downgraded.size(); i++)
        for (int j=0; j<(int)downgraded[0].size(); j++)
            if (downgraded[i][j]==1)
                downgraded[i][j] = 0;
            else if (downgraded[i][j]==3)
                downgraded[i][j] = 1;
}

vector<vector<int>> makeSobell(const vector<vector<int>>& vvi, int t) {
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
            g>t ? vi.push_back(1) : vi.push_back(0);
        }
        sobell.push_back(vi);
    }
    return sobell;
}

vector<vector<int>> makeHyst(const vector<vector<int>>& vvi, int lt, int ht) {
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
            if (g>=ht)
                vi.push_back(2);
            else if (g<lt)
                vi.push_back(0);
            else
                vi.push_back(1);
        }
        sobell.push_back(vi);
    }
    return sobell;
}

void writeSobell(const vector<vector<int>>& sobell, const string& filename) {
    ofstream fout(filename);
    fout<<"P3 "<<width<<" "<<height<<" "<<1<<endl;
    for (auto& vi : sobell) {
        for (int i : vi)
            fout << i << " "<< i << " "<< i << " ";
        fout << endl;
    }
}

void part1() {
    auto vvi = readPPM("image.ppm");
    writeGray(vvi, "imageg.ppm");
    writeSobell(makeSobell(vvi, 250), "images.ppm");
}

void part2(int argc, char* argv[]) {
    int lt = 125, ht = 225;
    string infile = "image.ppm", outfile="image1.ppm";
    if (argc>0) {
        for (int i = 1; i < argc; i += 2) {
            string var = argv[i];
            if (var == "-f")
                infile = argv[i + 1];
            else if (var == "-lt")
                lt = stoi(argv[i + 1]);
            else if (var == "-ht")
                ht = stoi(argv[i + 1]);
            else if (var == "-of")
                outfile = argv[i + 1];
        }
    }
    auto vvi = readPPM(infile);
    auto sobell = makeHysteresis(vvi, lt, ht);
    for (int r=0; r<(int)sobell.size(); r++)
        for (int c=0; c<(int)sobell[0].size(); c++)
            if (sobell[r][c]==2)
                promote(sobell, r, c);
    makeGood(sobell);
    writeSobell(sobell, outfile);
}

int main(int argc, char* argv[]) {
    part2(argc, argv);
}