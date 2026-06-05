//Torbert, e-mail: smtorbert@fcps.edu
//version 6.17.2003

import javax.swing.*;
import java.awt.*;

public class ExamplePanel extends JPanel {
    public void paintComponent(Graphics g) {
      /*
      This is a walkthrough/demonstration of many graphics commands!
      RUN GraphicsExampleDriver.java FIRST, and look at the resulting image AS you read along with the comments below.

      ExamplePanel is a content pane is made up of individual pixels, each identified by an x coordinate and a y coordinate.
      In Java graphics, x and y coordinates are counted from the TOP LEFT corner.  In other words, the top left is (0,0).  
      The x value of a pixel increases to the right as you'd expect.  The y value increases on the way DOWN.  So the 
      point (10, 25) is directly ABOVE (10, 100), and in this particular program's case (400,400) is the BOTTOM RIGHT.
      
      You draw objects or words onto the screen with individual graphics commands.  These draw one thing at a time onto 
      the content pane.  It all happens so fast that it looks like it's simultaneous, but it isn't.  You'll notice below 
      that we take the Graphics object g automatically passed into this method and alternate setting a color and then
      drawing something.  Each time you set a color, that color is used for all the things you draw until you set a 
      different color on a later line of code.
      
      Java�s Color class predefines thirteen color constants:  BLACK, BLUE, CYAN, DARK_GRAY, GRAY, GREEN, LIGHT_GRAY, 
      MAGENTA, ORANGE, PINK, RED, WHITE, and YELLOW.  You can see several examples below.  You can also define your 
      own colors; see NOTE 1 at the bottom of this file.
            
      As you read this, please feel free to experiment!  Change values, move commands around, watch what happens!
      */

        //Fill in background.  We'll use a rectangle to cover the whole content pane, which is 400x400.
        g.setColor(Color.LIGHT_GRAY);
        g.fillRect(0, 0, 400, 400);  //4 args.  Starting at top left corner, (x, y, width, height).

        //Draw house
        g.setColor(Color.GREEN.darker());      //We can call .darker() or .brighter() on any built in color constant.
        g.drawLine(0, 350, 400, 350);                //Draw the green ground.  4 args, (x, y, x2, y2) draws a line from (x, y) to (x2, y2).
        g.setColor(Color.RED);
        g.drawRect(100, 200, 150, 150);            //Draw a square for red walls.  Note difference between drawRect and fillRect.
        g.setColor(Color.BLACK);
        g.fillRect(150, 275, 50, 75);           //Draw a solid black door.

        //Draw the triangle roof, which needs three points: 	(75, 200) and
        int xPoints[] = {75, 175, 275};            //			      (175, 150) and
        int yPoints[] = {200, 150, 200};            //			      (275, 200)
        g.drawPolygon(xPoints, yPoints, 3);        //Draw the roof (color is still black).  More explanation of this method in NOTE 2 below.


        //Draw the sun
        g.setColor(Color.YELLOW);
        g.fillOval(300, 75, 50, 50);  //4 args; this one's a little strange.  Imagine a rectangle around the oval and
        //the arguments are (x, y, width, height) as before, where (x, y) is the top left
        //OF THAT RECTANGLE (not the oval's center).  So, the sun is not centered at (300,75).
        //If you drew a rectangle (square in this case) around the sun, the top left would be
        //at (300,75).  The center of this circle is at (325, 100) - how do I know that?

        //Write the text
        //Font is a type of object in Java.  Constructor takes (style, plain/bold/italic, and size).  More examples in NOTE 3.
        g.setFont(new Font("Serif", Font.BOLD | Font.ITALIC, 30));  //We'll use size 30 serif font, bold AND italic.
        g.setColor(Color.WHITE);
        g.drawString("Welcome Home", 50, 50); //This is (text, x, y), where x,y is the location of the BOTTOM left corner
        //of the first letter.  (Not the TOP left corner, like the rectangles/ovals.)

        //Draw the picket fence (still white from setting the color above).
        for (int x = 5; x < 400; x += 10)  //Use a loop to draw equally spaced identical shapes; note x+=10 not x+=1.
            g.drawLine(x, 300, x, 350);

        //Draw the clouds (also still white).  These are over top of the sun because we drew them later.
        for (int x = 20; x < 380; x += 40)
            g.fillOval(x, 100, 25, 25);
    }
}


/*
NOTE 1: custom colors!

Google "color picker", and you'll get a little Google interface that lets you pick your own colors.
In the lower left corner, you'll see a box that says "RGB".  Use those three values in a constructor
to create your own color.  (We'll learn more about what those values mean later on!)  For example:

g.setColor(new Color(66, 135, 245));   //Common mistake: don't forget "new".



NOTE 2: how drawPolygon works!

To be specific, drawPolygon takes two integer arrays and a number of points.  It iterates over both lists
simultaneously, taking each x coordinate in turn from the first and each y coordinate in turn from the second.
The last point is automatically connected back to the first.  For this to work, the length of both arrays
should be equal to the integer given as the final argument.



NOTE 3: More Font examples!

new Font("Serif", Font.PLAIN, 8)
new Font("SansSerif", Font.BOLD, 20)
new Font("Monospaced", Font.ITALIC, 12)
new Font("Arial", Font.BOLD | Font.ITALIC, 60)

Try them out and see what they look like!
*/