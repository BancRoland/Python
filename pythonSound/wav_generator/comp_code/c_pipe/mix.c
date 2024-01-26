#include <stdio.h>
#include <stdlib.h>
#include <complex.h>
#include <math.h>
#include <unistd.h>
#include <malloc.h>
int main(int argc, char **argv)
{


	complex float* mixer;
	complex float out[1]; //kimenet
	// FILE* f;

	unsigned int N=atoi(argv[1]);
	unsigned int a=atoi(argv[2]);

	mixer=malloc(sizeof(complex float)*N);
	if(mixer==NULL){
		fprintf(stderr,"malloc error\n");
		return -3;
	}

	double p;
	for(int i=0;i<N;i++){
		// mixer[i]=cexp(I*i/N*2*M_PI);
		p=(double)(2*M_PI/N*i);
		mixer[i]=cexp(1*I*p);
		//mixer[i]=cos(p)+I*sin(p);
	}



	int i=0;
	int k;
	complex float in[1];
	while(1){
		k=fread(in,sizeof(complex float),1, stdin);
		if(feof(stdin))break; 
		if(k>0) {

			// input[i]=in[0];
			// i=(i+1)%length;
			// out[0]=0+0*I;
			// int p=i;
			// for(int j=0;j<length;j++){
			// 	out[0]+=(h[j]*input[p]);
			// 	p=(p+1)%length;
			// }

			out[0]=in[0]*mixer[i];
			i=(i+a)%N;

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
