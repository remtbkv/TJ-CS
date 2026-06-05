import edu.fcps.karel2.Display;
import edu.fcps.karel2.Robot;

public class CountStop extends ObstacleBot {
  private int stop;
  public CountStop(int x, int row) {
    super(x);
    stop = row;
  }

  boolean keepGoing() {
    if (getY() == stop) {
      return false;
    }
    else {
      return true;
    }
  }
}
