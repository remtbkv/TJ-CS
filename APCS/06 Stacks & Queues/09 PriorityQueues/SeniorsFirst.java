// name: J1-26-23
// date: 1/29/23

import java.util.*;
import java.io.*;
public class SeniorsFirst
{
   public static final int CUSTOMERS_PER_MINUTE = 2;  
   private static String[] classes = new String[]{"Senior", "Junior", "Sophomor", "Freshman"};
   private static int[] longest = new int[]{0,0,0,0}, total = new int[]{0,0,0,0}, checkedWait = new int[]{0,0,0,0}, checked = new int[]{0,0,0,0}, Total = new int[]{0,0,0,0};
   private static int Served = 0;
   public static void main(String[] args) throws FileNotFoundException
   {     
      PrintWriter outfile = setUpFile();      
      
      System.out.println("Seniors First Simulation! ");
      Scanner kb = new Scanner(System.in);
      System.out.print("How many cashiers? ");
      int number_of_cashiers = kb.nextInt();
      System.out.print("How long, in minutes, should the simulation run? ");
      int time = kb.nextInt();
      
      waitTimes(time, number_of_cashiers, outfile);  //run the simulation
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
  
   public static void outfileCashiersAndQueues(PrintWriter outfile, int min, ArrayList<MyPriorityQueue<Customer>> cashier, Queue<Customer> removed)
   {
      if (removed.size()>0) {
         for (Customer c : removed) {
            int num = c.getNum();
            Served++;
            Total[num]+=c.getTimeSpent();
            outfile.println("customers served: "+Served+", Customer from minute "+c+" had total wait time: "+c.getTimeSpent()+", total minutes (for all customers of the same grade): "+Total[num]);
         }
      }
      outfile.println("minute " + min + ": ");
      for( MyPriorityQueue<Customer> q : cashier )
      {
         outfile.print("      ");
         for( Customer c : q )
            outfile.print(c+" ");
         outfile.println();
      }
      outfile.println("*****");
   }
  
   public static MyPriorityQueue<Customer> shortestQ(ArrayList<MyPriorityQueue<Customer>> cashiers) {
      MyPriorityQueue<Customer> min = cashiers.get(0);
      for (MyPriorityQueue<Customer> q : cashiers)
         if (q.size()<min.size())
            min = q;
      return min;
   }

   public static void waitTimes(int time, int number_of_cashiers, PrintWriter outfile)
   {
      ArrayList<MyPriorityQueue<Customer>> cashiers = new ArrayList<>();
      for(int i=0; i<number_of_cashiers; i++)
         cashiers.add( new MyPriorityQueue<Customer>() );
      PrintWriter out = setUpFile();   
      for (int t=0; t<time; t++) { 
         Queue<Customer> removed = new LinkedList<Customer>();
         for (MyPriorityQueue<Customer> q : cashiers) {
            if (!q.isEmpty()) {
               for (Customer c : q) c.increaseSpent();
               Customer c = q.peek();
               c.decreaseWait();
               int i = c.getNum();
               if (c.getWaitTime()==0) {
                  checked[i]++;
                  int spent = c.getTimeSpent();
                  if (spent>longest[i]) longest[i] = spent;
                  checkedWait[i]+=spent;
                  removed.add(q.remove());
               }
            }
         }
         for (int j=0; j<CUSTOMERS_PER_MINUTE; j++) {
            Customer c = new Customer(t);
            int i = c.getNum();
            if (c.getWaitTime()>longest[i]) longest[i] = c.getWaitTime();
            shortestQ(cashiers).add(c);
            total[i]++;
         }
         outfileCashiersAndQueues(out, t, cashiers, removed);
      }
      out.println("Customer\t\tTotal\t\tLongest\tAverage Wait");
      for (int i=0; i<4; i++) out.println(classes[i]+"\t\t"+checked[i]+"\t\t"+longest[i]+"\t\t"+(double)checkedWait[i]/checked[i]);
      out.close();	
      System.out.println("Customer\t\tTotal\t\tLongest\t\tAverage Wait");
      for (int i=0; i<4; i++) System.out.println(classes[i]+"\t\t\t"+checked[i]+"\t\t\t"+longest[i]+"\t\t\t"+(double)checkedWait[i]/checked[i]);
   }
}

class Customer implements Comparable<Customer>
{
   private int arrivedAt;
   private int timeSpentAtCashier;
   private int waitTime;
   private String academic;
   private String[] classes = new String[]{"Senior", "Junior", "Sophomor", "Freshman"};
   private int num;

   public Customer(int t) {
      arrivedAt = t;
      timeSpentAtCashier = 0;
      waitTime = (int)(Math.random() * (6-2+1)) + 2;
      num = (int)(Math.random() * 4);
      academic = classes[num];
   }
   public int getNum() {
      return num;
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
   public String getAcademic() {
      return academic;
   }
   public void decreaseWait() {
      if (waitTime>0) waitTime--;
   }
   public void increaseSpent() {
      timeSpentAtCashier++;
   }
   public String toString() {
      return arrivedAt+"-"+academic.substring(0,2)+":"+waitTime;
   }
   public int compareTo(Customer other) {
      if (num!=other.getNum()) return num-other.getNum();
      else return arrivedAt-other.getTimeArrived();
   }
}

class MyPriorityQueue<E extends Comparable<E>> extends PriorityQueue<E> {
   ArrayList<E> arr;
   public MyPriorityQueue() {
      arr = new ArrayList<E>();
   }
   public boolean add(E obj) {
      int i=0;
      while (i<arr.size() && obj.compareTo(arr.get(i))>0) i++;
      arr.add(i, obj);
      return true;
   }
   public int size() {
      return arr.size();
   }
   public E remove() {
      return arr.remove(0);
   }
   public E peek() {
      return arr.get(0);
   }
   public boolean isEmpty() {
      return arr.size()==0;
   }
   public Iterator<E> iterator() {
      return arr.iterator();
   }
}
