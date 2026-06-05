// Name: J1-26-22
// Date: 8/23/22

import java.text.DecimalFormat;
public class SmartCard 
{
   public final static DecimalFormat df = new DecimalFormat("$0.00");
   public final static double MIN_FARE = 0.5;
   
   /* enter the private fields */
   private double money=0.0;
   private Station station=null;
   private boolean isBoarded=false;
   
   /* the one-arg constructor  */
   public SmartCard(double money) {
      this.money = money;
   }

   /* write the instance methods  */
   public double getBalance() {
      return money;
   }
   
   public String getFormattedBalance() {
      return df.format(money);
   }
   
   public boolean getIsBoarded() {
      return isBoarded;
   }
   
   public Station getBoardedAt() {
      if (!isBoarded) {
         return null;
      }
      return station;
   }
   
   public void board(Station s) {
      if (isBoarded) {
         System.out.println("Error: already boarded?!");      
      }
      else if (money<0.5) {
         System.out.println("Insufficient funds to board. Please add more money.");
      }
      else {
         isBoarded = true;
         station = s;
      }
   }
   
   public double cost(Station s) {
      int diff = Math.abs(s.getZone()-station.getZone());
      if (diff==0) {
         return 0.5; 
      }
      else {
         return 0.5+diff*0.75;
      }
   }
   
   public void exit(Station s) {
      double price = cost(s);
      if (!isBoarded) {
         System.out.println("Error: Did not board?!" );
      }
      else if (price>money) {
         System.out.println("Insufficient funds to exit. Please add more money.");
      }
      else {
         money-=price;
         System.out.println("From "+station.getName()+" to "+s.getName()+" costs "+df.format(price)+". Smartcard has "+df.format(money)+".");
         station = s;
         isBoarded=false;
      }
   }   
   
   public void addMoney(double d) {
      money+=d;
      System.out.println(df.format(d)+" added. Your new balance is "+df.format(money));
   }
}
   
// ***********  start a new class.  The new class does NOT have public or private.  ***/
class Station
{
   private String name;
   private int zone;
   
   public Station(String name, int zone) {
      this.name = name;
      this.zone = zone;
   }
   
   public String getName() {
      return name;
   }
   
   public int getZone() {
      return zone;
   } 
}

