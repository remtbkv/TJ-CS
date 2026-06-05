//  Driver for the SmartCard class.
public class SmartCard_Driver
{
   public static void main(String[] args) 
   {
      Station downtown = new Station("Downtown", 1);
      Station center = new Station("Center City", 1);
      Station uptown = new Station("Uptown", 2);
      Station suburbia = new Station("Suburb", 4);
   
      SmartCard buddy = new SmartCard(20.00); 
      
      /*  test cases  */
      System.out.println("getBalance() "+ buddy.getBalance());
      System.out.println("getIsBoarded() "+ buddy.getIsBoarded());
      System.out.println("getBoardedAt() "+ buddy.getBoardedAt());
      System.out.println("getFormattedBalance() "+ buddy.getFormattedBalance());
      buddy.addMoney(5);            		
      System.out.println();
      
      SmartCard b = new SmartCard(10.00);   
      b.board(center);            		    
      b.exit(downtown);					      // Standard case
      System.out.println("getIsBoarded() "+ b.getIsBoarded());
      System.out.println("getBoardedAt() "+ b.getBoardedAt());
      System.out.println();
   
      SmartCard z = new SmartCard(10.00); 
      z.board(downtown);
      System.out.println("getIsBoarded() "+ z.getIsBoarded());
      System.out.println("getBoardedAt() "+ z.getBoardedAt());
      z.board(suburbia);             // Did not exit
      System.out.println("getIsBoarded() "+ z.getIsBoarded());
      System.out.println("getBoardedAt() "+ z.getBoardedAt());
      System.out.println();
      
      SmartCard kim = new SmartCard(.25);    
      kim.board(uptown);            		// Not enough money to board
      System.out.println();
         
      SmartCard susie = new SmartCard(1.00); 
      susie.board(uptown);            		
      susie.exit(suburbia);				   // Not enough money to exit
      System.out.println();
       
      SmartCard jimmy = new SmartCard(20.00); 
      jimmy.board(center);               
      jimmy.exit(suburbia);              // Standard case
      System.out.println("getIsBoarded() "+ jimmy.getIsBoarded());
      System.out.println("getBoardedAt() "+ jimmy.getBoardedAt());
      jimmy.exit(uptown);			   	  // Exit twice in a row
      System.out.println();
   	 
      
      //What other tests can you think of that will break the code?
          
   }
} 	


     /*******************  Sample Run ************

 getBalance() 20.0
 getIsBoarded() false
 getBoardedAt() null
 getFormattedBalance() $20.00
 $5.00 added.  Your new balance is $25.00
 
 From Center City to Downtown costs $0.50. SmartCard has $9.50
 getIsBoarded() false
 getBoardedAt() null
 
 getIsBoarded() true
 getBoardedAt() Station@34c45dca
 Error: already boarded?!
 getIsBoarded() true
 getBoardedAt() Station@34c45dca
 
 Insufficient funds to board. Please add more money.
 
 Insufficient funds to exit. Please add more money.
 
 From Center City to Suburb costs $2.75. SmartCard has $17.25
 getIsBoarded() false
 getBoardedAt() null
 Error: Did not board?!
 
 
************************************************/