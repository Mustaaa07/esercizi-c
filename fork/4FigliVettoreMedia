#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>

int main(int argc, char *argv[])
{
    int f1, f2, f3, f4;
    int n1 = 0;
    int n2 = 0;

    do
    {
        n1 = rand() % 21;
        n2 = rand() % 21;
    } while (n1==n2);
    printf("Sono il padre mio PID=%d\n", getpid());
    printf("N1 ha valore= %d\nN2 ha valore= %d\n", n1, n2);
    f1 = fork();
    if(f1==0)
    {
        int dim;
        printf("Sono F1 PID= %d\n", getpid());
        int somma=0;
        do{
            printf("Inserisci la dimensione: ");
            scanf("%d", &dim);

        }while(dim<0);
        int a[dim];
        for(int i=0; i<dim; i++)
        {
            int numero= rand() %11;
            a[i]= numero;
            somma=somma+a[i];
        }
        printf("La somma è: %d", somma);
        exit(0);
        
    }
    f2 = fork();
    if(f2==0)
    {
        waitpid(f2, n1, 0);
        int n3= rand() % 7;
        return n3;
    }
    f3 = fork();
    f4 = fork();
    return 0;
}
