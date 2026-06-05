// Name: J1-26-22
// Date: 12/11/22

//  DoubleLinkedList, circular, with a dummy head node
//  implements some of the List and LinkedList interfaces: 
//	 	  size(), add(i, o), remove(i);  addFirst(o), addLast(o); 
//  This class also overrides toString().
//  the list is zero-indexed.
//  Uses DLNode.

class DLL  
{
   private int size;
   private DLNode head; //points to a dummy node--very useful--don't mess with it
   public DLL()  
   {
      size = 0;
      head = new DLNode();
      //make it circular
      head.setNext(head);
      head.setPrev(head);
   } 
   
   /* two accessor methods  */
   public int size()
   {
      return size;
   }
   public DLNode getHead()
   {
      return head;
   }
   
   /* appends obj to end of list; increases size;
   	  @return true  */
   public boolean add(Object obj)
   {
      addLast(obj);
      return true;   
   }
   
   /* inserts obj at position index (the list is zero-indexed).  
      increments size. 
      no need for a special case when size == 0.
	   */
   public void add(int index, Object obj) throws IndexOutOfBoundsException
   {
      if( index > size || index < 0 )
         throw new IndexOutOfBoundsException("Index: " + index + ", Size: " + size);
      /* enter your code below  */
      DLNode p = head.getNext();
      for (int i=0; i<index; i++)
         p = p.getNext();
      DLNode addNode = new DLNode(obj, p.getPrev(), p);
      p.getPrev().setNext(addNode);
      p.setPrev(addNode);
      size++;
   }
   
    /* return obj at position index (zero-indexed). 
    */
   public Object get(int index) throws IndexOutOfBoundsException
   { 
      if(index >= size || index < 0)
         throw new IndexOutOfBoundsException("Index: " + index + ", Size: " + size);
      /* enter your code below  */
      DLNode p = head.getNext();
      for (int i=0; i<index; i++)
         p = p.getNext();
      return p.getValue();
   }
   
   /* replaces obj at position index (zero-indexed). 
        returns the obj that was replaced.
        */
   public Object set(int index, Object obj) throws IndexOutOfBoundsException
   {
      if(index >= size || index < 0)
         throw new IndexOutOfBoundsException("Index: " + index + ", Size: " + size);
      /* enter your code below  */
      DLNode p = head.getNext();
      for (int i=0; i<index; i++)
         p = p.getNext();
      Object repl = p.getValue();
      p.setValue(obj);
      return repl;
   }
   
   /*  removes the node from position index (zero-indexed).  decrements size.
       @return the object in the node that was removed. 
        */
   public Object remove(int index) throws IndexOutOfBoundsException
   {
      if(index >= size || index < 0)
         throw new IndexOutOfBoundsException("Index: " + index + ", Size: " + size);
      /* enter your code below  */
      DLNode p = head.getNext();
      for (int i=0; i<index; i++)
         p = p.getNext();
      Object repl = p.getValue();
      p.getNext().setPrev(p.getPrev());
      p.getPrev().setNext(p.getNext());
      size--;
      return repl;
   }
   
  	/* inserts obj to front of list, increases size.
	    */ 
   public void addFirst(Object obj)
   {
      DLNode addNode = new DLNode(obj, head, head.getNext());
      head.getNext().setPrev(addNode);
      head.setNext(addNode);
      size++;
   }
   
   /* appends obj to end of list, increases size.
       */
   public void addLast(Object obj)
   {
      DLNode addNode = new DLNode(obj, head.getPrev(), head);
      head.getPrev().setNext(addNode);
      head.setPrev(addNode);
      size++;
   }
   
   /* returns the first element in this list  
      */
   public Object getFirst()
   {
      return head.getNext().getValue();
   }
   
   /* returns the last element in this list  
     */
   public Object getLast()
   {
      return head.getPrev().getValue();
   }
   
   /* returns and removes the first element in this list, or
      returns null if the list is empty  
      */
   public Object removeFirst()
   {
      if (size==0)
         return null;
      Object del = head.getNext().getValue();
      head.getNext().getNext().setPrev(head);
      head.setNext(head.getNext().getNext());
      size--;
      return del;
   }
   
   /* returns and removes the last element in this list, or
      returns null if the list is empty  
      */
   public Object removeLast()
   {
      if (size==0)
         return null;
      Object del = head.getPrev().getValue();
      head.getPrev().getPrev().setNext(head);
      head.setPrev(head.getPrev().getPrev());
      size--;
      return del;
   }
   
   /*  returns a String with the values in the list in a 
       friendly format, for example   [Apple, Banana, Cucumber]
       The values are enclosed in [], separated by one comma and one space.
    */
   public String toString()
   {
      DLNode p = head.getNext();
      String out = "[";
      while (p != head) {
         out += ""+p.getValue();
         p = p.getNext();
         if (p != head)
            out += ", ";
      }
      return out+"]";
   }
}