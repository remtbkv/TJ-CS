import java.util.Arrays;

public class SelectionSorter extends MeasureSorter {
    public SelectionSorter(String filename) throws Exception {
        super(filename);
    }

    public int findMinIndex(int startingIndex) {
        for (int x = startingIndex; x < measures.length; x++) {
            if (measures[x].compareTo(measures[startingIndex]) < 0) {
                startingIndex = x;
            }
        }
        return startingIndex;
    }

    public void sortMe() {
        for (int x = 0; x < measures.length - 1; x++) {
            System.out.println(Arrays.toString(measures));
            swap(x, findMinIndex(x));
        }
        System.out.println(Arrays.toString(measures));
    }
}
