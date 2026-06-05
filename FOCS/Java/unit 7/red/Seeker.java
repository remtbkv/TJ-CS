import edu.fcps.karel2.Display;
import edu.fcps.karel2.Robot;

public class Seeker extends Athlete {
  private int x=0;
  private int y=1;

  public Seeker() {
    super(1, 1, Display.NORTH, 0);
  }

  public void high() {
    turnRight();
    move();
    turnRight();
  }

  public void low() {
    turnLeft();
    move();
    turnLeft();
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

  public void deposit() {
    int xx = getX();
    int yy = getY();

    pickBeeper();

    if (xx>1) {
      faceWest();
      for (int i=0; i<xx-1; i++) {
        move();
      }
    }
    else {
      faceEast();
      for (int i=0; i<xx-1; i++) {
        move();
      }
    }

    if (yy>1) {
      faceSouth();
      for (int i=0; i<yy-1; i++) {
        move();
      }
    }
    else {
      faceNorth();
      for (int i=0; i<yy-1; i++) {
        move();
      }
    }
    putBeeper();
    faceNorth();
  }

  public void seek() {
    if (nextToABeeper()) {
      deposit();
    }
    else if (y == 75) {
      if (x%2==0) {
        high();
      }
      else {
        low();
      }
      x++;
      y=1;
      seek();
    }
    else {
      move();
      y++;
      seek();
    }
  }
}
