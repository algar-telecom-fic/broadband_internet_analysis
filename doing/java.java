import java.util.Scanner;

public class java {
  public static void main(String args[]) {
    Scanner input = new Scanner(System.in);
    String s;
    while (input.hasnNextLine()) {
      s = input.nextLine();
      System.out.println(s);
    }
  }
}