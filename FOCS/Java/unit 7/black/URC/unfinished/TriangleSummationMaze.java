import edu.fcps.karel2.Display;
import edu.fcps.karel2.Robot;
import java.util.*;


public class TriangleSummationMaze extends Athlete implements Runnable {
  HashMap<String, Integer> coords = new HashMap<>();
  private int beeps = 0;

  public TriangleSummationMaze() {
    super(0, 0, Display.NORTH, 0);
  }

  public TriangleSummationMaze(int x, int y) {
    super(x, y, Display.NORTH, 0);
  }

  void put(int x) {
    if (x==0) {
      ;
    }
    else {
      putBeeper();
      x--;
      put(x);
    }
  }

  void pick() {
    if (nextToABeeper()) {
      pickBeeper();
      beeps++;
      pick();
    }
    else {
      put(beeps);
    }
  }

  public void log() {
    pick();
    int[] pos = {getX(), getY()};
    coords.put(Arrays.toString(pos), beeps);
  }

  public void place() {
    int[] side = {getX()-1, getY()};
    int[] bottom = {getX(), getY()-1};
    put(coords.get(Arrays.toString(side))+coords.get(Arrays.toString(bottom)));
  }

  public void run() {
    log();
    if (getX()>1 && getY()>1) {
      place();
    }
    System.out.println(coords);
  }
}
