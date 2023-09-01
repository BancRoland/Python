#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct	//koordináta
{
	double longi;
	double lati;
	char name[30];
	char* colour;
}line;

int main()
{
    FILE *out;
    FILE *head;
    FILE *coord;
    coord=fopen("coordTags.txt","rt");

    char puffer[1024];
    line myline[100];
    int cnt=0;

    while(fgets(puffer,1024,coord))
    {

        char* token=strtok(puffer,",");
            myline[cnt].lati=atof(token);

            token=strtok(NULL,",");
            myline[cnt].longi=atof(token);


            token=strtok(NULL,"\n");
            strcpy(myline[cnt].name,token);

         cnt++;
    }

    for(int i=0;i<cnt;i++)
    {
        printf("\
<Placemark>\n\
    <name>%s</name>\n\
    <hotSpot x=\"32\" y=\"1\" xunits=\"pixels\" yunits=\"pixels\"/>\n\
        <Style>\n\
            <IconStyle>\n\
                <color>ff0000ff</color>\n\
                <scale>1.1</scale>\n\
                <Icon>\n\
                    <href>http://maps.google.com/mapfiles/kml/paddle/wht-blank.png</href>\n\
                </Icon>\n\
                <hotSpot x=\"32\" y=\"1\" xunits=\"pixels\" yunits=\"pixels\"/>\n\
            </IconStyle>\n\
        </Style>\n\
    <description>DESCRIPTION</description>\n\
    <Point>\n\
        <coordinates>%lf,%lf</coordinates>\n\
    </Point>\n\
</Placemark>\n\n", myline[i].name, myline[i].longi, myline[i].lati);
    }

    fclose(coord);
    return 0;
}