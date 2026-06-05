//name: J1-26-23  date: ______________________
import java.util.*;

public class Generics_Demo
{
   public static void main(String[] args)
   {
   /*************  non-generic data structures **********************/
   
      List myList = new ArrayList();          //old style, non-generic
      myList.add("this is a string");         //put a String in the arrayList
      String str;
      // str = myList.get(0);           //error: ClassCastException
      str = (String) myList.get(0);
      str = String.valueOf(myList.get(0));
      str = "" + myList.get(0);
      str = myList.get(0).toString();
      System.out.println( str );
   
      List theList = new ArrayList();         //old style, non-generic
      theList.add(3);                         //put an int in the arrayList    
      int x;
      //x = theList.get(0);          //error: ClassCastException
      x = (int) theList.get(0);
      x = Integer.parseInt("" +theList.get(0));
      x = Integer.parseInt(theList.get(0).toString());
      int square = x * x;                  // it behaves like an Integer
      System.out.println( square );
      
    /*************  generic data structures  **********************/  
     
      List<String> stringList = new ArrayList<String>();  // ArrayList<E>
      stringList.add("this is a string");
      String str2 = stringList.get(0);       //it "remembers" the data is a String
      String str3 = str2.substring(1,2);     //all String methods are available without casting
      System.out.println( str3 );
      
      LinkedList<Integer> ints = new LinkedList<Integer>();  // LinkedList<E>
      ints.add(3);
      Integer y = ints.getFirst();          //it "remembers" the data is an Integer
      Integer Square = y * y;               //no need to cast
      System.out.println( Square );
   
   /*************  ListNode  **********************/   
   
      ListNode<Integer> s = new ListNode<>(4, null);   //uses the generic ListNode<E>, see below
      ListNode<Integer> t = new ListNode<>(5, s);
      Integer num = t.getNext().getValue();            //what type does getNext() return?
      Integer sq = num * num;                    
      System.out.println( sq );
   }


   static class ListNode<E>     //write the generic ListNode<E> class
   {
   /*  two private fields  */
      private E value;
      private ListNode<E> next;
      
   /* one two-arg constructor  */
      public ListNode(E v, ListNode<E> n) {
         value = v;
         next = n;
      }
      
   /*  2 accessor methods   */       
      public E getValue() {
         return value;
      }
      public ListNode<E> getNext() {
         return next;
      }
      
   /*  2 modifier methods  */         
      public void setValue(E v) {
         value = v;
      }
      public void setNext(ListNode<E> n) {
         next = n;
      }
   }
}
