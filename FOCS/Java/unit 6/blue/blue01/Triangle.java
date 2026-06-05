public class Triangle implements Shape, Comparable<Shape> {
   private double a, b, c;

   public Triangle(double s1, double s2, double s3) {
      a = s1;
      b = s2;
      c = s3;
   }

   public double getPerimeter() {
      return a+b+c;
   }

   public double getArea() {
     double s = (a+b+c)/2;
     return Math.sqrt(s*(s-a)*(s-b)*(s-c));
   }

   public int compareTo(Shape x) {
     if (getArea() > x.getArea()) return 1;
     else if (getArea() < x.getArea()) return -1;
     else return 0;
   }

   public String toString() {
     return "Triangle with sides "+a+" "+b+" "+c+" has area "+getArea();
   }
}
