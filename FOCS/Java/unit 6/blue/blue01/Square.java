public class Square implements Shape, Comparable<Shape> {
  private double a;

  public Square(double s) {
    a = s;
  }

  public double getPerimeter() {
    return a*4;
  }

  public double getArea() {
    return a*a;
  }

  public int compareTo(Shape x) {
    if (getArea() > x.getArea()) return 1;
    if (getArea() < x.getArea()) return -1;
    else return 0;
  }

  public String toString() {
    return "Square with side "+a+" has area "+getArea();
  }
}
