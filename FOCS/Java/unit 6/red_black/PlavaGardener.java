import java.util.Scanner;
import java.io.FileWriter;
import java.io.File;
import java.io.IOException;
import java.util.Arrays;

public class PlavaGardener
{
   //Global variables
   //1) How are these like fields?  How are they different?
   public static int money;
   public static int expertise;
   public static Scanner in;
   public static Plant[] plants;

   public static void reportAllStatus()
   {
      boolean some = false;
      for(int i = 0; i < plants.length; i++)
      {
         if(plants[i] != null) //2) What is this line for?
         {
            some = true;
            System.out.println("In plot number " + i + ":");
            plants[i].statusReport();
            System.out.println();
         }
      }
      if(!some)
      {
         System.out.println("You don't have any plants!  Buy some at the store!");
      }
   }
   public static void soundAllPlants()
   {
     for(int i = 0; i < plants.length; i++)
     {
        if(plants[i] != null)
        {

          if (!plants[i].isAlive())
          {
            System.out.println("Plant in plot number "+i+" is dead!");
          }

          else
          {
            System.out.print("For plot number " + i + ", your " + plants[i] + " will be in a loud or quiet environment? ");
            String inp = in.nextLine();
            plants[i].setSound(inp);
          }
        }
     }
   }
   public static void waterAllPlants()
   {
      System.out.println("Most plants need somewhere between 0 and 2 tablespoons of water per day per 10 inches of height.");
      System.out.println("Plava plants might be unpredictable, though!");
      System.out.println("For each plant below, give a decimal value of tablespoons of water to give per day.");
      for(int i = 0; i < plants.length; i++)
      {
         if(plants[i] != null)
         {

           if (!plants[i].isAlive())
           {
             System.out.println("Plant in plot number "+i+" is dead!");
           }

           else
           {
             System.out.print("For plot number " + i + ", your " + plants[i] + " should get: ");
             String inpt = in.nextLine();
             double water = Double.parseDouble(inpt);
             plants[i].setWater(water);  //3) This line relies on the Plant interface to work.  How?
           }
         }
      }
   }
   public static void sunlightAllPlants()
   {
      System.out.println("You have three options for the sunlight each plant gets - direct, indirect, or shade.");
      System.out.println("For each plant below, either type what sunlight you'd like it to get, or just type 'x' if you want to leave it where it is.");
      for(int i = 0; i < plants.length; i++)
      {
         if(plants[i] != null)
         {

           if (!plants[i].isAlive())
           {
             System.out.println("Plant in plot number "+i+" is dead! You might want to discard it.");
           }

           else
           {
             System.out.println("For plot number " + i + ", your " + plants[i] + " is currently getting " + plants[i].getSunlight() + ".");
             System.out.print("Type a different option to change, or 'x' to keep as is: ");
             String inpt = in.nextLine();
             plants[i].setSunlight(inpt); //4) Why don't I need to check to see if inpt has a valid answer before calling this?
           }
         }
      }
   }
   public static void growAllPlants()
   {
      for(int i = 0; i < plants.length; i++)
      {
         if(plants[i] != null)
         {
            plants[i].grow();
         }
      }
   }
   public static Plant goShopping()
   {
      System.out.println("Welcome to the Plava plant store!");
      System.out.println("I currently have two options for sale.");
      System.out.println("1) Plava Rose -- $2");
      System.out.println("2) Plava Cactus -- $5");
      System.out.println("3) Plava Short -- $7");
      System.out.println("4) Plava Stupid -- $1");
      System.out.println("You currently have $" + money + ".");
      System.out.print("What would you like to buy (type the number of the option you choose or 0 to buy nothing)? ");
      String inpt = in.nextLine();
      int choice = Integer.parseInt(inpt);
      if(choice == 1 && money >= 2)
      {
         money -= 2;
         return new PlavaRose();
      }
      else if(choice == 2 && money >= 5)
      {
         money -= 5;
         return new PlavaCactus();
      }
      else if(choice == 3 && money >= 7)
      {
         money -= 7;
         return new PlavaShort();
      }
      else if(choice == 4 && money >= 3)
      {
         money -= 1;
         return new PlavaStupid();
      }
      System.out.println("You don't have enough money for that!");
      return null;
   }
   public static void save()
   {
     try {
       FileWriter file = new FileWriter("savegame.txt");
       file.write(Integer.toString(money)+"\n");
       file.write(Integer.toString(expertise)+"\n");
       for (int x=0; x<plants.length; x++) {
         if (plants[x] != null) {
           file.write(plants[x]+","+Integer.toString(plants[x].getHeight())+","+Integer.toString(plants[x].getBlooms())+","+Integer.toString(plants[x].getStage())+"\n");
         }
         else file.write("null\n");
       }
       file.close();
       System.out.println("Saved!");
     }
     catch (IOException e) {
       e.printStackTrace();
     }
   }
   public static void load()
   {
     try {
       Scanner infile = new Scanner(new File("savegame.txt"));
       money = Integer.parseInt(infile.nextLine());
       expertise = Integer.parseInt(infile.nextLine());
       for (int x=0; x<10; x++)
       {
          String[] temp = infile.nextLine().strip().split(",");
          if (temp[0].equals("null"))
          {
            plants[x] = null;
          }
          else
          {
            if (infile.nextLine().equals("Plava Rose")) {
              plants[x] = new PlavaRose();
            }
            else if (infile.nextLine().equals("Plava Short")) {
              plants[x] = new PlavaShort();
            }
            else if (infile.nextLine().equals("Plava Stupid")) {
              plants[x] = new PlavaStupid();
            }
            else {
              plants[x] = new PlavaCactus();
            }

            plants[x].setHeight(Integer.parseInt(temp[1]));
            plants[x].setBlooms(Integer.parseInt(temp[2]));
            plants[x].setStage(Integer.parseInt(temp[3]));
          }
        }
        System.out.println("Loaded!");
      }
     catch (Exception e)
     {
       e.printStackTrace();
     }

   }
   public static void gameLoop()
   {
      while(true)  //5) This looks like it will go on forever!  How does this loop end?
      {
         System.out.println();
         System.out.println("You can choose any of the following options:");
         System.out.println("1) Check on the status of your plants");
         System.out.println("2) Decide how much to water each plant this week");
         System.out.println("3) Decide how much sunlight to give each plant this week");
         System.out.println("4) Wait a week to see how your plants grow/don't grow");
         System.out.println("5) Buy a new plant from the store");
         System.out.println("6) Throw away a plant that you own");
         System.out.println("7) Cut a flower off of one of your plants and sell it");
         System.out.println("8) Decide how loud the environment should be");
         System.out.println("9) Learn about current plants (need expertise)");
         System.out.println("10) Check money and expertise");
         System.out.println("11) Save current progress");
         System.out.println("12) Load progress");
         System.out.println("0) Quit the game (your progress will not be saved)");
         System.out.print("Type the number of your choice: ");
         String inpt = in.nextLine();
         int choice = Integer.parseInt(inpt);
         if(choice == 1)
         {
            reportAllStatus();
         }
         else if(choice == 2)
         {
            waterAllPlants();
         }
         else if(choice == 3)
         {
            sunlightAllPlants();
         }
         else if(choice == 4)
         {
            System.out.println("A week passes.  Check your plant status to see how they did!");
            growAllPlants();
         }
         else if(choice == 5)
         {
           boolean able = false;
           for (int x=0; x<plants.length; x++)
           {
             if (plants[x] == null) able = true;
           }

           if (able)
           {
               {
                  Plant temp = goShopping();
                  if(temp != null)
                  {
                     for(int plot = 0; plot < plants.length; plot++)
                     {
                        if(plants[plot] == null)
                        {
                           plants[plot] = temp;
                           System.out.println("Your new plant is in plot #" + plot);
                           System.out.println();
                           break;
                        }
                     }
                  }
               }
           }
           else
           {
             System.out.println("Plots are full! Can't buy more plants.");
           }
         }
         else if(choice == 6)
         {
            System.out.print("Which plot would you like to throw away? ");
            String inpt2 = in.nextLine();
            int choice2 = Integer.parseInt(inpt2);
            plants[choice2] = null;
         }
         else if(choice == 7)
         {
            System.out.println("Which plot would you like to sell? ");
            String inpt3 = in.nextLine();
            int choice3 = Integer.parseInt(inpt3);

            if (plants[choice3].trim() == 1)
            {
              money += plants[choice3].getValue();
              expertise += Math.ceil(plants[choice3].getValue()/2.0);
            }

            else
            {
              System.out.println("You can't cut a flower with no leaves!");
            }
         }
         else if (choice == 8)
         {
           soundAllPlants();
         }
         else if (choice == 9)
         {
           System.out.println("Which plot would you like to learn about? ");
           String inpt4 = in.nextLine();
           int choice4 = Integer.parseInt(inpt4);

           if (plants[choice4] != null)
           {
             if (expertise >= 15)
             {
               plants[choice4].learn(3);
             }
             else if (expertise >= 10)
             {
               plants[choice4].learn(2);
             }
             else if (expertise >= 5)
             {
               plants[choice4].learn(1);
             }
             else
             {
               System.out.println("Not enough expertise!");
             }
           }
         }
         else if (choice == 10)
         {
           System.out.println("Money: $"+money);
           System.out.println("Expertise: "+expertise);
         }
         else if (choice == 11)
         {
           save();
         }
         else if (choice == 12)
         {
           load();
         }
         else
         {
           return;
         }
      }
   }

   public static void main(String[] args)
   {
      //7) Over the next three lines, the variable types are NOT given.  Why?
      in = new Scanner(System.in);
      money = 10;
      plants = new Plant[10];

      System.out.println("Welcome to Plava Gardener!");
      gameLoop();
   }
}
