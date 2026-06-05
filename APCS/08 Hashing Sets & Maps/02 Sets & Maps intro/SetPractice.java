import java.util.*;
public class SetPractice
{
   public static void main(String[] args)
   {
      Set<String> s = new HashSet<String>();
      s.add("Mary");
      s.add("Joan");
      s.add("Mary");    //duplicate!
      s.add("Dennis");
      s.add("Bob");
      s.add("MaryAnn");
      s.add("Zoe");
      System.out.println("Size:  " + s.size());
      Iterator <String> it = s.iterator(); //iterator   
      while(it.hasNext())
         System.out.print(it.next() + " ");
      System.out.println();
      
      Set<String> t = new TreeSet<String>(s);//from HashSet to TreeSet
      for( String str : t )                //for-each
         System.out.print( str + " " );
      System.out.println();                 //<-----place breakpoint here
      System.out.println(s);    //print any Collection--wow!
      System.out.println(t);
      
      //Student practice:  add more names, print the set, remove a name, print the set
      
      
      
   }
}
/******************
 
 Size:  3
 Joan Mary Dennis 
 Dennis Joan Mary 
 [Joan, Mary, Dennis]
 [Dennis, Joan, Mary]
     
 ************************/