import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class Green2Panel extends JPanel {
    JLabel prompt;
    JLabel number;
    JTextField LuserIn;
    JTextField RuserIn;
    double num;

    public Green2Panel() {

        setLayout(new BorderLayout());

        // title
        JLabel title = new JLabel("Lab-08-GREEN-02!");
        title.setFont(new Font("Serif", Font.BOLD, 20));
        title.setHorizontalAlignment(SwingConstants.CENTER);
        add(title, BorderLayout.NORTH);

        // bottom
        JPanel botSub = new JPanel();
        botSub.setLayout(new GridLayout(1, 4));
        JButton ADD = new JButton("Add");
        ADD.addActionListener(new Green2Panel.ADDListener());
        botSub.add(ADD);
        JButton SUB = new JButton("Subtract");
        SUB.addActionListener(new Green2Panel.SUBListener());
        botSub.add(SUB);
        JButton MULT = new JButton("Multiply");
        MULT.addActionListener(new Green2Panel.MULTListener());
        botSub.add(MULT);
        JButton DIV = new JButton("Divide");
        DIV.addActionListener(new Green2Panel.DIVListener());
        botSub.add(DIV);
        add(botSub, BorderLayout.SOUTH);

        // west
        JPanel westSub = new JPanel();
        westSub.setLayout(new GridLayout(2, 1));
        prompt = new JLabel("Enter a number");
        prompt.setFont(new Font("Serif", Font.BOLD, 10));
        prompt.setHorizontalAlignment(SwingConstants.LEFT);
        prompt.setVerticalAlignment(SwingConstants.BOTTOM);
        westSub.add(prompt);
        LuserIn = new JTextField("0", 10);
        LuserIn.setHorizontalAlignment(SwingConstants.CENTER);
        westSub.add(LuserIn);
        add(westSub, BorderLayout.WEST);

        // east
        JPanel eastSub = new JPanel();
        eastSub.setLayout(new GridLayout(2, 1));
        prompt = new JLabel("Enter a number");
        prompt.setFont(new Font("Serif", Font.BOLD, 10));
        prompt.setHorizontalAlignment(SwingConstants.LEFT);
        prompt.setVerticalAlignment(SwingConstants.BOTTOM);
        eastSub.add(prompt);
        RuserIn = new JTextField("0", 10);
        RuserIn.setHorizontalAlignment(SwingConstants.CENTER);
        eastSub.add(RuserIn);
        add(eastSub, BorderLayout.EAST);

        // center
        num = 0;
        number = new JLabel("" + num);
        number.setFont(new Font("Serif", Font.BOLD, 80));
        number.setHorizontalAlignment(SwingConstants.CENTER);
        add(number);
    }

    private class ADDListener implements ActionListener {
        public void actionPerformed(ActionEvent e) {
            double LVal = Double.parseDouble(LuserIn.getText());
            double RVal = Double.parseDouble(RuserIn.getText());
            num = LVal + RVal;
            number.setText("" + num);
        }
    }

    private class SUBListener implements ActionListener {
        public void actionPerformed(ActionEvent e) {
            double LVal = Double.parseDouble(LuserIn.getText());
            double RVal = Double.parseDouble(RuserIn.getText());
            num = LVal - RVal;
            number.setText("" + num);
        }
    }

    private class MULTListener implements ActionListener {
        public void actionPerformed(ActionEvent e) {
            double LVal = Double.parseDouble(LuserIn.getText());
            double RVal = Double.parseDouble(RuserIn.getText());
            num = LVal * RVal;
            number.setText("" + num);
        }
    }

    private class DIVListener implements ActionListener {
        public void actionPerformed(ActionEvent e) {
            double LVal = Double.parseDouble(LuserIn.getText());
            double RVal = Double.parseDouble(RuserIn.getText());
            num = LVal / RVal;
            number.setText("" + num);
        }
    }
}