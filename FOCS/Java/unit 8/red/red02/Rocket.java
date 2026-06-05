import java.awt.*;

public class Rocket {
    private Color myColor;
    private int mySize, mydy, myX, myY;

    public Rocket() {
        myColor = new Color(10, 10, 10);
        mySize = 10;
        mydy = -6;
    }

    public void setXY(int x, int y) {
        myX = x;
        myY = y;
    }

    public void move() {
        myY += mydy;
    }

    public void adddy(int dy) {
        mydy += dy;
    }

    public boolean check() {
        return myY <= -(mySize * 3);
    }

    public void draw(Graphics myBuffer) {
        myBuffer.setColor(myColor);
        myBuffer.fillRect(myX - mySize / 2, myY - mySize * 3, mySize, mySize * 3);
    }
}