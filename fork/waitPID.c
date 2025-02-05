/*Scrivi il codice sorgente di un prg in cui
   il processo padre P genera due figli: F1 e  F2.

   A F1 assegna un tempo t di sleep(t) (ritardo) 2 secondi;
   F1 deve restituire al padre P il numero 2.
   A F2 assegna un tempo t di sleep(t) (ritardo) 4 secondi;
   F2 deve restituire al padre P il numero 4.

   Padre P deve attendere la terminazione del figlio che dorme di piÃ¹, ossia F2, e
   deve scrivere quanti secondi ha dormito tale figlio.

   La prima cosa che ciascun processo deve fare, appena genera un processo figlio,
   Ã¨ dichiararsi nel modo seguente:
   "P: mio PID=..., mio figlio F1 ha PID=...
   La prima cosa che ciascun processo figlio deve fare appena Ã¨ stato generato,
   Ã¨ dichiararsi nel modo seguente:
   "F1: mio PID=..., mio padre P ha PID=..."

   Ogni volta che un processo visualizza qualcosa sullo schermo deve dichiararsi nel modo seguente:
   "P: quello che P deve visualizzare"
   "..."
*/

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>

int main() {
    int f1, f2;
    int status1, status2;
    
    printf("P: mio PID=%d\n", getpid());
    
    f1 = fork();
    if (f1 < 0) {
        perror("Errore generazione processo F1");
        exit(1);
    }
    
    if (f1 == 0) {
        printf("F1: mio PID=%d, mio padre P ha PID=%d\n", getpid(), getppid());
        sleep(2);
        exit(2);
    }
    
    printf("P: mio PID=%d, mio figlio F1 ha PID=%d\n", getpid(), f1);
    
    f2 = fork();
    if (f2 < 0) {
        perror("Errore generazione processo F2");
        exit(1);
    }
    
    if (f2 == 0) {
        printf("F2: mio PID=%d, mio padre P ha PID=%d\n", getpid(), getppid());
        sleep(4);
        exit(4);
    }
    
    printf("P: mio PID=%d, mio figlio F2 ha PID=%d\n", getpid(), f2);
    
    waitpid(f2, &status2, 0);
    
    if (WIFEXITED(status2)) {
        int sleepTime = WEXITSTATUS(status2);
        printf("P: il figlio che ha dormito di più ha dormito %d secondi\n", sleepTime);
    }
    
    return 0;
}
