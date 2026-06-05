import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.KeyAdapter;
import java.awt.event.KeyEvent;
import java.awt.image.BufferedImage;

public class TrianglePanel5 extends JPanel {
    public static final int FRAME = 400;
    private static final Color BACKGROUND = new Color(204, 204, 204);

    private BufferedImage myImage;
    private Graphics myBuffer;
    private Triangle5 tri;
    private Rocket2 rock;
    private Enemy bad;
    private boolean up, down, left, right, rocket, badA;
    private int dx, dy, rX, rY, rS, bX, bY, bS;
    private Timer t, t2, t3;

    public TrianglePanel5() {
        myImage = new BufferedImage(FRAME * 2, FRAME, BufferedImage.TYPE_INT_RGB);
        myBuffer = myImage.getGraphics();
        myBuffer.setColor(BACKGROUND);
        myBuffer.fillRect(0, 0, FRAME * 2, FRAME);

        addKeyListener(new Key());
        setFocusable(true);

        t = new Timer(10, new animationListener());

        up = down = left = right = rocket = false;
    }

    public void paintComponent(Graphics g) {
        g.drawImage(myImage, 0, 0, getWidth(), getHeight(), null);
    }

    public void begin() {
        t.start();
    }

    public void reset(Color c, int w, int h) {
        myBuffer.setColor(BACKGROUND);
        myBuffer.fillRect(0, 0, FRAME * 2, FRAME);

        tri = new Triangle5(c, w, h);
        tri.draw(myBuffer);

        bad = new Enemy();
        badA = true;

        rock = new Rocket2();

        repaint();
    }

    public void animate() {
        myBuffer.setColor(BACKGROUND);
        myBuffer.fillRect(0, 0, FRAME * 2, FRAME);

        tri.move();
        tri.draw(myBuffer);

        if (rocket) {
            rock.move();
            rock.draw(myBuffer);
        }
        if (rock.check()) {
            rocket = false;
        }

        if (badA) {
            rX = rock.getX();
            rY = rock.getY();
            rS = rock.getSize();
            bX = bad.getX();
            bY = bad.getY();
            bS = bad.getSize();

            if ((rY <= bY && bY - bS <= rY) && (bX <= rX && rX <= bX + bS * 2 - rS)) {
                badA = false;
            }
            else {
                if (bX <= 10) {
                    bad.setdx(5);
                }
                else if (bX >= 790 - (bS * 2)) {
                    bad.setdx(-5);
                }
                bad.move();
                bad.draw(myBuffer);
            }
        }
        repaint();
    }

    private class animationListener implements ActionListener {
        public void actionPerformed(ActionEvent e) {
            animate();
        }
    }

    private class Key extends KeyAdapter {
        public void keyPressed(KeyEvent e) {
            if (e.getKeyCode() == KeyEvent.VK_SPACE && !rocket) {
                rock.setXY(tri.getX(), tri.getY());
                rocket = true;
            }
            if (e.getKeyCode() == KeyEvent.VK_UP && !up) {
                tri.adddy(-5);
                up = true;
            }
            if (e.getKeyCode() == KeyEvent.VK_DOWN && !down) {
                tri.adddy(5);
                down = true;
            }
            if (e.getKeyCode() == KeyEvent.VK_LEFT && !left) {
                tri.adddx(-5);
                left = true;
            }
            if (e.getKeyCode() == KeyEvent.VK_RIGHT && !right) {
                tri.adddx(5);
                right = true;
            }
            repaint();
        }

        public void keyReleased(KeyEvent e) {
            if (e.getKeyCode() == KeyEvent.VK_UP) {
                tri.adddy(5);
                up = false;
            }
            if (e.getKeyCode() == KeyEvent.VK_DOWN) {
                tri.adddy(-5);
                down = false;
            }
            if (e.getKeyCode() == KeyEvent.VK_LEFT) {
                tri.adddx(5);
                left = false;
            }
            if (e.getKeyCode() == KeyEvent.VK_RIGHT) {
                tri.adddx(-5);
                right = false;
            }
            repaint();
        }
    }
}