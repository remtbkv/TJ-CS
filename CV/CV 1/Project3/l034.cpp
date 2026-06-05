#include <iostream>
#include <fstream>
#include <random>
#include <cmath>
#include <sstream>
#include <algorithm>
#include <iomanip>
#include <list>
#include <chrono>
#include<unordered_map>


using namespace std;
typedef unsigned long long int li;

string Bout, Rout, Oout, Nout;

random_device device;
default_random_engine engine(device());
uniform_real_distribution<double> rando(0.0, 1.0);
double rd() {
    return rando(engine);
};

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
        int getSX() {
            return int(x*800);
        }
        int getSY() {
            return int(y*800);
        }
        void illum() {
            r=0, g=0, b=0;
        }
        void illum (int red, int green, int blue) {
            r=red, g=green, b=blue;
        }
        string getColor() {
            return to_string(r)+" "+to_string(g)+" "+to_string(b);
        }
        string out() {
            ostringstream s;
            s << fixed;
            s.precision(23);
            s << "(" << x << "," << y << ")";
            return s.str();
        }
        bool operator<(const Point& other) const {
            return (x < other.getX()) || ((x == other.getX()) && (y < other.getY()));
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
        static void circle(Point c, double radius, int red, int green, int blue) {
            int cx=c.getSX(), cy=c.getSY(), r=int(radius*800), xmax=(int)ceil(radius*800/pow(2,0.5)-0.5);
            int y=r, ty=2*y-1, y2=y*y, y2_n=y2;
            if (r>5) xmax++;
            for (int x=0; x<=xmax; x++) {
                if (y2 - y2_n >= ty)
                    y2 -= ty, y -= 1, ty -= 2;
                y2_n -= 2*x-3;
                double Xu=800-cx, Xd=-cx, Yu=800-cy, Yd=-cy;
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

class Bundle {
    private:
        double d=0;
        Point p1, p2;
    public:
        Bundle(Point &point1, Point &point2) {
            d=dist(point1, point2), p1=point1, p2=point2;
        }
        Bundle(Point &point1, Point &point2, double distance) {
            d=distance, p1=point1, p2=point2;
        }
        double getD() {
            return d;
        }
        Point getP1() {
            return p1;
        }
        Point getP2() {
            return p2;
        }
        bool operator<(const Bundle& other) const {
            return d < other.d;
        }
};

void part0() {
    cout << "Generate points? (yes/no)" <<endl;
    string s;
    cin >> s;
    if (s == "yes") {
        ofstream pout("points.txt");
        cout << "How many points?" <<endl;
        int n;
        cin >> n;
        for (int i=0; i<n; i++) {
            pout << setprecision(23) << rd() << "  " << rd() << endl;
        }
    }
}

void part1() {
    ifstream pin("points.txt");
    list<Point> p;
    double x, y;
    while (pin >> x >> y)
        p.emplace_back(x, y);
    auto Bstart = chrono::high_resolution_clock::now();
    Point p1=p.front(), p2=*(++p.begin());
    double closest = dist(p1, p2);
    
    for (auto it=p.begin(); it != p.end(); ++it) {
        for (auto jit=next(it); jit != p.end(); ++jit) {
            Point a = *it, b = *jit;
//            Render::circle(a, 2/800.0), Render::circle(a, 3/800.0);
//            Render::circle(b, 2/800.0), Render::circle(b, 3/800.0);
            double c = dist(a, b);
            if (c<closest)
                closest=c, p1=a, p2=b;
        }
    }
    auto Bstop = chrono::high_resolution_clock::now();
    auto Bduration = chrono::duration_cast<chrono::microseconds>(Bstop - Bstart);
    ostringstream s;
    s << fixed;
    s.precision(23);
    s << p1.out() << endl << p2.out() << endl << closest << endl;
    double t = (long)Bduration.count()/pow(10,6);
    s <<"Bruteforce time (sec): "<< t << endl;
    Bout = s.str();
    
    Render::circle(p1, 2/800.0, 255, 0, 0), Render::circle(p1, 3/800.0, 255, 0, 0);
    Render::circle(p2, 2/800.0, 255, 0, 0), Render::circle(p2, 3/800.0, 255, 0, 0);
    writePPM("points.ppm");
}

Bundle recur(vector<Point> &p, int l, int r) {
    Point pl = p.at(l), pr = p.at(r);
    if (r-l==1)
        return {pl, pr};
    if (r-l==2) {
        Point pm = p.at(l+1);
        return min(Bundle(pl, pr), min(Bundle(pl, pm), Bundle(pm, pr)));
    }
    int mid = (l+r)/2;
    double midX = p.at(mid).getX();
    Bundle d = min(recur(p, l, mid), recur(p, mid+1, r));
    double minDist = d.getD();
    int lsplit=l, rsplit=r;
    for (int i=l; i<mid; i++)
        if (p.at(i).getX()>=midX-minDist) {
            lsplit = i;
            break;
        }
    for (int i=mid; i<=r; i++)
        if (p.at(i).getX()>=midX+minDist) {
            rsplit = i;
            break;
        }
    
    Point p1 = d.getP1(), p2 = d.getP2();
    for (int i=lsplit; i<=mid; i++) {
        for (int j=mid+1; j<=rsplit; j++) {
            double td = dist(p.at(i), p.at(j));
            if (td<minDist)
                minDist=td, p1=p.at(i), p2=p.at(j);
        }
    }
    return {p1, p2, minDist};
}

void part2() {
    cout << "Recursive - enter filename (without .txt):" << endl;
    string fn;
    cin >> fn;
    fn += ".txt";
    ifstream pin(fn);
//    ifstream pin("points.txt");
    vector<Point> p;
    double x, y;
    while (pin >> x >> y)
        p.emplace_back(x, y);
    auto Rstart = chrono::high_resolution_clock::now();
    sort(p.begin(), p.end());
    Bundle smallest = recur(p, 0, (int)p.size()-1);
    auto Rstop = chrono::high_resolution_clock::now();
    auto Rduration = chrono::duration_cast<chrono::microseconds>(Rstop - Rstart);
    ostringstream s;
    s << fixed;
    s.precision(23);
    s << smallest.getP1().out() << endl << smallest.getP2().out() << endl << smallest.getD() << endl;
    double t = (long)Rduration.count()/pow(10,6);
    s <<"Recursive time (sec): "<< t << endl;
    Rout = s.str();
}

bool ycomp(Point a, Point b) {
    return a.getY() < b.getY();
}

Bundle recurO(vector<Point> &p, int l, int r) {
    Point pl = p.at(l), pr = p.at(r);
    if (r-l==1)
        return {pl, pr};
    if (r-l==2) {
        Point pm = p.at(l+1);
        return min(Bundle(pl, pr), min(Bundle(pl, pm), Bundle(pm, pr)));
    }
    int mid = (l+r)/2;
    double midX = p.at(mid).getX();
    Bundle d = min(recurO(p, l, mid), recurO(p, mid+1, r));
    double minDist = d.getD();
    
    vector<Point> vp;
    for (int i=l; i<=r; i++) {
        Point pt = p.at(i);
        if (pt.getX() >= midX-minDist && pt.getX() <= midX+minDist)
            vp.push_back(pt);
    }
    sort(vp.begin(), vp.end(), ycomp);
    Point p1 = d.getP1(), p2 = d.getP2();
    for (unsigned int i=0; i<vp.size(); i++) {
        unsigned int j = i+1;
        Point a = vp.at(i);
        while (j<vp.size() && j<=i+15) {
            Point b = vp.at(j);
            double td = dist(a,b);
            if (td<minDist)
                minDist = td, p1=a, p2=b;
            j++;
        }
    }
    return {p1, p2, minDist};
}

void part3() {
//    cout << "Recursive optimized - enter filename (without .txt):" << endl;
//    string fn;
//    cin >> fn;
//    fn += ".txt";
//    ifstream pin(fn);
    ifstream pin("points.txt");
    vector<Point> p;
    double x, y;
    while (pin >> x >> y)
        p.emplace_back(x, y);
    auto Ostart = chrono::high_resolution_clock::now();
    sort(p.begin(), p.end());
    Bundle smallest = recurO(p, 0, (int)p.size()-1);
    auto Ostop = chrono::high_resolution_clock::now();
    auto Oduration = chrono::duration_cast<chrono::microseconds>(Ostop - Ostart);
    
    ostringstream s;
    s << fixed;
    s.precision(23);
    s << smallest.getP1().out() << endl << smallest.getP2().out() << endl << smallest.getD() << endl;
    double t = (long)Oduration.count()/pow(10,6);
    s <<"Recursive optimized time (sec): "<< t << endl;
    Oout = s.str();
}

class Box {
    private:
        li x, y;
    public:
        Box(li x1, li y1) {
            x=x1, y=y1;
        }
        li getX() const {
            return x;
        }
        li getY() const {
            return y;
        }
        bool operator==(const Box& other) const {
            return x == other.x && y == other.y;
        }
};

class Hasher {
    public:
        size_t operator()(const Box& p) const {
            return p.getX() << 32 | p.getY();
        }
};

void shuffle(vector<Point>& vp) {
    li s = vp.size();
    for (li i=0; i<s; i++) {
        li j = i+(li)(rd()*(s-i-1));
        swap(vp[i], vp[j]);
    }
}

void part4() {
    ifstream pin("points.txt");
    vector<Point> p;
    double tx, ty;
    while (pin >> tx >> ty)
        p.emplace_back(tx, ty);
    auto Nstart = chrono::high_resolution_clock::now();
    shuffle(p);
    unordered_map<Box, Point, Hasher> bp;
    li psize = p.size();
    bp.reserve(psize);
    Point& p1=p[0], p2=p[1];
    double d = dist(p1, p2);
    for (li i=0; i<psize; i++) {
        Point& pt = p[i];
        li bx = (li)(2*pt.getX()/d), by = (li)(2*pt.getY()/d);
        li xmin = bx<2 ? bx : bx-2, ymin = by<2 ? by : by-2;
        bool insert = true;
        for (li x1=xmin; x1<xmin+5; x1++)
            for (li y1=ymin; y1<ymin+5; y1++) {
                Box tb(x1, y1);
                auto fit = bp.find(tb);
                if (fit != bp.end()) {
                    Point& pt2 = fit->second;
                    double td = dist(pt, pt2);
                    if (td<d)
                        p1=pt, p2=pt2, d=td, insert=false;
                }
            }
        if (insert)
            bp[{bx, by}] = pt;
        else {
            bp.clear();
            for (li i2=0; i2<=i; i2++) {
                Point& tp = p[i2];
                li tsubX = (li)(2*tp.getX()/d), tsubY = (li)(2*tp.getY()/d);
                bp[{tsubX,tsubY}] = tp;
            }
        }
    }
    auto Nstop = chrono::high_resolution_clock::now();
    auto Nduration = chrono::duration_cast<chrono::microseconds>(Nstop - Nstart);
    ostringstream s;
    s << fixed;
    s.precision(23);
    s << p1.out() << endl << p2.out() << endl << d << endl;
    double t = (long)Nduration.count()/pow(10,6);
    s <<"Randomized algorithm time (sec): "<< t << endl;
    Nout = s.str();
}

int main() {
    part0();
    part3();
    cout << Oout << endl;
    part4();
    cout << Nout;
    ofstream rout("results.txt");
    rout << Oout << endl << Nout;
}