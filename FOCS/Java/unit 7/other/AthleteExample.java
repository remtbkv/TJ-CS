import edu.fcps.karel2.Display;
import edu.fcps.karel2.Robot;
import java.util.Scanner;

public class AthleteExample {
  public static void main(String[] args) {
    Display.openWorld("maps/shuttle.map");
    Display.setSize(7,7);
    Display.setSpeed(5);

    Athlete athlete = new Athlete();
    athlete.putBeeper();
    String path = "";

   }
}
