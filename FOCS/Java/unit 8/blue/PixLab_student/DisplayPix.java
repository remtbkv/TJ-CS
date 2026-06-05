import java.awt.*;
import java.awt.image.BufferedImage;
import java.io.File;
import javax.swing.*;
import java.util.Stack;

public class DisplayPix extends JPanel {
    private PixelOperations pix = new PixelOperations();
    private ImageIcon i = new ImageIcon("folder/images/beach.jpg");
    private BufferedImage img = new BufferedImage(1600, 1200, BufferedImage.TYPE_INT_RGB);
    private Graphics buf = img.getGraphics();

    private boolean clicked = false;
    private int x, y;
    private Stack<Color[][]> history = new Stack<Color[][]>();
    private Stack<Color[][]> r_history = new Stack<Color[][]>();

    public DisplayPix() {
        int w = img.getWidth();
        int h = img.getHeight();

        buf.drawImage(i.getImage(), 0, 0, w, h, null);
    }

    public int getXval() // not getX !
    {
        return x;
    }

    public int getYval() // not getY !
    {
        return y;
    }

    public int getRow() {
        return y * img.getHeight() / getHeight();
    }

    public int getCol() {
        return x * img.getWidth() / getWidth();
    }

    public int getRGB(int x, int y) {
        int xpos = x * img.getWidth() / getWidth();
        int ypos = y * img.getHeight() / getHeight();
        //
        return img.getRGB(xpos, ypos);
    }

    public void update(int xval, int yval) {
        clicked = true;

        x = xval;
        y = yval;
    }
//

    /**********************************************************************/
//
// pixel operations
// 
    public void zeroBlue() {
        history.push(pix.getArray(img));
        Color[][] tmp = pix.getArray(img);
        pix.zeroBlue(tmp);
        pix.setImage(img, tmp);
    }
//
//    ------>  enter your methods below  <-----------

    public void Negate() {
        history.push(pix.getArray(img));
        Color[][] tmp = pix.getArray(img);
        pix.Negate(tmp);
        pix.setImage(img, tmp);
    }

    public void Grayscale() {
        history.push(pix.getArray(img));
        Color[][] tmp = pix.getArray(img);
        pix.Grayscale(tmp);
        pix.setImage(img, tmp);
    }

    public void SepiaTone() {
        history.push(pix.getArray(img));
        Color[][] tmp = pix.getArray(img);
        pix.SepiaTone(tmp);
        pix.setImage(img, tmp);
    }

    public void Blur() {
        history.push(pix.getArray(img));
        Color[][] tmp = pix.getArray(img);
        pix.Blur(tmp);
        pix.setImage(img, tmp);
    }

    public void Posterize() {
        history.push(pix.getArray(img));
        Color[][] tmp = pix.getArray(img);
        pix.Posterize(tmp);
        pix.setImage(img, tmp);
    }

    public void Splash() {
        Color[][] tmp = pix.getArray(img);
        history.push(pix.getArray(img));
        pix.Splash(tmp);
        pix.setImage(img, tmp);
    }

    public void MirrorLR() {
        Color[][] tmp = pix.getArray(img);
        history.push(pix.getArray(img));
        pix.MirrorLR(tmp);
        pix.setImage(img, tmp);
    }

    public void MirrorUD() {
        Color[][] tmp = pix.getArray(img);
        history.push(pix.getArray(img));
        pix.MirrorUD(tmp);
        pix.setImage(img, tmp);
    }

    public void FlipLR() {
        Color[][] tmp = pix.getArray(img);
        history.push(pix.getArray(img));
        pix.FlipLR(tmp);
        pix.setImage(img, tmp);
    }

    public void FlipUD() {
        Color[][] tmp = pix.getArray(img);
        history.push(pix.getArray(img));
        pix.FlipUD(tmp);
        pix.setImage(img, tmp);
    }

    public void Pixelate() {
        Color[][] tmp = pix.getArray(img);
        history.push(pix.getArray(img));
        pix.Pixelate(tmp);
        pix.setImage(img, tmp);
    }

    public void Sunsetize() {
        Color[][] tmp = pix.getArray(img);
        history.push(pix.getArray(img));
        pix.Sunsetize(tmp);
        pix.setImage(img, tmp);
    }

    public void RedEye() {
        Color[][] tmp = pix.getArray(img);
        history.push(pix.getArray(img));
        pix.RedEye(tmp);
        pix.setImage(img, tmp);
    }

    public void Detect() {
        Color[][] tmp = pix.getArray(img);
        history.push(pix.getArray(img));
        pix.Detect(tmp);
        pix.setImage(img, tmp);
    }

    // challenge

    public void Modify(int rMult, int gMult, int bMult) {
        Color[][] tmp = pix.getArray(img);
        history.push(pix.getArray(img));
        pix.Modify(tmp, rMult, gMult, bMult);
        pix.setImage(img, tmp);
    }

    public void Undo() {
        if (history.isEmpty()) {
            System.out.println("Do something before you undo!");
        }
        else {
            r_history.push(pix.getArray(img));
            pix.setImage(img, history.pop());
        }
    }

    public void Redo() {
        history.push(pix.getArray(img));
        if (r_history.isEmpty()) {
            System.out.println("Undo something before you redo!");
        }
        else {
            pix.setImage(img, r_history.pop());
        }
    }

    /**********************************************************************/

    public void resetImage() {
        history.push(pix.getArray(img));
        int w = img.getWidth();
        int h = img.getHeight();
        buf.drawImage(i.getImage(), 0, 0, w, h, null);
    }

    public boolean openImage() {
        history.push(pix.getArray(img));
        int w = img.getWidth();
        int h = img.getHeight();
        //
        JFileChooser fc = new JFileChooser("folder/images");
        fc.showOpenDialog(null);
        File f = fc.getSelectedFile();
        //
        try {
            i = new ImageIcon("folder/images/" + f.getName());
        } catch (Exception e) {
            return false;
        }
        buf.drawImage(i.getImage(), 0, 0, w, h, null);
        //
        return true;
    }

    public void up() {
        y = Math.max(0, y - 1);
    }

    public void down() {
        y = Math.min(getHeight() - 1, y + 1);
    }

    public void left() {
        x = Math.max(0, x - 1);
    }

    public void right() {
        x = Math.min(getWidth() - 1, x + 1);
    }

    public void paintComponent(Graphics g) {
        g.drawImage(img, 0, 0, getWidth(), getHeight(), null);
        //
        if (clicked) {
            g.setColor(Color.black);
            g.drawLine(x - 5, y - 1, x + 5, y - 1);
            g.drawLine(x - 5, y + 1, x + 5, y + 1);
            g.drawLine(x - 1, y - 5, x - 1, y + 5);
            g.drawLine(x + 1, y - 5, x + 1, y + 5);
            //
            g.setColor(Color.yellow);
            g.drawLine(x - 5, y, x - 1, y);
            g.drawLine(x + 1, y, x + 5, y);
            g.drawLine(x, y - 5, x, y - 1);
            g.drawLine(x, y + 1, x, y + 5);
        }

    }
}