#include <iostream>
#include <fstream>
#include <random>
#include <cmath>

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
};

double dist(Point A, Point B) {
    return sqrt(pow(A.getX()-B.getX(),2) + pow(A.getY()-B.getY(),2));
}

Point(*ppm)[800] = new Point[800][800];

class Render {
    public:
        static void line(Point a, Point b) { // precondition: A and B are valid points
            int x1=a.getSX(), y1=a.getSY(), x2=b.getSX(), y2=b.getSY(), dX=abs(x1-x2)+1, dY=abs(y1-y2)+1, e=dY-dX;
            if (x1==x2)
                for (int y = min(y1, y2); y<max(y1, y2); y++)
                    ppm[x1][y].illum();
            else if (y1==y2)
                for (int x = min(x1, x2); x<max(x1, x2); x++)
                    ppm[x][y1].illum();
            else if (dX>=dY) {
                if (x1 > x2) { // switches A and B so A.x is smaller
                    int tx = x1, ty = y1;
                    x1=x2, x2=tx, y1=y2, y2=ty;
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
            }
            else {
                if (y1 > y2) { // switches A and B so A.y is smaller
                    int tx=x1, ty=y1;
                    x1=x2, x2=tx, y1=y2, y2=ty;
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

int main() {
    double x1=rd(), x2=rd(), x3=rd(), y1=rd(), y2=rd(), y3=rd();
    Point A = Point(x1, y1), B = Point(x2, y2), C = Point(x3, y3);
    double a=dist(B, C), b=dist(C, A), c=dist(B, A); // side length
    double aA=acos((pow(b,2)+pow(c,2)-pow(a,2))/(2*b*c)), aB=acos((pow(c,2)+pow(a,2)-pow(b,2))/(2*c*a)), aC=acos((pow(a,2)+pow(b,2)-pow(c,2))/(2*a*b)); // angles
    vector<Point> points{A, B, C};
    vector<double> sides{a, b, c}, angles{aA, aB, aC};
    double p=a+b+c, s=p/2, sp=sin(2*aA)+sin(2*aB)+sin(2*aC);
    double ix=(a*x1+b*x2+c*x3)/p, iy=(a*y1+b*y2+c*y3)/p, ir=sqrt((s-a)*(s-b)*(s-c)/s); // incircle
    double cx=(x1*sin(2*aA)+x2*sin(2*aB)+x3*sin(2*aC))/sp, cy=(y1*sin(2*aA)+y2*sin(2*aB)+y3*sin(2*aC))/sp, cr=a*b*c/(4*ir*s); // circumcicrle
    double centX=(x1+x2+x3)/3, centY=(y1+y2+y3)/3, orthX=3*centX-2*cx, orthY=3*centY-2*cy, npx=(orthX+cx)/2, npy=(orthY+cy)/2, npr=cr/2; // 9p circle
    double mE = (centY-cy)/(centX-cx), bE=cy-mE*cx; // euler line
    auto check = [](double x) -> double {
        return (x==1.0) ? 799/800.0 : x;
    };
    double bx=check(-bE/mE), tx=check((1 - bE)/mE), ly=check(bE), ry=check(mE + bE);
    vector<Point> e;
    if (tx >= 0 && tx < 1) e.emplace_back(tx, 799 / 800.0);
    if (bx >= 0 && bx < 1) e.emplace_back(bx, 0.0);
    if (ly >= 0 && ly < 1) e.emplace_back(0.0, ly);
    if (ry >= 0 && ry < 1) e.emplace_back(799 / 800.0, ry);
    for (int i=0; i<3; i++)
        Render::line(points.at(i), points.at((i+1)%3));
    Render::circle(Point(ix, iy), ir);
    Render::circle(Point(cx, cy), cr);
    Render::circle(Point(npx, npy), npr);
    Render::line(e.at(0), e.at(1));
    
    Render::circle(Point(0.25, 0.75), 0.00625); // update point
    
    ofstream fout("./triangle.ppm");
    fout<<"P3 800 800 255"<<endl;
    for (int row=799; row >= 0; row--) {
        for (int col=0; col < 800; col++)
            fout<< ppm[col][row].getColor() + " ";
        fout<<endl;
    }
    fout.close();
    
    delete[] ppm;
}
