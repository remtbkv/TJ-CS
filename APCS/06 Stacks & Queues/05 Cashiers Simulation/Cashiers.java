//name: J1-26-23
//date: 1/26/23

import java.util.*;
import java.io.*;
public class Cashiers
{
   public static final int CUSTOMERS_PER_MINUTE = 2;  
   public static int Total = 0;
   public static int Served = 0;
   public static int customersCheckedOut = 0;
   public static int longestWaitTime = 0;
   public static int longestQueue = 0;
   public static int totalMinutes = 0;
   public static int num=0;
   public static void main(String[] args) throws FileNotFoundException
   {     
      System.out.println("Cashiers and Customers Simulation! ");
      Scanner kb = new Scanner(System.in);
      System.out.print("How many cashiers? ");
      int number_of_cashiers = kb.nextInt();
      System.out.print("How long, in minutes, should the simulation run? ");
      int time = kb.nextInt();
      num = number_of_cashiers;
      waitTimes(time, number_of_cashiers);  //run the simulation
   } 
 
   public static void outfileCashiersAndQueues(PrintWriter outfile, int min, ArrayList<Queue<Customer>> cashier, Queue<Customer> removed)
   {
      if (removed.size()>0) {
         for (Customer c : removed) {
            Served++;
            Total+=c.getTimeSpent();
            outfile.println("customers served: "+Served+", Customer from minute "+c.getTimeArrived()+" had total wait time: "+c.getTimeSpent()+", total minutes (for all customers): "+Total);
         }
      }
      outfile.println("minute " + min + ": ");
      for( Queue<Customer> q : cashier )
      {
         outfile.print("      ");
         for( Customer c : q )
            outfile.print(c+" ");
         outfile.println();
      }
      outfile.println("*****");
   }

    public static Queue<Customer> shortestQ(ArrayList<Queue<Customer>> cashiers) {
        Queue<Customer> min = cashiers.get(0);
        for (Queue<Customer> q : cashiers)
            if (q.size()<min.size())
                min = q;
        return min;
    }

   public static double calculateAverage(int totalMinutes, int customers)
   {
      return (int)(1.0 * totalMinutes/customers * 10)/10.0;
   }
   
   public static PrintWriter setUpFile()
   {
      PrintWriter outfile = null; 
      try
      {
         outfile = new PrintWriter(new FileWriter("customerWaitTimes.txt"));
      }
      catch(IOException e)
      {
         System.out.println("File not created");
         System.exit(0);
      }
      return outfile;
   }

   public static void waitTimes(int time, int num)
   {
      PrintWriter out = setUpFile();  
      ArrayList<Queue<Customer>> cashiers = new ArrayList<Queue<Customer>>();
      for(int i=0; i<num; i++)
         cashiers.add( new LinkedList<Customer>() );
      for (int t=0; t<time; t++) { 
         Queue<Customer> removed = new LinkedList<Customer>();
         for (Queue<Customer> q : cashiers) {
            if (!q.isEmpty()) {
                for (Customer c : q) c.increaseSpent();
                Customer c = q.peek();
                c.decreaseWait();
                if (c.getWaitTime()==0) {
                    customersCheckedOut++;
                    int spent = c.getTimeSpent();
                    if (spent>longestWaitTime) longestWaitTime = spent;
                    totalMinutes+=spent;
                    removed.add(q.remove());
                }
            }
         }
         for (int i=0; i<CUSTOMERS_PER_MINUTE; i++) { // add customers and log info
            Customer c = new Customer(t);
            if (c.getWaitTime()>longestWaitTime) longestWaitTime = c.getWaitTime();
            shortestQ(cashiers).add(c);
            for (Queue<Customer> q : cashiers) if (q.size()>longestQueue) longestQueue=q.size();
         }
         outfileCashiersAndQueues(out, t, cashiers, removed);
      }
      out.println();
      out.println("Number of cashiers = "+ num);
      out.println("Customers joining each minute = "+ CUSTOMERS_PER_MINUTE);
      out.println("Customers who joined queues = " + CUSTOMERS_PER_MINUTE*time);
      out.println("Customers who were checked out = " + customersCheckedOut);
      out.println("Total wait: "+totalMinutes);
      out.println("Average wait time of those who were checked out = " + calculateAverage(totalMinutes, customersCheckedOut));
      out.println("Longest wait time of those who were checked out = " + longestWaitTime);
      out.println("Longest queue of customers = " + longestQueue);
      out.close();
      System.out.println("Number of cashiers = "+ num);
      System.out.println("Customers joining each minute = "+ CUSTOMERS_PER_MINUTE);
      System.out.println("Customers who joined queues = " + CUSTOMERS_PER_MINUTE*time);
      System.out.println("Customers who were checked out = " + customersCheckedOut);
      System.out.println("Total wait: "+totalMinutes);
      System.out.println("Average wait time of those who were checked out = " + calculateAverage(totalMinutes, customersCheckedOut));
      System.out.println("Longest wait time of those who were checked out = " + longestWaitTime);
      System.out.println("Longest queue of customers = " + longestQueue);
}
   
   static class Customer      
   {
      private int arrivedAt;
      private int timeSpentAtCashier;
      private int waitTime;
      
      public Customer(int t) {
         arrivedAt = t;
         timeSpentAtCashier = 0;
         waitTime = (int)(Math.random()*5)+2;
      }
      public int getWaitTime() {
         return waitTime;
      }
      public int getTimeArrived() {
         return arrivedAt;
      }
      public int getTimeSpent() {
         return timeSpentAtCashier;
      }
      public void decreaseWait() {
          if (waitTime>0) waitTime--;
      }
      public void increaseSpent() {
         timeSpentAtCashier++;
      }
      public String toString() {
         return arrivedAt + ":"+waitTime;
      }
   }
}

/******************************************************
 Cashiers and Customers Simulation! 
 How many cashiers? 3
 How long, in minutes, should the simulation run? 10
 minute 0: 
           4 
           5 
           
 minute 1: 
           3 6 
           4 
           5 
 minute 2: 
           2 6 
           3 3 
           4 6 
 minute 3: 
           1 6 6 
           2 3 6 
           3 6 
 minute 4: 
           6 6 5 
           1 3 6 
           2 6 6 
 minute 5: 
           5 6 5 4 
           3 6 5 
           1 6 6 
 minute 6: 
           4 6 5 4 
           2 6 5 5 
           6 6 2 
 minute 7: 
           3 6 5 4 3 
           1 6 5 5 
           5 6 2 4 
 minute 8: 
           2 6 5 4 3 
           6 5 5 5 
           4 6 2 4 5 
 minute 9: 
           1 6 5 4 3 5 
           5 5 5 5 3 
           3 6 2 4 5 
 Number of cashiers = 3
 Customers joining each minute = 2
 Customers who joined queues = 20
 Customers who were checked out = 4
 Average wait time of those who were checked out = 6.0
 Longest wait time of those who were checked out = 7
 Longest queue of customers = 6

****************************************************/