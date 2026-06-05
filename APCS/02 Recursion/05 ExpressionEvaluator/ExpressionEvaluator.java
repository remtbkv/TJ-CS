// Name: J1-26-22
// Date: 9/29/22

import java.util.*;

/**
 * This program calculates the value of an expression
 * consisting of numbers, arithmetic operators, and parentheses.
 */
public class ExpressionEvaluator {
   public static void main(String[] args) {
      Scanner in = new Scanner(System.in);
      System.out.print("Enter an expression: ");
      String input = in.nextLine().trim();
      Evaluator e = new Evaluator(input);
      // int value = e.getExpressionValue();
      int value = e.getExpressionValueEXT();
      System.out.println(input + " = " + value);
   }
}

/**
 * A class that can compute the value of an arithmetic expression.
 */
class Evaluator {
   private ExpressionTokenizer tokenizer;

   /**
    * Constructs an evaluator.
    * 
    * @param anExpression a string containing the expression
    *                     to be evaluated
    */
   public Evaluator(String anExpression) {
      tokenizer = new ExpressionTokenizer(anExpression);

   }

   /**
    * Evaluates the expression.
    * 
    * @return the value of the expression.
    */
   public int getExpressionValue() {
      int term;
      if (tokenizer.peekToken().equals("-")) {
         tokenizer.nextToken();
         term = -getTermValue();
      } else {
         term = getTermValue();
      }
      if (tokenizer.peekToken() != null) {
         if (tokenizer.peekToken().equals("+")) {
            tokenizer.nextToken();
            if (tokenizer.peekToken().equals("-")) {
               tokenizer.nextToken();
               return term - getExpressionValue();
            }
            return term + getExpressionValue();
         } else if (tokenizer.peekToken().equals("-")) {
            tokenizer.nextToken();
            if (tokenizer.peekToken().equals("-")) {
               tokenizer.nextToken();
               return term + getExpressionValue();
            }
            return term - getExpressionValue();
         }
      }
      return term;
   }

   /**
    * Evaluates the next term found in the expression.
    * 
    * @return the value of the term
    */
   public int getTermValue() {
      int factor = getFactorValue();
      if (tokenizer.peekToken() != null) {
         if (tokenizer.peekToken().equals("*")) {
            tokenizer.nextToken();
            if (tokenizer.peekToken().equals("-")) {
               tokenizer.nextToken();
               return -factor * getTermValue();
            }
            return factor * getTermValue();
         } else if (tokenizer.peekToken().equals("/")) {
            tokenizer.nextToken();
            if (tokenizer.peekToken().equals("-")) {
               tokenizer.nextToken();
               return -factor / getTermValue();
            }
            return factor / getTermValue();
         }
      }
      return factor;
   }

   /**
    * Evaluates the next factor found in the expression.
    * 
    * @return the value of the factor
    */
   public int getFactorValue() {
      int value;
      String next = tokenizer.peekToken();
      if ("(".equals(next)) {
         tokenizer.nextToken(); // Discard "("
         value = getExpressionValue();
         tokenizer.nextToken(); // Discard ")"
      } else {
         value = Integer.parseInt(tokenizer.nextToken());
      }
      return value;
   }

   /**
    * Extension
    * 
    */
   public int getExpressionValueEXT() {
      int term;
      if (tokenizer.peekToken().equals("-")) {
         tokenizer.nextToken();
         term = -getTermValueEXT();
      } else {
         term = getTermValueEXT();
      }
      return getExpressionValueEXT(term, tokenizer.peekToken());
   }

   public int getExpressionValueEXT(int term, String nextOp) {
      if (nextOp != null && (nextOp.equals("+") || nextOp.equals("-"))) {
         int term2;
         if (tokenizer.peekToken().equals("-")) {
            tokenizer.nextToken();
            term2 = getTermValueEXT();
            if (nextOp.equals("+")) {
               term -= term2;
            } else {
               term += term2;
            }
         } else {
            term2 = getTermValueEXT();
            if (nextOp.equals("+")) {
               term += term2;
            } else {
               term -= term2;
            }
         }
         return getExpressionValueEXT(term, tokenizer.peekToken());
      }
      return term;
   }

   public int getTermValueEXT() {
      return getTermValueEXT(getFactorValueEXT(), tokenizer.peekToken());
   }

   public int getTermValueEXT(int factor, String nextOp) {
      if (nextOp != null && (nextOp.equals("*") || nextOp.equals("/"))) {
         int factor2;
         if (tokenizer.peekToken().equals("-")) {
            tokenizer.nextToken();
            factor2 = getFactorValueEXT();
            if (nextOp.equals("*")) {
               factor *= -factor2;
            } else {
               factor /= -factor2;
            }
         } else {
            factor2 = getFactorValueEXT();
            if (nextOp.equals("*")) {
               factor *= factor2;
            } else {
               factor /= factor2;
            }
         }
         return getTermValueEXT(factor, tokenizer.peekToken());
      }
      return factor;
   }

   public int getFactorValueEXT() {
      int value;
      String next = tokenizer.peekToken();
      if ("(".equals(next)) {
         tokenizer.nextToken(); // Discard "("
         value = getExpressionValueEXT();
         tokenizer.nextToken(); // Discard ")"
      } else {
         value = Integer.parseInt(tokenizer.nextToken());
      }
      return value;
   }
}

/**
 * This class breaks up a string describing an expression
 * into tokens: numbers, parentheses, and operators.
 */
class ExpressionTokenizer {
   private String input;
   private int start; // The start of the current token
   private int end; // The position after the end of the current token

   /**
    * Constructs a tokenizer.
    * 
    * @param anInput the string to tokenize
    */
   public ExpressionTokenizer(String anInput) {
      input = anInput;
      start = 0;
      end = 0;
      nextToken(); // Find the first token
   }

   public String getter() {
      return input.substring(start, end);
   }

   /**
    * Peeks at the next token without consuming it.
    * 
    * @return the next token or null if there are no more tokens
    */
   public String peekToken() {
      if (start >= input.length()) {
         return null;
      } else {
         return input.substring(start, end);
      }
   }

   /**
    * Gets the next token and moves the tokenizer to the following token.
    * 
    * @return the next token or null if there are no more tokens
    */
   public String nextToken() {
      String r = peekToken();
      start = end;
      if (start >= input.length()) {
         return r;
      }
      if (Character.isDigit(input.charAt(start))) {
         end = start + 1;
         while (end < input.length()
               && Character.isDigit(input.charAt(end))) {
            end++;
         }
      } else {
         end = start + 1;
      }
      return r;
   }
}