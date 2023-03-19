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
	int cntr=0;
	complex float in[1];
	while(1){
		k=fread(in,sizeof(complex float),1, stdin);
		if(feof(stdin))break; 
		if(k>0) {
				out[0]=out[0]+in[0];
				cntr=cntr+1;
				if(cntr==N)
				{
					out[0]=out[0]/N;
					fwrite(out,sizeof(complex float),1,stdout);
					fflush(stdout);
					out[0]=0;
					cntr=0;
				}
					
		}
		else{
			usleep(100);
		}
	}

	return 0;
}
