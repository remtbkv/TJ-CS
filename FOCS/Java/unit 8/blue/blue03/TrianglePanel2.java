import javax.swing.*;
import java.awt.*;
import java.awt.event.KeyAdapter;
import java.awt.event.KeyEvent;
import java.awt.image.BufferedImage;

public class TrianglePanel2 extends JPanel {
    public static final int FRAME = 400;
    private static final Color BACKGROUND = new Color(204, 204, 204);

    private BufferedImage myImage;
    private Graphics myBuffer;
    private Triangle2 tri;

    public TrianglePanel2() {
        myImage = new BufferedImage(FRAME * 2, FRAME, BufferedImage.TYPE_INT_RGB);
        myBuffer = myImage.getGraphics();
        myBuffer.setColor(BACKGROUND);
        myBuffer.fillRect(0, 0, FRAME * 2, FRAME);

        addKeyListener(new Key());
        setFocusable(true);
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
        tri = new Triangle2(c, w, h);
        blank();
        tri.draw(myBuffer);
        repaint();
    }

    private class Key extends KeyAdapter {
        public void keyPressed(KeyEvent e) {
            if (e.getKeyCode() == KeyEvent.VK_UP) {
                moveTriangle(0, -10);
            }

            else if (e.getKeyCode() == KeyEvent.VK_DOWN) {
                moveTriangle(0, 10);
            }

            else if (e.getKeyCode() == KeyEvent.VK_LEFT) {
                moveTriangle(-10, 0);
            }

            else if (e.getKeyCode() == KeyEvent.VK_RIGHT) {
                moveTriangle(10, 0);
            }

            repaint();
        }
    }
}