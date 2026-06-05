import edu.fcps.karel2.Display;
import edu.fcps.karel2.Robot;

abstract class ObstacleBot extends Athlete implements Runnable {
  private int times;
  abstract boolean keepGoing();

  public ObstacleBot(int x) {
    super(x, 1, Display.NORTH, 0);
  }

  public void aroundWall(int num) {
    turnLeft();
    move();
    turnLeft();
    for (int x=0; x<num; x++) {
      move();
    }
    turnRight();
  }

  public void run() {
    while (keepGoing()) {
      if (frontIsClear()) {
        move();
      }
      else {
        turnRight();
        while (!leftIsClear()) {
          move();
          times++;
        }
        aroundWall(times);
        times=0;
      }
    }
  }
}
