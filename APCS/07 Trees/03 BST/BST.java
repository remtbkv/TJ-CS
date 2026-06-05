//Name: J1-26-23
//Date: 2/21/23

interface BSTinterface
{
   public int size();
   public TreeNode getRoot();
   public boolean contains(String obj);
   public void add(String obj);           //does not balance
   //public void addBalanced(String obj);  //AVL
   //public void remove(String obj);       //BST with remove
   //public void removeBalanced(String obj); //extra lab 
   public String min();
   public String max();
   public String display();
   public String toString();
}

/*******************
Represents a binary search tree holding Strings. 
Implements (most of) BSTinterface, above. 
The recursive methods all have a public method calling a private helper method. 
Copy the display() method from TreeLab. 
**********************/
class BST implements BSTinterface
{
   private TreeNode root;
   private int size;
   public BST()
   {
      root = null;
      size = 0;
   }
   public int size()
   {
     return size;
   }
   public TreeNode getRoot()   //accessor method
   {
      return root;
   }
   /***************************************
   @param s -- one string to be inserted
   ****************************************/
   public void add(String s) 
   {
      root = add(root, s);
      size++;
   }
   private TreeNode add(TreeNode t, String s) //recursive helper method
   {  
      if (t==null) return new TreeNode(s);
      if (s.compareTo(t.getValue()+"")>0) t.setRight(add(t.getRight(), s));
      else t.setLeft(add(t.getLeft(), s));
      return t;
   }
   
   public String display()
   {
      return display(root, 0);
   }
   private String display(TreeNode t, int level) //recursive helper method
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
   
   public boolean contains( String obj)
   {
      return contains(root, obj);
   }
   private boolean contains(TreeNode t, String x) //recursive helper method
   {
      if (t==null) return false;
      String c = ""+t.getValue();
      if (x.equals(c)) return true;
      if (x.compareTo(c)<=0) return contains(t.getLeft(), x);
      return contains(t.getRight(), x);
   }
   
   public String min()
   {
      return min(root);
   }
   private String min(TreeNode t)  //use iteration
   {
      if (t==null) return null;
      TreeNode p = t;
      while (p.getLeft() != null)
         p = p.getLeft();
      return p.getValue()+"";
   }
   
   public String max()
   {
      return max(root);
   }
   private String max(TreeNode t)  //recursive helper method
   {
      if (t==null) return null;
      if (t.getRight()==null) return t.getValue()+"";
      return max(t.getRight());
   }
   
   public String toString()
   {
      return toString(root);
   }
   private String toString(TreeNode t)  //an in-order traversal.  Use recursion.
   {
      if (t==null) return "";
      String out = "";
      out += toString(t.getLeft());         //recurse left
      out += t.getValue()+" ";                     //process root
      out += toString(t.getRight());			//recurse right
      return out;
   }
   public String preorderExtension(String inorder, String postorder) {
      if (inorder.length()==0 || postorder.length()==0) return "";

      String root = postorder.substring(postorder.length()-1); // last char of postorder
      int ind = inorder.indexOf(root); // middle of inorder
      
      String leftIn="", leftPost="", rightIn="", rightPost="";
      if (ind>0) { // left half of string to recurse left
         leftIn = inorder.substring(0, ind);
         leftPost = postorder.substring(0, ind);
      }
      if (ind<inorder.length()-1) { // right half of string to recurse right
         rightIn = inorder.substring(ind+1);
         rightPost = postorder.substring(ind, postorder.length()-1);
      }
      String left = preorderExtension(leftIn, leftPost); // recurse left
      String right = preorderExtension(rightIn, rightPost); // recurse right
      return root+left+right; // preorder
   }
}
