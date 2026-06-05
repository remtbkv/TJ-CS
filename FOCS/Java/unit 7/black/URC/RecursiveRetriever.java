import edu.fcps.karel2.Display;
import edu.fcps.karel2.Robot;
import java.util.*;

public class RecursiveRetriever extends Athlete {
  private int size;

  public RecursiveRetriever() {
    super(1, 1, Display.NORTH, 0);
  }

  void pick() {
    if (nextToABeeper()) {
      pickBeeper();
      pick();
    }
    else {
      ;
    }
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

  void upF() {
    if (rightIsClear()) {
      turnRight();
      move();
      turnRight();
    }
    else {
      move();
      size++;
      upF();
    }
  }

  void downF(int x) {
    if (x==0) {
      pick();
      turnAround();
    }
    else {
      pick();
      move();
      x--;
      downF(x);
    }
  }

  void upB(int x) {
    if (x==0) {
      turnLeft();
      move();
      turnLeft();

    }
    else {
      move();
      x--;
      upB(x);
    }
  }

  void downB(int x) {
    if (x==0) {
      put(getBeepers());
    }
    else {
      move();
      x--;
      downB(x);
    }
  }

  void go() {
    upF();
    downF(size);
    upB(size);
    downB(size);
    turnAround();
    move();
  }

}
