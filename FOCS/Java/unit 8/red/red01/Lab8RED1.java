import javax.swing.*;

public class Lab8RED1 {
    public static void main(String[] args) {
        JFrame frame = new JFrame("GUI + a graphics JFrame");
        frame.setSize(900, 500);
        frame.setLocation(20, 20);
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setContentPane(new GUIPanel3());
        frame.setVisible(true);
    }
}