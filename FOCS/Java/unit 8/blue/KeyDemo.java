import javax.swing.*;
import java.awt.*;
import java.awt.event.*;
import java.awt.image.*;

public class KeyDemo
{
   public static void main(String[] args)
   { 
      JFrame frame = new JFrame("GUI + a graphics JFrame");
      frame.setSize(600, 430);
      frame.setLocation(20, 20);
      frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
      frame.setContentPane(new KeyPanel());
      frame.setVisible(true);
   }
}

class KeyPanel extends JPanel
{
   RGBPanel gfx;  //A subpanel for our graphics, as in the last demo. 
                  //The keyboard input will also be handled there.
   
   public KeyPanel()
   {
      setLayout(new BorderLayout());
      
      JLabel title = new JLabel("Key demo!  Press 'Reset' then type 'r', 'g', or 'b' keys several times.");
      title.setFont(new Font("Serif", Font.BOLD, 20));
      title.setHorizontalAlignment(SwingConstants.CENTER);
      add(title, BorderLayout.NORTH);
      
      gfx = new RGBPanel();
      add(gfx);
      
      JButton resetButton = new JButton("Reset");
      resetButton.addActionListener(new ResetListener());
      add(resetButton, BorderLayout.SOUTH);   
   }
   
   private class ResetListener implements ActionListener
   {
      public void actionPerformed(ActionEvent e)
      {
         gfx.reset();
         gfx.requestFocusInWindow();  //This is ESSENTIAL, otherwise keyboard input won't be sent to the subpanel!
      }
   }
}

class RGBPanel extends JPanel
{
   public static final int FRAME = 400;
   private int r, g, b;
   private BufferedImage myImage;
   private Graphics myBuffer;
      
   public RGBPanel()
   {
      myImage =  new BufferedImage(FRAME, FRAME, BufferedImage.TYPE_INT_RGB);
      myBuffer = myImage.getGraphics();
      r = g = b = 0;
      myBuffer.setColor(new Color(r, g, b));
      myBuffer.fillRect(0,0,FRAME,FRAME);
      
      addKeyListener(new Key());  //Key listeners listen for keyboard inputs
      setFocusable(true);         //Need this in order to be able to receive keyboard input, along with .requestFocusInWindow() above
   }
   
   public void paintComponent(Graphics g)  //The same method as before!
   {
      g.drawImage(myImage, 0, 0, getWidth(), getHeight(), null);  //Draw the buffered image we've stored as a field
   }
   
   public void reset()
   {
      r = g = b = 0;
      myBuffer.setColor(new Color(r, g, b));
      myBuffer.fillRect(0,0,FRAME,FRAME);
      repaint();
   }
   
   private class Key extends KeyAdapter  //This subpanel must have focus for keyboard input to register (see above)
   {
      public void keyPressed(KeyEvent e)  //We override this method; "e" contains a lot of information...
      {
      	//...including a Key Code, which will let us see which key the user pressed.  Check for 'r':
         if(e.getKeyCode() == KeyEvent.VK_R)
            r += 10;
         //Check for 'g':
         else if(e.getKeyCode() == KeyEvent.VK_G)
            g += 10;
         //Check for 'b':
         else if(e.getKeyCode() == KeyEvent.VK_B)
            b += 10;
         
         //Fix bad input
         if(r > 255)
            r = 255;
         if(g > 255)
            g = 255;
         if(b > 255)
            b = 255;
         
         //no matter what key was pressed, update and repaint
         myBuffer.setColor(new Color(r, g, b));
         myBuffer.fillRect(0,0,FRAME,FRAME);
         repaint();
      }
   }
}