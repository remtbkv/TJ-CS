// Name:
// Date:
import java.util.*;
/*******************
This driver provides an ArrayList of input strings. One by one, it adds  
the letters to the tree.   Display it as a sideways 
tree (take the code from TreeLab).  Prompt the user for a target and 
search the BST for it.  Display the tree's minimum and maximum values.  
Print the letters in order from smallest to largest.
**********************/
public class BST_Driver
{
   public static void main(String[] args)
   {
      Scanner keyboard = new Scanner(System.in);
      ArrayList<String> list = new ArrayList<String>();
      list.add("M A E N I R A C");
      list.add("A M E R I C A N");
      list.add("A A C E I M N R");
      list.add("A");
      list.add("6 8 2 9 3 0 1");
      list.add("Florida Oklahoma Colorado Massachusetts Arizona Iowa New_Hampshire Washington West_Virginia Kazakhstan Arkansas");
   
      for( String string : list )
      {
         BST bst = new BST();   //we want to start anew 
		 System.out.println(bst.preorderExtension("ABCDEFGHI", "ACEDBHIGF"));
         String[] str = string.split(" ");
         for(String item : str)
            bst.add( item );
            
         System.out.println("Root is " + bst.getRoot());
         System.out.println( bst.display() );
         System.out.println( "Size = " + bst.size() );
         System.out.println("Min = " + bst.min());
         System.out.println("Max = " + bst.max());	
         System.out.print("Input target: ");
         String target =  keyboard.next();    
         boolean itemFound = bst.contains(target);
         if(itemFound)
            System.out.println("found: " + target);
         else
            System.out.println(target +" not found.");
         System.out.println("in-order traversal: " + bst.toString());
         System.out.println("--------------------------");
      }
   }
}
   

/*******************  Sample Run

Root is TreeNode@5b6f7412
 		R
 	N
 M
 			I
 		E
 			C
 	A
 		A
 
 Size = 8
 Min = A
 Max = R
 Input target: E
 found: E
 in-order traversal: A A C E I M N R 
 --------------------------
 Root is TreeNode@1e80bfe8
 		R
 			N
 	M
 			I
 		E
 			C
 A
 	A
 
 Size = 8
 Min = A
 Max = R
 Input target: X
 X not found.
 in-order traversal: A A C E I M N R 
 --------------------------
 Root is TreeNode@66a29884
 						R
 					N
 				M
 			I
 		E
 	C
 A
 	A
 
 Size = 8
 Min = A
 Max = R
 Input target: a
 a not found.
 in-order traversal: A A C E I M N R 
 --------------------------
 Root is TreeNode@4769b07b
 A
 
 Size = 1
 Min = A
 Max = A
 Input target: A
 found: A
 in-order traversal: A 
 --------------------------
 Root is TreeNode@cc34f4d
 		9
 	8
 6
 		3
 	2
 			1
 		0
 
 Size = 7
 Min = 0
 Max = 9
 Input target: 0
 found: 0
 in-order traversal: 0 1 2 3 6 8 9 
 --------------------------
 Root is TreeNode@17a7cec2
 			West_Virginia
 		Washington
 	Oklahoma
 			New_Hampshire
 		Massachusetts
 				Kazakhstan
 			Iowa
 Florida
 	Colorado
 			Arkansas
 		Arizona
 
 Size = 11
 Min = Arizona
 Max = West_Virginia
 Input target: Kazakhstan
 found: Kazakhstan
 in-order traversal: Arizona Arkansas Colorado Florida Iowa Kazakhstan Massachusetts New_Hampshire Oklahoma Washington West_Virginia 
 --------------------------
 ************************************/