 // Name: J1-26-23
 // Date: 3/18/23

import java.util.*;

interface PolynomialInterface
{
   public void makeTerm(Integer exp, Integer coef);
   public Map<Integer, Integer> getMap();
   public double evaluateAt(double x);
   
   //precondition: both polynomials are in standard form
   //postcondition: terms with zero disappear. If all terms disappear (the size is zero), 
   //               add pair (0,0).
   public Polynomial add(Polynomial other);
   
   //precondition: both polynomials are in standard form
   //postcondition: terms with zero disappear. If all terms disappear (the size is zero), 
   //               add pair (0,0)
   public Polynomial multiply(Polynomial other);
   public String toString();
}

class Polynomial implements PolynomialInterface
{
   private Map<Integer, Integer> map;
   public Polynomial(Polynomial other) {
      map = new TreeMap<Integer, Integer>();
      map.putAll(other.map);
   }
   public Polynomial() {
      map = new TreeMap<Integer, Integer>();
   }
   public Map<Integer, Integer> getMap() {
      return map;
   }
   public void makeTerm(Integer exp, Integer coef) {
      map.put(exp, coef);
   }
   public double evaluateAt(double x) {
      Double sum = 0.0;
      for (int exp : map.keySet())
         sum+=map.get(exp)*Math.pow(x, exp);
      return sum;
   }
   public Polynomial add(Polynomial o) {
      Polynomial t = new Polynomial(o);
      for (int exp : map.keySet()) {
         int coef = map.get(exp);
         if (t.map.containsKey(exp)) coef+=t.map.get(exp);
         if (coef!=0) t.map.put(exp, coef);
         else t.map.remove(exp);
      }
      if (t.map.size()==0) t.map.put(0, 0);
      return t;
   }
   public Polynomial multiply(Polynomial o) {
      Polynomial t = new Polynomial();
      for (int expL : map.keySet())
         for (int expR : o.map.keySet()) {
            int coef = map.get(expL)*o.map.get(expR);
            int exp = expL + expR;
            if (t.map.containsKey(exp)) coef+=t.map.get(exp);
            if (coef!=0) t.map.put(exp, coef);
            else t.map.remove(exp);
         }
      if (t.map.size()==0) t.map.put(0, 0);
      return t;
   }
   public String toString() {
      Stack<Integer> st = new Stack<Integer>();
      for (Integer n : map.keySet())
         st.push(n);
      String out = "";
      while (!st.isEmpty()) {
         int exp = st.pop();
         int coef = map.get(exp);
         if (coef==-1 && exp!=0) out+="-";
         else if (!(coef==1 && exp!=0)) out+=coef;
         if (exp==1) out+="x";
         if (exp>1) out+="x^"+exp;
         if (!st.isEmpty()) out+=" + ";
      }
      return out;
   }
}