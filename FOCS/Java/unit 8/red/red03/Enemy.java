import java.awt.*;

public class Enemy {
    private Color myColor;
    private int mySize, mydx, myX, myY;

    public Enemy() {
        myColor = new Color(10, 10, 10);
        mySize = 40;
        mydx = 5;
        myX = 10;
        myY = 40;
    }

    public void move() {
        myX += mydx;
    }

    public int getX() {
        return myX;
    }

    public int getY() {
        return myY + mySize;
    }

    public int getSize() {
        return mySize;
    }

    public void setdx(int dx) {
        mydx = dx;
    }

    public void draw(Graphics myBuffer) {
        myBuffer.setColor(myColor);
        myBuffer.fillRect(myX, myY, mySize * 2, mySize);
    }
}