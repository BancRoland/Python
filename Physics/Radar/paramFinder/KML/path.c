#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

#define RES 50
#define PI 3.141592653

typedef struct	//koordináta
{
	double longi;
	double lati;
    double alti;
}line;

int main()
{
    FILE *out;
    FILE *head;
    FILE *coord;
    coord=fopen("coordPath.txt","rt");

    char puffer[1024];
    line myline[100];
    int cnt=0;

    char NAME[1024];
    char edgeC[1024];
    float edgeW=0;
    
    fgets(puffer,1024,coord);
        char* token=strtok(puffer,",");
        strcpy(NAME,token);

        token=strtok(NULL,",");
        strcpy(edgeC,token);

        token=strtok(NULL,"\n");
        edgeW=atof(token);

    while(fgets(puffer,1024,coord))
    {
        char* token=strtok(puffer,",");
        myline[cnt].lati=atof(token);

        token=strtok(NULL,",");
        myline[cnt].longi=atof(token);

        token=strtok(NULL,"\n");
        myline[cnt].alti=atof(token);

         cnt++;
    }
    
    printf("\
	<Placemark>\n\
		<name>%s</name>\n\
		<Style>\n\
			<LineStyle>\n\
				<color>%s</color>\n\
				<width>%f</width>\n\
			</LineStyle>\n\
		</Style>\n\
		<LineString>\n\
			<tessellate>1</tessellate>\n\
                <coordinates>\n",NAME,edgeC,edgeW);
                for(int k=0;k<cnt;k++)
                {
                    printf("%f,%f,0\n",myline[k].lati,myline[k].longi);
                }
                printf("</coordinates>\n\
        </LineString>\n\
	</Placemark>\n\n");

    fclose(coord);
    return 0;
}
