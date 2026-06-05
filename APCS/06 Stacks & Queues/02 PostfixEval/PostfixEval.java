// Name: J1-26-23
// Date: 1/19/23

import java.util.*;

public class PostfixEval
{
   public static final String operators = "+ - * / % ^ !";
   
   public static void main(String[] args)
   {
      System.out.println("Postfix  -->  Evaluate");
      ArrayList<String> postfixExp = new ArrayList<String>();
      /*  build your list of expressions here  */
      postfixExp.add("3 4 2 ! ^ * 1 - 2 +");
      
      for( String pf : postfixExp )
      {
         System.out.println(pf + "\t\t" + eval(pf));
      }
   }
   
   public static double eval(String pf)
   {
      List<String> postfixParts = new ArrayList<String>(Arrays.asList(pf.split(" ")));
      /*  enter your code here  */
      Stack<Double> st = new Stack<Double>();
      for (int i=0; i<postfixParts.size(); i++) {
         String s = postfixParts.get(i);
         if (isOperator(s)) {
            if (s.equals("!")) st.push(fact(st.pop()));
            else {
               double second = st.pop(), first = st.pop();
               st.push(eval(first, second, s));
            }
         }
         else st.push(Double.parseDouble(s));
      }
      return st.pop();
   }

   public static double fact(double a) {
      if (a==1) return 1;
      return a*fact(a-1);
   }

   public static double eval(double a, double b, String op)
   {
      if (op.equals("+")) return a+b;
      if (op.equals("-")) return a-b;
      if (op.equals("*")) return a*b;
      if (op.equals("/")) return a/b;
      if (op.equals("%")) return a%b;
      else return Math.pow(a, b);
   }
   
   public static boolean isOperator(String op)
   {
      return operators.indexOf(op)>=0;
   }
}

/**********************************************
Postfix  -->  Evaluate
 3 4 5 * +		23
 3 4 * 5 +		17
 10 20 + -6 6 * +		-6
 3 4 + 5 6 + *		77
 3 4 5 + * 2 - 5 /		5
 8 1 2 * + 9 3 / -		7
 2 3 ^		8
 20 3 %		2
 21 3 %		0
 22 3 %		1
 23 3 %		2
 5 !		120
 1 1 1 1 1 + + + + !		120
 
 
 *************************************/