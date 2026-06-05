import java.awt.*;

public class Triangle {
    private Color color;
    private int[] xP, yP;
    private int width=50, height=50;

    public Triangle(Color color1, int width1, int height1) {
        color = color1;
        if (width1>0) { width = width1; }
        if (height1>0) { height = height1; }
        xP = new int[] {400-width/2, 400, 400+width/2};
        yP = new int[] {390, 400-height, 390};
    }

    void move(int dx, int dy) {
        for (int x=0; x<xP.length; x++) {
            xP[x] += dx;
            yP[x] += dy;
        }
    }

    void draw(Graphics myBuffer) {
        myBuffer.setColor(color);
        myBuffer.fillPolygon(xP, yP, xP.length);
    }
}