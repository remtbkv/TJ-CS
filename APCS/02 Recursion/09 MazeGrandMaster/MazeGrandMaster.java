// Name: J1-26-22
// Date: 10/15/22

import java.util.*;
import java.io.*;

public class MazeGrandMaster {
   public static void main(String[] args) {
      Scanner sc = new Scanner(System.in);
      System.out.print("Enter the maze's filename (no .txt): ");
      Maze m = new Maze(sc.next() + ".txt"); // append the .txt
      m.display();
      System.out.println("Options: ");
      System.out.println("1: Length of the shortest path\n\tIf no path exists, say so.");
      System.out.println(
            "2: Length of the shortest path\n\tList the shortest path\n\tDisplay the shortest path\n\tIf no path exists, say so.");
      System.out.print("Please make a selection: ");
      m.solve(sc.nextInt());
      sc.close();
   }
}

class Maze {
   // constants
   private final char WALL = 'W';
   private final char DOT = '.';
   private final char START = 'S';
   private final char EXIT = 'E';
   private final char TEMP = 'o';
   private final char PATH = '*';

   // instance fields
   private char[][] maze;
   private int startRow, startCol;

   /**
    * Constructor.
    * Creates a "deep copy" of the array.
    * We use this in Codepost.
    */
   public Maze(char[][] m) {
      maze = m;
      for (int r = 0; r < maze.length; r++) {
         for (int c = 0; c < maze[0].length; c++) {
            if (maze[r][c] == START) // identify start
            {
               startRow = r;
               startCol = c;
            }
         }
      }
   }

   /**
    * Write this one-arg constructor.
    * Use a try-catch block.
    * Use next(), not nextLine()
    * Search the maze to find the location of 'S'
    */
   public Maze(String filename) {
      Scanner sc = null;
      try {
         sc = new Scanner(new File(filename));
      }
      catch (FileNotFoundException e) {
         System.out.println(e);
         System.exit(0);
      }
      int R = sc.nextInt();
      int C = sc.nextInt();
      maze = new char[R][C];
      for (int row = 0; row < R; row++) {
         String s = sc.next();
         for (int col = 0; col < C; col++) {
            maze[row][col] = s.charAt(col);
            if (s.charAt(col) == 'S') {
               startRow = row;
               startCol = col;
            }
         }
      }
   }

   public char[][] getMaze() {
      return maze;
   }

   public void display() {
      for (int r = 0; r < maze.length; r++) {
         for (int c = 0; c < maze[0].length; c++)
            System.out.print(maze[r][c]);
         System.out.println();
      }
   }

   public void solve(int n) {
      switch (n) {
         case 1:
            int shortestPath = findShortestLengthPath(startRow, startCol);
            if (shortestPath < 999)
               System.out.println("Shortest path is " + shortestPath);
            else
               System.out.println("No path exists.");
            display();
            break;

         case 2:
            String strShortestPath = findShortestPath(startRow, startCol);
            if (strShortestPath.length() != 0) {
               System.out.println("Shortest length path is: " + getPathLength(strShortestPath));
               System.out.println("Shortest path is: " + strShortestPath);
               markPath(strShortestPath);
               display(); // display solved maze
            } else
               System.out.println("No path exists.");
            break;
         default:
            System.out.println("File not found");
      }
   }

   /*
    * MazeGrandMaster 1
    * recur until you find E, then return the shortest path
    * returns 999 if it fails
    * precondition: Start can't match with Exit
    */
   public int findShortestLengthPath(int r, int c) {
      if (r >= 0 && c >= 0 && r < maze.length && c < maze[0].length && maze[r][c] != 'W') {
         if (maze[r][c] == 'E')
            return 0;
         if (maze[r][c] != 'S')
            maze[r][c] = 'W';
         int left = 1 + findShortestLengthPath(r, c - 1);
         int right = 1 + findShortestLengthPath(r, c + 1);
         int up = 1 + findShortestLengthPath(r - 1, c);
         int down = 1 + findShortestLengthPath(r + 1, c);
         if (maze[r][c] != 'S')
            maze[r][c] = '.';
         return Math.min(up, Math.min(down, Math.min(left, right)));
      }
      return 999;
   }

   /*
    * MazeGrandMaster 2
    * recur until you find E, then build the path with (r,c) locations
    * and the number of steps, e.g. ((5,0),10),((5,1),9),((6,1),8),((6,2),7),
    * ((6,3),6),((6,4),5),((6,5),4),((6,6),3),((5,6),2),((4,6),1),((4,7),0)
    * 
    * as you build, choose the shortest path at each step
    * returns empty String if there is no path
    * precondition: Start can't match with Exit
    */
   public String findShortestPath(int r, int c) {
      if (r >= 0 && c >= 0 && r < maze.length && c < maze[0].length && maze[r][c] != 'W') {
         if (maze[r][c] == 'E')
            return "((" + r + "," + c + "),0)";
         if (maze[r][c] != 'S')
            maze[r][c] = 'W';
         String temp = "((" + r + "," + c + "),";
         String left = findShortestPath(r, c - 1);
         String right = findShortestPath(r, c + 1);
         String up = findShortestPath(r - 1, c);
         String down = findShortestPath(r + 1, c);
         int Left = getPathLength(left);
         int Right = getPathLength(right);
         int Up = getPathLength(up);
         int Down = getPathLength(down);
         int min = 1 + Math.min(Left, Math.min(Right, Math.min(Up, Down)));
         if (maze[r][c] != 'S')
            maze[r][c] = '.';
         if (min == Left+1)
            return temp + min + ")," + left;
         if (min == Right+1)
            return temp + min + ")," + right;
         if (min == Up+1)
            return temp + min + ")," + up;
         if (min == Down+1)
            return temp + min + ")," + down;
      }
      return "";
   }

   /**
    * MazeGrandMaster 2
    * returns the length, i.e., third number when the format of the strPath is
    * "((3,4),10),((3,5),9),..."
    * returns 999 if the string is empty
    * precondition: strPath is either empty or follows the format above
    */
   public int getPathLength(String strPath) {
      if (strPath.equals(""))
         return 999;
      String[] arr = strPath.split("\\)\\,\\(");
      String s = arr[0];
      int l = s.length();
      int i = 0;
      while (!Character.isDigit(s.charAt(l-1-i)))
         i++;
      s = s.substring(0, l - i);
      l = s.length();
      i = 0;
      while (Character.isDigit(s.charAt(l - 1 - i)))
         i++;
      return Integer.parseInt(s.substring(l - i));
   }

   /**
    * MazeGrandMaster 2
    * recursive method that takes a String created by findShortestPath(r, c)
    * in the form of ((5,0),10),((5,1),9),((6,1),8),((6,2),7),
    * ((6,3),6),((6,4),5),((6,5),4),((6,6),3),((5,6),2),((4,6),1),
    * ((4,7),0) and marks the actual path in the maze
    * precondition: the String is either an empty String or one that
    * has the format shown above
    * the (r,c) must be correct for this method to work
    */
   public void markPath(String strPath) {
      if (strPath.equals(""))
         return;
      /* enter your code below */
      String[] arr = strPath.split("\\)\\,\\(");
      for (int k = 0; k < arr.length; k++) {
         String s = arr[k].substring(1);
         if (k==0) 
            s = s.substring(1);
         int i = 0;
         while (Character.isDigit(s.charAt(i)))
            i++;
         int r = Integer.parseInt(s.substring(0, i));
         s = s.substring(i+1);
         i = 0;
         while (Character.isDigit(s.charAt(i)))
            i++;
         int c = Integer.parseInt(s.substring(0, i));
         if (k == 0)
            maze[r][c] = 'S';
         else if (k == arr.length - 1)
            maze[r][c] = 'E';
         else
            maze[r][c] = '*';
      }
   }
}

/*************************************************************
 * ----jGRASP exec: java MazeGrandMaster_teacher
 * Enter the maze's filename (no .txt): maze1
 * WWWWWWWW
 * W....W.W
 * WW.W...W
 * W....W.W
 * W.W.WW.E
 * S.W.WW.W
 * W......W
 * WWWWWWWW
 * 
 * Options:
 * 1: Length of the shortest path
 * If no path exists, say so.
 * 2: Length of the shortest path
 * List the shortest path
 * Display the shortest path
 * If no path exists, say so.
 * Please make a selection: 1
 * Shortest path is 10
 * WWWWWWWW
 * W....W.W
 * WW.W...W
 * W....W.W
 * W.W.WW.E
 * S.W.WW.W
 * W......W
 * WWWWWWWW
 * 
 * 
 * ----jGRASP: operation complete.
 * 
 ******************************************************************/
/**************************************************************
 * ----jGRASP exec: java MazeGrandMaster_teacher
 * Enter the maze's filename (no .txt): maze1
 * WWWWWWWW
 * W....W.W
 * WW.W...W
 * W....W.W
 * W.W.WW.E
 * S.W.WW.W
 * W......W
 * WWWWWWWW
 * 
 * Options:
 * 1: Length of the shortest path
 * If no path exists, say so.
 * 2: Length of the shortest path
 * List the shortest path
 * Display the shortest path
 * If no path exists, say so.
 * Please make a selection: 2
 * Shortest length path is: 10
 * Shortest path is:
 * ((5,0),10),((5,1),9),((6,1),8),((6,2),7),((6,3),6),((6,4),5),((6,5),4),((6,6),3),((5,6),2),((4,6),1),((4,7),0)
 * WWWWWWWW
 * W....W.W
 * WW.W...W
 * W....W.W
 * W.W.WW*E
 * S*W.WW*W
 * W******W
 * WWWWWWWW
 * 
 * 
 * ----jGRASP: operation complete.
 * 
 ******************************************/