// Name: J1-26-22
// Date: 10/2/22

import java.util.*;
import java.io.*;

public class MazeMaster {
   public static void main(String[] args) {
      Scanner sc = new Scanner(System.in);
      System.out.print("Enter the maze's filename (no .txt): "+'\n');
      Maze m = new Maze(sc.next() + ".txt"); // append the .txt here
      //Maze m = new Maze(); //extension
      m.display();
      System.out.println("Options: ");
      System.out.println("1: Mark all dots.");
      System.out.println("2: Mark all dots and display the number of recursive calls.");
      System.out.println("3: Mark only the correct path.");
      System.out.println("4: Mark only the correct path. If no path exists, say so.");
      System.out.println("5: Mark only the correct path and display the number of steps.\n\tIf no path exists, say so.");
      System.out.println("6: Mark only the correct path and list the steps.\n\tIf no path exists, say so.");
      System.out.print("Please make a selection: ");
      m.solve(sc.nextInt());
      m.display(); // display solved maze
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

   // constructors

   /*
    * EXTENSION
    * This is a no-arg constructor that generates a random maze
    * Do not comment it out. Do not delete it.
    */
   public Maze() {
      Random rand = new Random();
      int MIN = 2;
      int MAX = 20;
      int sizeRow = rand.nextInt(MAX + 1 - MIN) + MIN; // minimum 2x2
      int sizeCol = rand.nextInt(MAX + 1 - MIN) + MIN;
      startRow = rand.nextInt(sizeRow);
      startCol = rand.nextInt(sizeCol);
      int endRow = rand.nextInt(sizeRow);
      int endCol = rand.nextInt(sizeCol);
      while (endRow == startRow && endCol == startCol) { // different places
         endRow = rand.nextInt(sizeRow);
         endCol = rand.nextInt(sizeRow);
      }
      maze = new char[sizeRow][sizeCol];

      maze[startRow][startCol] = START;
      maze[endRow][endCol] = EXIT;
      maze[startRow][startCol] = START;
      int sRow = startRow, sCol = startCol, eRow = endRow, eCol = endCol;
      while (sRow != eRow || sCol != eCol) {
         int n = rand.nextInt(2);
         if (maze[sRow][sCol] == '\0')
            maze[sRow][sCol] = DOT;
         if (eRow > sRow && n == 0)
            sRow++;
         else if (eRow < sRow && n == 0)
            sRow--;
         if (eCol > sCol && n == 1)
            sCol++;
         else if (eCol < sCol && n == 1)
            sCol--;
      }

      for (int r = 0; r < maze.length; r++) {
         for (int c = 0; c < maze[0].length; c++) {
            if (maze[r][c] == '\0') { // != START && maze[r][c] != EXIT && maze[r][c] != PATH)
               int n = rand.nextInt(2);
               if (n == 1)
                  maze[r][c] = WALL;
               else
                  maze[r][c] = DOT;
            }
         }
      }
   }

   /**
    * Constructor.
    * Creates a "deep copy" of the array.
    * We use this in Codepost.
    */
   public Maze(char[][] m) {
      maze = m;
      for (int r = 0; r < maze.length; r++) {
         for (int c = 0; c < maze[0].length; c++) {
            if (maze[r][c] == START) // location of start location
            {
               startRow = r;
               startCol = c;
            }
         }
      }
   }

   /*
    * Write this one-arg constructor.
    * the filename already has ".txt"
    * Use a try-catch block.
    * Use next(), not nextLine()
    * Search the maze and save the location of 'S'
    */
   public Maze(String filename) {
      Scanner sc = null;
      try {
         sc = new Scanner(new File(filename));
      } catch (FileNotFoundException e) {
         System.out.println(e);
         System.exit(0);
      }
      int R = sc.nextInt();
      int C = sc.nextInt();
      maze = new char[R][C];
      for (int r = 0; r < R; r++) {
         String s = sc.next();
         for (int c = 0; c < C; c++) {
            if (s.charAt(c) == START) {
               startRow = r;
               startCol = c;
            }
            maze[r][c] = s.charAt(c);
         }
      }
   }

   public char[][] getMaze() {
      return maze;
   }

   public void display() {
      if (maze == null)
         return;
      for (int a = 0; a < maze.length; a++) {
         for (int b = 0; b < maze[0].length; b++) {
            System.out.print(maze[a][b]);
         }
         System.out.println();
      }
      System.out.println();
   }

   public void solve(int n) {
      switch (n) {
         case 1:
            markAll(startRow, startCol);
            break;
         case 2:
            int count = markAllAndCountRecursions(startRow, startCol);
            System.out.println("Number of recursions = " + count);
            break;
         case 3:
         case 4:
            if (markTheCorrectPath(startRow, startCol)) {
            } else // use mazeNoPath.txt
               System.out.println("No path exists.");
            break;
         case 5:
            if (markCorrectPathAndCountSteps(startRow, startCol, 0)) {
            } else // use mazeNoPath.txt
               System.out.println("No path exists.");
            break;
         case 6:
            if (markCorrectPathAndListSteps(startRow, startCol, "")) {
               System.out.println();
            } else
               System.out.println("No path exists.");
            break;
         default:
            System.out.println("File not found");
      }
   }

   /*
    * From handout, #1.
    * Fill the maze, mark every step.
    * This is a lot like AreaFill.
    */
   public void markAll(int r, int c) {
      if (maze[r][c] != START)
         maze[r][c] = PATH;

      if (r > 0 && maze[r - 1][c] == DOT) { // up
         markAll(r - 1, c);
      }
      if (r < maze.length-1 && maze[r + 1][c] == DOT) { // down
         markAll(r + 1, c);
      }
      if (c > 0 && maze[r][c - 1] == DOT) { // left
         markAll(r, c - 1);
      }
      if (c < maze[0].length-1 && maze[r][c + 1] == DOT) { // right
         markAll(r, c + 1);
      }
   }

    /*
    * From handout, #2.
    * Fill the maze, mark and count every recursive call as you go.
    * Like AreaFill's counting without a static variable.
    */
   public int markAllAndCountRecursions(int r, int c) {
      if (r < 0 || c < 0 || r >= maze.length || c >= maze[0].length || (maze[r][c] != '.' && maze[r][c] != START))
         return 1;
      if (maze[r][c] != START)
         maze[r][c] = PATH;
      return 1 + markAllAndCountRecursions(r - 1, c) + markAllAndCountRecursions(r + 1, c)
            + markAllAndCountRecursions(r, c - 1) + markAllAndCountRecursions(r, c + 1);
   }

   /*
    * From handout, #3.
    * Solve the maze, OR the booleans, and mark the path through it with an
    * asterisk
    * Recur until you find E, then mark the path.
    */
   public boolean markTheCorrectPath(int r, int c) {
      if (r >= 0 && c >= 0 && r < maze.length && c < maze[0].length && (maze[r][c] == DOT || maze[r][c] == EXIT || maze[r][c] == START)) {
         if (maze[r][c] == EXIT)
            return true;
         maze[r][c] = TEMP;
         if (markTheCorrectPath(r - 1, c) || markTheCorrectPath(r + 1, c) || markTheCorrectPath(r, c - 1) || markTheCorrectPath(r, c + 1)) {
            maze[r][c] = PATH;
            maze[startRow][startCol] = START;
            return true;
         }
         maze[r][c] = DOT;
      }
      return false;
   }

   /*
    * 4 Mark only the correct path. If no path exists, say so.
    * Hint: the method above returns the boolean that you need.
    */

   /*
    * From handout, #5.
    * Solve the maze, mark the path, count the steps.
    * Mark only the correct path and display the number of steps.
    * If no path exists, say so.
    */
   public boolean markCorrectPathAndCountSteps(int r, int c, int count) {
      if (r >= 0 && c >= 0 && r < maze.length && c < maze[0].length && (maze[r][c] == DOT || maze[r][c] == EXIT || maze[r][c] == START)) {
         if (maze[r][c] == EXIT) {
            System.out.println("Number of steps = " + count);
            return true;
         }
         maze[r][c] = TEMP;
         if (markCorrectPathAndCountSteps(r - 1, c, count + 1) || markCorrectPathAndCountSteps(r + 1, c, count + 1) || markCorrectPathAndCountSteps(r, c - 1, count + 1) || markCorrectPathAndCountSteps(r, c + 1, count + 1)) {
            maze[r][c] = PATH;
            maze[startRow][startCol] = START;
            return true;
         }
         maze[r][c] = DOT;
      }
      return false;
   }

   public boolean markCorrectPathAndListSteps(int r, int c, String s) {
      if (r >= 0 && c >= 0 && r < maze.length && c < maze[0].length
            && (maze[r][c] == DOT || maze[r][c] == EXIT || maze[r][c] == START)) {
         if (maze[r][c] == EXIT) {
            System.out.print("Steps = " + s.substring(0, s.length() - 2));
            return true;
         }
         maze[r][c] = TEMP;
         if (markCorrectPathAndListSteps(r - 1, c, s + "(" + String.valueOf(r) + ", " + String.valueOf(c) + "), ")
               || markCorrectPathAndListSteps(r + 1, c, s + "(" + String.valueOf(r) + ", " + String.valueOf(c) + "), ")
               || markCorrectPathAndListSteps(r, c - 1, s + "(" + String.valueOf(r) + ", " + String.valueOf(c) + "), ")
               || markCorrectPathAndListSteps(r, c + 1,
                     s + "(" + String.valueOf(r) + ", " + String.valueOf(c) + "), ")) {
            maze[r][c] = PATH;
            maze[startRow][startCol] = START;
            return true;
         }
         maze[r][c] = DOT;
      }
      return false;
   }
}

/*****************************************
 * 
 * ----jGRASP exec: java MazeMaster_teacher
 * Enter the maze's filename (no .txt): maze1
 * WWWWWWWW
 * W....W.W
 * WW.WW..W
 * W....W.W
 * W.W.WW.E
 * S.W.WW.W
 * WW.....W
 * WWWWWWWW
 * 
 * Options:
 * 1: Mark all dots.
 * 2: Mark all dots and display the number of recursive calls.
 * 3: Mark only the correct path.
 * 4: Mark only the correct path. If no path exists, say so.
 * 5: Mark only the correct path and display the number of steps.
 * If no path exists, say so.
 * Please make a selection: 1
 * WWWWWWWW
 * W****W*W
 * WW*WW**W
 * W****W*W
 * W*W*WW*E
 * S*W*WW*W
 * WW*****W
 * WWWWWWWW
 * 
 * 
 * ----jGRASP: operation complete.
 * 
 * ----jGRASP exec: java MazeMaster_teacher
 * Enter the maze's filename (no .txt): maze1
 * WWWWWWWW
 * W....W.W
 * WW.WW..W
 * W....W.W
 * W.W.WW.E
 * S.W.WW.W
 * WW.....W
 * WWWWWWWW
 * 
 * Options:
 * 1: Mark all dots.
 * 2: Mark all dots and display the number of recursive calls.
 * 3: Mark only the correct path.
 * 4: Mark only the correct path. If no path exists, say so.
 * 5: Mark only the correct path and display the number of steps.
 * If no path exists, say so.
 * Please make a selection: 2
 * Number of recursions = 105
 * WWWWWWWW
 * W****W*W
 * WW*WW**W
 * W****W*W
 * W*W*WW*E
 * S*W*WW*W
 * WW*****W
 * WWWWWWWW
 * 
 * 
 * ----jGRASP: operation complete.
 * 
 * ----jGRASP exec: java MazeMaster_teacher
 * Enter the maze's filename (no .txt): maze1
 * WWWWWWWW
 * W....W.W
 * WW.WW..W
 * W....W.W
 * W.W.WW.E
 * S.W.WW.W
 * WW.....W
 * WWWWWWWW
 * 
 * Options:
 * 1: Mark all dots.
 * 2: Mark all dots and display the number of recursive calls.
 * 3: Mark only the correct path.
 * 4: Mark only the correct path. If no path exists, say so.
 * 5: Mark only the correct path and display the number of steps.
 * If no path exists, say so.
 * Please make a selection: 3
 * WWWWWWWW
 * W....W.W
 * WW.WW..W
 * W***.W.W
 * W*W*WW*E
 * S*W*WW*W
 * WW.****W
 * WWWWWWWW
 * 
 * 
 * ----jGRASP: operation complete.
 * 
 * 
 * ----jGRASP exec: java MazeMaster_teacher
 * Enter the maze's filename (no .txt): mazeNoPath
 * WWWWWWWW
 * W....W.W
 * WW.WW..E
 * W..WW.WW
 * W.W.W..W
 * S.W.WW.W
 * WWW....W
 * WWWWWWWW
 * 
 * Options:
 * 1: Mark all dots.
 * 2: Mark all dots and display the number of recursive calls.
 * 3: Mark only the correct path.
 * 4: Mark only the correct path. If no path exists, say so.
 * 5: Mark only the correct path and display the number of steps.
 * If no path exists, say so.
 * Please make a selection: 4
 * No path exists.
 * WWWWWWWW
 * W....W.W
 * WW.WW..E
 * W..WW.WW
 * W.W.W..W
 * S.W.WW.W
 * WWW....W
 * WWWWWWWW
 * 
 * 
 * ----jGRASP: operation complete.
 * 
 * ----jGRASP exec: java MazeMaster_teacher
 * Enter the maze's filename (no .txt): maze1
 * WWWWWWWW
 * W....W.W
 * WW.WW..W
 * W....W.W
 * W.W.WW.E
 * S.W.WW.W
 * WW.....W
 * WWWWWWWW
 * 
 * Options:
 * 1: Mark all dots.
 * 2: Mark all dots and display the number of recursive calls.
 * 3: Mark only the correct path.
 * 4: Mark only the correct path. If no path exists, say so.
 * 5: Mark only the correct path and display the number of steps.
 * If no path exists, say so.
 * Please make a selection: 5
 * Number of steps = 14
 * WWWWWWWW
 * W....W.W
 * WW.WW..W
 * W***.W.W
 * W*W*WW*E
 * S*W*WW*W
 * WW.****W
 * WWWWWWWW
 * 
 * 
 * ----jGRASP: operation complete.
 ********************************************/