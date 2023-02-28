import java.util.Scanner;

public class zadanie5 {
    public static void main(String[] args) {

        Scanner sc = new Scanner(System.in);

        System.out.println("podaj mase obiektu: ");
        double masa = sc.nextDouble();


        double ciezar = masa*9.8;

        System.out.println("ciężar wynosi: "+ciezar+" niutonow");

if(ciezar>1000){

    System.out.println("obiekt jest za ciężki");



}else if(ciezar<10){
            System.out.println("obiekt jest za lekki");



        }


    }
    }
