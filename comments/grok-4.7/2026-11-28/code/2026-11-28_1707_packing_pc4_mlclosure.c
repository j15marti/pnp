/* Exact degree-d multilinear F2 polynomial-calculus closure (the "full bounded multilinear
   closure" system of T3/L05-36 Sec.2), for NAE4 axioms on a 4-uniform hypergraph.
   usage: mlclosure n d enc edgefile    enc=g (grouped NAE4 p_e, deg 3) | r (raw two clauses, deg 4)
   Prints rank after every variable step, and REFUTED / FIXED_POINT. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
typedef uint64_t u64;
static int n,d,D,WD; static int *monmask; static int *deg; static int **mul;
static int idx_of(int m){ /* binary search not needed: use hash via array of size 2^n */ return 0; }
static int *maskidx;
static u64 **B; static int *piv; static int nb=0; static int *pivrow; /* pivrow[col] = row or -1 */
static inline int getb(u64*v,int c){return (v[c>>6]>>(c&63))&1;}
static inline void flip(u64*v,int c){v[c>>6]^=1ULL<<(c&63);}
static inline void xorv(u64*a,const u64*b){for(int w=0;w<WD;w++)a[w]^=b[w];}
static int iszero(u64*v){for(int w=0;w<WD;w++)if(v[w])return 0;return 1;}
static int lead(u64*v){ /* highest index set bit; monomials sorted by degree so high index = high degree */
  for(int w=WD-1;w>=0;w--) if(v[w]) return w*64+63-__builtin_clzll(v[w]); return -1;}
/* insert into W echelon (pivot = leading = highest column). returns 1 if new */
static int insertW(u64*v){
  u64*t=malloc(WD*8); memcpy(t,v,WD*8);
  for(;;){int l=lead(t); if(l<0){free(t);return 0;} if(pivrow[l]<0){B[nb]=t;piv[nb]=l;pivrow[l]=nb;nb++;return 1;} xorv(t,B[pivrow[l]]);}
}
static void mulx(int i,u64*src,u64*dst){memset(dst,0,WD*8);for(int c=0;c<D;c++) if(getb(src,c)) flip(dst,mul[i][c]);}
int main(int argc,char**argv){
  n=atoi(argv[1]); d=atoi(argv[2]); char enc=argv[3][0]; FILE*f=fopen(argv[4],"r");
  /* monomials: all subsets of size<=d, sorted by degree then lexicographic mask */
  int cap=1; maskidx=malloc(sizeof(int)<<n); for(int m=0;m<(1<<n);m++)maskidx[m]=-1;
  monmask=malloc(sizeof(int)<<n); deg=malloc(sizeof(int)<<n); D=0;
  for(int k=0;k<=d;k++) for(int m=0;m<(1<<n);m++) if(__builtin_popcount(m)==k){monmask[D]=m;deg[D]=k;maskidx[m]=D;D++;}
  WD=(D+63)/64; mul=malloc(n*sizeof(int*));
  for(int i=0;i<n;i++){mul[i]=malloc(D*sizeof(int));for(int c=0;c<D;c++){int m=monmask[c]|(1<<i);mul[i][c]=maskidx[m];}} /* -1 if deg>d */
  B=malloc(sizeof(u64*)*(D+1)); piv=malloc(sizeof(int)*(D+1)); pivrow=malloc(sizeof(int)*D); for(int c=0;c<D;c++)pivrow[c]=-1;
  int a,b,c2,e; int ne=0;
  while(fscanf(f,"%d %d %d %d",&a,&b,&c2,&e)==4){ int S[4]={a,b,c2,e}; ne++;
    /* expand prod_{j in S} x_j  and prod (1+x_j) as subset sums */
    u64*P=calloc(WD,8),*Q=calloc(WD,8);
    for(int sub=0;sub<16;sub++){int m=0,k=0;for(int j=0;j<4;j++)if(sub>>j&1){m|=1<<S[j];k++;}
      if(k<=d) flip(Q,maskidx[m]); else if(enc=='r'){fprintf(stderr,"raw needs d>=4\n");return 1;}
      if(sub==15 && k<=d) flip(P,maskidx[m]);}
    if(enc=='g'){ xorv(P,Q); insertW(P);} else {insertW(P);insertW(Q);}
    free(P);free(Q);}
  printf("n=%d d=%d enc=%c edges=%d D=%d initial_rank=%d\n",n,d,enc,ne,D,nb); fflush(stdout);
  u64*tmp=malloc(WD*8);
  for(int sweep=1;;sweep++){ int changed=0;
    for(int i=0;i<n;i++){
      /* kernel of H_i: columns c with deg==d and !(monmask has i) */
      int R=nb; u64**C=malloc(sizeof(u64*)*R); int *cp=malloc(sizeof(int)*D); for(int c=0;c<D;c++)cp[c]=-1;
      u64**K=malloc(sizeof(u64*)*R); int nk=0; int nr=0;
      for(int r=0;r<R;r++){ u64*t=malloc(WD*8); memcpy(t,B[r],WD*8);
        for(;;){ int found=-1; /* highest masked column set */
          for(int w=WD-1;w>=0&&found<0;w--){u64 x=t[w]; while(x){int c=w*64+63-__builtin_clzll(x); if(deg[c]==d && !(monmask[c]>>i&1)){found=c;break;} x&=~(1ULL<<(c&63));}}
          if(found<0){K[nk++]=t;break;}
          if(cp[found]<0){cp[found]=nr;C[nr++]=t;break;}
          xorv(t,C[cp[found]]); }
      }
      int added=0;
      for(int k=0;k<nk;k++){ mulx(i,K[k],tmp); /* mul[i][c] defined for all c in kernel support */ if(insertW(tmp)){added++;changed=1;} }
      for(int r=0;r<nr;r++)free(C[r]); for(int k=0;k<nk;k++)free(K[k]); free(C);free(K);free(cp);
      if(pivrow[0]>=0){printf("REFUTED sweep=%d var=%d rank=%d\n",sweep,i,nb);return 0;}
      if(added){printf("sweep %d var %d +%d rank %d\n",sweep,i,added,nb);fflush(stdout);}
    }
    if(!changed){printf("FIXED_POINT sweeps=%d rank=%d dual_dim=%d (1 not in W)\n",sweep,nb,D-nb);return 0;}
  }
}
