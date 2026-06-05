import edu.fcps.karel2.Display;
import edu.fcps.karel2.Robot;

public class SmileDemo
{
   public static void main(String[] args)
   {
      int n=16; // change number to change size of map (16x16)
      Display.openWorld(String.format("Smile/%1$sx%1$s.map", Integer.toString(n)));
      Display.setSize(n+1,n+1);
      Display.setSpeed(10);
      Smile bot = new Smile();
      try {
         bot.go_map();
      }
      catch (Exception e) {
         System.out.println("File not found!");
      }
   }
}
