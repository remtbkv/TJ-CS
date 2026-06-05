import javax.swing.*;
import java.awt.*;
import java.awt.event.*;
import java.awt.image.*;

public class GUIPanel2 extends JPanel {

    private JTextField r, g, b, w, h;
    private TrianglePanel2 gfx;

    public GUIPanel2() {
        setLayout(new BorderLayout());

        gfx = new TrianglePanel2();
        add(gfx);

        JLabel title = new JLabel("The moving triangle!");
        title.setFont(new Font("Serif", Font.BOLD, 20));
        title.setHorizontalAlignment(SwingConstants.CENTER);
        add(title, BorderLayout.NORTH);

        JButton reset = new JButton("Reset with a new triangle!");
        reset.addActionListener(new GUIPanel2.ResetListener());
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
            gfx.requestFocusInWindow();
        }
    }
}