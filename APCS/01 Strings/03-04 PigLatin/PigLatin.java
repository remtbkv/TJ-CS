// Name: J1-26-22
// Date: 8/28/22

import java.util.*;
import java.io.*;

public class PigLatin {
   public static void main(String[] args) {
      // part_1_using_pig();
      part_2_using_piglatenizeFile();

      /* extension only */
      // String pigLatin = pig("What!?");
      // System.out.print(pigLatin + "\t\t" + pigReverse(pigLatin));
      // pigLatin = pig("{(Hello!)}");
      // System.out.print("\n" + pigLatin + "\t\t" + pigReverse(pigLatin));
      // pigLatin = pig("\"McDonald???\"");
      // System.out.println("\n" + pigLatin + " " + pigReverse(pigLatin));
   }

   public static void part_1_using_pig() {
      Scanner sc = new Scanner(System.in); // input from the keyboard
      while (true) {
         System.out.print("\nWhat word? ");
         String s = sc.next(); // reads up to white space
         if (s.equals("-1")) {
            System.out.println("Goodbye!");
            sc.close();
            System.exit(0);
         }
         String p = pig(s);
         System.out.println(p);
      }
   }

   public static final String punct = ",./;:'\"?<>[]{}|`~!@#$%^&*()-";
   public static final String letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz";
   public static final String vowels = "AEIOUYaeiouy";

   public static String pig(String s) {
      if (s.length() == 0) {
         return "";
      }
      boolean up = false;
      String sPunc = "";
      String ePunc = "";
      int x = 0;

      // vowels
      if (Character.toLowerCase(s.charAt(0)) == 'y') {
         x++;
      }
      while (vowels.indexOf(s.charAt(x)) < 0 && x < s.length()) {
         if (x == s.length() - 1 && s.charAt(0) != 'y') {
            return "**** NO VOWEL ****";
         }
         x++;
      }

      // starting punctuation
      x = 0;
      while (letters.indexOf(s.charAt(x)) < 0 && x < s.length()) {
         x++;
      }
      sPunc = s.substring(0, x);
      s = s.substring(x);

      // ending punctuation
      x = s.length() - 1;
      while (letters.indexOf(s.charAt(x)) < 0 && x > 0) {
         x--;
      }
      ePunc = s.substring(x + 1);
      s = s.substring(0, x + 1);

      // uppercase
      x = 0;
      if (Character.isUpperCase(s.charAt(0))) {
         s = Character.toLowerCase(s.charAt(0)) + s.substring(1);
         up = true;
      }

      // main
      x = 0;
      if (vowels.indexOf(s.charAt(0)) > -1 && s.charAt(0) != 'y') {
         s += "way";
      }
      else {
         if (s.charAt(0) == 'y') {
            x++;
         }
         while (x < s.length() && vowels.indexOf(s.charAt(x)) < 0) {
            if (s.length() > x + 2 && s.substring(x, x + 2).toLowerCase().equals("qu")) {
               x = x + 2;
            }
            else {
               x++;
            }
         }
         s = s.substring(x) + s.substring(0, x) + "ay";
      }

      if (up) {
         return sPunc + Character.toUpperCase(s.charAt(0)) + s.substring(1) + ePunc;
      }
      return sPunc + s + ePunc;
   }

   public static void part_2_using_piglatenizeFile() {
      Scanner sc = new Scanner(System.in);
      System.out.print("input filename including .txt: ");
      String fileNameIn = sc.next();
      System.out.print("output filename including .txt: ");
      String fileNameOut = sc.next();
      piglatenizeFile(fileNameIn, fileNameOut);
      System.out.println("Piglatin done!");
      sc.close();
   }

   /******************************
    * piglatinizes each word in each line of the input file
    * precondition: both fileNames include .txt
    * postcondition: output a piglatinized .txt file
    ******************************/
   public static void piglatenizeFile(String fileNameIn, String fileNameOut) {
      Scanner infile = null;
      try {
         infile = new Scanner(new File(fileNameIn));
      }
      catch (IOException e) {
         System.out.println("oops");
         System.exit(0);
      }

      PrintWriter outfile = null;
      try {
         outfile = new PrintWriter(new FileWriter(fileNameOut));
      }
      catch (IOException e) {
         System.out.println("File not created");
         System.exit(0);
      }

      StringTokenizer st;
      ArrayList<String> arrL = new ArrayList<String>();
      String s;

      while (infile.hasNextLine()) {
         st = new StringTokenizer(infile.nextLine(), " ", true);
         while (st.hasMoreTokens()) {
            s = st.nextToken();
            if (!s.equals(" ")) {
               arrL.add(pig(s));
            }
            else {
               arrL.add(s);
            }
         }
         for (String str : arrL) {
            outfile.write(str);
         }
         outfile.write('\n');
         arrL.clear();
      }

      outfile.close();
      infile.close();
   }

   public static String pigReverse(String s) {
      if (s.length() == 0)
         return "";

      boolean up2 = false;
      String sPunc2 = "";
      String ePunc2 = "";
      int x = 0;

      // starting punctuation
      x = 0;
      while (letters.indexOf(s.charAt(x)) < 0 && x < s.length()) {
         x++;
      }
      sPunc2 = s.substring(0, x);
      s = s.substring(x);

      // ending punctuation
      x = s.length() - 1;
      while (letters.indexOf(s.charAt(x)) < 0 && x > 0) {
         x--;
      }
      ePunc2 = s.substring(x + 1);
      s = s.substring(0, x + 1);

      // uppercase
      x = 0;
      if (Character.isUpperCase(s.charAt(0))) {
         s = Character.toLowerCase(s.charAt(0)) + s.substring(1);
         up2 = true;
      }

      // reverse
      x = 0;
      char[] s2 = new char[s.length()];
      while (x < s.length()) {
         s2[x] = s.charAt(s.length() - 1 - x);
         x++;
      }
      s = new String(s2);

      if (up2) {
         return sPunc2 + Character.toUpperCase(s.charAt(0)) + s.substring(1) + ePunc2;
      }
      return sPunc2 + s + ePunc2;
   }
}
