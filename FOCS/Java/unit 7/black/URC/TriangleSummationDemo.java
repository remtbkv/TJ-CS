import edu.fcps.karel2.Display;
import edu.fcps.karel2.Robot;

public class TriangleSummationDemo
{
   public static void main(String[] args)
   {
      Display.openWorld("URCmaps/E2.map");
      Display.setSize(10,10);
      Display.setSpeed(10);

      TriangleSummation bot = new TriangleSummation();
      bot.go();
   }
}
