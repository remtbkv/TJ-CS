// Name: J1-26-22
// Date: 12/6/22

import java.util.*;
import java.io.*;

public class Josephus
{
   private static String WINNER = "Josephus";
   
   public static void main(String[] args) throws FileNotFoundException
   {
   /* Josephus Part I, insert() and print()   */
      ListNode last = null;
      last = insert(last, "B");  
      last = insert(last, "C");
      last = insert(last, "D");
      last = insert(last, "E");
      last = insert(last, "F");
      print(last);
       
   /* Josephus Part II  */ 
      /* run numberCircle first with J_numbers.txt  */
      Scanner sc = new Scanner(System.in);
      System.out.print("How many names (2-20)? ");
      int n = Integer.parseInt(sc.next());
      System.out.print("How many names to count off each time? ");
      int countOff = Integer.parseInt(sc.next());
      ListNode winningPos = numberCircle(n, countOff, "J_numbers.txt");
      System.out.println(winningPos.getValue() + " wins!");  
     
      /* run josephusCircle next with J_names.txt  */
      System.out.println("\n ****  Now start all over. **** \n");
      System.out.print("Where should "+WINNER+" stand?  ");
      int winPos = Integer.parseInt(sc.next());        
      ListNode theWinner = josephusCircle(n, countOff, "J_names.txt", winPos);
      System.out.println(theWinner.getValue() + " wins!");  
   }
   
   public static ListNode numberCircle(int n, int countOff, String filename) throws FileNotFoundException
   {
      ListNode p = null;
      p = readNLinesOfFile(n, new File(filename));
      p = countingOff(p, countOff, n);
      return p;
   }
   
   public static ListNode josephusCircle(int n, int countOff, String filename, int winPos) throws FileNotFoundException
   {
      ListNode p = null;
      p = readNLinesOfFile(n, new File(filename));
      replaceAt(p, WINNER, winPos);
      p = countingOff(p, countOff, n);
      return p;
   }

   /* reads the names, calls insert(), builds the linked list.
      DEBUG:  set a breakpoint in this method and see if the data is read into the circle 
	 */
   public static ListNode readNLinesOfFile(int n, File f) throws FileNotFoundException
   {
      ListNode out = null;
      Scanner in = new Scanner(f);
      for (int i=0; i<n; i++)
         out = insert(out, in.next());
      in.close();
      return out;
   }
   
   /* helper method to build the list.  Creates the node, then
      inserts it in the circular linked list.
	 */
   public static ListNode insert(ListNode p, Object obj)
   {
      ListNode head = p;
      if (head==null) {
         head = new ListNode(obj, null);
         head.setNext(head);
         return head;
      }
      while (head.getNext() != p)
         head = head.getNext();
      p.setNext(new ListNode(obj, p.getNext()));
      return p.getNext();
   }
   
   /* Runs a Josephus game, counting off and removing each name. Prints after each removal.  
      Ends with one remaining name, who is the winner.
      DEBUG:  set a breakpoint in this method and see if the counting off is correct 
	 */
   public static ListNode countingOff(ListNode p, int count, int n)
   {
      print(p);
      ListNode head = p;
      while (n != 1) {
         head = remove(head, count);
         print(head);
         n--;
      }
      return head;
   }
   
   /* removes the node after counting off count-1 nodes.
	 */
   public static ListNode remove(ListNode p, int count)
   {
      ListNode head = p;
      for (int i=0; i<count-1; i++)
         head = head.getNext();
      head.setNext(head.getNext().getNext());
      return head;
   }
   
   /* prints the circular linked list.
	 */
   public static void print(ListNode p)
   {
      ListNode head = p.getNext();
      while (head.getNext() != p.getNext()) {
         System.out.print(head.getValue() + " ");
         head = head.getNext();
      }
      System.out.println(head.getValue());
   }
	
   /* replaces the value (the String) at the winning node.
	 */
   public static void replaceAt(ListNode p, Object obj, int pos)
   {
      for (int i=0; i<pos; i++)
         p = p.getNext();
      p.setValue(obj);
   }
}
/**********************************************************
     
 B C D E F
 How many names (2-20)? 5
 How many names to count off each time? 2
 1 2 3 4 5
 3 4 5 1
 5 1 3
 3 5
 3
 3 wins!
 
  ****  Now start all over. **** 
 
 Where should Josephus stand?  3
 Michael Hannah Josephus Ruth Matthew
 Josephus Ruth Matthew Michael
 Matthew Michael Josephus
 Josephus Matthew
 Josephus
 Josephus wins!
 
  ----jGRASP: operation complete.
  
  **************************************************/

