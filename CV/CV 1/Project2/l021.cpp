#include <iostream>
#include <fstream>
#include <random>
#include <cmath>
#include <sstream>

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
        void illum (int red, int green, int blue) {
            r=red, g=green, b=blue;
        }
        void mark() {
            r=255, g=0, b=0;
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
};

double dist(Point A, Point B) {
    return sqrt(pow(A.getX()-B.getX(),2) + pow(A.getY()-B.getY(),2));
}

double heron(Point A, Point B, Point C) {
    double a=dist(A,B), b=dist(B,C), c=dist(C,A), s=(a+b+c)/2;
    return sqrt(s*(s-a)*(s-b)*(s-c));
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

int main() {
    part1();
}