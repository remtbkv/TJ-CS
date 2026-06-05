import javax.swing.JFrame;
    public class GraphicsExampleDriver
   {
       public static void main(String[] args)
      {
         JFrame frame = new JFrame("Squidward");
         frame.setSize(400, 425);      //In Windows, the menu bar at the top is 25 pixels tall...
         frame.setLocation(100, 50);
         frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
         frame.setContentPane(new Squidward());    //...so we would expect the content pane to be 400x400.
         frame.setVisible(true);
      }
   }