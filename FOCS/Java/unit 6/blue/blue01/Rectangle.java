public class Rectangle implements Shape, Comparable<Shape> {
  private double a, b;

  public Rectangle(double s1, double s2) {
    a=s1;
    b=s2;
  }

  public double getPerimeter() {
    return (a*2)+(b*2);
  }

  public double getArea() {
    return a*b;
  }

  public int compareTo(Shape x) {
    if (getArea() > x.getArea()) return 1;
    else if (getArea() < x.getArea()) return -1;
    else return 0;
  }

  public String toString() {
    return "Rectangle with sides "+a+" and "+b+" has area "+getArea();
  }
}
