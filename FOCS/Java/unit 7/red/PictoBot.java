import edu.fcps.karel2.Display;
import edu.fcps.karel2.Robot;
import java.util.Arrays;
import java.util.ArrayList;

public class PictoBot extends Athlete {
  private int [] x = new int[2];
  private int[] coord = new int[2];
  private ArrayList<Integer> switched = new ArrayList<Integer>();

  public PictoBot() {
    super(1, 1, Display.EAST, 0);
  }

  public void faceNorth() {
    while (!facingNorth()) {
      turnLeft();
    }
  }
  public void faceEast() {
    while (!facingEast()) {
      turnLeft();
    }
  }
  public void faceSouth() {
    while (!facingSouth()) {
      turnLeft();
    }
  }
  public void faceWest() {
    while (!facingWest()) {
      turnLeft();
    }
  }

  public void switchCoord() {
    switched.add(getY());
    switched.add(4-getX()+1);
  }
  public void mover() {
    for (int x=0; x<4; x++) {
      if (nextToABeeper()) {
        pickBeeper();
        switchCoord();
      }
      move();
      if (nextToABeeper()) {
        pickBeeper();
        switchCoord();
      }
    }
  }
  public void left() {
    turnLeft();
    move();
    turnLeft();
  }
  public void right() {
    turnRight();
    move();
    turnRight();
  }

  public void place() {
    for (int j=0; j<switched.size(); j+=2) {
      int x = switched.get(j);
      int y = switched.get(j+1);
      int cx = getX();
      int cy = getY();

      if (x>cx) {
        faceEast();
        for (int i=0; i<x-cx; i++) {
          move();
        }
      }
      else {
        faceWest();
        for (int i=0; i<cx-x; i++) {
          move();
        }
      }
      if (y>cy) {
        faceNorth();
        for (int i=0; i<y-cy; i++) {
          move();
        }
      }
      else {
        faceSouth();
        for (int i=0; i<cy-y; i++) {
          move();
        }
      }
      putBeeper();
    }
  }

  public void rotate() {
    for (int x=0; x<4; x++) {
      mover();
      left();
      mover();
      right();
    }
    place();
  }
}
