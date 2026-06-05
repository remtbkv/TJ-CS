import javax.swing.*;

public class Lab8RED3 {
    public static void main(String[] args) {
        JFrame frame = new JFrame("GUI + a graphics JFrame");
        frame.setSize(900, 500);
        frame.setLocation(20, 20);
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setContentPane(new GUIPanel5());
        frame.setVisible(true);
    }
}