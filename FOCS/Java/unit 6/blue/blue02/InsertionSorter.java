import java.util.Arrays;

public class InsertionSorter extends MeasureSorter {

  public InsertionSorter(String filename) throws Exception {
    super(filename);
  }

  public void sortMe() {
    int y = 0;
    for (int x=0; x<measures.length; x++) {
      y = x;
      while (y>0 && measures[y].compareTo(measures[y-1])<0) {
        swap(y, y-1);
        y--;
      }
      System.out.println(Arrays.toString(measures));
    }
  }
}
