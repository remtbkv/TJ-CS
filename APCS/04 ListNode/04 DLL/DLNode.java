//////////////////////////////////////
//Keith Ainsworth, 11/13/2006
class DLNode 
{
   private Object value;
   private DLNode prev;
   private DLNode next;
   public DLNode()
   {
      value=null;
      next=null;
      prev=null;
   }
   public DLNode(Object obj, DLNode p, DLNode n)
   {
      value=obj;
      prev=p;
      next=n;
   }

   public Object getValue()
   {
      return value;
   }
   public DLNode getPrev()
   {
      return prev;
   }
   public void setValue(Object obj)
   {
      value=obj;
   }
   public void setPrev(DLNode p)
   {
      prev=p;
   }
   public void setNext(DLNode n)
   {
      next=n;
   }

   public DLNode getNext()
   {
      return next;
   }

}
