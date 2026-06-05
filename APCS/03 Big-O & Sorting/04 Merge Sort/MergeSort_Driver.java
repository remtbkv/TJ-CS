// Name: J1-26-22
// Date: 10/27/22

import java.util.*;
import java.io.*;

public class MergeSort_Driver
{
   public static void main(String[] args) throws Exception
   {
      //Part 1, for doubles
      double[] array = {3,1,4,1,5,9,2,6};    // small example array from the MergeSort handout
      // int n = (int)(Math.random()*50+10);
      // double[] array = new double[n];
      // for(int k = 0; k < array.length; k++)
      //    array[k] = Math.random();
         	
      MergeSort.sort(array);
   
      print(array);
      if( isAscending(array) )
         System.out.println("In order!");
      else
         System.out.println("oops!");
         
      //Part 2, for Comparables
      int size = 100;
      Scanner sc = new Scanner(new File("declaration.txt"));
      Comparable[] arrayStr = new String[size];
      for(int k = 0; k < arrayStr.length; k++)
         arrayStr[k] = sc.next();

      MergeSort.sort(arrayStr);
      print(arrayStr);
      System.out.println();
      if( isAscending(arrayStr) )
         System.out.println("In order!");
      else
         System.out.println("Out of order  :-( ");
   }

   
   public static void print(double[] a)   
   {                             
      for(double number : a)    
         System.out.print(number + " ");
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
  
   public static void print(Object[] peach)
   {
      for (Object p : peach)
         System.out.print(p + " ");
      System.out.println();
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
/////////////////////////////////////////////
// 15 Oct 07
// MergeSort Code Handout
// from Lambert & Osborne, p. 482 - 485

class MergeSort
{
   private static final int CUTOFF = 10; // for small lists, recursion isn't worth it
  
   public static void print(double[] array, int start, int end) {
      for (int i=start; i<end; i++) {
         System.out.print(array[i] + " ");
      }
      System.out.println();
   }

   public static void sort(double[] array)
   { 
      double[] copyBuffer = new double[array.length];
      mergeSortHelper(array, copyBuffer, 0, array.length - 1);
   }
   
   /*  array			array that is being sorted
       copyBuffer		temp space needed during the merge process
       low, high		bounds of subarray
       middle			midpoint of subarray   
   */
   private static void mergeSortHelper(double[] array, double[] copyBuffer,
                                                      int low, int high)
   {
      // if (high - low < CUTOFF) //switch to selection sort  when
      //    SelectionLowHigh.sort(array, low, high); //the list gets small enough 
      // else if (low < high) {
      if (low < high) {
         int middle = (low + high) / 2;
         mergeSortHelper(array, copyBuffer, low, middle);
         mergeSortHelper(array, copyBuffer, middle + 1, high);
         merge(array, copyBuffer, low, middle, high);
      }
   }
   
   /* array				array that is being sorted
      copyBuffer		temp space needed during the merge process
      low				beginning of first sorted subarray
      middle			end of first sorted subarray
      middle + 1		beginning of second sorted subarray
      high				end of second sorted subarray   
   */
   public static void merge(double[] array, double[] copyBuffer, int low, int middle, int high)
   {
      int i1 = low;
      int i2 = middle + 1;
      int i = low;

      while (i1 <= middle && i2 <= high) {
         if (array[i1] <= array[i2]) {
            copyBuffer[i] = array[i1];
            i1++;
         }
         else {
            copyBuffer[i] = array[i2];
            i2++;
         }
         i++;
      }
      while (i1 <= middle) {
         copyBuffer[i] = array[i1];
			i1++;
			i++;
		}
      while (i2 <= high) {
         copyBuffer[i] = array[i2];
			i2++;
			i++;
      }

      for (int j = low; j <= high; j++) {
         array[j] = copyBuffer[j];
      }
   }	
      
   @SuppressWarnings("unchecked")//this removes the warning for Comparable
   public static void sort(Comparable[] array)
   { 
      Comparable[] copyBuffer = new Comparable[array.length];
      mergeSortHelper(array, copyBuffer, 0, array.length - 1);
   }

   /* array				array that is being sorted
      copyBuffer		temp space needed during the merge process
      low, high		bounds of subarray
      middle			midpoint of subarray  */
   @SuppressWarnings("unchecked")
   private static void mergeSortHelper(Comparable[] array, Comparable[] copyBuffer, int low, int high)
   {
     if (low < high)
      {
         int middle = (low + high) / 2;
         mergeSortHelper(array, copyBuffer, low, middle);
         mergeSortHelper(array, copyBuffer, middle + 1, high);
         merge(array, copyBuffer, low, middle, high);
      }
   }
   
   /* array				array that is being sorted
      copyBuffer		temp space needed during the merge process
      low				beginning of first sorted subarray
      middle			end of first sorted subarray
      middle + 1		beginning of second sorted subarray
      high				end of second sorted subarray   */
   @SuppressWarnings("unchecked")
   public static void merge(Comparable[] array, Comparable[] copyBuffer, int low, int middle, int high)
   {
      int i1 = low;
      int i2 = middle + 1;
      int i = low;
      
      while (i1 <= middle && i2 <= high) {
         if (array[i1].compareTo(array[i2])<=0) {
            copyBuffer[i] = array[i1];
            i1++;
         }
         else {
            copyBuffer[i] = array[i2];
            i2++;
         }
         i++;
      }

      while (i1 <= middle) {
         copyBuffer[i] = array[i1];
			i1++;
			i++;
		}
      while (i2 <= high) {
         copyBuffer[i] = array[i2];
			i2++;
			i++;
      }
      for (int j = low; j <= high; j++) {
         array[j] = copyBuffer[j];
      }
   }    

}

/***************************************************
This is the extension.  You will have to uncomment Lines 89-90 above.
***************************************************/

class SelectionLowHigh
{
   public static void sort(double[] array, int low, int high)
   {  
      for (int i=high; i>low; i--) {
         swap(array, findMax(array, low, high+1),i);
      }
   }
   private static int findMax(double[] array, int low, int upper)
   {
      int max = low;
      for (int i = low; i < upper; i++) {
         if (array[i] > array[max]) {
            max = i;
         }
      }
      return max;
   }
   private static void swap(double[] array, int a, int b)
   {
      double temp = array[a];
      array[a] = array[b];
      array[b] = temp;
   } 
}
