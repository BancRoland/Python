#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

#define RES 10
#define PI 3.141592653

int main()
{
    FILE *out;
    FILE *head;
    FILE *coord;
    coord=fopen("coordSlice.txt","rt");
    char puffer[1024];
    int cnt=0;
    float circ[RES+1][3]={0};
    float R_0=6371000;

    float lati;
    float longi;
    float radius;
    float th0;
    float alpha;
    float edgeW;

    char fillC[100];
    char edgeC[100];
    char name[100];
    
    fgets(puffer,1024,coord);
    char* token=strtok(puffer,",");
        lati=atof(token);
        // printf("%s",token);

        token=strtok(NULL,",");
        longi=atof(token);
        // printf("%s",token);

        token=strtok(NULL,",");
        radius=atof(token);
        // printf("%s",token);

        token=strtok(NULL,",");
        th0=atof(token);
        // printf("%s",token);

        token=strtok(NULL,",");
        alpha=atof(token);
        // printf("%s",token);


        token=strtok(NULL,",");
        strcpy(fillC,token);
        // printf("%s",token);

        token=strtok(NULL,",");
        strcpy(edgeC,token);
        // printf("%s",token);

        token=strtok(NULL,",");
        edgeW=atof(token);
        // printf("%s",token);

        token=strtok(NULL,"\n");
        strcpy(name,token);
   

    float S_0=lati;
    float H_0=longi;
    float r_0=radius/cos(S_0*M_PI/180);
    float r=r_0/R_0;

    for(int i=0;i<RES+1;i++)
    {
        float th=((th0-alpha/2)/180.0*M_PI)+(float)i/RES*(alpha/180.0*M_PI);

        float H=sin(r)*sin(th);
        float S=sin(r)*cos(th)*cos(S_0*M_PI/180);

        circ[i][0]=H*180/M_PI+H_0;    //szélesség
        circ[i][1]=S*180/M_PI+S_0;    //hosszúság
        circ[i][2]=0;
    }

    
    printf("\
	<Placemark>\n\
		<name>%s</name>\n\
		<Style>\n\
			<PolyStyle>\n\
				<color>%s</color>\n\
				<outline>1</outline>\n\
			</PolyStyle>\n\
			<LineStyle>\n\
				<color>%s</color>\n\
				<width>%f</width>\n\
			</LineStyle>\n\
		</Style>\n\
		<Polygon>\n\
			<tessellate>1</tessellate>\n\
			<outerBoundaryIs>\n\
				<LinearRing>\n\
					<coordinates>\n",name,fillC,edgeC,edgeW);
                    printf("%f,%f,0\n",longi,lati);
                    for(int k=0;k<RES+1;k++)
                    {
                        printf("%f,%f,%f\n",circ[k][0],circ[k][1],circ[k][2]);
                    }
                    printf("%f,%f,0\n",longi,lati);
                    printf("</coordinates>\n\
				</LinearRing>\n\
			</outerBoundaryIs>\n\
		</Polygon>\n\
	</Placemark>\n\n");

    fclose(coord);
    return 0;
}
