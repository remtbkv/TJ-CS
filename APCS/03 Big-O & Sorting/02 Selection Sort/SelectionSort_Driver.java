// Name: J1-26-22
// Date: 10/25/22

import java.util.*;
import java.io.*;

public class SelectionSort_Driver
{
   public static void main(String[] args) throws Exception
   {
     //Part 1, for doubles
      int n = (int)(Math.random()*100)+20;
      double[] array = new double[n];
      for(int k = 0; k < array.length; k++)
         array[k] = Math.random()*100;	
      
      Selection.sort(array);   //students must write
      print(array);
      if( isAscending(array) )
         System.out.println("In order!");
      else
         System.out.println("Out of order  :-( ");
      System.out.println();
      
      //Part 2, for Strings
      int size = 100;
      Scanner sc = new Scanner(new File("declaration.txt"));
      Comparable[] arrayStr = new String[size];
      for(int k = 0; k < arrayStr.length; k++)
         arrayStr[k] = sc.next();	
   
      Selection.sort(arrayStr);  //students must write
      print(arrayStr);
      System.out.println();
      
      if( isAscending(arrayStr) )
         System.out.println("In order!");
      else
         System.out.println("Out of order  :-( ");
   }
  
   public static void print(double[] a)
   {
      // for(int k = 0; k < a.length; k++)
         // System.out.println(a[k]);
      for(double temp: a)         //for-each
         System.out.print(temp+" ");
      System.out.println();
   }
  
   public static void print(Object[] papaya)
   {
      for(Object temp : papaya)     //for-each
         System.out.print(temp + " ");
      System.out.println();
   }
  
   public static boolean isAscending(double[] a)
   {
      int prev = 0;
      for (int i = 1; i < a.length; i++) {
         if (a[i] >= a[prev]) {
            prev++;
         }
         else
            return false;
      }
      return true;
   }
   
   @SuppressWarnings("unchecked")
   public static boolean isAscending(Comparable[] a)
   {
      int prev = 0;
      for (int i = 1; i < a.length; i++) {
         if (a[i].compareTo(a[prev])>=0) {
            prev++;
         }
         else
            return false;
      }
      return true;
   }
}
/////////////////////////////////////////////////////

class Selection
{
   public static void sort(double[] array)
   {
      for (int i=array.length; i>0; i--) {
         swap(array, findMax(array, i),i-1);
      }
   }

   
   // upper controls where the inner loop of the Selection Sort ends
   private static int findMax(double[] array, int upper)
   {
      int max = 0;
      for (int i = 1; i < upper; i++) {
         if (array[i] > array[max])
            max = i;
      }
      return max;
   }
   private static void swap(double[] array, int a, int b)
   {
      double temp = array[b];
      array[b] = array[a];
      array[a] = temp;
   }   	
   
	/*******  for Comparables ********************/
   @SuppressWarnings("unchecked")
   public static void sort(Comparable[] array)
   {
      for (int i=array.length; i>0; i--) {
         swap(array, findMax(array, i),i-1);
      }
   }
   
   @SuppressWarnings("unchecked")
   public static int findMax(Comparable[] array, int upper)
   {
      int max = 0;
      for (int i = 1; i < upper; i++) {
         if (array[i].compareTo(array[max])>0)
            max = i;
      }
      return max;
   }
   public static void swap(Object[] array, int a, int b)
   {
      Object temp = array[b];
      array[b] = array[a];
      array[a] = temp;
   }
}

