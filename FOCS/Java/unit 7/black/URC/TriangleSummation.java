import edu.fcps.karel2.Display;
import edu.fcps.karel2.Robot;
import java.util.*;


public class TriangleSummation extends Athlete {
  private HashMap<String, Integer> coords = new HashMap<>();
  private int beeps;
  private int tempS;
  private int permS;
  private int finish;

  public TriangleSummation() {
    super(1, 1, Display.NORTH, Display.INFINITY);
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

  void top(int len) {
    if (len==0) {
      turnAround();
      permS--;
    }
    else {
      len--;
      move();
      top(len);
    }
  }

  void step() {
    if (nextToABeeper()) {
      move();
      tempS--;
    }
    else {
      turnRight();
      move();
      turnRight();
      top(permS);
    }
  }

  void mark() {
    pick();
    int[] point = {getX(), getY()};
    coords.put(Arrays.toString(point), beeps);
    beeps=0;
  }

  void mark2(int x) {
    int[] point = {getX(), getY()};
    coords.put(Arrays.toString(point), x);
  }

  int place() {
    int[] side = {getX()-1, getY()};
    int[] bottom = {getX(), getY()-1};
    int sum = coords.get(Arrays.toString(side))+coords.get(Arrays.toString(bottom));
    put(sum);
    return sum;
  }

  void getSize() {
    if (nextToABeeper()) {
      mark();
      move();
      permS++;
      getSize();
    }
    else {
      turnRight();
      move();
      turnRight();
      top(permS);
      finish = permS;
      tempS = permS;

    }
  }

  void mover() {
    if (permS==1) { // change to 0 to move off of last pile
      last(finish+1);
    }
    else if (tempS==0) {
      step();
      tempS = permS;
      mover();
    }
    else if (getY()==1) {
      mark();
      step();
      mover();
    }
    else {
      mark2(place());
      step();
      mover();
    }
  }

  void last(int x) {
    if (x==0) {
      turnLeft();
      last2(finish);
    }
    else {
      move();
      x--;
      last(x);
    }
  }

  void last2(int x) {
    if (x==0) {
      turnRight();
    }
    else {
      move();
      x--;
      last2(x);
    }
  }

  public void go() {
    getSize();
    mover();
  }
}
