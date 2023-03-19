#include <stdio.h>
#include <stdlib.h>
#include <complex.h>
#include <math.h>

int main(int argc, char **argv)
{
	complex float z[13] = {1+0*I,1+0*I,1+0*I,1+0*I,1+0*I,-1+0*I,-1+0*I,1+0*I,1+0*I,-1+0*I,1+0*I,-1+0*I,1+0*I};
	unsigned long n=8,m;

	if(argc==1){
		for(unsigned long i=0;i<13;i++){
			fwrite(z+i,sizeof(complex float),1,stdout);
		}
	}

	if(argc==3){
		n=atol(argv[1]);
		m=atol(argv[2]);
		complex float z0[1] = {0+0*I};

		for(unsigned long i=0;i<n;i++){
			fwrite(z0,sizeof(complex float),1,stdout);
		}
		for(unsigned long i=0;i<13;i++){
			fwrite(z+i,sizeof(complex float),1,stdout);
		}
		for(unsigned long i=0;i<m;i++){
			fwrite(z0,sizeof(complex float),1,stdout);
		}
	}

	if(!(argc==1 || argc==3)){
		fprintf(stderr,"2 input needed (zeros before, zeros after)\n");
		return -1;
	}


	return 0;
}
