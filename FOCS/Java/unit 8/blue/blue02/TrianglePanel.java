import javax.swing.*;
import java.awt.*;
import java.awt.image.BufferedImage;

public class TrianglePanel extends JPanel {
    public static final int FRAME = 400;
    private static final Color BACKGROUND = new Color(204, 204, 204);

    private BufferedImage myImage;
    private Graphics myBuffer;
    private Triangle tri;

    public TrianglePanel() {
        myImage = new BufferedImage(FRAME * 2, FRAME, BufferedImage.TYPE_INT_RGB);
        myBuffer = myImage.getGraphics();
        myBuffer.setColor(BACKGROUND);
        myBuffer.fillRect(0, 0, FRAME * 2, FRAME);
    }

    public void paintComponent(Graphics g) {
        g.drawImage(myImage, 0, 0, getWidth(), getHeight(), null);
    }

    public void blank() {
        myBuffer.setColor(BACKGROUND);
        myBuffer.fillRect(0, 0, FRAME * 2, FRAME);
    }

    public void moveTriangle(int dx, int dy) {
        tri.move(dx, dy);
        blank();
        tri.draw(myBuffer);
        repaint();
    }

    public void reset(Color c, int w, int h) {
        tri = new Triangle(c, w, h);
        blank();
        tri.draw(myBuffer);
        repaint();
    }
}