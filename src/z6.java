public class z6 {
    public static void main(String[] args) {


        int room1=3*4;

        int room2=3*4;

        int room3=2*3;

        int room4=2*2;
        int powCalkowita=room1+room2+room4+room3;

        int powNaOsobe1=room1/4;
        int powNaOsobe2=room2/4;
        int powNaOsobe3=room3/4;
        int powNaOsobe4=room4/4;
        int powNaOsobeCal=powCalkowita/4;


        System.out.print("powiechrznia 1 pomieszczenia: ");

        System.out.print(room1 +"\n");

        System.out.print("liczba powiechrzni na 1 osobe(przy 4 osobach): ");

        System.out.print(powNaOsobe1 +"\n");


        System.out.print("powiechrznia 2 pomieszczenia: ");
        System.out.print(room2+"\n");
        System.out.print("liczba powiechrzni na 1 osobe(przy 4 osobach): ");
        System.out.print(powNaOsobe2 +"\n");

        System.out.print("powiechrznia 3 pomieszczenia:" );
        System.out.print(room3 +"\n");
        System.out.print("liczba powiechrzni na 1 osobe(przy 4 osobach): ");
        System.out.print(powNaOsobe3 +"\n");

        System.out.print("powiechrznia 4 pomieszczenia: ");
        System.out.print(room4 +"\n");
        System.out.print("liczba powiechrzni na 1 osobe(przy 4 osobach): ");
        System.out.print(powNaOsobe4 +"\n");

        System.out.print("powiechrznia calego mieszkania: ");
        System.out.print(powCalkowita +"\n");
        System.out.print("liczba powiechrzni na 1 osobe(przy 4 osobach): ");
        System.out.print(powNaOsobeCal +"\n");




    }
}
