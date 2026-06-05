// Name: J1-26-23
// Date: 3/2/23

interface BSTinterface
{
   public int size();
   public TreeNode getRoot() ;
   public boolean contains(String obj);
   public void add(String obj);          //does not balance
   public void addBalanced(String obj);  //AVL
   public void remove(String obj);       //does not re-balance
   //public void removeBalanced(String obj); //extension
   public String min();
   public String max();
   public String display();
   public String toString();
}

public class BST implements BSTinterface
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
      if (x.compareTo(c)<0) return contains(t.getLeft(), x);
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
   
   public TreeNode maxNode(TreeNode t) {
      if (t==null) return null;
      if (t.getRight()==null) return t;
      return maxNode(t.getRight());
   }
   public boolean childless(TreeNode t) {
      return t.getLeft()==null && t.getRight()==null;
   }
   public TreeNode parentNode(TreeNode rt, TreeNode t) {
      if (rt==t || rt.getRight()==t || rt.getLeft()==t) return rt;
      if ((t.getValue()+"").compareTo(""+rt.getValue())>0) return parentNode(rt.getRight(), t);
      return parentNode(rt.getLeft(), t);
   }
   public void setChild(TreeNode p, TreeNode c, TreeNode l, TreeNode r) {
      if (p.getRight()==c || (p==c && p.getRight()!=null)) {
         if (r!=null) p.setRight(r);
         else p.setRight(l);
      }
      else {
         if (r!=null) p.setLeft(r);
         else p.setLeft(l);
      }
   }
   
   /*  precondition:  target must be in the tree.
                      implies that tree cannot be null.
   */
   public void remove(String target)
   {
      root = remove(root, target);
      size--;
   }
   private TreeNode remove(TreeNode c, String t)
   {
      TreeNode h = c;
      while (!t.equals(c.getValue()+"")) {
         if (t.compareTo(c.getValue()+"")>0) c=c.getRight();
         else c=c.getLeft();
      }
      TreeNode r = c.getRight(), l = c.getLeft();
      if (size==1) return null;
      if (r!=null && l!=null) {
         TreeNode m = maxNode(l);
         c.setValue(""+m.getValue());
         setChild(parentNode(h, m), m, m.getLeft(), m.getRight());
      }
      else if (h==c) return l!=null ? l : r;
      else setChild(parentNode(h, c), c, l, r);
      return h;
   }

   /*  start the addBalanced methods */
   private int calcBalance(TreeNode current) //height to right minus 
   {                                    //height to left
      // return current.getRight().getHeight() - current.getLeft().getHeight();
      if (current==null) return 0;
      return height(current.getRight()) - height(current.getLeft());
   }

   private int height(TreeNode t)   //from TreeLab
   {
      if (t==null) return -1;
      int left = 0, right = 0;
      if (t.getLeft()!=null) left = 1 + height(t.getLeft());
      if (t.getRight()!=null) right = 1 + height(t.getRight());
      return Math.max(left, right);
   }
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
   public void addBalanced(String value)  
   {
      size++;
      root = addBalanced( root , value);   // for an AVL tree. Put in the arguments you want.
   }
   private TreeNode addBalanced( TreeNode t, String s)  //recursive.  Whatever makes sense.
   {
      if (t==null) return new TreeNode(s);
      if (s.compareTo(t.getValue()+"")>0) t.setRight(addBalanced(t.getRight(), s));
      else t.setLeft(addBalanced(t.getLeft(), s));

      if (calcBalance(t)>1) {
         if (calcBalance(t.getRight())<= -1) return DL(t);
         else return LL(t);
      }
      else if (calcBalance(t)< -1) {
         if (calcBalance(t.getLeft())>=1) return DR(t);
         else return RR(t);
      }
      return t;
   }
   
   // 4 rotation helper methods
   public TreeNode LL(TreeNode c) {
      TreeNode root = c.getRight();
      c.setRight(root.getLeft());
      root.setLeft(c);
      return root;
   }
   public TreeNode RR(TreeNode c) {
      TreeNode root = c.getLeft();
      c.setLeft(root.getRight());
      root.setRight(c);
      return root;
   }
   public TreeNode DL(TreeNode c) {
      c.setRight(RR(c.getRight()));
      return LL(c);
   }
   public TreeNode DR(TreeNode c) {
      c.setLeft(LL(c.getLeft()));
      return RR(c);
   }
}