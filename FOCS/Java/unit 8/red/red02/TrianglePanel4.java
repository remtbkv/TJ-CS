import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.KeyAdapter;
import java.awt.event.KeyEvent;
import java.awt.image.BufferedImage;

public class TrianglePanel4 extends JPanel {
    public static final int FRAME = 400;
    private static final Color BACKGROUND = new Color(204, 204, 204);

    private BufferedImage myImage;
    private Graphics myBuffer;
    private Triangle4 tri;
    private Rocket rock;
    private boolean up, down, left, right, rocket;
    private int dx, dy;
    private Timer t, t2;

    public TrianglePanel4() {
        myImage = new BufferedImage(FRAME * 2, FRAME, BufferedImage.TYPE_INT_RGB);
        myBuffer = myImage.getGraphics();
        myBuffer.setColor(BACKGROUND);
        myBuffer.fillRect(0, 0, FRAME * 2, FRAME);

        addKeyListener(new Key());
        setFocusable(true);

        rock = new Rocket();
        t = new Timer(5, new moveListener());
        t2 = new Timer(5, new rocketListener());
        up = down = left = right = rocket = false;
    }

    public void paintComponent(Graphics g) {
        g.drawImage(myImage, 0, 0, getWidth(), getHeight(), null);
    }

    public void begin() {
        t.start();
        t2.start();
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

    public void moveRocket() {
        if (rocket) {
            rock.move();
            rock.draw(myBuffer);
            repaint();
        }

        if (rock.check()) {
            rocket=false;
        }
    }

    public void reset(Color c, int w, int h) {
        blank();
        tri = new Triangle4(c, w, h);
        tri.draw(myBuffer);
        repaint();
    }

    private class moveListener implements ActionListener {
        public void actionPerformed(ActionEvent e) {
            moveTriangle();
        }
    }

    private class rocketListener implements ActionListener {
        public void actionPerformed(ActionEvent e) {
            if (rocket) {
                moveRocket();
            }
        }
    }

    private class Key extends KeyAdapter {
        public void keyPressed(KeyEvent e) {
            if (e.getKeyCode() == KeyEvent.VK_SPACE && !rocket) {
                rock.setXY(tri.getX(), tri.getY());
                rocket = true;
            }
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