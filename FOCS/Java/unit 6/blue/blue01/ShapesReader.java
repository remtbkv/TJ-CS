import java.io.File;
import java.util.Scanner;
import java.util.Arrays;
import java.lang.String;

public class ShapesReader {
  private Shape[] shapes;

  public ShapesReader(String name) throws Exception {
    Scanner infile = new Scanner(new File(name));
    int numItems = Integer.parseInt(infile.nextLine());
    shapes = new Shape[numItems];

    for (int x=0; x<numItems; x++) {
      String[] content = infile.nextLine().strip().split(" ");
      if (content[0].equals("Triangle")) {
        shapes[x] = new Triangle(Double.parseDouble(content[1]), Double.parseDouble(content[2]), Double.parseDouble(content[3]));
      }
      else if (content[0].equals("Square")) {
        shapes[x] = new Square(Double.parseDouble(content[1]));
      }
      else if (content[0].equals("Rectangle")) {
        shapes[x] = new Rectangle(Double.parseDouble(content[1]), Double.parseDouble(content[2]));
      }
      else if (content[0].equals("Circle")) {
        shapes[x] = new Circle(Double.parseDouble(content[1]));
      }
      else {
        shapes[x] = new Parallelogram(Double.parseDouble(content[1]), Double.parseDouble(content[2]), Double.parseDouble(content[3]));
      }
    }
  }

  public void sortMe() {
    Arrays.sort(shapes);
  }

  public String toString() {
    return Arrays.toString(shapes);
  }


}
