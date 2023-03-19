#include <stdio.h>
#include <stdlib.h>
#include <complex.h>
#include <math.h>
#include <unistd.h>
#include <malloc.h>
int main(int argc, char **argv)
{
	complex float out[1]; //kimenet
	unsigned int INC=atoi(argv[1]);
	unsigned int DEC=atoi(argv[2]);
	unsigned int OVERSAMP=atoi(argv[3]);
	unsigned int CNT=0;
	complex float summer=0+0*I;
	
	INC=INC*OVERSAMP;

	int k;
	complex float in[1];
	while(1){
		k=fread(in,sizeof(complex float),1, stdin);
		if(feof(stdin))break; 
		if(k>0) {
			CNT=CNT+INC;
			summer=summer+in[0];
			if(CNT>=DEC)
			{
				fwrite(&summer,sizeof(complex float),1,stdout);
				fflush(stdout);
				CNT=CNT%DEC;
				summer=0+0*I;
			}
		}
		else{
			usleep(100);
		}
	}

	return 0;
}
