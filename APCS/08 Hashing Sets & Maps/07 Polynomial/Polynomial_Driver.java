 /* mlbillington@fcps.edu   03.07.2011
    copied from _Study Guide to accompany Cay Horstmann's
    Java Concepts for AP Computer Science_, Frances Trees, p.416-418.
    Answer code on p. 466-468.
*/ 

import java.util.*;
public class Polynomial_Driver
{
   public static void main(String[] args)
   {
      // -4x^2 + 3x plus 5x^3 + -3x 

      Polynomial poly = new Polynomial();    
      poly.makeTerm(2, -4);        
      poly.makeTerm(1, 3);       
      System.out.println("poly:  " + poly.toString()); 
      
      System.out.println("-----------");
      Polynomial poly2 = new Polynomial();  
      poly2.makeTerm(3, 5);       
      poly2.makeTerm(1, -3);      
      System.out.println("poly2:  " +poly2.toString());
      System.out.println("-----------");
      System.out.println("Sum: " + poly.add(poly2));
      // System.out.println("Product:  " + poly.multiply(poly2));
      
      // System.out.println("-----------");
      // Polynomial poly3 = new Polynomial();   
      // poly3.makeTerm(1, 1);      // x
      // poly3.makeTerm(0, 1);      // 1
      // System.out.println("poly3:  " + poly3.toString()); // x + 1
         
      // Polynomial poly4 = new Polynomial();    
      // poly4.makeTerm(1, 1);     //  x
      // poly4.makeTerm(0, -1);    // -1
      // System.out.println("poly4:  " + poly4.toString()); //  x + -1
      // System.out.println("Sum:  " + poly4.add(poly3));   //  2x
      // System.out.println("Product:  " + poly4.multiply(poly3));   // x^2 + -1 
      // System.out.println("Product:  " + poly3.multiply(poly4));   // x^2 + -1
      
      // System.out.println("-----------");
      // Polynomial poly5 = new Polynomial();    
      // poly5.makeTerm(1, -1);     // -x
      // poly5.makeTerm(0, 1);      //  1
      // System.out.println("poly5:  " + poly5.toString());  // -x + 1
      // System.out.println("poly4:  " + poly4.toString());  //  x + -1
      // System.out.println("Sum:  " + poly4.add(poly5));    //  0
      // System.out.println("Product:  " + poly4.multiply(poly5));  // -x^2 + 2x + -1
      
      /*  extension:  constructor with a string argument  */
   //   System.out.println("-----------");
   //   Polynomial poly6 = new Polynomial("2x^3 + 4x^2 + 6x^1 + -3");
   //   System.out.println("Map:  " + poly6.getMap());  
   //   System.out.println(poly6);
   }
}


   /***************************************  
 Map:  {0=2, 1=-4, 3=2}
 poly:  2x^3 + -4x + 2
 Evaluated at 2.0: 10.0
 -----------
 Map:  {0=-3, 1=4, 4=2}
 poly2:  2x^4 + 4x + -3
 Evaluated at -10.5: 24265.125
 -----------
 Sum: 2x^4 + 2x^3 + -1
 Product:  4x^7 + -8x^5 + 12x^4 + -6x^3 + -16x^2 + 20x + -6
 -----------
 poly3:  x + 1
 poly4:  x + -1
 Sum:  2x
 Product:  x^2 + -1
 Product:  x^2 + -1
 -----------
 poly5:  -1x + 1
 poly4:  x + -1
 Sum:  0
 Product:  -x^2 + 2x + -1
 
 ********************************************/