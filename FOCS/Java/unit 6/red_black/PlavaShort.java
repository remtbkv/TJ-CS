public class PlavaShort implements Plant {
     //Fields
     private int height;
     private int blooms;
     private int stage;
     private String sunlight;
     private String sound;
     private double lastWater;
     private final int value = 9;

     //Constructors
     public PlavaShort()
     {
        height = 10;
        blooms = 0;
        stage = 0;
        sunlight = "shade";
        sound = "quiet";
        lastWater = 0;
     }
     public PlavaShort(int customHeight, int customBlooms, int customStage, String customSunlight, String customSound, double customLastWater)
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
         System.out.println("PlavaShort likes the shade!");
       }
       if (stage>1)
       {
         System.out.println("PlavaShort likes exactly 1.1x more water than the tens digit of its height!");
       }
     }

     //Instance methods
     public void grow()
     {
        if(stage >= 0)
        {
           if(sunlight.equals("shade"))
           {
             if (lastWater == (1.1 * height/10))
             {
               stage ++;
               System.out.println("did this");
             }
           }
        }
        if(stage >= 3)
        {
           stage = 3;
           blooms += 10;
        }
     }
     public int trim()
     {
        if(blooms > 0)
        {
           blooms-=5;
           return 1;
        }
        return 0;
     }
     public void statusReport()
     {
        if(stage == -1)
           System.out.println("Your Plava Short is dead!");
        else
        {
           System.out.println("Your Plava Short is " + height + " inches tall.");
           System.out.println("It has " + blooms + " flowers.");
           if(stage == 0)
           {
              System.out.println("Your Plava Short looks like celery.");
           }
           else if(stage == 1)
           {
              System.out.println("Your Plava Short has grown a few green things.");
           }
           else if(stage == 2)
           {
              System.out.println("Your Plava Short has a fat flower bud.");
           }
           else
           {
              System.out.println("Your Plava Short is blooming! (10 at once!!!)");
           }
        }
     }
     public boolean isAlive()
     {
        return stage >= 0;
     }
     public String toString()
     {
        return "Plava Short";
     }
}
