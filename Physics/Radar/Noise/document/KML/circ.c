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
	double radius;
    char name[30];
    char fillC[30];
    char edgeC[30];
    double edgeW;
	char* colour;
}line;

int main()
{
    FILE *out;
    // FILE *head;
    FILE *coord;
    coord=fopen("coordCirc.txt","rt");
    char puffer[1024];
    line myline[100];
    int cnt=0;
    float circ[RES+1][3]={0};
    float R_0=6371000;
    

    while(fgets(puffer,1024,coord))
    {
        // printf("%s\n",puffer);

        char* token=strtok(puffer,",");
            myline[cnt].lati=atof(token);

            token=strtok(NULL,",");
            myline[cnt].longi=atof(token);

            token=strtok(NULL,",");
            myline[cnt].radius=atof(token);

            token=strtok(NULL,",");
            strcpy(myline[cnt].fillC,token);

            token=strtok(NULL,",");
            strcpy(myline[cnt].edgeC,token);

            token=strtok(NULL,",");
            myline[cnt].edgeW=atof(token);

            token=strtok(NULL,"\n");
            strcpy(myline[cnt].name,token);

         cnt++;
    }

    for(int j=0;j<cnt;j++)
    {
        float S_0=myline[j].lati;
        float H_0=myline[j].longi;
        float r_0=myline[j].radius/cos(S_0*M_PI/180);
        float r=r_0/R_0;

        for(int i=0;i<RES+1;i++)
        {
            float th=(float)i/RES*2.0*M_PI;


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
                        <coordinates>\n",myline[j].name,myline[j].fillC,myline[j].edgeC,myline[j].edgeW);
                        for(int k=0;k<RES+1;k++)
                        {
                            printf("%f,%f,%f\n",circ[k][0],circ[k][1],circ[k][2]);
                        }
                        printf("</coordinates>\n\
                    </LinearRing>\n\
                </outerBoundaryIs>\n\
            </Polygon>\n\
        </Placemark>\n\n");
    }

    fclose(coord);
    return 0;
}
