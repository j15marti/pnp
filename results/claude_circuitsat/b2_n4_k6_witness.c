// Prints one 6-gate circuit computing a function whose minimum formula needs 8 leaves (7 gates): a fan-out witness for n=4.
// Usage: b2_n4_k6_witness L4.bin   (L4.bin = formula_n4.c output)
#include <stdio.h>
#include <stdlib.h>
#define M 0xFFFFu
static unsigned char L[65536]; static unsigned node[10]; static int gi[10],gj[10],gk[10]; static int done=0;
static inline unsigned op(int k,unsigned a,unsigned b){switch(k){case 0:return a&b;case 1:return a&~b&M;case 2:return ~a&b&M;case 3:return ~a&~b&M;default:return a^b;}}
static const char*N[5]={"AND","A&~B","~A&B","NOR","XOR"};
static void rec(int d){
  int nn=4+d; if(done)return;
  if(d==5){unsigned g=node[nn-1];
    for(int y=0;y<nn-1;y++)for(int k=0;k<5;k++){unsigned f=op(k,g,node[y]);
      if(L[f]==8){done=1;
        for(int t=4;t<nn;t++)printf("g%d = %s(n%d,n%d) = %04x\n",t-3,N[gk[t]],gi[t],gj[t],node[t]);
        printf("g6 = %s(g5,n%d) = %04x  (formula leaves 8)\n",N[k],y,f);
        int fo[10]={0};for(int t=4;t<nn;t++){fo[gi[t]]++;fo[gj[t]]++;}fo[nn-1]++;fo[y]++;
        for(int t=0;t<nn;t++)printf("fanout n%d = %d\n",t,fo[t]);return;}}
    return;}
  for(int i=0;i<nn;i++)for(int j=i+1;j<nn;j++)for(int k=0;k<5;k++){
    unsigned f=op(k,node[i],node[j]); if(f==0||f==M)continue; if(f&1)f^=M;
    int dup=0;for(int t=0;t<nn;t++)if(node[t]==f||(node[t]^M)==f){dup=1;break;} if(dup)continue;
    node[nn]=f;gi[nn]=i;gj[nn]=j;gk[nn]=k;rec(d+1);}
}
int main(int c,char**v){FILE*f=fopen(v[1],"rb");fread(L,1,65536,f);fclose(f);
  for(int i=0;i<4;i++){unsigned t=0;for(int a=0;a<16;a++)if((a>>i)&1)t|=1u<<a;node[i]=t;}
  for(int fg=0;fg<2&&!done;fg++){node[4]=fg?node[0]^node[1]:node[0]&node[1];if(node[4]&1)node[4]^=M;gi[4]=0;gj[4]=1;gk[4]=fg?4:0;rec(1);}
  return 0;}
