/*import java.util.Scanner;


public class zadanie9 {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        System.out.print("wprowadz wage przesylki(kg): ");

        double waga = sc.nextDouble();

        System.out.print("wprowadz odleglosc(km): ");

        double odleglosc = sc.nextDouble();

        double multi;
        double cena1;


        if (waga <= 1) {

             cena1 = 1.1;


        }
        if (waga > 1 && waga <= 3) {
             cena1 = 2.2;


        }
        if (waga > 3 && waga <= 5) {


             cena1 = 3.7;


        }
        if (waga > 5) {


             cena1 = 3.8;


        }


        if (odleglosc<=500){

         multi = 1;

    }else if(odleglosc>500&&odleglosc<=1000) {

         multi = 2;


    }
    else if(odleglosc>1000&&odleglosc<=1500) {

         multi = 3;


    }
    else if(odleglosc>1500&&odleglosc<=2000) {

         multi = 4;


    }
    else if(odleglosc>2000&&odleglosc<=2500) {

         multi = 5;


    }
    else if(odleglosc>2500&&odleglosc<=3000) {

         multi = 6;


    }else {

        System.out.print("maksymalna odleglosc wysylki paczki to 3000km");

    }


    double cena2=cena1*multi;
    System.out.print("cena wysylki wynosi: "+cena2);

}
    }
*/