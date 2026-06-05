import edu.fcps.karel2.Display;
import edu.fcps.karel2.Robot;
import java.util.Scanner;
public class School  {
  public static void main(String[] args) {
    Display.openWorld("maps/school.map");
    Display.setSize(10,10);
    Display.setSpeed(5);

    Robot lisa = new Robot();
    Robot pete = new Robot (4, 5, Display.SOUTH, 0);

    String l_move = "wwlwlwubwrwlwwwlwwwlwwrwp";
    for (int x=0; x<l_move.length(); x++) {
      if (l_move.charAt(x)=='w') {
        lisa.move();
      }
      else if (l_move.charAt(x)=='l') {
        lisa.turnLeft();
      }
      else if (l_move.charAt(x)=='r') {
        lisa.turnLeft();
        lisa.turnLeft();
        lisa.turnLeft();
      }
      else if (l_move.charAt(x)=='b') {
        lisa.turnLeft();
        lisa.turnLeft();
      }
      else if (l_move.charAt(x)=='u') {
        lisa.pickBeeper();
      }
      else {
        lisa.putBeeper();
      }
    }

    String p_move = "uwlwwlwwrwwlwlwwrwwlwwp";
    for (int x=0; x<p_move.length(); x++) {
      if (p_move.charAt(x)=='w') {
        pete.move();
      }
      else if (p_move.charAt(x)=='l') {
        pete.turnLeft();
      }
      else if (p_move.charAt(x)=='r') {
        pete.turnLeft();
        pete.turnLeft();
        pete.turnLeft();
      }
      else if (p_move.charAt(x)=='b') {
        pete.turnLeft();
        pete.turnLeft();
      }
      else if (p_move.charAt(x)=='u') {
        pete.pickBeeper();
      }
      else {
        pete.putBeeper();
      }
    }
  }
}
