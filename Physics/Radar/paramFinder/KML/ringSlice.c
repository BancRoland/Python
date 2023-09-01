#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

#define RES 10
#define PI 3.141592653

int main()
{
    FILE *out;
    FILE *coord;
    coord=fopen("coordRingSlice.txt","rt");

    char puffer[1024];
    int cnt=0;
    float circ[2][RES+1][3]={0};
    float R_0=6371000;

    float lati;
    float longi;
    float radiusIN;
    float radiusOUT;
    float th0;
    float alpha;
    // float edgeW;

    char fillC[100];
    char edgeC[100];
    char name[100];
    
    fgets(puffer,1024,coord);
        char* token=strtok(puffer,",");
            lati=atof(token);

            token=strtok(NULL,",");
            longi=atof(token);
            // printf("%s\n",token);

            token=strtok(NULL,",");
            radiusIN=atof(token);
            // printf("%s\n",token);

            token=strtok(NULL,",");
            radiusOUT=atof(token);
            // printf("%s\n",token);

            token=strtok(NULL,",");
            th0=atof(token);
            // printf("%s\n",token);

            token=strtok(NULL,",");
            alpha=atof(token);
            // printf("%s\n",token);


            token=strtok(NULL,",");
            strcpy(fillC,token);
            // printf("%s\n",token);

            token=strtok(NULL,"\n");
            strcpy(name,token);

    float S_0=lati;
    float H_0=longi;
    float r_0_IN=radiusIN/cos(S_0*M_PI/180);
    float r_0_OUT=radiusOUT/cos(S_0*M_PI/180);

    float r_IN=r_0_IN/R_0;
    float r_OUT=r_0_OUT/R_0;
    float r[2]={r_IN,r_OUT};

    for(int j=0;j<2;j++)
    {
        for(int i=0;i<RES+1;i++)
        {
            float th=((th0-alpha/2)/180.0*M_PI)+(float)i/RES*(alpha/180.0*M_PI);

            float H=sin(r[j])*sin(th);
            float S=sin(r[j])*cos(th)*cos(S_0*M_PI/180);

            circ[j][i][0]=H*180/M_PI+H_0;    //szélesség
            circ[j][i][1]=S*180/M_PI+S_0;    //hosszúság
            circ[j][i][2]=0;
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
					<coordinates>\n",name,fillC);
                    for(int k=0;k<RES+1;k++)
                    {
                        printf("%f,%f,%f\n",circ[1][k][0],circ[1][k][1],circ[1][k][2]);
                    }
                    for(int k=RES;k>=0;k--)
                    {
                        printf("%f,%f,%f\n",circ[0][k][0],circ[0][k][1],circ[0][k][2]);
                    }
                    printf("%f,%f,%f\n",circ[1][0][0],circ[1][0][1],circ[1][0][2]);
                    printf("</coordinates>\n\
				</LinearRing>\n\
			</outerBoundaryIs>\n\
		</Polygon>\n\
	</Placemark>\n\n");
    
    fclose(coord);
    return 0;
}
