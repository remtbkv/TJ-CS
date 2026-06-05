public class Circle implements Shape, Comparable<Shape> {
   private double a;

   public Circle(double r) {
     a = r;
   }

   public double getPerimeter() {
      return Math.PI*2*a;
   }

   public double getArea() {
      return Math.PI*(a*a);
   }

   public int compareTo(Shape x) {
     if (getArea() > x.getArea()) return 1;
     else if (getArea() < x.getArea()) return -1;
     else return 0;
   }

   public String toString() {
     return "Circle with radius "+a+" has area "+getArea();
   }
}
