public class Parallelogram implements Shape, Comparable<Shape> {
  private double a, b, c;

  public Parallelogram(double bs, double sh, double vh) {
    a=bs;
    b=sh;
    c=vh;
  }

  public double getPerimeter() {
    return b*2+a*2;
  }

  public double getArea() {
    return a*c;
  }

  public int compareTo(Shape x) {
    if (getArea() > x.getArea()) return 1;
    else if (getArea() < x.getArea()) return -1;
    else return 0;
  }

  public String toString() {
    return "Parallelogram with base "+a+" and slant height"+b+" and height "+c+" has area "+getArea();
  }
}
