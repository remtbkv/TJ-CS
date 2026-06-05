public class PlavaStupid implements Plant {

  //Fields
  private int height;
  private int blooms;
  private int stage;
  private String sunlight;
  private String sound;
  private double lastWater;
  private final int value = 3;

  //Constructors
  public PlavaStupid()
  {
     height = 10;
     blooms = 0;
     stage = 0;
     sunlight = "shade";
     sound = "quiet";
     lastWater = 0;
  }
  public PlavaStupid(int customHeight, int customBlooms, int customStage, String customSunlight, String customSound, double customLastWater)
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
    if (stage==1)
    {
      System.out.println("PlavaStupid likes direct light!");
    }
    else if (stage==2)
    {
      System.out.println("PlavaStupid likes sound!");
    }
    else
    {
      System.out.println("PlavaStupid likes 1.2x more water than the tens digit of its height!");
    }
  }

  //Instance methods
  public void grow()
  {
     if(stage >= 0)
     {
        if(sunlight.equals("direct") && sound.equals("loud"));
        {
          if (lastWater > 1.2 * height/10)
          {
            stage ++;
            height += 5;
          }
        }
     }
     if(stage >= 3)
     {
        blooms += 3;
        stage = -1;
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
     {
       System.out.println("Your Plava Stupid bloomed and now is dead!");
       System.out.println("It has " + blooms + " flowers.");
     }
     else
     {
        System.out.println("Your Plava Stupid is " + height + " inches tall.");
        System.out.println("It has " + blooms + " flowers.");
        if(stage == 0)
        {
           System.out.println("Your Plava Stupid looks like a bare stalk.");
        }
        else if(stage == 1)
        {
           System.out.println("Your Plava Stupid has grown a few leaves.");
        }
        else if(stage == 2)
        {
           System.out.println("Your Plava Stupid has a few flower buds.");
        }
        else
        {
           System.out.println("Your Plava Stupid is blooming!");
        }
     }
  }
  public boolean isAlive()
  {
     return stage >= 0;
  }
  public String toString()
  {
     return "Plava Stupid";
  }
}
