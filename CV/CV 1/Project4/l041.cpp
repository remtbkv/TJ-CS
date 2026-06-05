#include <iostream>
#include <fstream>
#include <random>
#include <cmath>
#include <sstream>
#include <algorithm>
#include <iomanip>
#include <set>


using namespace std;

random_device device;
default_random_engine engine(device());
uniform_real_distribution<double> rando(0.0, 1.0);
double rd() {
    return rando(engine);
};

const int ppmsize = 400;
const double epsilon = 1e-10;

class Point {
    private:
        double x, y;
        int r=255, g=255, b=255;
    public:
        Point() {
            x=0.0, y=0.0;
        }
        Point(double x1, double y1) {
            x=x1, y=y1;
        }
        double getX() const {
            return x;
        }
        double getY() const {
            return y;
        }
        int getSX() const {
            return int(x*ppmsize);
        }
        int getSY() const{
            return int(y*ppmsize);
        }
        void illum() {
            r=0, g=0, b=0;
        }
        void illum (int red, int green, int blue) {
            r=red, g=green, b=blue;
        }
        string getColor() const{
            return to_string(r)+" "+to_string(g)+" "+to_string(b);
        }
        string out() const {
            ostringstream s;
            s << fixed;
            s.precision(23);
            s << "(" << x << "," << y << ")";
            return s.str();
        }
        bool operator==(const Point& other) const {
            return x==other.getX() && y==other.getY();
        }
        bool operator<(const Point& other) const {
            return (x < other.getX()) || ((x == other.getX()) && (y < other.getY()));
        }
};

Point(*ppm)[ppmsize] = new Point[ppmsize][ppmsize];

void writePPM(const string &filename) {
    ofstream fout(filename);
    fout<<"P3 "<<ppmsize<<" "<<ppmsize<<" 255"<<endl;
    for (int row=ppmsize-1; row >= 0; row--) {
        for (int col=0; col<ppmsize; col++)
            fout<< ppm[col][row].getColor() + " ";
        fout<<endl;
    }
    fout.close();
    delete[] ppm;
}

class Render {
    public:
        static void segment(Point a, Point b) { // precondition: A and B are valid points
            int x1 = a.getSX(), y1 = a.getSY(), x2 = b.getSX(), y2 = b.getSY(), dX = abs(x1 - x2) + 1, dY =
                    abs(y1 - y2) + 1, e = dY - dX;
            if (x1 == x2)
                for (int y = min(y1, y2); y < max(y1, y2); y++)
                    ppm[x1][y].illum();
            else if (y1 == y2)
                for (int x = min(x1, x2); x < max(x1, x2); x++)
                    ppm[x][y1].illum();
            else if (dX >= dY) {
                if (x1 > x2) { // switches A and B so A.x is smaller
                    int tx = x1, ty = y1;
                    x1 = x2, x2 = tx, y1 = y2, y2 = ty;
                }
                int p = 1;
                if (y2 < y1)
                    p = -1;
                for (int x = x1; x <= x2; x++) {
                    ppm[x][y1].illum();
                    if (e >= 0)
                        y1 += p, e -= dX;
                    e += dY;
                }
            } else {
                if (y1 > y2) { // switches A and B so A.y is smaller
                    int tx = x1, ty = y1;
                    x1 = x2, x2 = tx, y1 = y2, y2 = ty;
                }
                e *= -1;
                int p = 1;
                if (x2 < x1)
                    p = -1;
                for (int y = y1; y <= y2; y++) {
                    ppm[x1][y].illum();
                    if (e >= 0)
                        x1 += p, e -= dY;
                    e += dX;
                }
            }
        }
        static void circle(Point c, double radius, int red, int green, int blue) {
            int cx=c.getSX(), cy=c.getSY(), r=int(radius*ppmsize), xmax=(int)ceil(radius*ppmsize/pow(2,0.5)-0.5);
            int y=r, ty=2*y-1, y2=y*y, y2_n=y2;
            if (r>5) xmax++;
            for (int x=0; x<=xmax; x++) {
                if (y2 - y2_n >= ty)
                    y2 -= ty, y -= 1, ty -= 2;
                y2_n -= 2*x-3;
                double Xu=ppmsize-cx, Xd=-cx, Yu=ppmsize-cy, Yd=-cy;
                if (x>=Xd && x<Xu) {
                    if (y>=Yd && y<Yu) ppm[x+cx][y+cy].illum(red, green, blue);
                    if (-y>=Yd && -y<Yu) ppm[x+cx][-y+cy].illum(red, green, blue);
                }
                if (-x>=Xd && -x<Xu) {
                    if (y>=Yd && y<Yu) ppm[-x+cx][y+cy].illum(red, green, blue);
                    if (-y>=Yd && -y<Yu) ppm[-x+cx][-y+cy].illum(red, green, blue);
                }
                if (y>=Xd && y<Xu) {
                    if (x>=Yd && x<Yu) ppm[y+cx][x+cy].illum(red, green, blue);
                    if (-x>=Yd && -x<Yu) ppm[y+cx][-x+cy].illum(red, green, blue);
                }
                if (-y>=Xd && -y<Xu) {
                    if (x>=Yd && x<Yu) ppm[-y+cx][x+cy].illum(red, green, blue);
                    if (-x>=Yd && -x<Yu) ppm[-y+cx][-x+cy].illum(red, green, blue);
                }
            }
        }
};

double dist(Point A, Point B) {
    return sqrt(pow(A.getX()-B.getX(),2) + pow(A.getY()-B.getY(),2));
}

void part0() {
    ofstream pout("points.txt");
    for (int i=0; i<60; i++) {
        pout << setprecision(23) << rd() << "  " << rd() << endl;
    }
}

double slope(const Point& A, const Point& B) {
    return (B.getY() - A.getY()) / (B.getX() - A.getX());
}

double yint(const Point& A, double m) {
    return A.getY() - m * A.getX();
}

bool isgreaterthan(double a, double b) {
    return a-b>epsilon;
}

bool islessthan(double a, double b) {
    return b-a>epsilon;
}

set<Point> points_right(Point& A, Point& B, vector<Point>& vp) {
    double m = slope(A, B), b = yint(A, m);
    bool b_to_right = B.getX()>A.getX();
    set<Point> toRight;
    for (Point& pt : vp)
        if ((b_to_right && islessthan(pt.getY(), m*pt.getX()+b)) || (!b_to_right && isgreaterthan(pt.getY(), m*pt.getX()+b)))
            toRight.insert(pt);
    return toRight;
}

void find_hull(set<Point>& s, Point& A, Point& B, vector<Point>& p, vector<Point>& hull) {
    if (!s.empty()) {
        double a = slope(A, B), b = -1, c = yint(A, a), maxdist=0;
        Point maxpt;
        for (Point pt : s) {
            double d = abs(a*pt.getX()+b*pt.getY()+c)/(sqrt(a*a+b*b));
            if (d>maxdist)
                maxdist = d, maxpt = pt;
        }
        hull.insert(find(hull.begin(), hull.end(), A)+1, maxpt);
        set<Point> s1 = points_right(A, maxpt, p), s2 = points_right(maxpt, B, p);
        find_hull(s1, A, maxpt, p, hull);
        find_hull(s2, maxpt, B, p, hull);
    }
}

void part1() {
    part0();
    vector<Point> p, hull;
    ifstream pin("points.txt");
    double x, y;
    while (pin >> x >> y)
        p.emplace_back(x, y);
    Point& minp = *min_element(p.begin(), p.end());
    Point& maxp = *max_element(p.begin(), p.end());
    hull.push_back(minp), hull.push_back(maxp), hull.push_back(minp);
    set<Point> s1 = points_right(minp, maxp, p), s2 = points_right(maxp, minp, p);
    find_hull(s1, minp, maxp, p, hull);
    find_hull(s2, maxp, minp, p, hull);
    for (Point& pt : p) {
        if (find(hull.begin(), hull.end(), pt)!=hull.end())
            Render::circle(pt, 3/800.0, 255, 0, 0), Render::circle(pt, 4/800.0, 255, 0, 0);
        else
            Render::circle(pt, 3/800.0, 0, 0, 0);
    }

    for (int i=0; i<(int)hull.size()-1; i++)
        Render::segment(hull[i], hull[i+1]);
    writePPM("quickhull.ppm");
}

int main() {
    part1();
}