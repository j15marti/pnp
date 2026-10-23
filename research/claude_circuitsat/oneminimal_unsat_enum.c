// count/exist 1-minimal UNSAT AND/OR circuits (fan-in 2, literals as leaves) with n vars, g gates, all vars used
#include <stdio.h>
#include <stdlib.h>
int n,g,L,A; unsigned full;
int sa[16],sb[16],so[16]; unsigned tt[40]; long long found=0,cnt_unsat=0; int shown=0;
unsigned eval(int ovA,int ovB){ // override wire index w: gate k wire a=2k,b=2k+1 set to 1 (full); -1 none
  unsigned v[40]; for(int i=0;i<L;i++)v[i]=tt[i];
  for(int k=0;k<g;k++){unsigned x=v[sa[k]],y=v[sb[k]]; if(ovA==2*k)x=full; if(ovA==2*k+1)y=full; v[L+k]=so[k]?(x|y):(x&y);}
  return v[L+g-1];}
void rec(int k){
  if(k==g){
    if(tt[L+g-1]!=0)return; cnt_unsat++;
    int used[40]={0}; for(int i=0;i<g;i++){used[sa[i]]=1;used[sb[i]]=1;}
    for(int i=0;i<g-1;i++) if(!used[L+i])return;
    for(int v=0;v<n;v++) if(!used[2*v]&&!used[2*v+1])return;
    for(int w=0;w<2*g;w++) if(eval(w,0)==0)return;
    found++; if(shown<2){shown++; printf("  ex:"); for(int i=0;i<g;i++)printf(" [%c %d %d]",so[i]?'|':'&',sa[i],sb[i]); printf("\n");}
    return;}
  int S=L+k;
  for(int a=0;a<S;a++)for(int b=a+1;b<S;b++)for(int o=0;o<2;o++){
    sa[k]=a;sb[k]=b;so[k]=o; tt[L+k]=o?(tt[a]|tt[b]):(tt[a]&tt[b]); rec(k+1);}
}
int main(int c,char**v){n=atoi(v[1]);g=atoi(v[2]);L=2*n;full=(1u<<(1<<n))-1;
 for(int i=0;i<n;i++){unsigned t=0;for(int a=0;a<(1<<n);a++)if(a>>i&1)t|=1u<<a; tt[2*i]=t; tt[2*i+1]=full&~t;}
 rec(0); printf("n=%d g=%d unsat=%lld oneminimal=%lld\n",n,g,cnt_unsat,found);}
