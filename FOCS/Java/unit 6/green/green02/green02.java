import java.util.Scanner;
import java.util.Arrays;

public class green02 {
  public static void main(String[] args) {
    String str = "ExampleString";

    System.out.println("#1: "+str.charAt(2));
    System.out.println("#2: "+str.charAt(4));
    System.out.println("#3: "+str.length());
    System.out.println("#4: "+str.charAt(0));
    System.out.println("#5: "+str.charAt(str.length()-1));
    System.out.println("#6: "+str.charAt(str.length()-2));
    System.out.println("#7: "+str.substring(3,8));
    System.out.println("#8: "+str.substring(str.length()-5));
    System.out.println("#9: "+str.substring(3));
    System.out.println("#10: "+str.toLowerCase());
    System.out.println("#11: "+str.toUpperCase());
    char[] bruh = new char[str.length()];
    for (int x=0; x<str.length(); x++) {
      bruh[x] = str.charAt(x);
    }
    System.out.println("#12: "+Arrays.toString(bruh));
    System.out.println("#13: "+str.substring(0,str.length()-1));
    System.out.println("#14: "+str.substring(1));
    int c = 0;
    for (int x=0; x<str.length(); x++) {
      if (str.charAt(x) == 'e') c+=1;
    }
    System.out.println("#15: "+c);
    for (int x=0; x<str.length(); x++) {
      if (str.charAt(x) == 'E') c+=1;
    }
    System.out.println("#16: "+c);
    String vowels = "aeiouAEIOU";
    int v = 0;
    String vow = "";
    for (int x=0; x<str.length(); x++) {
      if (vowels.indexOf(str.charAt(x)) != -1) {
        v+=1;
        vow+=str.charAt(x);
      }
    }
    System.out.println("#17: "+v);
    System.out.println("#18: "+Arrays.toString(vow.toCharArray()));
    String other = "";
    for (int x=0; x<str.length(); x+=2) {
      other += str.charAt(x);
    }
    System.out.println("#19: "+other);
    other = "";
    for (int x=1; x<str.length(); x+=2) {
      other += str.charAt(x);
    }
    System.out.println("#20: "+other);
    String[] part = new String[str.length()-1];
    for (int x=0; x<str.length()-1; x++) {
      part[x] = str.substring(x,x+2);
    }
    System.out.println("#21: "+Arrays.toString(part));
    String third = "";
    for (int x=0; x<str.length(); x++) {
      if (x%3==0) third+='!';
      else third+=str.charAt(x);
    }
    System.out.println("#22: "+third);
    third = "";
    for (int x=0; x<str.length(); x++) {
      if (x%3==2) third+='!';
      else third+=str.charAt(x);
    }
    System.out.println("#23: "+third);
  }
}
