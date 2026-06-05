// Name: J1-26-22
// Date: 9/26/22
  
import java.util.*;

public class Permutations
{
   public static int count = 0;
    
   public static void main(String[] args)
   {
      Scanner sc = new Scanner(System.in);
      System.out.println("How many digits? ");
      int n = sc.nextInt();
      superprime(n); 
      
      if(count==0) {
         System.out.println("no superprimes");
      }
      else {
         System.out.println("Count is "+count);
      }
   }
   
    /**
     * Builds all the permutations of a string of length n containing Ls and Rs
     * @param s A string 
     * @param n An postive int representing the length of the string
     */
   public static void leftRight(String s, int n)
   {
	   if (s.length() == n) {
			System.out.println(s);
	    }
	    else {
			leftRight(s+"L", n);
			leftRight(s+"R", n);
		}
   }
   
    /**
     * Builds all the permutations of a string of length n containing odd digits
     * @param s A string 
     * @param n A postive int representing the length of the string
     */
   public static void oddDigits(String s, int n)
   {
	   if (s.length() == n) {
			System.out.println(s);
		}
		else {
			oddDigits(s+"1", n);
			oddDigits(s+"3", n);
			oddDigits(s+"5", n);
			oddDigits(s+"7", n);
			oddDigits(s+"9", n);
		}
   }
      
    /**
     * Builds all combinations of a n-digit number whose value is a superprime
     * @param n A positive int representing the desired length of superprimes  
     */
   public static void superprime(int n)
   {
      if (n>0) {
         recur(2, n);
         recur(3, n); 
         recur(5, n);
         recur(7, n);
      }
   }

    /**
     * Recursive helper method for superprime
     * @param k The possible superprime
     * @param n A positive int representing the desired length of superprimes
     */
   private static void recur(int k, int n)
   {
      if (isPrime(k)) {
         if ((k+"").length()<n) {
            recur(Integer.parseInt(k+"1"), n);
            recur(Integer.parseInt(k+"3"), n);
            recur(Integer.parseInt(k+"5"), n);
            recur(Integer.parseInt(k+"7"), n);
            recur(Integer.parseInt(k+"9"), n);
         }
         else {
            System.out.println(k);
            count+=1;
         }
      }
   }

    /**
     * Determines if the parameter is a prime number.
     * @param n An int.
     * @return true if prime, false otherwise.
     */
   public static boolean isPrime(int n)
   {
      if (n<=1) {
         return false;
      }
      else if (n==2) {
         return true;
      }
      else if (n%2==0) {
         return false;
      }
      for (int x=3; x<Math.sqrt(n)+1; x=x+2) {
         if (n%x==0) {
            return false;
         }
      }
      return true;
   }
}
