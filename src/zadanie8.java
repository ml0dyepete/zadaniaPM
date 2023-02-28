import java.util.Scanner;


public class zadanie8 {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

    System.out.println("wprowadz ilość pakietow");

    int ilosc = sc.nextInt();


    if (ilosc>=10&&ilosc<20){

        double cena = ilosc*(99*0.8);

        System.out.println("rabat to 20% cena calkowita wynosi "+ cena);



        } else if (ilosc>=20&&ilosc<50) {

        double cena = ilosc*(99*0.7);

        System.out.println("rabat to 30% cena calkowita wynosi "+ cena);


    } else if (ilosc>=50&&ilosc<100) {

        double cena = ilosc*(99*0.6);

        System.out.println("rabat to 40% cena calkowita wynosi "+ cena);


    } else if (ilosc>=100) {

        double cena = ilosc*(99*0.5);

        System.out.println("rabat to 50% cena calkowita wynosi "+ cena);

    } else if (ilosc<10) {

        double cena = ilosc*99;

        System.out.println("rcena calkowita wynosi "+ cena);

    }


    }
    }
