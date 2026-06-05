
public class Position
{
   private int x;
   private int y;
   public Position(int x, int y)
   {
      this.x = x;
      this.y = y;
   }
   public int getx()
   {
      return x;
   }
   public int gety()
   {
      return y;
   }
   /* enter the methods that make the hashSet discard duplicates  */
   public boolean equals(Object other) {
      if (other instanceof Position) {
         Position o = (Position)other;
         return x==o.x && y==o.y;
      }
      return false;
   }
   public int hashCode() {
      return toString().hashCode();
   }   
   public String toString()
   {
      return "("+ x +", "+ y +")";
   }
}