import java.util.Scanner;

public class zadanie11 {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);



        System.out.print("wprowadz nazwisko pierwszego biegacza: ");

        String naz1 = sc.nextLine();


        System.out.print("wprowadz czas pierwszego biegacza(min): ");
        double czas1 = sc.nextDouble();
sc.nextLine();
        System.out.print("wprowadz nazwisko drugiego biegacza: ");

        String naz2 = sc.nextLine();


        System.out.print("wprowadz czas drugiego biegacza(min): ");
        double czas2 = sc.nextDouble();
        sc.nextLine();


        System.out.print("wprowadz nazwisko trzeciego biegacza: ");

        String naz3 = sc.nextLine();

        System.out.print("wprowadz czas trzeciego biegacza(min): ");
        double czas3 = sc.nextDouble();
        sc.nextLine();


               if(czas1>czas2 && czas2>czas3){

            System.out.print("1."+naz3+" 2."+naz2+"3."+naz1);


        } else if(czas2>czas1 && czas1>czas3){

            System.out.print("1."+naz3+" 2."+naz1+"3."+naz2);


        } else if(czas3>czas1 && czas1>czas2){

            System.out.print("1."+naz2+" 2."+naz1+"3."+naz3);


        } else if(czas2>czas3 && czas3>czas1){

            System.out.print("1."+naz1+" 2."+naz3+"3."+naz2);


        }
               else if(czas1>czas3 && czas2<czas3){

                   System.out.print("1."+naz2+" 2."+naz3+"3."+naz1);


               }
               else if(czas3>czas2 && czas2>czas1){

                   System.out.print("1."+naz1+" 2."+naz2+"3."+naz3);


               }


    }
}
