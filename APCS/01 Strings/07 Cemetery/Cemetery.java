// Name: JT-26-22
// Date: 9/3/22

import java.util.*;
import java.io.*;
import java.text.DecimalFormat;

public class Cemetery {
   public static void main(String[] args) {
      File file = new File("cemetery_short.txt");
      // File file = new File("cemetery_orig.txt");
      int numEntries = countEntries(file);
      Person[] cemetery = readIntoArray(file, numEntries);

      for (int i = 0; i < cemetery.length; i++)
         System.out.println(cemetery[i]);
      int min = locateMinAgePerson(cemetery);
      int max = locateMaxAgePerson(cemetery);
      System.out.println("\nIn the St. Mary Magdelene Old Fish Cemetery --> ");
      System.out.println("Name of youngest person: " + cemetery[min].getName());
      System.out.println("Age of youngest person: " + cemetery[min].getAge());
      System.out.println("Name of oldest person: " + cemetery[max].getName());
      System.out.println("Age of oldest person: " + cemetery[max].getAge());

      // makeSorted(cemetery);
   }

   /*
    * Counts and returns the number of entries in File f.
    * Returns 0 if the File f is not valid.
    * Uses a try-catch block.
    * 
    * @param f -- the file object
    */
   public static int countEntries(File f) {
      int x = 0;
      try {
         Scanner sc = new Scanner(f);
         while (sc.hasNextLine()) {
            x++;
            sc.nextLine();
         }
         sc.close();
         return x;
      }
      catch (IOException e) {
         return 0;
      }
   }

   /*
    * Reads the data from file f (you may assume each line has same allignment).
    * Fills the array with Person objects. If File f is not valid return null.
    * 
    * @param f -- the file object
    * 
    * @param num -- the number of lines in the File f
    */
   public static Person[] readIntoArray(File f, int num) {
      try {
         Scanner sc = new Scanner(f);
         Person[] ppl = new Person[num];
         for (int x = 0; x < num; x++) {
            ppl[x] = makeObjects(sc.nextLine());
         }
         sc.close();
         return ppl;
      }
      catch (IOException e) {
         return null;
      }
   }

   // sorts people from Person[] arr and outputs to a file
   public static void makeSorted(Person[] arr) {
      // insertion sort
      for (int i = 0; i < arr.length; i++) {
         int j = i;
         while (j > 0 && arr[j].getAge() < arr[j - 1].getAge()) {
            Person temp = arr[j];
            arr[j] = arr[j - 1];
            arr[j - 1] = temp;
            j--;
         }
      }
      try {
         PrintWriter outfile = new PrintWriter(new FileWriter("sortedPeople.txt"));
         for (Person p : arr) {
            outfile.write(p.toString() + '\n');
         }
         outfile.close();
      }
      catch (IOException e) {
         System.out.println(e);
      }
   }

   /*
    * A helper method that instantiates one Person object.
    * 
    * @param entry -- one line of the input file.
    * This method is made public for gradeit testing purposes.
    * This method should not be used in any other class!!!
    */
   public static Person makeObjects(String entry) {
      String name = entry.substring(0, 25);
      String burialDate = entry.substring(25, 36);
      String age = entry.substring(37, 41).trim();
      return new Person(name, burialDate, age);
   }

   /*
    * Finds and returns the location (the index) of the Person
    * who is the youngest. (if the array is empty it returns -1)
    * If there is a tie the lowest index is returned.
    * 
    * @param arr -- an array of Person objects.
    */
   public static int locateMinAgePerson(Person[] arr) {
      if (arr.length == 0) {
         return -1;
      }
      int pos = 0;
      for (int x = 1; x < arr.length; x++) {
         if (arr[x].age < arr[pos].age) {
            if (arr[pos].age != arr[x].age) {
               pos = x;
            }
         }
      }
      return pos;
   }

   /*
    * Finds and returns the location (the index) of the Person
    * who is the oldest. (if the array is empty it returns -1)
    * If there is a tie the lowest index is returned.
    * 
    * @param arr -- an array of Person objects.
    */
   public static int locateMaxAgePerson(Person[] arr) {
      if (arr.length == 0) {
         return -1;
      }
      int pos = 0;
      for (int x = 1; x < arr.length; x++) {
         if (arr[x].age > arr[pos].age) {
            if (arr[pos].age != arr[x].age) {
               pos = x;
            }
         }
      }
      return pos;
   }
}

class Person {
   // constant that can be used for formatting purposes
   private static final DecimalFormat df = new DecimalFormat("0.0000");

   /* private fields */
   String name;
   String burialDate;
   double age;

   /*
    * a three-arg constructor
    * 
    * @param name, burialDate may have leading or trailing spaces
    * It creates a valid Person object in which each field has the leading and
    * trailing
    * spaces eliminated
    */
   public Person(String name, String burialDate, String age) {
      this.name = name.trim();
      this.burialDate = burialDate.trim();
      this.age = calculateAge(age);
   }

   /*
    * any necessary accessor methods (at least "double getAge()" and
    * "String getName()" )
    * make sure your get and/or set methods use the same data type as the field
    */
   public String getName() {
      return name;
   }

   public String getBurialDate() {
      return burialDate;
   }

   public double getAge() {
      return age;
   }

   /*
    * handles the inconsistencies regarding age
    * 
    * @param a = a string containing an age from file. Ex: "12", "12w", "12d"
    * returns the age transformed into year with 4 decimals rounding
    */
   public double calculateAge(String a) {
      if (a.indexOf('w') > -1) {
         return Double.parseDouble(df.format(Double.parseDouble(a.substring(0, a.indexOf('w'))) * 7 / 365));
      }
      else if (a.indexOf('d') > -1) {
         return Double.parseDouble(df.format(Double.parseDouble(a.substring(0, a.indexOf('d'))) / 365));
      }
      else {
         return Double.parseDouble(a);
      }
   }

   public String toString() {
      return this.name + ", " + this.burialDate + ", " + this.age;
   }

}

/******************************************
 * 
 * John William ALLARDYCE, 17 Mar 1844, 2.9
 * Frederic Alex. ALLARDYCE, 21 Apr 1844, 0.17
 * Philip AMIS, 03 Aug 1848, 1.0
 * Thomas ANDERSON, 06 Jul 1845, 27.0
 * Edward ANGEL, 20 Nov 1842, 22.0
 * Lucy Ann COLEBACK, 23 Jul 1843, 0.2685
 * Thomas William COLLEY, 08 Aug 1833, 0.011
 * Joseph COLLIER, 03 Apr 1831, 58.0
 * 
 * In the St. Mary Magdelene Old Fish Cemetery -->
 * Name of youngest person: Thomas William COLLEY
 * Age of youngest person: 0.011
 * Name of oldest person: Joseph COLLIER
 * Age of oldest person: 58.0
 * 
 **************************************/