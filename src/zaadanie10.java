import java.util.Scanner;

public class zaadanie10 {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);


        System.out.print("wprowadz liczbe kalorii(kcal): ");

        double kcal = sc.nextDouble();

        System.out.print("wprowadz ilosc gramow tluszczu: ");

        double gram = sc.nextDouble();


        double kcaltluszcz = gram*9;
        double procent = kcaltluszcz/kcal*100;

        if (kcaltluszcz>kcal) {


            System.out.print("wprowadzone dane są nieprawidłowe  ");


        } else  {

            System.out.print("ilość kcal pochodzących z tłuszczu: "+kcaltluszcz+" co stanowi: "+procent+"%");

        }






        if(procent<=30){

            System.out.print("produkt jest niskotluszczowy");

        }


    }
}
