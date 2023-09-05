#include <stdio.h>
#include <stdlib.h>
#include <complex.h>
#include <math.h>
#include <unistd.h>
#include <malloc.h>
int main(int argc, char **argv)
{

	if(argc==1){
		complex float out[1]; //kimenet

		// float N=atof(argv[1]);

		int k;
		complex float in[1];
		while(1){
			k=fread(in,sizeof(complex float),1, stdin);
			if(feof(stdin))break; 
			if(k>0) {

				out[0]=cabsf(in[0]);

				fwrite(out,sizeof(complex float),1,stdout);
				fflush(stdout);
			}
			else{
				usleep(100);
			}
		}
	}
	else{
		fprintf(stderr,"0 input needed [ multiplicator (float) ]\n");
		return -1;
	}

	return 0;
}
