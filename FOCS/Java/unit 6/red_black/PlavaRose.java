public class PlavaRose implements Plant
{
   //Fields
   private int height;
   private int blooms;
   private int stage;
   private String sunlight;
   private String sound;
   private double lastWater;
   private final int value = 5;

   //Constructors
   public PlavaRose()
   {
      height = 10;
      blooms = 0;
      stage = 0;
      sunlight = "shade";
      sound = "quiet";
      lastWater = 0;
   }
   public PlavaRose(int customHeight, int customBlooms, int customStage, String customSunlight, String customSound, double customLastWater)
   {
      height = customHeight;
      blooms = customBlooms;
      stage = customStage;
      sunlight = customSunlight;
      sound = customSound;
      lastWater = customLastWater;
   }

   //Accessors & modifiers
   public void setHeight(int customHeight)
   {
     height = customHeight;
   }
   public void setStage(int customStage)
   {
     stage = customStage;
   }
   public void setBlooms(int customBlooms)
   {
     blooms = customBlooms;
   }
   public int getStage()
   {
     return stage;
   }
   public int getHeight()
   {
      return height;
   }
   public int getBlooms()
   {
      return blooms;
   }
   public String getSunlight()
   {
      return sunlight;
   }
   public String getSound()
   {
     return sound;
   }
   public int getValue()
   {
      return value;
   }
   public void setSunlight(String newSun)
   {
      if(newSun.equals("shade") || newSun.equals("indirect") || newSun.equals("direct"))
      {
         sunlight = newSun;
      }
   }
   public void setSound(String newSound)
   {
     if (newSound.equals("loud")||newSound.equals("quiet"))
     {
       sound = newSound;
     }
   }
   public void setWater(double tablespoons)
   {
      if (tablespoons>=0) {
        lastWater = tablespoons;
      }
      else {
        System.out.println("You can't remove water from the plant!");
      }
   }
   public void learn(int stage)
   {
     if (stage>0)
     {
       System.out.println("PlavaRose likes direct light!");
     }
     if (stage>1)
     {
       System.out.println("PlavaRose hates the shade!");
     }
     if (stage>2)
     {
       System.out.println("PlavaRose likes within 1.2 and 2.0 times more water than the tens digit of its height!");
     }
   }
   //Instance methods
   public void grow()
   {
      //12) Put into your own words: what does a Plava Rose need to bloom?
      if(stage >= 0)
      {
         if(sunlight.equals("direct"))
         {
            if(lastWater > 1.2 * height / 10 && lastWater < 2.0 * height / 10)
            {
               stage ++;
               height += 5;
            }
         }
         if(sunlight.equals("shade"))
         {
            stage --;
            height -= 5;
         }
      }
      if(stage >= 3)
      {
         stage = 3;
         blooms += 1;
      }
   }
   public int trim()
   {
      if(blooms > 0)
      {
         blooms--;
         return 1;
      }
      return 0;
   }
   public void statusReport()
   {
      if(stage == -1)
         System.out.println("Your Plava Rose is dead!");
      else
      {
         System.out.println("Your Plava Rose is " + height + " inches tall.");
         System.out.println("It has " + blooms + " flowers.");
         if(stage == 0)
         {
            System.out.println("Your Plava Rose looks like a bare stalk.");
         }
         else if(stage == 1)
         {
            System.out.println("Your Plava Rose has grown a few leaves.");
         }
         else if(stage == 2)
         {
            System.out.println("Your Plava Rose has a few flower buds.");
         }
         else
         {
            System.out.println("Your Plava Rose is blooming!");
         }
      }
   }
   public boolean isAlive()
   {
      return stage >= 0;
   }
   public String toString()
   {
      return "Plava Rose";
   }
}
