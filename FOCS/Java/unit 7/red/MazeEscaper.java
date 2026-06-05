import edu.fcps.karel2.Display;
import edu.fcps.karel2.Robot;

public class MazeEscaper extends Athlete {

  public MazeEscaper() {
    super(1, 1, Display.NORTH, 0);
  }

  void escape() {
    while (!nextToABeeper()) {
      if (!leftIsClear() && frontIsClear()) {
        move();
      }
      else {
        if (leftIsClear()) {
          turnLeft();
          move();
        }
        else if (rightIsClear()) {
          turnRight();
          move();
        }
        else {
          turnLeft();
        }
      }
    }
  }
}
