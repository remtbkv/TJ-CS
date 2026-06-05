import edu.fcps.karel2.Display;
import edu.fcps.karel2.Robot;
import java.io.File;
import java.util.Scanner;

public class Smile extends Athlete {
   private int size=1;
   private int mult;

   public Smile() {
      super(1, 1, Display.NORTH, Display.INFINITY);
   }

   void Mover(int n) {
     for (int x=0; x<n; x++) {
       move();
     }
   }

   void PutMover(int n) {
     for (int x=0; x<n; x++) {
       putBeeper();
       move();
     }
   }

   void Starter() {
      move();
      turnRight();
      Mover(2);
   }

   void Sizer() {
      turnRight();
      while (frontIsClear()) {
         move();
         size++;
      }
      turnLeft();
      move();
      turnLeft();
   }

   void Block() {
      for (int i=0; i<mult; i++) {
         PutMover(mult);
         turnLeft();
         move();
         turnLeft();
         Mover(mult);
         turnAround();
      }
   }

   void toLeftCorner() {
      Mover(mult);
      turnAround();
   }

   void Inside(int n) {
     if (n>1) {
       PutMover(size-(2*mult)-2);
       turnAround();
       Mover(size-(2*mult)-2);
       turnLeft();
       move();
       turnLeft();
       n--;
       Inside(n);
     }
     else {
       Mover(size-(2*mult)-2);
       turnLeft();
       Mover(mult);
       turnAround();
     }
   }

   void toRightEye() {
     turnAround();
     Mover(mult+2);
     turnLeft();
     Mover(mult+1);
     turnLeft();
   }

   void toLeftEye() {
     turnRight();
     Mover(size-4);
     turnLeft();
   }

   void Victory() {
     turnAround();
     Mover(2);
     turnLeft();
     while (frontIsClear()) {
       move();
     }
     turnLeft();
     while (frontIsClear()) {
       move();
     }
     turnLeft();
     while (frontIsClear()) {
       move();
     }
     turnLeft();
     while (frontIsClear()) {
       move();
     }
     turnLeft();
     while (frontIsClear()) {
       move();
     }
     explode();
   }

   public void go_map() {
      Sizer();
      mult = size/2-3;
      Mover(2);
      PutMover(size-4);
      turnRight();
      toLeftCorner();
      Block();
      move();
      turnLeft();
      Inside(mult);
      Block();
      toRightEye();
      Block();
      toLeftEye();
      Block();
      Victory();

   }

   public void go_file() throws Exception {
      Scanner infile = new Scanner( new File("smilesize.txt") );
      size = Integer.parseInt(infile.nextLine());
      mult = size/2-3;
      Starter();
      PutMover(size-4);
      turnAround();
      Mover(size-3);
      turnRight();
      toLeftCorner();
      Block();
      move();
      turnLeft();
      Inside(mult);
      Block();
      toRightEye();
      Block();
      toLeftEye();
      Block();
      Victory();
   }
}
