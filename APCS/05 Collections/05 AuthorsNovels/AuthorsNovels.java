//  Name:  J1-26-23

import java.io.*;
import java.util.*;

public class AuthorsNovels
{
   public static void main(String[] args) throws IOException
   {
      /*  start the lab  */
      Scanner keyboard = new Scanner(System.in);
      System.out.print("\nEnter input file name: ");
      String inFileName = keyboard.nextLine().trim()+".txt";
      // String inFileName = "C:\\Users\\remtb\\OneDrive - Fairfax County Public Schools\\CS\\APCS\\05 Collections\\05 AuthorsNovels\\infile2.txt";
      Scanner inputFile = new Scanner(new File(inFileName));
      //System.out.print("\nEnter output file name: ");
      //String outFileName = keyboard.nextLine().trim();
      AuthorList authors = readAndMakeTheList(inputFile);
      String outFileName = "authorsNovelsOut.txt";
      PrintWriter outputFile = new PrintWriter(new FileWriter(outFileName));
      outputFile.println( authors.toString() );
      inputFile.close(); 						
      outputFile.close();
      keyboard.close();
      System.out.println("Done.");
   }
   
   public static AuthorList readAndMakeTheList(Scanner inputFile)
   {
      AuthorList theList = new AuthorList();
      while(inputFile.hasNextLine())
      {
         theList.readOneLine(inputFile.nextLine());
      }
      return theList;
   }
}

class AuthorList extends ArrayList<AuthorEntry>
{
    /**   you get an ArrayList for free   **/
   public AuthorList()
   {
      super();
   }
     /** extracts the author and book from oneLine.
         calls addAuthorEntry      
      */
   public void readOneLine(String oneLine) 
   {  
      String[] arr = oneLine.split(", ");
      addAuthorEntry(arr[0], arr[1]);
   }
   
    /** use a listIterator.  Needs to call .previous() 
          either inserts a new AuthorEntry object, or 
          adds a novel to a previous AuthorEntry object,
          in alphabetic order
    */
   public void addAuthorEntry(String name, String book)
   {
      name = name.toUpperCase();
      if (this.size()==0)
         this.add(new AuthorEntry(name, book));
      else {
         ListIterator<AuthorEntry> it = this.listIterator();
         while (it.hasNext()) {
            AuthorEntry curr = it.next();
            if (curr.getName().equals(name)) {
               curr.addNovel(book);
               break;
            }
            else if (curr.getName().compareTo(name)>0) {
               it.previous();
               it.add(new AuthorEntry(name, book));
               it.next();
               break;
            }
            else if (!it.hasNext())
               it.add(new AuthorEntry(name, book));
         }         
       }
   }
   
   public String toString()
   {  
      String str = "";
      for (AuthorEntry a: this) {
         str += a+"\n";
      }
      return str;
   }
}

class AuthorEntry implements Comparable<AuthorEntry>
{
   //fields
   private String name;
   private ArrayList<String> novels;
   
   //two constructors. argument n may be in lowercase. 
   public AuthorEntry(String n)
   {
      name = n.toUpperCase();
      novels = new ArrayList<String>();
   }
   public AuthorEntry(String n, String book)
   {
      name = n.toUpperCase();
      novels = new ArrayList<String>();
      novels.add(book);
   }
   
   /**  appends book to novels, but only if it is not already in that list.    
       */
   public void addNovel(String book)
   {
      for (String s: novels)
         if (s.equals(book))
            return;
      novels.add(book);
   }
   
   /** two standard accessor methods  */
   public String getName() {
      return name;
   }
   public ArrayList<String> getNovels() {
      return novels;
   }
   /**  pre:  name is not an empty string.  novels might be an empty ArrayList.
       uses:  either a for-each loop or an iterator
       post:  returns a string representation of this AuthorEntry in the format as 
              shown on each line of the output file.  
     */
   public String toString()
   {
      String out = name;
      if (novels.size()>0) {
         out+=": ";
         ListIterator<String> it = novels.listIterator();
         while (it.hasNext())  {
            out += it.next();
            if (it.hasNext()) out+=", ";
         }
      }
      return out;
   }

   public int compareTo(AuthorEntry other) {
      return name.compareTo(other.getName());
   }
}


/********************   Extension   
// class Author extends ArrayList<String> implements Comparable<Author>
// {
// }


/**********************  SAMPLE RUN  ********************************
 name: AAAA
 novels: []
 toString(): AAAA
 name: DD
 novels: [y, z, x]
 toString(): DD: y, z, x
 3
 -3
 
 Enter input file name: infile2
 Done.
 
 **********************************************************/
   /******** Output file for infile2:
   
   DOSTOEVSKI: Crime and Punishment, The Possessed, The Brothers Karamazov, The Grand Inquisitor
   FLAUBERT: Madame Bovary, A Simple Heart, Memoirs of a Madman, Sentimental Education
   STENDHAL: The Red and the Black
   TOLSTOY: Anna Karenina, War and Peace, The Death of Ivan Illyich, The Kreutzer Sonata
   
    */