import java.util.Scanner;

public class zadanie6 {
    public static void main(String[] args) {


        Scanner sc = new Scanner(System.in);

        System.out.print("wprowadz liczbe sekund: ");

        double sekundy = sc.nextDouble();
        double minuty = sekundy/60;
        double godziny = minuty/60;
        double dni = sekundy/86400;


        if(sekundy>=60&&sekundy<3600) {
            System.out.println("ilosc minut to: " + minuty);
        }
        else if(sekundy>=3600&&sekundy<86400) {
            System.out.println("ilosc minut to: " + minuty+" ilosc godzin to: " + godziny);



        }
        else if (sekundy>=86400){

            System.out.println("ilosc minut to: " + minuty+" ilosc godzin to: " + godziny+"ilosc dni to: " + dni);



        }
    }
}