/* produced by Nobuki Ozawa ver. 1.00  23/10/2020  
   Prepare dump file for initial structures  */
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#define BUF 256
#define header1 "ni.dump."
#define header2 "ysz28A.dump."
#define ATOM 50000
#define interval 5.0

int total;
int pnum[2]={1,1}; // Number of dump files for Ni and metal oxide
//int pratio[2]={515,1100}; //Ratio of Ni and metal oxide
int pratio[2]={505,1070}; //Ratio of Ni and metal oxide
double axis[3]={3600,3600,10800};
double pi;
int massnum=5;
char elementlist[5][BUF] = {
"  1   91.224\n",
"  2   88.905\n",
"  3   15.999\n",
"  4   58.693\n",
"  5   1.0080\n"};

int  read_dump (char* file, int option[ATOM][2], double array[ATOM][6]);
double get_radius (int tt, double array[ATOM][6]);
void write_check (int option[ATOM][2], double array[ATOM][6]);
void write_inputrd (int option[ATOM][2], double array[ATOM][6]);

int main(int argc,char **argv)
{
	int i,j,k,a,b,c,d,e,f,g;
	int (*atomc)[2];
	double	(*posv)[6];
	double	r,dx,dy,dz,l,l0,l1,ramda[3];
	double	x0,y0,z0,x1,y1,z1,x2,y2,z2,x3,y3,z3;
	
	double	(*pos1v)[ATOM][6],(*pos2v)[ATOM][6];
	int	(*atom1c)[ATOM][2],(*atom2c)[ATOM][2];
	double	*rmax0,*rmax1;
	int *total0,*total1;
	double	(*pori)[3];
	int	(*porik)[2];
	int ni_num, ysz_num;
	
	total0=malloc(sizeof(int)*pnum[0]);
	total1=malloc(sizeof(int)*pnum[1]);
	atom1c=(int(*)[ATOM][2])malloc(pnum[0]*ATOM*2*sizeof(int));
	atom2c=(int(*)[ATOM][2])malloc(pnum[1]*ATOM*2*sizeof(int));
	pos1v=(double(*)[ATOM][6])malloc(pnum[0]*ATOM*6*sizeof(double));
	pos2v=(double(*)[ATOM][6])malloc(pnum[1]*ATOM*6*sizeof(double));
	rmax0=malloc(sizeof(double)*pnum[0]);
	rmax1=malloc(sizeof(double)*pnum[1]);
	pori=malloc(sizeof(double)*(pratio[0]+pratio[1])*3);
	porik=malloc(sizeof(int)*(pratio[0]+pratio[1])*2);
	
	char buf1[BUF],file1[BUF],*temp;
	char command[256];
	FILE *fp1,*fp2,*fp3,*fp4;
	
	pi=4*atan(1);
	
	for (j = 0; j < pnum[0];j++){
        sprintf(file1,"%s%d",header1,j); /* Input file */ 
        total0[j]=read_dump(file1,atom1c[j],pos1v[j]);
	    rmax0[j]=get_radius(total0[j],pos1v[j]);
		printf("radius of Ni%d %lf\n",j,rmax0[j]);
/*	for (i = 0; i < total0[j];i++){
		printf("check %lf %d %d %lf %lf %lf\n",rmax0[j],i,atom1c[j][i][1],pos1v[j][i][0],pos1v[j][i][1],pos1v[j][i][2]);
	}*/
	}
	for (j = 0; j < pnum[1];j++){
	    sprintf(file1,"%s%d",header2,j);  
	    total1[j]=read_dump(file1,atom2c[j],pos2v[j]);
	    rmax1[j]=get_radius(total1[j],pos2v[j]);
		printf("radius of YSZ%d %lf\n",j,rmax1[j]);
/*	for (i = 0; i < total1[j];i++){
		printf("check %lf %d %d %lf %lf %lf\n",rmax1[j],i,atom2c[j][i][1],pos2v[j][i][0],pos2v[j][i][1],pos2v[j][i][2]);
	}*/
	}
	
	srand((unsigned int)time(NULL));
	int flag=0;
	int itr=0;
	int value=0;
	while (flag==0){
	    flag=1;
	    total=0;
		ni_num=0;
		ysz_num=0;
    	for (i = 0; i < pratio[0]+ pratio[1];i++){
    	    for (j = 0; j < 3;j++){
    	    	value=(int)(axis[j]/interval);
    	        pori[i][j]= axis[j]*(rand()%value+1)/(double)value+0.5*interval;
    	        if (i==0)pori[i][j]= axis[j]*0.5;
	        }
    		if (i%2==0){
    			if (ni_num == pratio[0]&&ysz_num<pratio[1]){
			        a=rand()%pnum[1];
			        porik[i][0]=1;
			        porik[i][1]=a;
			        total+=total1[a];
	    			ysz_num+=1;
    			}
    			if (ni_num < pratio[0]){
			        a=rand()%pnum[0];
			        porik[i][0]=0;
			        porik[i][1]=a;
			        total+=total0[a];
    				ni_num+=1;
    			}
//	        printf("%d %d %f %f %f\n",porik[i][0],porik[i][1],pori[i][0],pori[i][1],pori[i][2]);
    		}
    		if (i%2==1){
    			if (ysz_num == pratio[1]&&ni_num < pratio[0]){
			        a=rand()%pnum[0];
			        porik[i][0]=0;
			        porik[i][1]=a;
			        total+=total0[a];
    				ni_num+=1;
    			}
    			if (ysz_num < pratio[1]){
			        a=rand()%pnum[1];
			        porik[i][0]=1;
			        porik[i][1]=a;
			        total+=total1[a];
	    			ysz_num+=1;
    			}
//	        printf("%d %d %f %f %f\n",porik[i][0],porik[i][1],pori[i][0],pori[i][1],pori[i][2]);
    		}
    	}
	    for (i = 0; i < pratio[0]+pratio[1]-1;i++){
	        if (porik[i][0]==0) l0=rmax0[porik[i][1]];
	        if (porik[i][0]==1) l0=rmax1[porik[i][1]];
	        for (j = i+1; j < pratio[0]+pratio[1];j++){
	            dx=labs(pori[i][0]-pori[j][0]);
                if (dx > axis[0]*0.5) dx-=axis[0];
	            dy=labs(pori[i][1]-pori[j][1]);
                if (dy > axis[1]*0.5) dy-=axis[1];
	            dz=labs(pori[i][2]-pori[j][2]);
                if (dz > axis[2]*0.5) dz-=axis[2];
                r=sqrt(dx*dx+dy*dy+dz*dz);
                if (porik[j][0]==0) l1=rmax0[porik[j][1]];
                if (porik[j][0]==1) l1=rmax1[porik[j][1]];
                l=l0+l1;
//                printf("%d %d %.3f %.3f\n",i,j,r,l);
                if (r < l+1.0) flag=0;
	        }
	    }
	    itr++;
	    if (itr%1000==0)printf("iteration %d\n",itr);
		if (itr> 1e7) printf("iteration is over limit.\n Increase cell size\n");
		if (itr> 1e7) exit(1);
	}
	printf("ni %d %d\n",ni_num,ysz_num);
	
    atomc=malloc(sizeof(int)*total*2);
	posv=malloc(sizeof(double)*total*6);
	int cont=0;
	for (k = 0; k < pratio[0]+pratio[1];k++){
	    a=porik[k][0];
	    b=porik[k][1];
	    if (a==0) c=total0[b];
	    if (a==1) c=total1[b];
	    for (j = 0; j < 3;j++){
	        d=rand()%360;
	        ramda[j]=(double)d/180.0*pi;
	    }
	    for (i = 0; i < c;i++){
	        if (a==0) {
	            atomc[cont][0]=atom1c[b][i][0];
	            x0=pos1v[b][i][0];
	            y0=pos1v[b][i][1];
	            z0=pos1v[b][i][2];
	            posv[cont][3]=pos1v[b][i][3];
	            posv[cont][4]=pos1v[b][i][4];
	            posv[cont][5]=pos1v[b][i][5];
	        }
	        if (a==1) {
	            atomc[cont][0]=atom2c[b][i][0];
	            x0=pos2v[b][i][0];
	            y0=pos2v[b][i][1];
	            z0=pos2v[b][i][2];
	            posv[cont][3]=pos2v[b][i][3];
	            posv[cont][4]=pos2v[b][i][4];
	            posv[cont][5]=pos2v[b][i][5];
	        }

	        x1=x0*cos(ramda[0])-y0*sin(ramda[0]);
			y1=x0*sin(ramda[0])+y0*cos(ramda[0]);
			z1=z0;
	        x2=x1;
			y2=y1*cos(ramda[1])-z1*sin(ramda[1]);
			z2=y1*sin(ramda[1])+z1*cos(ramda[1]);
			y3=y2;
			z3=z2*cos(ramda[1])-x2*sin(ramda[1]);
			x3=z2*sin(ramda[1])+x2*cos(ramda[1]);
			posv[cont][0]=x3+pori[k][0];
			posv[cont][1]=y3+pori[k][1];
			posv[cont][2]=z3+pori[k][2];
	        for (j = 0; j < 3;j++){
	            if (posv[cont][j]>axis[j])posv[cont][j]-=axis[j];
	            if (posv[cont][j]<0)posv[cont][j]+=axis[j];
	        }
//	        printf("%d %d %.3f %.3f %.3f\n",cont+1,atomc[cont],posv[cont][0],posv[cont][1],posv[cont][2]);
	        cont++;
	    }
	}
	write_check(atomc,posv);
	write_inputrd(atomc,posv);
	
}

int read_dump (char* file, int option[ATOM][2], double arr[ATOM][6]) {
	int i, j, k, a, b, c;
    double maxis[3],daxis[3],laxis[3];
    double x,y,z,vx,vy,vz;
    FILE *fp;
    char buf[BUF];
        
    fp = fopen(file,"r");/*rd file*/
    if( fp==NULL ){
   	    printf("Error : These is no %s !! This process will stop.\n",file);
        fclose(fp);
        exit(1);
    }
    for (i = 0; i < 4;i++){fgets( buf, BUF, fp );}
    sscanf( buf, "%d",&a);
    fgets( buf, BUF, fp );
    for (i = 0; i < 3;i++){
        fgets( buf, BUF, fp );
        sscanf( buf, "%lf %lf",&daxis[i], &maxis[i]);
        laxis[i]=maxis[i]-daxis[i];
    }
    fgets( buf, BUF, fp );
    for (i = 0; i < a;i++){
        fgets( buf, BUF, fp );
        sscanf( buf, "%d%d%lf%lf%lf%lf%lf%lf",&c,&b,&x,&y,&z,&vx,&vy,&vz);
        option[c-1][0]=b;
        option[c-1][1]=0;
        arr[c-1][0]=x-daxis[0];
        arr[c-1][1]=y-daxis[1];
        arr[c-1][2]=z-daxis[2];
        arr[c-1][3]=vx*100.0;
        arr[c-1][4]=vy*100.0;
        arr[c-1][5]=vz*100.0;
    }
    fclose(fp);
	return a;
}

double get_radius (int tt, double arr[ATOM][6]) {
    int i, j, k, a, b, c;
    double center[3];
    double dd[3],r,rmax=0.0;
	
	for (i = 0; i < 3;i++){center[i]=0.0;}
	for (i = 0; i < tt;i++){
		for (j = 0; j < 3;j++){center[j]+=arr[i][j]/(double)tt;}
	}
	for (i = 0; i < tt;i++){
		for (j = 0; j < 3;j++){
			dd[j]=arr[i][j]-center[j];
			arr[i][j]=dd[j];
			r=dd[j]*dd[j];
		}
		r=sqrt(r);
		if (r > rmax) rmax=r;
	}
	return rmax;
}

void write_check (int option[ATOM][2], double arr[ATOM][6]) {
    int i, j, k, a, b, c;
    FILE *fp;
    fp = fopen("dump.check","w");
    
    fprintf(fp,"ITEM: TIMESTEP\n0\nITEM: NUMBER OF ATOMS\n");
	fprintf(fp,"%d\n",total);
	fprintf(fp,"ITEM: BOX BOUNDS pp pp pp\n");
	for(j = 0; j < 3;j++){fprintf(fp,"0.000 %.3f\n",axis[j]);}
	fprintf(fp,"ITEM: ATOMS id type x y z\n");
    for (i = 0; i < total;i++){
	    fprintf(fp,"%d %2d",i+1,option[i][0]);
	    fprintf(fp," %.3f %.3f %.3f\n",arr[i][0],arr[i][1],arr[i][2]);
	}
    fclose(fp);
}

void write_inputrd (int option[ATOM][2], double arr[ATOM][6]) {
    int i, j, k, a, b, c;
    FILE *fp;
    fp = fopen("input.rd","w");
    
	fprintf(fp,"#cellx  0.000  %7.6lf\n",axis[0]);
	fprintf(fp,"#celly  0.000  %7.6lf\n",axis[1]);
	fprintf(fp,"#cellz  0.000  %7.6lf\n",axis[2]);
	fprintf(fp,"\n#masses %d\n",massnum);
	for (i = 0; i < massnum;i++){fprintf(fp,"%s",elementlist[i]);}
	fprintf(fp,"\n#atoms %d\n",total);
    for (i = 0; i < total;i++){
    	for (j = 0; j < 3;j++){
    		if (arr[i][j]<0) arr[i][j]+=axis[j];
    		if (arr[i][j]>=axis[j]) arr[i][j]-=axis[j];
    	}
        fprintf(fp,"%8d  %d   0",i+1,option[i][0]);
        fprintf(fp,"   %7.3lf   %7.3lf   %7.3lf",arr[i][0],arr[i][1],arr[i][2]);
        fprintf(fp,"   %7.3lf   %7.3lf   %7.3lf\n",arr[i][3],arr[i][4],arr[i][5]);
	}
    fclose(fp);
}
