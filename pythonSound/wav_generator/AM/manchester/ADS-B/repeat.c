#include <stdio.h>
#include <stdlib.h>
#include <complex.h>
#include <math.h>
#include <unistd.h>
#include <malloc.h>
int main(int argc, char **argv)
{
	complex float out[1]; //kimenet
	unsigned int N=atoi(argv[1]);

	int k;
	complex float in[1];
	while(1){
		k=fread(in,sizeof(complex float),1, stdin);
		if(feof(stdin))break; 
		if(k>0) {
			for(int i=0; i<N; i++)
			{
				fwrite(in,sizeof(complex float),1,stdout);
				fflush(stdout);
			}
		}
		else{
			usleep(100);
		}
	}

	return 0;
}
