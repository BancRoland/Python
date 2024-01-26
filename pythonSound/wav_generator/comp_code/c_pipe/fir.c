#include <stdio.h>
#include <stdlib.h>
#include <complex.h>
#include <math.h>
#include <unistd.h>
#include <malloc.h>

int main(int argc, char **argv)
{
	
	complex float* h; //súlyfüggvény
	complex float* input; //bemeneteket tároló tömb
	complex float out[1]; //kimenet
	unsigned int OVERSAMP=atoi(argv[2]);
	unsigned long length;
	
	FILE* f;
	f=fopen(argv[1],"r");
	if(f==NULL)
	{
		fprintf(stderr,"error file open\n");
		return -1;
	}
	fseek(f, 0, SEEK_END);
	length=ftell(f)/sizeof(complex float);
	fprintf(stderr, "%ld\n",length);
	rewind(f); //visszaviszi az elejére
	h=malloc(sizeof(complex float)*length);
	if(h==NULL)
	{
		fprintf(stderr,"malloc error\n");
		return -2;
	}
	fread(h,sizeof(complex float),length,f);
	//fwrite(h,sizeof(complex float),length,stdout);return 0;

	length=length*OVERSAMP;
	input=malloc(sizeof(complex float)*length);
	if(input==NULL){
		fprintf(stderr,"malloc error\n");
		return -3;
	}

	for(int i=0;i<length;i++)
	{
		input[i]=0+0*I;
	}

	int i=0;
	int k;
	complex float in[1];
	while(1){
		k=fread(in,sizeof(complex float),1, stdin);
		if(feof(stdin))break; 
		if(k>0) 
		{
			input[i]=in[0];
			i=(i+1)%length;
			out[0]=0+0*I;
			int p=i;
			for(int j=0;j<length;j++)
			{
				out[0]+=(h[j/OVERSAMP]*input[p]);
				p=(p+1)%length;
			}
			fwrite(out,sizeof(complex float),1,stdout);
			fflush(stdout);
		}
		else{
			usleep(100);
		}
	}

	free(h);
	free(input);
	fclose(f);
	return 0;
}
