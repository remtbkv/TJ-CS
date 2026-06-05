// Name: J1-26-23
// Date: 1/21/23
//uses PostfixEval

import java.util.*;
public class InfixPostfixEval
{
   public static final String LEFT  = "([{<";
   public static final String RIGHT = ")]}>";
   public static final String operators = "+ - * / % ^ !";
   
   public static void main(String[] args)
   {
      System.out.println("Infix  \t-->\tPostfix\t\t-->\tEvaluate");
      /*build your list of Infix expressions here  */
      List<String> infixExp = new ArrayList<>();
      infixExp.add("3 * ( 4 ^ 2 ! ) + 1 - 2");
      for( String infix : infixExp )
      {
         String pf = infixToPostfix(infix);  //get the conversion to work first
         System.out.println(infix + "\t\t\t" + pf );  
       //  System.out.println(infix + "\t\t\t" + pf + "\t\t\t" + PostfixEval.eval(pf));  //PostfixEval must work!
      }
   }
   
   public static String infixToPostfix(String infix)
   {
      List<String> nums = new ArrayList<String>(Arrays.asList(infix.split(" ")));
      /* enter your code here  */
      String post = "";
      Stack<String> st = new Stack<String>();
      for (int i=0; i<nums.size(); i++) {
         String s = nums.get(i);
         if (LEFT.indexOf(s)>=0) st.push(s);
         else if (RIGHT.indexOf(s)>=0) {
            while (!st.isEmpty() && LEFT.indexOf(st.peek())<0) post+=st.pop()+" ";
            st.pop();
         }
         else if (operators.indexOf(s)>=0) {
            while (!st.isEmpty() && isHigherOrEqual(st.peek(), s)) post+=st.pop()+" ";
            st.push(s);
         }
         else post+=s+" ";
      }
      while (!st.isEmpty())
         post+=st.pop()+" ";
      return post.strip();
   }
   
   //enter your precedence method below
   public static boolean isHigherOrEqual(String top, String next) {
      return getLevel(top)>=getLevel(next);
   }

   public static int getLevel(String op) {
      if (op.equals("+") || op.equals("-")) return 1;
      if (op.equals("*") || op.equals("/") || op.equals("%")) return 2;
      return -1;
   }
   
}


/********************************************

Infix  	-->	Postfix		-->	Evaluate
 5 - 1 - 1			5 1 - 1 -			3.0
 5 - 1 + 1			5 1 - 1 +			5.0
 12 / 6 / 2			12 6 / 2 /			1.0
 3 + 4 * 5			3 4 5 * +			23.0
 3 * 4 + 5			3 4 * 5 +			17.0
 1.3 + 2.7 + -6 * 6			1.3 2.7 + -6 6 * +			-32.0
 ( 33 + -43 ) * ( -55 + 65 )			33 -43 + -55 65 + *			-100.0
 8 + 1 * 2 - 9 / 3			8 1 2 * + 9 3 / -			7.0
 3 * ( 4 * 5 + 6 )			3 4 5 * 6 + *			78.0
 3 + ( 4 - 5 - 6 * 2 )			3 4 5 - 6 2 * - +			-10.0
 2 + 7 % 3			2 7 3 % +			3.0
 ( 2 + 7 ) % 3			2 7 + 3 %			0.0
      
***********************************************/
