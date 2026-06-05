import edu.fcps.karel2.Display;
import edu.fcps.karel2.Robot;

public class PileShifter extends Athlete {

  public PileShifter(int x, int y) {
    super(x, y, Display.WEST, 0);
  }

  public void shift() {
    while (true) {
      if (nextToABeeper()) {
        pickBeeper();
        turnAround();
        move();
        putBeeper();
        turnAround();
        move();
      }
      else if (getX()>1) {
        move();
      }
      else return;
    }
  }
}
