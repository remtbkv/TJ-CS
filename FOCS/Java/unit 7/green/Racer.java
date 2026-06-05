import edu.fcps.karel2.Display;
import edu.fcps.karel2.Robot;

public class Racer extends Athlete {
  public Racer() {
    super();
  }
  public Racer(int y) {
    super(1, y, Display.EAST, 0);
  }
  public void jumpFront() {
    turnLeft();
    move();
    turnRight();
    move();
    turnRight();
    move();
    turnLeft();
  }
  public void jumpBack() {
    turnRight();
    move();
    turnLeft();
    move();
    turnLeft();
    move();
    turnRight();
  }
  public void mover(int spaces) {
    for (int x=0; x<spaces; x++) {
      move();
    }
  }
  public void pick(int num) {
    for (int x=0; x<num; x++) {
      pickBeeper();
    }
  }
  public void put(int num) {
    for (int x=0; x<num; x++) {
      putBeeper();
    }
  }
  public void shuttle(int spaces, int beepers) {
    move();
    jumpFront();
    mover(spaces);
    pick(beepers);
    turnAround();
    mover(spaces);
    jumpBack();
    move();
    put(beepers);
    turnAround();
  }
}
