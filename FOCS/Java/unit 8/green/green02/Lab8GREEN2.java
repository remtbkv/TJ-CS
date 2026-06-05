import javax.swing.*;

public class Lab8GREEN2
{
    public static void main(String[] args)
    {
        JFrame frame = new JFrame("GUI with BorderLayout");
        frame.setSize(800, 400);
        frame.setLocation(20, 20);
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setContentPane(new Green2Panel());
        frame.setVisible(true);
    }
}