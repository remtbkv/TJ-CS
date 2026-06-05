#include <iostream>
#include <fstream>
#include <random>
#include <cmath>
#include <sstream>
#include <algorithm>
#include <tuple>
#include <iomanip>

using namespace std;

random_device device;
default_random_engine engine(device());
uniform_real_distribution<double> rando(0.0, 1.0);
double rd() {
    return rando(engine);
};

class Point {
    private:
        double x, y;
        int r=0, g=0, b=0;
    public:
        Point() {
            x=0.0, y=0.0;
        }
        Point(double x1, double y1) {
            x=x1, y=y1;
        }
        double getX() {
            return x;
        }
        double getY() {
            return y;
        }
        int getSX() {
            return int(x*800);
        }
        int getSY() {
            return int(y*800);
        }
        void illum() {
            r=255, g=255, b=255;
        }
        string getColor() {
            return to_string(r)+" "+to_string(g)+" "+to_string(b);
        }
        string out() {
            ostringstream s;
            s << fixed;
            s.precision(17);
            s << "(" << x << "," << y << ")";
            return s.str();
        }
        bool operator<(Point& other) {
            return (x < other.getX()) || ((x == other.getX()) && (y < other.getY()));
        }
};

class Line {
    private:
        Point A, B;
        double m, b;
        
    public:
        Line(Point pA, Point pB) {
            A=pA, B=pB;
            double x1=pA.getX(), y1=pA.getY(), x2=pB.getX(), y2=pB.getY();
            m = (y2-y1)/(x2-x1), b = y1-m*x1;
        }
        Line(double m1, double b1) {
            m = m1, b= b1;
        }
        Point getPA() {
            return A;
        }
        Point getPB() {
            return B;
        }
        double getM() {
            return m;
        }
        double getB() {
            return b;
        }
        string out() {
            return "y = "+to_string(m)+"x + "+to_string(b);
        }
        Point intersect(Line other) {
            double x = (other.getB()-b)/(m-other.getM()), y=m*x+b;
            return {x, y};
        }
        Line perp(Point p) {
            return {-1/m, p.getY()+p.getX()/m};
        }
};

Point(*ppm)[800] = new Point[800][800];

void writePPM(const string &filename) {
    ofstream fout(filename);
    fout<<"P3 800 800 255"<<endl;
    for (int row=799; row >= 0; row--) {
        for (int col=0; col < 800; col++)
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
        static void line(Line l) {
            double m = l.getM(), b=l.getB();
            auto check = [](double x) -> double {
                return (x==1.0) ? 799/800.0 : x;
            };
            double bx=check(-b/m), tx=check((1 - b)/m), ly=check(b), ry=check(m + b);
            vector<Point> v;
            if (tx >= 0 && tx < 1) v.emplace_back(tx, 799 / 800.0);
            if (bx >= 0 && bx < 1) v.emplace_back(bx, 0.0);
            if (ly >= 0 && ly < 1) v.emplace_back(0.0, ly);
            if (ry >= 0 && ry < 1) v.emplace_back(799 / 800.0, ry);
            segment(v.at(0), v.at(1));
        }
        static void circle(Point c, double radius) {
            int cx=c.getSX(), cy=c.getSY(), r=int(radius*800), xmax=(int)ceil(radius*800/pow(2,0.5)-0.5);
            int y=r, ty=2*y-1, y2=y*y, y2_n=y2;
            if (r>5) xmax++;
            for (int x=0; x<=xmax; x++) {
                if (y2 - y2_n >= ty)
                    y2 -= ty, y -= 1, ty -= 2;
                y2_n -= 2*x-3;
                double Xu=800-cx, Xd=-cx, Yu=800-cy, Yd=-cy;
                if (x>=Xd && x<Xu) {
                    if (y>=Yd && y<Yu) ppm[x+cx][y+cy].illum();
                    if (-y>=Yd && -y<Yu) ppm[x+cx][-y+cy].illum();
                }
                if (-x>=Xd && -x<Xu) {
                    if (y>=Yd && y<Yu) ppm[-x+cx][y+cy].illum();
                    if (-y>=Yd && -y<Yu) ppm[-x+cx][-y+cy].illum();
                }
                if (y>=Xd && y<Xu) {
                    if (x>=Yd && x<Yu) ppm[y+cx][x+cy].illum();
                    if (-x>=Yd && -x<Yu) ppm[y+cx][-x+cy].illum();
                }
                if (-y>=Xd && -y<Xu) {
                    if (x>=Yd && x<Yu) ppm[-y+cx][x+cy].illum();
                    if (-x>=Yd && -x<Yu) ppm[-y+cx][-x+cy].illum();
                }
            }
        }
};

double dist(Point A, Point B) {
    return sqrt(pow(A.getX()-B.getX(),2) + pow(A.getY()-B.getY(),2));
}

double heron(Point A, Point B, Point C) {
    double a=dist(A,B), b=dist(B,C), c=dist(C,A), s=(a+b+c)/2;
    return sqrt(s*(s-a)*(s-b)*(s-c));
}

bool to_remove(char c) {
    return c=='(' || c==')' || c==' ';
}

vector<string> split(const string &s, const char &del) {
    stringstream ss(s);
    vector<string> v;
    string token;
    while (getline(ss, token, del))  v.push_back(token);
    return v;
}

void part1() {
    Point A(rd(),rd()), B(rd(),rd()), C(rd(),rd());
    ofstream lout("log.txt"), pout("points.txt");
    string tri = A.out() +"\n"+ B.out() +"\n"+ C.out() + "\n";
    cout << tri, lout << tri;
    double epsilon = 1.0/(800*2);
    while (true) {
        Point p(rd(), rd());
        string tp = "testing point " + p.out() +"\n";
        cout << tp, lout << tp;
        if (abs(heron(A,B,p)+heron(B,C,p)+heron(C,A,p)-heron(A,B,C))<epsilon) {
            pout<<A.out()<<" , "<<B.out()<<" , "<<C.out()<<" , "<<p.out();
            break;
        }
    }
}

void squareCalc(vector<Point> v, vector<tuple<vector<Point>, vector<Line>, double>> &result) {
    Point p1 = v.at(0), p2 = v.at(1), p3 = v.at(2), p4 = v.at(3);
    Line l1(p1, p3);
    double dispX = abs(p1.getY()-p3.getY()), dispY = abs(p1.getX()-p3.getX());
    double x = p2.getX(), y = p2.getY(), m = -1/l1.getM(); // line "2"
    if (m<0)
        dispY *= -1;
    for (int l=0; l<2; l++) {
        if (l == 1)
            dispX *= -1, dispY *= -1;
        Point pE(x + dispX, y + dispY);
        Line l2(pE, p4), l3 = l2.perp(p1), l4 = l2.perp(p3), l5 = l3.perp(p2);
        Point v1 = l2.intersect(l3), v2 = l3.intersect(l5), v3 = l5.intersect(l4), v4 = l4.intersect(l2);
        result.emplace_back(vector<Point>{v1, v2, v3, v4}, vector<Line>{l2, l3, l4, l5}, pow(dist(v1, v2), 2));
    }
}

void part2() {
    ifstream pin("points.txt");
    string s;
    getline(pin, s);
    s.erase(remove_if(s.begin(), s.end(), to_remove), s.end());
    vector<string> v(split(s, ','));
    vector<Point> p;
    for (int i=0; i<8; i+=2) p.emplace_back(stod(v.at(i)), stod(v.at(i+1)));
    vector<Point> sp(p);
    vector<tuple<vector<Point>, vector<Line>, double>> result;
    
    sort(p.begin(), p.end());
    do squareCalc(p, result);
    while (next_permutation(p.begin(), p.end()));
    
    // in >= c++14 u can use auto instead of specificying type parameter
    sort(result.begin(), result.end(), [](tuple<vector<Point>, vector<Line>, double>& l, tuple<vector<Point>, vector<Line>, double>& r){return get<2>(l)<get<2>(r);});
    auto newEnd = unique(result.begin(), result.end(), [](tuple<vector<Point>, vector<Line>, double>& l, tuple<vector<Point>, vector<Line>, double>& r) {return abs(get<2>(l)-get<2>(r)) < pow(10,-7);});
    result.erase(newEnd, result.end());
    
    ofstream oout("output.txt");
    for (int i=0; i<4; i++) {
        oout << sp.at(i).out();
        if (i<3) oout << " , ";
        else oout << endl;
    }
    for (auto t: result) {
        vector<Point> r = get<0>(t);
        for (int i=0; i<4; i++) {
            oout <<r.at(i).out();
            if (i<3) oout << " , ";
        }
        oout << " Area = " << setprecision(17) << get<2>(t) << endl;
    }
    
    for (auto vertex : get<0>(result.at(0))) Render::circle(vertex, 4/800.0);
    for (auto l : get<1>(result.at(0))) Render::line(l);
    for (auto point : p) Render::circle(point, 3/800.0);
    
    writePPM("output.ppm");
}

int main() {
//    part1();
    part2();
}