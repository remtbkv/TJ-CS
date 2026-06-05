public class TJStudent {
  // Fields
  private String name;
  private String year;
  private int age;

  // Constructors
  public TJStudent() {
    name = "TJ Student";
    year = "Freshman";
    age = 14;
  }

  public TJStudent(String called, String grade, int old) {
    name = called;

    if (grade.equals("Freshman") || grade.equals("Sophomore") || grade.equals("Junior") || grade.equals("Senior")) year = grade;
    else {
      System.out.println("Error: "+grade+" is not a valid year.");
      year = "Freshman";
    }

    if (10<old && old<20) age = old;
    else {
      System.out.println("Error: "+old+" is not a valid age.");
      age = 14;
    }
  }

  // Accessor & modifier instance methods
  public void setName(String called) {
    name = called;
  }

  public void setYear(String grade) {
    if (grade.equals("Freshman") || grade.equals("Sophomore") || grade.equals("Junior") || grade.equals("Senior")) year = grade;
    else System.out.println("Error: "+grade+" is not a valid year.");
  }

  public void setAge(int old) {
    if (10<old && old<20) age = old;
    else System.out.println("Error: "+old+" is not a valid age.");
  }

  public boolean sameYear(TJStudent grade) {
    return year.equals(grade.getYear());
  }

  public boolean sameAge(TJStudent old) {
    return age == old.getAge();
  }

  public int getAge() {
    return age;
  }

  public String getYear() {
    return year;
  }

  public String getName() {
    return name;
  }

  public void summarize() {
    System.out.println(name+" is a "+age+"-year-old "+year+".");
  }
}
