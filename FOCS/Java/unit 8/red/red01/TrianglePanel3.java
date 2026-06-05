import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.KeyAdapter;
import java.awt.event.KeyEvent;
import java.awt.image.BufferedImage;

public class TrianglePanel3 extends JPanel {
    public static final int FRAME = 400;
    private static final Color BACKGROUND = new Color(204, 204, 204);

    private BufferedImage myImage;
    private Graphics myBuffer;
    private Triangle3 tri;
    private boolean up, down, left, right;
    private int dx, dy;
    private Timer t;

    public TrianglePanel3() {
        myImage = new BufferedImage(FRAME * 2, FRAME, BufferedImage.TYPE_INT_RGB);
        myBuffer = myImage.getGraphics();
        myBuffer.setColor(BACKGROUND);
        myBuffer.fillRect(0, 0, FRAME * 2, FRAME);

        addKeyListener(new Key());
        setFocusable(true);

        t = new Timer(5, new moveListener());
        up = down = left = right = false;
    }

    public void paintComponent(Graphics g) {
        g.drawImage(myImage, 0, 0, getWidth(), getHeight(), null);
    }

    public void begin() {
        t.start();
    }

    public void blank() {
        myBuffer.setColor(BACKGROUND);
        myBuffer.fillRect(0, 0, FRAME * 2, FRAME);
    }

    public void moveTriangle() {
        blank();
        tri.move();
        tri.draw(myBuffer);
        repaint();
    }

    public void reset(Color c, int w, int h) {
        blank();
        tri = new Triangle3(c, w, h);
        tri.draw(myBuffer);
        repaint();
    }

    private class moveListener implements ActionListener {
        public void actionPerformed(ActionEvent e) {
            moveTriangle();
        }
    }

    private class Key extends KeyAdapter {
        public void keyPressed(KeyEvent e) {
            if (e.getKeyCode() == KeyEvent.VK_UP && !up) {
                tri.adddy(-2);
                up = true;
            }
            else if (e.getKeyCode() == KeyEvent.VK_DOWN && !down) {
                tri.adddy(2);
                down = true;
            }
            else if (e.getKeyCode() == KeyEvent.VK_LEFT && !left) {
                tri.adddx(-2);
                left = true;
            }
            else if (e.getKeyCode() == KeyEvent.VK_RIGHT && !right) {
                tri.adddx(2);
                right = true;
            }
            repaint();
        }

        public void keyReleased(KeyEvent e) {
            if (e.getKeyCode() == KeyEvent.VK_UP) {
                tri.adddy(2);
                up = false;
            }
            else if (e.getKeyCode() == KeyEvent.VK_DOWN) {
                tri.adddy(-2);
                down = false;
            }
            else if (e.getKeyCode() == KeyEvent.VK_LEFT) {
                tri.adddx(2);
                left = false;
            }
            else if (e.getKeyCode() == KeyEvent.VK_RIGHT) {
                tri.adddx(-2);
                right = false;
            }
            repaint();
        }
    }


}