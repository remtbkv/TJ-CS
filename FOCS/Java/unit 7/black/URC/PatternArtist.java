import edu.fcps.karel2.Display;
import edu.fcps.karel2.Robot;
import java.util.*;

public class PatternArtist extends Athlete {
  private int x, y, n;

  public PatternArtist() {
    super(1, 1, Display.NORTH, 0);
  }
  public PatternArtist(int x) {
    super(x, 1, Display.NORTH, 0);
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

  void put(int x) {
    for (int i=0; i<x; i++) {
      putBeeper();
    }
  }

  int pick() {
    while (nextToABeeper()) {
      pickBeeper();
    }
    return getBeepers();
  }

  void locate(int cx, int cy) {
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
  }

  public void go() {
    if (nextToABeeper()) {
      x = pick();
      move();
      y = pick()-x;
      move();
      n = pick()-x-y;
      locate(getX(), getY());
      put(n);
      explode();
    }
    else {
      explode();
    }

  }

}
