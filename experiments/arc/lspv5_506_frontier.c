/* LSPV-5/506: exact layered recomputation-pebbling frontier (same model as
 * lspv5_506_recompute_frontier.py; that file is the readable spec and the
 * Python small-case cross-check). Input on stdin: n cap wmax obj(0=slot,1=byte)
 * then per node: size k p1..pk. Output: JSON lines per w reaching the sink. */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
typedef uint64_t u64;
typedef struct { u64 m; int c0, c1, prev, j; } E;
static int n, cap, wmax, obj, sz[64], np_[64], par[64][2]; static u64 pm[64];
#define HB 20
#define HS (1u<<HB)
typedef struct { E *e; int len, mx; int *h; } L;
static int find(L *l, u64 m) { unsigned x = (unsigned)((m * 0x9E3779B97F4A7C15ull) >> (64 - HB));
  while (l->h[x] >= 0 && l->e[l->h[x]].m != m) x = (x + 1) & (HS - 1); return x; }
static int bytes(u64 m){int s=0;for(int i=0;i<n;i++)if(m>>i&1)s+=sz[i];return s;}
int main(void){
  if(scanf("%d %d %d %d",&n,&cap,&wmax,&obj)!=4)return 2;
  for(int i=0;i<n;i++){scanf("%d %d",&sz[i],&np_[i]);pm[i]=0;for(int k=0;k<np_[i];k++){scanf("%d",&par[i][k]);pm[i]|=1ull<<par[i][k];}}
  L *Ls=calloc(wmax+1,sizeof(L));
  for(int w=0;w<=wmax;w++){Ls[w].mx=1<<16;Ls[w].e=malloc(sizeof(E)*Ls[w].mx);Ls[w].h=malloc(sizeof(int)*HS);memset(Ls[w].h,-1,sizeof(int)*HS);}
  Ls[0].e[0]=(E){0,0,0,-1,-1};Ls[0].len=1;Ls[0].h[find(&Ls[0],0)]=0;
  int sink=n-1; long trans=0;
  for(int w=1;w<=wmax;w++){
    L *a=&Ls[w-1],*b=&Ls[w];
    for(int s=0;s<a->len;s++){E cur=a->e[s];u64 S=cur.m;
      for(int j=0;j<n;j++){ if(pm[j]&~S)continue;
        u64 sub=S; for(;;){ u64 keep=sub;
          if(!(keep>>j&1)){ int peak=__builtin_popcountll(keep|pm[j])+1, ok=peak<=cap;
            if(!ok&&peak==cap+1)for(int k=0;k<np_[j];k++){int p=par[j][k];if(!(keep>>p&1)&&sz[p]>=sz[j])ok=1;}
            if(ok){ u64 post=keep|(1ull<<j); int ds=__builtin_popcountll(post),db=bytes(post);
              int c0=cur.c0+(obj?db:ds),c1=cur.c1+(obj?ds:db); trans++;
              int x=find(b,post),id=b->h[x];
              if(id<0){ if(b->len==b->mx){b->mx*=2;b->e=realloc(b->e,sizeof(E)*b->mx);} id=b->len++; b->h[x]=id; b->e[id]=(E){post,c0,c1,s,j}; }
              else if(c0<b->e[id].c0||(c0==b->e[id].c0&&c1<b->e[id].c1)){b->e[id].c0=c0;b->e[id].c1=c1;b->e[id].prev=s;b->e[id].j=j;} } }
          if(!sub)break; sub=(sub-1)&S; } } }
    int bi=-1; for(int i=0;i<b->len;i++)if(b->e[i].m>>sink&1){if(bi<0||b->e[i].c0<b->e[bi].c0||(b->e[i].c0==b->e[bi].c0&&b->e[i].c1<b->e[bi].c1))bi=i;}
    if(bi>=0){ int tr[256],rs[256]; u64 rm[256]; int k=0,id=bi; for(int ww=w;ww>=1;ww--){E e=Ls[ww].e[id];tr[k]=e.j;rm[k]=e.m;k++;id=e.prev;}
      printf("{\"w\":%d,\"states\":%d,\"primary\":%d,\"secondary\":%d,\"trace\":[",w,b->len,b->e[bi].c0,b->e[bi].c1);
      for(int i=k-1;i>=0;i--)printf("%d%s",tr[i],i?",":"");printf("],\"residents\":[");
      for(int i=k-1;i>=0;i--){printf("[");int f=1;for(int q=0;q<n;q++)if(rm[i]>>q&1){printf(f?"%d":",%d",q);f=0;}printf("]%s",i?",":"");}
      printf("]}\n"); (void)rs; }
    fprintf(stderr,"w=%d states=%d trans=%ld\n",w,b->len,trans);
  }
  return 0; }
