// Name: J1-26-23
// Date: 3/13/23

import java.io.*;
import java.util.*;

public class Dictionary
{
   public static void main(String[] args) 
   {
      Scanner infile = null;
      PrintWriter outputFile = null;
      try
      {
         infile = new Scanner(new File("spanglish.txt"));
         outputFile = new PrintWriter(new FileWriter("dictionaryOutput.txt"));
      }
      catch(Exception e)
      {
         System.out.println( e );
      }
      
      Map<String, Set<String>> eng2spn = makeDictionary( infile );
      outputFile.println("ENGLISH TO SPANISH");
      outputFile.println(display(eng2spn));
   
      Map<String, Set<String>>spn2eng = reverse(eng2spn);
      outputFile.println("SPANISH TO ENGLISH");
      outputFile.println(display(spn2eng));
      outputFile.close();
      
      System.out.println("File created.");
   }
   
   public static Map<String, Set<String>> makeDictionary(Scanner infile)
   {
		Map<String, Set<String>> m = new HashMap<String, Set<String>>();
		while (infile.hasNextLine()) {
			String eng = infile.next();
			String span = infile.next();
			add(m, eng, span);
		}
		return m;
   }
   
   public static void add(Map<String, Set<String>> d, String e, String s)
   { 
	if (d.containsKey(e)) d.get(e).add(s);
	else {
		Set<String> t = new HashSet<String>();
		t.add(s);
		d.put(e, t);
	}
   }
   
   public static String display(Map<String, Set<String>> m)
   {
		String out = "";
		for (String k : m.keySet())
			out+=k+" "+m.get(k).toString()+"\n";
		return out;
   }

   
   public static Map<String, Set<String>> reverse(Map<String, Set<String>> d)
   {
		Map<String, Set<String>> m = new HashMap<String, Set<String>>();
		for (String eng : d.keySet()) {
			Set<String> spanS = d.get(eng);
			for (String span : spanS) {
				if (m.containsKey(span)) m.get(span).add(eng);
				else {
					Set<String> t = new HashSet<String>();
					t.add(eng);
					m.put(span, t);
				}
			}
		}
		return m;
   }
}


   /********************
	FILE INPUT:
   	holiday
		fiesta
		holiday
		vacaciones
		party
		fiesta
		celebration
		fiesta
     <etc.>
  *********************************** 
	FILE OUTPUT:
		ENGLISH TO SPANISH
			banana [banana]
			celebration [fiesta]
			computer [computadora, ordenador]
			double [doblar, doble, duplicar]
			father [padre]
			feast [fiesta]
			good [bueno]
			hand [mano]
			hello [hola]
			holiday [fiesta, vacaciones]
			party [fiesta]
			plaza [plaza]
			priest [padre]
			program [programa, programar]
			sleep [dormir]
			son [hijo]
			sun [sol]
			vacation [vacaciones]

		SPANISH TO ENGLISH
			banana [banana]
			bueno [good]
			computadora [computer]
			doblar [double]
			doble [double]
			dormir [sleep]
			duplicar [double]
			fiesta [celebration, feast, holiday, party]
			hijo [son]
			hola [hello]
			mano [hand]
			ordenador [computer]
			padre [father, priest]
			plaza [plaza]
			programa [program]
			programar [program]
			sol [sun]
			vacaciones [holiday, vacation]

**********************/