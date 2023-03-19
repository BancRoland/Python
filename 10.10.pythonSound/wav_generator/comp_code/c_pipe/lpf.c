#include <stdio.h>
#include <stdlib.h>
#include <complex.h>
#include <math.h>
#include <unistd.h>

int main(int argc, char **argv)
{
	if(argc==2){
		float fval=atof(argv[1]);
		complex float mem=0+0*I;
		complex float in[1]={0+0*I};
		complex float out[1]={0+0*I};
		int i;
		while(1){
			i=fread(in,sizeof(complex float),1,stdin);
				if(feof(stdin)) break;
			if(i>0){
				out[0]=(1-fval)*in[0]+fval*mem;
				fwrite(out,sizeof(complex float), 1, stdout);
				mem=out[0];
			}
			else{
				usleep(100);
			}
		}
	}
	else{
		fprintf(stderr,"input invalid, 0 parameter needed");
		return -1;
	}
return 0;
}
