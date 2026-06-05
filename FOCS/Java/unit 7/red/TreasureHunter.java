import edu.fcps.karel2.Display;
import edu.fcps.karel2.Robot;

public class TreasureHunter extends Athlete {
  private int x;

  public TreasureHunter() {
    super(1, 1, Display.EAST, 0);
  }

  public void hunt() {
    while (true) {
      while (nextToABeeper()) {
        pickBeeper();
        x++;
      }
      if (x==1) {
        turnLeft();
      }
      else if (x==2) {
        turnAround();
      }
      else if (x==3) {
        turnRight();
      }
      else if (x==5) {
        return;
      }
      move();
      x=0;

    }
  }
}
