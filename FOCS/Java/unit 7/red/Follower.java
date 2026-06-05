import edu.fcps.karel2.Display;
import edu.fcps.karel2.Robot;
public class Follower extends Athlete {
  public Follower() {
    super(2, 2, Display.EAST, 0);
  }
  public void back() {
    turnAround();
    move();
  }

  public void follow() {
    while (true) {
      if (nextToABeeper() && frontIsClear()) {
        move();
      }
      else if (leftIsClear()) {
        turnLeft();
        move();
      }
      else {
        turnRight();
        move();
      }
      if (!nextToABeeper() && rightIsClear()) {
        back();
        turnLeft();
        move();
      }
      else if (!nextToABeeper()) {
        back();
        turnRight();
        move();
      }
      if (!nextToABeeper()) {
        back();
        move();
      }
      if (!nextToABeeper()) {
        back();
        turnLeft();
        return;
      }
    }
  }
}
