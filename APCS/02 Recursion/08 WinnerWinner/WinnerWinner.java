// Name: J1-26-22
// Date: 10/1/22
public class WinnerWinner
{
   public static void main(String[] args)
   {
      Board b = null;
      // b = new Board(3,4,"W-S-------X-"); 
      // b.display();
      // System.out.println("Shortest path is " + b.win());  //2
      
      // b = new Board(4,3,"S-W-----X-W-"); 
      // b.display();
      // System.out.println("Shortest path is " + b.win());  //4
      
      // b = new Board(3,4,"X-WS--W-W---"); 
      // b.display();
      // System.out.println("Shortest path is " + b.win());  //7
      
      // b = new Board(3,5,"W--WW-X----SWWW"); 
      // b.display();
      // System.out.println("Shortest path is " + b.win());  //1
      
      // b = new Board(3,3,"-SW-W-W-X");     //no path exists
      // b.display();
      // System.out.println("Shortest path is " + b.win());  //-1
      
      // b = new Board(5,7,"-W------W-W-WX--S----W----W-W--W---");     //Example Board 1
      // b.display();
      // System.out.println("Shortest path is " + b.win());  //5
      
      // b = new Board(4,4,"-WX--W-W-WW-S---");     //Example Board -1
      // b.display();
      // System.out.println("Shortest path is " + b.win());  //5
  
      //what other test cases should you test?
      b = new Board(8,8,"WWWWWWWWW....W.WWW.WW..WW....W.WW.W.WW.XS.W.WW.WW......WWWWWWWWW");
      b.display();
      System.out.println("Shortest path is " + b.win());  //10
   }
}

class Board
{
   private char[][] board;  
   private int maxPath;

   public Board(int rows, int cols, String line)  
   {
      int i = 0;
      board = new char[rows][cols];
      for (int r=0; r<rows; r++) {
         for (int c=0; c<cols; c++) {
            board[r][c] = line.charAt(i);
            i++;
         }
      }
      maxPath = rows*cols;
  }

	/**	returns the length of the longest possible path in the Board   */
   public int getMaxPath()		
   {  
      return maxPath; 
   }	
   
   public void display()
   {
      if(board==null) 
         return;
      System.out.println();
      for(int a = 0; a<board.length; a++)
      {
         for(int b = 0; b<board[0].length; b++)
         {
            System.out.print(board[a][b]);
         }
         System.out.println();
      }
   }

   /**	
    *  calculates and returns the shortest path from S to X, if it exists   
    *  @param r is the row of "S"
    *  @param c is the column of "S"
    */
   public int check(int r, int c) {
      if (r >= 0 && c >= 0 && r < board.length && c < board[0].length && board[r][c] != 'W') {
         if (board[r][c] == 'X')
            return 0;
         if (board[r][c] != 'S')
            board[r][c] = 'W';
         int left = 1 + check(r, c - 1);
         int right = 1 + check(r, c + 1);
         int up = 1 + check(r - 1, c);
         int down = 1 + check(r + 1, c);
         if (board[r][c] != 'S')
             board[r][c] = '.';
         return Math.min(up, Math.min(down, Math.min(left, right)));
      }
      return maxPath;
   }

   /**	
    *  precondition:  S and X exist in board
    *  postcondition:  returns either the length of the path
    *                  from S to X, or -1, if no path exists.    
    */
   public int win()
   {
      for (int x=0; x<board.length; x++) {
         for (int y=0; y<board[0].length; y++) {
            if (board[x][y]=='S') {
               int n = check(x,y);
               if (n < maxPath) {
                  return n;
               }
               else {
                  return -1;
               }
            }
         }
      }
      return -1;
   }
}

/************************ output ************
 W-S-
 ----
 --X-
 Shortest path is 2
 
 S-W
 ---
 --X
 -W-
 Shortest path is 4
 
 X-WS
 --W-
 W---
 Shortest path is 7
 
 W--WW
 -X---
 -SWWW
 Shortest path is 1
 
 -SW
 -W-
 W-X
 Shortest path is -1
 
 -W-----
 -W-W-WX
 --S----
 W----W-
 W--W---
 Shortest path is 5
 
 -WX-
 -W-W
 -WW-
 S---
 Shortest path is -1 
 ***************************************/