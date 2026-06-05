import edu.fcps.karel2.Display;
import edu.fcps.karel2.Robot;

public class TriangleSummationMazeDemo
{
   public static void main(String[] args)
   {
      Display.openWorld("URCmaps/F1.map");
      Display.setSize(10,10);
      Display.setSpeed(6);
      int n=8;

      for (int x=1; x<9; x++) {
        for (int y=1; y<n; y++) {
          // Runnable thing = new TriangleSummationMaze(x, y);
          // Thread bot = new Thread(thing);
          // bot.start();
          TriangleSummationMaze robot = new TriangleSummationMaze(x, y);
          robot.run();
        }
        n--;
      }
   }
}
