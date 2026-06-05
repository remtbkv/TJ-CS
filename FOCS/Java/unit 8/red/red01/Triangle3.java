import java.awt.*;

public class Triangle3 {
    private Color color;
    private int[] xP, yP;
    private int width = 50, height = 50, mydx = 0, mydy = 0;

    public Triangle3(Color color1, int width1, int height1) {
        color = color1;
        if (width1 > 0) {
            width = width1;
        }
        if (height1 > 0) {
            height = height1;
        }
        xP = new int[]{400 - width / 2, 400, 400 + width / 2};
        yP = new int[]{390, 390 - height, 390};
    }

    void move() {
        for (int x = 0; x < xP.length; x++) {
            xP[x] += mydx;
            yP[x] += mydy;
        }
        if (yP[1] < 0) {
            yP = new int[]{400, 400 - height, 400};
        }
        else if (yP[0] > 400) {
            yP = new int[]{height, 0, height};
        }
        if (xP[0] < 0) {
            xP = new int[]{800 - width, 800 - width / 2, 800};
        }
        else if (xP[2] > 800) {
            xP = new int[]{0, width / 2, width};
        }
    }

    public void adddy(int dy) {
        mydy += dy;
    }

    public void adddx(int dx) {
        mydx += dx;
    }

    void draw(Graphics myBuffer) {
        myBuffer.setColor(color);
        myBuffer.fillPolygon(xP, yP, xP.length);
    }
}