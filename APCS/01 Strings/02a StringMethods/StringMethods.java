// Name: J1-26-22
// Date: 8/25/22

public class StringMethods {
   public static void main(String[] args) {

      String s = "Internet", s2 = "net", s3 = "   Inter net ";


      String s7 = s.substring(5); // net
      String s8 = s.substring(0, 5); // Inter
      String s9 = s.substring(2, 6); // terne

      int pos11 = s.indexOf('e'); // 3
      int pos12 = s.indexOf('x'); // -1
      int pos13 = s.indexOf('e', 4); // 6
      int pos14 = s.lastIndexOf('e'); // 6
      int pos15 = s.lastIndexOf('e', 4); // 3
      int pos16 = s.lastIndexOf('e', 2); // -1
      int pos17 = s.indexOf(s2); // 5
      int pos18 = s.indexOf(s2, 6); // -1
      int pos19 = s.lastIndexOf(s2); // 5
      int pos20 = s.lastIndexOf(s2, 6); // 5

      boolean isSame22 = s.equals(s2); // false
      boolean isSame23 = s.equalsIgnoreCase("internet"); // true
      int result24 = s.compareTo("internet");// < 0
      int result25 = s2.compareTo(s); // > 0
      int result26 = s.compareToIgnoreCase("internet"); // 0
      String s28 = s.toUpperCase(); // INTERNET
      String s29 = s.replace("n", ""); // INTERET
      String s30 = s3.trim(); // Inter net
      // String methods never change the String object for which they are
      // called. They build and return a new string instead. For example,
      // s3.replace('a','A') by itself is useless, because s3 remains unchanged.
      // The technical term is "immutable," as in "Strings are immutable."

      char ch = s.charAt(0); // I
      boolean isSame36 = (ch == 'I'); // true
      boolean isLetter37 = Character.isLetter(ch); // true
      boolean isCap38 = Character.isUpperCase(ch); // true
      char ch39 = Character.toLowerCase(ch); // i
      String s40 = ch39 + s.substring(1); // internet

      // three ways to visit each character of a string
      // for (int i = 0; i < s.length(); i++)
      // System.out.print(s.substring(i, i + 1) + " "); // I n t e r n e t
      // for (int i = 0; i < s.length(); i++)
      // System.out.print(s.charAt(i) + " "); // I n t e r n e t
      // char[] chArray = s.toCharArray();
      // for (int i = 0; i < chArray.length; i++)
      // System.out.print(chArray[i] + " "); // I n t e r n e t
      // System.out.println();

      // Strings can be split: String[] split(String separator)
      // The method split() returns an array of substrings split around
      // the specified separator, which is then removed
      // String[] abra = "ABRACADABRA".split("A");
      // for (String str : abra)
      // System.out.print(str + " "); // BR C D BR
      // System.out.println();
      // String[] abra2 = "ABRACADABRA".split("BR");
      // for (String str : abra2)
      // System.out.print(str + " "); // A ACADA A
      // System.out.println();

      // ARE YOU SUPPOSED TO USE THIS FUNCTION????

      // for (char letter : "ABRACADABRA".toCharArray())
      // System.out.println(letter);

      // String[] words = "A sentence with lots of words".split(" ");
      // for(String str : words)
      // System.out.println(str+" "); // A
      // sentence
      // with
      // a
      // lot
      // of
      // words
      /*
       * String Methods #1
       * 1. The string dateStr represents a date in the format "mm/dd/yyyy".
       * Write a code fragment that changes dateStr to the format "dd-mm-yy".
       * For example, "09/16/2008" becomes "16-09-08".
       */
      // String dateStr = "09/16/2008";
      // String[] spl = dateStr.split("/");
      // System.out.println(spl.length);
      // dateStr = spl[1] + "-" + spl[0] + "-" + spl[2];
      // System.out.println(dateStr);
      /*
       * String Methods #2
       * 2. Given a line of text, print each word on its own line, but don't
       * print the blank lines.
       */
      // String line = "Fall Sports (football, golf, cheerleading, volleyball, field
      // hockey, cross country) start in 1 week. ";
      // for (String word : line.split(" ")) {
      // if (word.length() > 0) {
      // System.out.println(word);
      // }
      // }

      /*
       * String Methods #3
       * 3. Given a line of text, remove all punctuation from that line.
       * One way is to replace each punctuation mark with "".
       */

      // IS THE EMAIL SUPPOSED TO BE ON A NEW LINE?

      // String str = "RT @TJCheer2015: Freshman & Sophomores: Interested in cheer at
      // TJ? Email: thomasjeffersoncheer@gmail.com";
      // String punct = ",./;:'\"?<>[]{}|`~!@#$%^&*()";
      // for (int x = 0; x < punct.length(); x++) {
      // str = str.replace(punct.substring(x, x + 1), "");
      // }
      // System.out.println(str);

      /*
       * String Methods #4
       * 4. Given a line of text, remove all punctuation from that line.
       * One way is to keep all characters that are letters or a space.
       */

      // String str2 = "a @galaxy far, far away --right there! on the (TJ planetarium}
      // ceiling. https://t.co/XfoqbyA9JY";
      // String letters = " ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz";
      // String cleaned = "";

      // for (char let : str2.toCharArray()) {
      // if (letters.indexOf(let) >= 0) {
      // cleaned += let;
      // }
      // }
      // System.out.println(cleaned);
   }
}

/******************************
 * I n t e r n e t I n t e r n e t I n t e r n e t
 * BR C D BR
 * A ACADA A
 * A
 * B
 * R
 * A
 * C
 * A
 * D
 * A
 * B
 * R
 * A
 * 16-09-08
 * Fall
 * Sports
 * (football,
 * golf,
 * cheerleading,
 * volleyball,
 * field
 * hockey,
 * cross
 * country)
 * start
 * in
 * 1
 * week.
 * RT TJCheer2015 Freshman Sophomores Interested in cheer at TJ Email
 * thomasjeffersoncheergmailcom
 * a galaxy far far away right there on the TJ planetarium ceiling
 * httpstcoXfoqbyAJY
 * 
 ********************************/