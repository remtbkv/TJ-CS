import javax.swing.*;
import java.awt.*;

public class Squidward extends JPanel {
    public void paintComponent(Graphics g) {

        Color TEAL = new Color(182,219,202,255);

        // background
        g.setColor(new Color(28,144,226,255));
        g.fillRect(0, 0, 400, 400);

        // top head
        g.setColor(Color.BLACK);
        g.drawOval(100, 70, 200, 135);
        g.setColor(TEAL);
        g.fillOval(100, 70, 200, 135);

        // wrinkles
        g.setColor(Color.BLACK);
        g.drawArc(140, 95, 120, 30, 0, 180);
        g.drawArc(140, 110, 120, 30, 0, 180);

        // dots
        g.setColor(new Color(137,174,157,255));
        g.fillOval(150, 82, 4, 4);
        g.fillOval(170, 77, 4, 4);
        g.fillOval(190, 80, 4, 4);
        g.fillOval(210, 75, 4, 4);
        g.fillOval(235, 80, 4, 4);
        g.fillOval(255, 86, 4, 4);

        // mouth
        g.setColor(Color.BLACK);
        g.drawOval(125, 220, 150, 40);
        g.setColor(TEAL);
        g.fillOval(125, 220, 150, 40);

        // bottom head
        g.setColor(Color.BLACK);
        g.drawRect(149, 196, 1, 29);
        g.drawRect(150, 196, 100, 29);
        g.setColor(TEAL);
        g.fillRect(150, 196, 100, 30);
        g.fillRect(150, 197, 100, 30);

        // // mustache
        // g.setColor(Color.BLACK);
        // g.fillArc(133, 220, 134, 70, 180, -180);
        //
        // // bottom mouth
        // g.setColor(TEAL);
        // g.fillRect(150, 255, 100, 35);

        // smile
        g.setColor(Color.BLACK);
        g.drawArc(140, 239, 120, 10, 0, 180);
        g.drawArc(140, 240, 120, 10, 0, 180);

        // nose
        g.setColor(Color.BLACK);
        g.drawOval(182, 195, 36, 90);
        g.setColor(new Color(172,209,192,255));
        g.fillOval(182, 195, 36, 90);

        // eyes
        int y = 190;

        for (int x=155; x<=200; x+=45) {
            g.setColor(Color.BLACK);
            g.drawOval(x, 150, 45, 65);
            g.setColor(new Color(231,236,182,255));
            g.fillOval(x, 150, 45, 65);
            g.setColor(new Color(125,26,21,255));
            g.fillOval(y, 175, 10, 20);
            y+=45;
            g.setColor(new Color(162,199,182,255));
            g.fillArc(x, 150, 45, 65, 180, -180);
            // g.setColor(Color.BLACK);
            // g.drawRect(x, 177, 45, 5);
        }

        useless(g); // just enough to get credit for assignment

    }

    public void useless(Graphics g) {
        // polygon
        g.setColor(Color.BLACK);
        int xPoints[] = {5+10, 20+10, 40+10, 25+10};
        int yPoints[] = {356-10, 356-20, 356-20, 356-10};
        g.drawPolygon(xPoints, yPoints, 4);
        g.setColor(Color.WHITE);
        g.fillPolygon(xPoints, yPoints, 4);

        // words
        g.setFont(new Font("Monospaced", Font.BOLD | Font.ITALIC, 30));
        g.setColor(Color.WHITE);
        g.drawString("Welcome Home", 65, 350);
        g.setFont(new Font("Arial", Font.BOLD | Font.ITALIC, 30));
        g.drawString("(yay)", 300, 350);
    }
}