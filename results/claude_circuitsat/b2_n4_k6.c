// Which n=4 functions have a B2 circuit of <=6 gates?  Exhaustive over circuits (negation free, complement-normalised nodes).
// Symmetry: first gate fixed to x0&x1 or x0^x1 (input perm/negation); the hit set is closed under that group afterwards (python).
// Last gate must use gate 5 (else gate 5 is dead). No order pruning (an earlier pruned version wrongly lost 64 functions).
// Usage: b2_n4_k6 first_gate(0=and,1=xor) chunk nchunks out.bin   (chunks split on the gate-2 choice index)
#include <stdio.h>
#include <stdlib.h>
#define M 0xFFFFu
static unsigned char hit[65536]; static unsigned node[10]; static int chunk,nch; static long long states=0,cnt2=0;
static inline unsigned nrm(unsigned f){return (f&1)?(f^M):f;}
static inline unsigned op(int k,unsigned a,unsigned b){switch(k){case 0:return a&b;case 1:return a&~b&M;case 2:return ~a&b&M;case 3:return ~a&~b&M;default:return a^b;}}
static void rec(int d,unsigned prev){
  int nn=4+d;
  if(d==5){ states++; unsigned g=node[nn-1];
    for(int y=0;y<nn-1;y++)for(int k=0;k<5;k++){unsigned f=op(k,g,node[y]);hit[f]=hit[f^M]=1;}
    return;}
  for(int i=0;i<nn;i++)for(int j=i+1;j<nn;j++)for(int k=0;k<5;k++){
    unsigned f=nrm(op(k,node[i],node[j])); if(f==0)continue;
    int dup=0;for(int t=0;t<nn;t++)if(node[t]==f||(node[t]^M)==f){dup=1;break;} if(dup)continue;
    /* no canonical-order pruning: it is unsound together with the "last gate uses gate 5" rule */
    if(d==1&&((cnt2++)%nch)!=chunk) continue;
    node[nn]=f; rec(d+1,f);
  }
}
int main(int c,char**v){
  int fg=atoi(v[1]);chunk=atoi(v[2]);nch=atoi(v[3]);
  for(int i=0;i<4;i++){unsigned t=0;for(int a=0;a<16;a++)if((a>>i)&1)t|=1u<<a;node[i]=t;}
  node[4]=nrm(fg?node[0]^node[1]:node[0]&node[1]);
  rec(1,node[4]);
  FILE*o=fopen(v[4],"wb");fwrite(hit,1,65536,o);fclose(o);
  printf("states %lld\n",states);return 0;}
