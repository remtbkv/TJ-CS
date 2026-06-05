import javax.swing.*;
import java.awt.*;
import java.awt.event.*;
import java.awt.image.*;

public class GUIPanel extends JPanel {

    private JTextField r, g, b, w, h;
    private TrianglePanel gfx;

    public GUIPanel() { // add(gfx) shows error?
        setLayout(new BorderLayout());

        gfx = new TrianglePanel();
        add(gfx);

        JLabel title = new JLabel("The moving triangle!");
        title.setFont(new Font("Serif", Font.BOLD, 20));
        title.setHorizontalAlignment(SwingConstants.CENTER);
        add(title, BorderLayout.NORTH);

        JButton reset = new JButton("Reset with a new triangle!");
        reset.addActionListener(new GUIPanel.ResetListener());
        add(reset, BorderLayout.SOUTH);

        JPanel west = new JPanel();
        west.setLayout(new GridLayout(5, 2));
        JLabel R = new JLabel("Red: ");
        R.setHorizontalAlignment(SwingConstants.RIGHT);
        west.add(R);
        r = new JTextField("0", 12);
        r.setHorizontalAlignment(SwingConstants.CENTER);
        west.add(r);
        JLabel G = new JLabel("Green: ");
        G.setHorizontalAlignment(SwingConstants.RIGHT);
        west.add(G);
        g = new JTextField("0", 12);
        g.setHorizontalAlignment(SwingConstants.CENTER);
        west.add(g);
        JLabel B = new JLabel("Blue: ");
        B.setHorizontalAlignment(SwingConstants.RIGHT);
        west.add(B);
        b = new JTextField("0", 12);
        b.setHorizontalAlignment(SwingConstants.CENTER);
        west.add(b);
        JLabel H = new JLabel("Height: ");
        H.setHorizontalAlignment(SwingConstants.RIGHT);
        west.add(H);
        h = new JTextField("0", 12);
        h.setHorizontalAlignment(SwingConstants.CENTER);
        west.add(h);
        JLabel W = new JLabel("Width: ");
        W.setHorizontalAlignment(SwingConstants.RIGHT);
        west.add(W);
        w = new JTextField("0", 12);
        w.setHorizontalAlignment(SwingConstants.CENTER);
        west.add(w);
        add(west, BorderLayout.WEST);

        JPanel east = new JPanel();
        east.setLayout(new GridLayout(5, 3));
        JLabel tmp1 = new JLabel("");
        east.add(tmp1);
        JLabel tmp2 = new JLabel("");
        east.add(tmp2);
        JLabel tmp3 = new JLabel("");
        east.add(tmp3);
        JLabel tmp4 = new JLabel("");
        east.add(tmp4);
        JButton up = new JButton("^");
        up.setHorizontalAlignment(SwingConstants.CENTER);
        up.addActionListener(new GUIPanel.UpListener());
        east.add(up);
        JLabel tmp5 = new JLabel("");
        east.add(tmp5);
        JButton left = new JButton("<");
        left.setHorizontalAlignment(SwingConstants.CENTER);
        left.addActionListener(new GUIPanel.LeftListener());
        east.add(left);
        JLabel tmp6 = new JLabel("");
        east.add(tmp6);
        JButton right = new JButton(">");
        right.setHorizontalAlignment(SwingConstants.CENTER);
        right.addActionListener(new GUIPanel.RightListener());
        east.add(right);
        JLabel tmp7 = new JLabel("");
        east.add(tmp7);
        JButton down = new JButton("v");
        down.setHorizontalAlignment(SwingConstants.CENTER);
        down.addActionListener(new GUIPanel.DownListener());
        east.add(down);
        JLabel tmp8 = new JLabel("");
        east.add(tmp8);
        JLabel tmp9 = new JLabel("");
        east.add(tmp9);
        JLabel tmp10 = new JLabel("");
        east.add(tmp10);
        JLabel tmp11 = new JLabel("");
        east.add(tmp11);
        add(east, BorderLayout.EAST);


    }

    private class ResetListener implements ActionListener {
        public void actionPerformed(ActionEvent e) {
            int width = Integer.parseInt(w.getText());
            int height = Integer.parseInt(h.getText());
            int rInt = Integer.parseInt(r.getText());
            int gInt = Integer.parseInt(g.getText());
            int bInt = Integer.parseInt(b.getText());
            Color c = new Color(rInt, gInt, bInt);
            gfx.reset(c, width, height);
        }
    }

    private class UpListener implements ActionListener {
        public void actionPerformed(ActionEvent e) {
            gfx.moveTriangle(0, -10);
        }
    }

    private class DownListener implements ActionListener {
        public void actionPerformed(ActionEvent e) {
            gfx.moveTriangle(0, 10);
        }
    }

    private class LeftListener implements ActionListener {
        public void actionPerformed(ActionEvent e) {
            gfx.moveTriangle(-10, 0);
        }
    }

    private class RightListener implements ActionListener {
        public void actionPerformed(ActionEvent e) {
            gfx.moveTriangle(10, 0);
        }
    }


}