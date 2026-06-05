// Name: J1-26-22
// Date: 10/27/22

public class Widget implements Comparable<Widget>
{
   //fields
   private int myCubits;
   private int myHands;
   //constructors
   public Widget() {
      myCubits = 0;
      myHands = 0;
   }
   public Widget(int c, int h) {
      myCubits = c;
      myHands = h;
   }

   public Widget(Widget w) {
      myCubits = w.getCubits();
      myHands = w.getHands();
   }
   //accessors and modifiers
   public void setCubits(int c) {
      myCubits = c;
   }

   public void setHands(int h) {
      myHands = h;
   }

   public int getCubits() {
      return myCubits;
   }

   public int getHands() {
      return myHands;
   }
   //compareTo and equals
   public int compareTo(Widget w2) {
      if (myCubits > w2.getCubits()) {
         return 1;
      }
      else if (myCubits < w2.getCubits()) {
         return -1;
      }
      else {
         if (myHands > w2.getHands())
            return 1;
         else if (myHands < w2.getHands())
            return -1;
         else
            return 0;
      }
   }
   public boolean equals(Widget w2) {
      return (myCubits == w2.getCubits() && myHands == w2.getHands());
   }
   //toString
   @Override
   public String toString() {
      return myCubits + " cubits " + myHands + " hands";
   }
}
