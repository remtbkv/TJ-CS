import java.util.*;
public class Position_Driver
{
   public static void main(String[] args)
   {
      Set<Position> allPositions = new HashSet<Position>();
      for( int x=0; x<100; x++)  
      {
         allPositions.add(new Position((int)(Math.random() * 5),
                                       (int)(Math.random() * 5)));
      }
      System.out.println( allPositions );
      
      List<String> noDuplicates = new ArrayList<>();  //convert them to Strings
      for( Position p : allPositions )
         noDuplicates.add(p.toString());
      for( int i = 0; i < noDuplicates.size(); i++)
         for(int j=noDuplicates.size()-1; j>i; j--)
            if(noDuplicates.get(i).equals(noDuplicates.get(j)) )
               noDuplicates.remove(j);
               
      System.out.println("Size of the hashSet: " + allPositions.size()); 
      System.out.println("Size without duplicates: " + noDuplicates.size());               
   }
}

/**************************************************************
     ----jGRASP exec: java Position_Driver
 [(2, 1), (2, 3), (4, 2), (4, 4), (0, 2), (4, 0), (0, 4), (0, 0), (3, 4), (3, 2), (1, 3), (3, 0), (1, 1), (2, 0), (2, 2), (2, 4), (4, 3), (0, 3), (4, 1), (0, 1), (3, 3), (3, 1), (1, 4), (1, 2), (1, 0)]
 Size of the hashSet: 25
 Size without duplicates: 25
 
  ----jGRASP: operation complete.
  ********************************************/