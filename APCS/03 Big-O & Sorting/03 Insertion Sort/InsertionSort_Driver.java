 //Name: J1-26-22
 //Date: 10/25/22

import java.util.*;
import java.io.*;

public class InsertionSort_Driver
{
   public static void main(String[] args) throws Exception
   {
      //Part 1, for doubles
      int n = (int)(Math.random())+10;
      double[] array = new double[n];
      for(int k = 0; k < array.length; k++)
         array[k] = Math.random()*100;	
      
      Insertion.sort(array);  //students write
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
   
      Insertion.sort(arrayStr);   //students write
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
      for(Object temp : papaya)    
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
   
   @SuppressWarnings("unchecked")//this removes the warning for Comparable
   public static boolean isAscending(Comparable[] a)
   {
      int prev = 0;
      for (int i = 1; i < a.length; i++) {
         if (a[i].compareTo(a[prev])>=0)
            prev++;
         else
            return false;
      }
      return true;
   }
}

//**********************************************************

class Insertion
{
   public static void sort(double[] array)
   { 
      for (int i = 1; i < array.length; i++) {
         double temp = array[i];
         int place = shift(array, i-1, temp);
         array[place] = temp;
      }
   }
 
   private static int shift(double[] array, int index, double value)
   {
      while (index >= 0 && value < array[index]) {
         array[index + 1] = array[index];
         index--;
      }
      return index + 1;
   }
 
   @SuppressWarnings("unchecked")
   public static void sort(Comparable[] array)
   { 
      for (int i = 1; i < array.length; i++) {
         Comparable temp = array[i];
         int place = shift(array, i-1, temp);
         array[place] = temp;
      }
   }
   
   @SuppressWarnings("unchecked")
   private static int shift(Comparable[] array, int index, Comparable value)
   {
      while (index >= 0 && value.compareTo(array[index])<0) {
         array[index + 1] = array[index];
         index--;
      }
      return index+1;
   }
}
