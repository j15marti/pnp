// Exact count of 4-input functions with min B2 circuit size <=K (gates counted, negation free).
// Usage: b2_n4 K ; enumerates all circuits with K gates (ops: 8 AND-type + XOR/XNOR); chunk by first gate via argv[2] (0..9 op index of gate1 pair is fixed: gate1 on inputs i,j).
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
typedef unsigned short u16;
static signed char best[65536]; static int K; static u16 node[16]; static int nn;
static void rec(int g){
  if(g==K) return;
  for(int a=0;a<nn;a++)for(int b=a+1;b<nn;b++){
    u16 x=node[a],y=node[b];
    u16 r[10]; int c=0;
    for(int m=0;m<4;m++){ u16 xa=(m&1)?~x:x, yb=(m&2)?~y:y; r[c++]=xa&yb; r[c++]=~(xa&yb);} 
    // ops: 4 input-negation combos x {AND, NAND}=8 ; plus xor, xnor
    r[8]=x^y; r[9]=~(x^y);
    for(int o=0;o<10;o++){
      u16 v=r[o]; if(best[v]>g+1||best[v]<0) best[v]=g+1;
      node[nn++]=v; rec(g+1); nn--;
    }
  }
}
int main(int argc,char**argv){
  K=atoi(argv[1]); int i0=argc>2?atoi(argv[2]):-1; // chunk: first gate pair index among inputs pairs 0..5, -1 all
  memset(best,-1,sizeof best);
  u16 in[4]={0xAAAA,0xCCCC,0xF0F0,0xFF00};
  best[0]=best[0xFFFF]=0; for(int i=0;i<4;i++){best[in[i]]=0;best[(u16)~in[i]]=0;}
  nn=0; node[nn++]=in[0];node[nn++]=in[1];node[nn++]=in[2];node[nn++]=in[3];
  // restrict first gate to chunk if requested
  if(i0<0){ rec(0);} else {
    int p=0;
    for(int a=0;a<4;a++)for(int b=a+1;b<4;b++,p++) if(p==i0){
      u16 x=in[a],y=in[b]; u16 r[10]; int c=0;
      for(int m=0;m<4;m++){u16 xa=(m&1)?~x:x,yb=(m&2)?~y:y; r[c++]=xa&yb; r[c++]=~(xa&yb);} r[8]=x^y;r[9]=~(x^y);
      for(int o=0;o<10;o++){u16 v=r[o]; if(best[v]<0||best[v]>1)best[v]=1; node[nn++]=v; rec(1); nn--;}
    }
  }
  for(int f=0;f<65536;f++) printf("%d%c",best[f],f==65535?'\n':' ');
}
