import edu.fcps.karel2.Display;
import edu.fcps.karel2.Robot;

public class ThreadRacer extends Racer implements Runnable {
  private int[] distance;
  private int[] beeps;

  public ThreadRacer(int y, int[] dist, int[] beep) {
    super(y);
    distance = dist;
    beeps = beep;
  }

  public void run() {
    for (int x=0; x<distance.length; x++) {
      move();
      jumpFront();
      mover(distance[x]);
      pick(beeps[x]);
      turnAround();
      mover(distance[x]);
      jumpBack();
      move();
      put(beeps[x]);
      turnAround();
    }
    move();
  }

}
