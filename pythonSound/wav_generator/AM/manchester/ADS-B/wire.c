#include <stdio.h>
#include <stdlib.h>
#include <complex.h>
#include <math.h>
#include <unistd.h>
#include <malloc.h>
int main(int argc, char **argv)
{

	// complex float* h; //súlyfüggvény
	// complex float* input; //bemeneteket tároló tömb
	complex float* mixer;
	complex float out[1]; //kimenet
	// FILE* f;

	int k;
	complex float in[1];
	while(1){
		k=fread(in,sizeof(float),1, stdin);
		if(feof(stdin))break; 
		if(k>0) {

			out[0]=in[0];

			fwrite(out,sizeof(complex float),1,stdout);
			fflush(stdout);
		}
		else{
			usleep(100);
		}
	}

	free(mixer);
	// free(h);
	// free(input);
	// fclose(f);
	return 0;
}
