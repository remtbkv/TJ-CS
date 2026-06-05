import edu.fcps.karel2.Display;
import edu.fcps.karel2.Robot;

public class RecursiveRetrieverDemo
{
   public static void main(String[] args)
   {
      Display.openWorld("URCmaps/A1.map");
      Display.setSize(10,10);
      Display.setSpeed(10);

      RecursiveRetriever bot = new RecursiveRetriever();
      bot.go();
   }
}
