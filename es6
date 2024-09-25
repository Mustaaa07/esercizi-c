#include <stdio.h>

int main() {
    int i=0,somma=0,a,b,n;
    double media=0;
    
    do{
        printf("inserisci a: ");
        scanf("%d",&a);
        printf("inserisci b: ");
        scanf("%d",&b);
        
        
    }while(b<a);
    
    do
	{
		printf("inserisci un numero\n");
		scanf("%d", &n);

		if (n >= a && n <= b)
		{
			somma = somma + n;
			i++;
		}

	} while (n >= a && n <= b);
	media = (double)somma / (double)i;

	printf("\nla media è: %f\n\n", media);

	return 0;
}
