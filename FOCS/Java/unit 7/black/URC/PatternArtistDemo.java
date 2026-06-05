import edu.fcps.karel2.Display;
import edu.fcps.karel2.Robot;

public class PatternArtistDemo
{
   public static void main(String[] args)
   {
      Display.openWorld("URCmaps/D2.map");
      Display.setSize(10,10);
      Display.setSpeed(10);
      for (int x=1; x<50; x++) {
        PatternArtist bot = new PatternArtist(x);
        bot.go();
      }
      PatternArtist bot = new PatternArtist();

   }
}
