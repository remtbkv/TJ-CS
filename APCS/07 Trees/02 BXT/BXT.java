// Name: J1-26-23
// Date: 2/19/23
/*  Represents a binary expression tree.
 *  The BXT builds itself from postorder expressions. It can
 *  evaluate and print itself.  Also prints inorder and postorder strings. 
 */
 
import java.util.*;

public class BXT
{
   public static final String operators = "+ - * / % ^ !";
   private TreeNode root;   
   
   public BXT()
   {
      root = null;
   }
   public TreeNode getRoot()   //for Codepost
   {
      return root;
   }
   
   public void buildTree(String str)
   {
     	String[] a = str.split(" ");
      Stack<TreeNode> st = new Stack<TreeNode>();
      for (String s : a) {
         if (isOperator(s)) {
            TreeNode r = st.pop();
            if (s.equals("!"))
               st.push(new TreeNode(s, r, null));
            else
               st.push(new TreeNode(s, st.pop(), r));
         }
         else st.push(new TreeNode(s));
      }  
      root = st.pop();
   }
   
   public double evaluateTree()
   {
      return evaluateNode(root);
   }
   
   private double evaluateNode(TreeNode t)  //recursive
   {
      if (t==null) return 0.0;
      String curr = ""+t.getValue();
      if (isOperator(curr))
         return computeTerm(curr, evaluateNode(t.getLeft()) , evaluateNode(t.getRight()));
      return Double.parseDouble(curr);
   }
   
   private double computeTerm(String s, double a, double b)
   {
     if (s.equals("+")) return a+b;
     if (s.equals("-")) return a-b;
     if (s.equals("*")) return a*b;
     if (s.equals("/")) return a/b;
     if (s.equals("%")) return a%b;
     if (s.equals("^")) return Math.pow(a, b);
     if (s.equals("!")) return fact(a);
     return 0;
   }
   private double fact(double n) {
      if (n <= 2) return n;
      return n * fact(n - 1);
   }
   
   private boolean isOperator(String s)
   {
      return operators.indexOf(s)>=0;
   }
   
   public String display()
   {
      return display(root, 0);
   }
   
   private String display(TreeNode t, int level)
   {
      String toRet = "";
      if(t == null)
         return "";
      toRet += display(t.getRight(), level + 1); //recurse right
      for(int k = 0; k < level; k++)
         toRet += "\t";
      toRet += t.getValue() + "\n";
      toRet += display(t.getLeft(), level + 1); //recurse left
      return toRet;
   }
    
   public String inorderTraverse()
   {
      return inorderTraverse(root);
   }
   
   private  String inorderTraverse(TreeNode t)
   {
     String out = "";
      if (t==null) return "";
      out += inorderTraverse(t.getLeft());         //recurse left
      out += t.getValue()+" ";                     //process root
      out += inorderTraverse(t.getRight());			//recurse right
      return out;
   }
   
   public String preorderTraverse()
   {
      return preorderTraverse(root);
   }
   
   private String preorderTraverse(TreeNode t)
   {
       String toReturn = "";
      if(t == null) return "";
      toReturn += t.getValue() + " ";              //process root
      toReturn += preorderTraverse(t.getLeft());   //recurse left
      toReturn += preorderTraverse(t.getRight());  //recurse right
      return toReturn; 
   }
   
  /* extension */
   public String inorderTraverseWithParentheses()
   {
      return inorderTraverseWithParentheses(root);
   }
   public static int getLevel(String op) {
      if (op.equals("+") || op.equals("-")) return 1;
      if (op.equals("*") || op.equals("/") || op.equals("%")) return 2;
      if (op.equals("^")) return 3;
      if (op.equals("!")) return 4;
      return 0;
   }
   
   private String inorderTraverseWithParentheses(TreeNode t)
   {
      if (t==null) return "";
      String out = "";
      
      if (t.getLeft() != null && isOperator(""+t.getLeft().getValue()) && getLevel(""+t.getLeft().getValue())<getLevel(""+t.getValue()))
         out += "( " + inorderTraverseWithParentheses(t.getLeft()) + ") ";
      else out += inorderTraverseWithParentheses(t.getLeft()); 
      
      out += t.getValue()+" ";
      
      if (t.getRight() != null && isOperator(""+t.getRight().getValue()) && getLevel(""+t.getRight().getValue())<getLevel(""+t.getValue()))
         out += "( " + inorderTraverseWithParentheses(t.getRight()) + ") "; 
      else out += inorderTraverseWithParentheses(t.getRight());
      
      return out;
   }
}