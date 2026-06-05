public interface Plant
{
   public void setHeight(int customHeight);
   public void setStage(int customStage);
   public void setBlooms(int customBlooms);
   public int getStage();
   public int getHeight();
   public int getBlooms();
   public String getSunlight();
   public String getSound();
   public int getValue();
   public void setSunlight(String newSun);
   public void setSound(String newSound);
   public void setWater(double tablespoons);
   public void grow();
   public void learn(int stage);
   public int trim();
   public void statusReport();
   public boolean isAlive();
   //8) Why doesn't this interface need toString() defined?
}
