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
	double radiusIN;
    double radiusOUT;
    char name[30];
    char fillC[30];
}line;

int main()
{
    FILE *out;
    FILE *coord;
    coord=fopen("coordRing.txt","rt");

    char puffer[1024];
    line myline[100];
    int cnt=0;
    float circ[2][RES+1][3]={0};
    float R_0=6371000;
    

    while(fgets(puffer,1024,coord))
    {
        char* token=strtok(puffer,",");
            myline[cnt].lati=atof(token);

            token=strtok(NULL,",");
            myline[cnt].longi=atof(token);


            token=strtok(NULL,",");
            myline[cnt].radiusIN=atof(token);

            
            token=strtok(NULL,",");
            myline[cnt].radiusOUT=atof(token);
            
            token=strtok(NULL,",");
            strcpy(myline[cnt].fillC,token);

            token=strtok(NULL,"\n");
            strcpy(myline[cnt].name,token);

         cnt++;
    }

    for(int j=0;j<cnt;j++)
    {
    float S_0=myline[j].lati;
    float H_0=myline[j].longi;
    float r_0_IN=myline[j].radiusIN/cos(S_0*M_PI/180);
    float r_0_OUT=myline[j].radiusOUT/cos(S_0*M_PI/180);

    float r_IN=r_0_IN/R_0;
    float r_OUT=r_0_OUT/R_0;
    float r[2]={r_IN,r_OUT};

    for(int k=0;k<2;k++)
    {
        for(int i=0;i<RES+1;i++)
        {
            float th=(float)i/RES*2.0*M_PI;


            float H=sin(r[k])*sin(th);
            float S=sin(r[k])*cos(th)*cos(S_0*M_PI/180);

            circ[k][i][0]=H*180/M_PI+H_0;    //szélesség
            circ[k][i][1]=S*180/M_PI+S_0;    //hosszúság
            circ[k][i][2]=0;
        }
    }

    
    printf(\
	"<Placemark>\n\
        <name>%s</name>\n\
		<Style>\n\
			<PolyStyle>\n\
				<color>%s</color>\n\
				<outline>1</outline>\n\
			</PolyStyle>\n\
			<LineStyle>\n\
				<color>ff000000</color>\n\
				<width>3</width>\n\
			</LineStyle>\n\
		</Style>\n\
		<Polygon>\n\
			<tessellate>1</tessellate>\n\
			<outerBoundaryIs>\n\
				<LinearRing>\n\
					<coordinates>\n",myline[j].name,myline[j].fillC);
                    for(int k=0;k<RES+1;k++)
                    {
                        printf("%f,%f,%f\n",circ[1][k][0],circ[1][k][1],circ[1][k][2]);
                    }
                    printf("</coordinates>\n\
				</LinearRing>\n\
			</outerBoundaryIs>\n\
            <innerBoundaryIs>\n\
				<LinearRing>\n\
					<coordinates>\n");
                    for(int k=0;k<RES+1;k++)
                    {
                        printf("%f,%f,%f\n",circ[0][k][0],circ[0][k][1],circ[0][k][2]);
                    }
                    printf("</coordinates>\n\
				</LinearRing>\n\
			</innerBoundaryIs>\n\
		</Polygon>\n\
	</Placemark>\n\n");
    }

    fclose(coord);
    return 0;
}
