// Name: J1-26-22
// Date: 9/29/22

import java.awt.*;
import java.awt.event.*;
import javax.swing.*;
import java.util.*;

public class NQueens extends JPanel {
   // Instance Variables: Encapsulated data for EACH NQueens problem
   private JButton[][] board;
   private int N;
   JSlider speedSlider;
   private int timerDelay;

   public NQueens() { // extension
      Scanner sc = new Scanner(System.in);
      System.out.println("Enter size of board: ");
      N = sc.nextInt();

      if (N == 0) {
         System.out.println("Solution not found");
      }
      else {
         this.setLayout(new BorderLayout());

         JPanel north = new JPanel();
         north.setLayout(new FlowLayout());
         add(north, BorderLayout.NORTH);
         JLabel label = new JLabel(N + " Queens solution");
         north.add(label);

         JPanel center = new JPanel();
         center.setLayout(new GridLayout(N, N));
         add(center, BorderLayout.CENTER);
         board = new JButton[N][N];
         for (int r = 0; r < N; r++) {
            for (int c = 0; c < N; c++) {
               board[r][c] = new JButton();
               board[r][c].setBackground(Color.blue);
               center.add(board[r][c]);
            }
         }

         speedSlider = new JSlider();
         speedSlider.setValue(0);
         speedSlider.setInverted(true);

         add(speedSlider, BorderLayout.SOUTH);

         if (!solve())
            System.out.println("Solution not found");
         else {
            JFrame frame = new JFrame("N-Queens");
            frame.setSize(400, 400);
            frame.setLocation(200, 100);
            frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
            frame.setContentPane(this);
            frame.setVisible(true);
         }
      }
   }

   public NQueens(int n) // normal
   {
      if (n == 0)
         System.out.println("Invalid size");
      else {
         N = n;
         this.setLayout(new BorderLayout());

         JPanel north = new JPanel();
         north.setLayout(new FlowLayout());
         add(north, BorderLayout.NORTH);
         JLabel label = new JLabel(N + " Queens solution");
         north.add(label);

         JPanel center = new JPanel();
         center.setLayout(new GridLayout(N, N));
         add(center, BorderLayout.CENTER);
         board = new JButton[N][N];
         for (int r = 0; r < N; r++)
            for (int c = 0; c < N; c++) {
               board[r][c] = new JButton();
               board[r][c].setBackground(Color.blue);
               center.add(board[r][c]);
            }

         speedSlider = new JSlider();
         speedSlider.setInverted(true);
         add(speedSlider, BorderLayout.SOUTH);
      }
   }

   /** Returns the number of queens to be placed on the board. **/
   public int numQueens() {
      return N;
   }

   /** Solves (or attempts to solve) the N Queens Problem. **/
   public boolean solve() {
      return isPlaced(0, 0);
   }

   /**
    * Iteratively try to place the queen in each column.
    * Recursively try the next row.
    **/

   private boolean isPlaced(int row, int col) {
      if (row == N)
         return true;
      if (col < N) {
         if (locationIsOK(row, col)) {
            addQueen(row, col);
            if (isPlaced(row + 1, 0))
               return true;
            removeQueen(row, col);
         }
         return isPlaced(row, col + 1);
      }
      return false;
   }

   /**
    * Verify that another queen can't attack this location.
    * You only need to check the locations above this row.
    * Iteration is fine here.
    **/
   private boolean locationIsOK(int r, int c) {
      if (r == 0 && c == 0) {
         return true;
      }

      for (int row = r - 1; row >= 0; row--) { // vertical
         if (board[row][c].getBackground() == Color.RED) {
            return false;
         }
      }

      for (int col = c - 1; col >= 0; col--) { // horizontal
         if (board[r][col].getBackground() == Color.RED) {
            return false;
         }
      }

      int i = 0;
      while (r - i >= 0 && c - i >= 0) { // top left
         if (board[r - i][c - i].getBackground() == Color.RED) {
            return false;
         }
         i++;
      }

      i = 0;
      while (r - i >= 0 && c + i < N) { // top right
         if (board[r - i][c + i].getBackground() == Color.RED) {
            return false;
         }
         i++;
      }

      i = 0;
      while (r + i < N && c - i >= 0) { // bottom left
         if (board[r + i][c - i].getBackground() == Color.RED) {
            return false;
         }
         i++;
      }

      i = 0;
      while (r + i < N && c + i < N) { // bottom right
         if (board[r + i][c + i].getBackground() == Color.RED) {
            return false;
         }
         i++;
      }

      return true;
   }

   /**
    * Adds a queen to the specified location.
    **/
   private void addQueen(int r, int c) {
      board[r][c].setBackground(Color.RED);
      pause();
   }

   /**
    * Removes a queen from the specified location.
    **/
   private void removeQueen(int r, int c) {
      board[r][c].setBackground(Color.BLUE);
      pause();
   }

   private void pause() {
      int timerDelay = speedSlider.getValue();
      for (int i = 1; i <= timerDelay * 1E7; i++) {
      }
   }
}