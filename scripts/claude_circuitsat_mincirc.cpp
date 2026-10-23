// exact min B2 circuit size by exhaustive DFS over normal gates (AND,a&~b,~a&b,OR,XOR); cost(f)=cost(~f)
#include <bits/stdc++.h>
using namespace std;
int n,K; unsigned M; vector<unsigned> v; vector<int> best; // indexed by normalized tt
unsigned mask;
void rec(int k){ // k gates placed
  int m=v.size();
  if(k==K) return;
  for(int i=0;i<m;i++)for(int j=i+1;j<m;j++){
    unsigned a=v[i],b=v[j];
    unsigned g[5]={a&b,a&~b&mask,~a&b&mask,a|b,a^b};
    for(int t=0;t<5;t++){
      unsigned f=g[t]; // normal since a,b normal
      bool dup=false; for(unsigned x:v) if(x==f){dup=true;break;}
      if(dup) continue;
      if(best[f]>k+1) best[f]=k+1;
      v.push_back(f); rec(k+1); v.pop_back();
    }
  }
}
int main(int argc,char**argv){
  n=atoi(argv[1]);K=atoi(argv[2]); M=1u<<n; mask=(M==32)?0xffffffffu:((1u<<M)-1);
  best.assign(1u<<M,99);
  for(int i=0;i<n;i++){unsigned t=0;for(unsigned x=1;x<M;x++) if((x>>i)&1) t|=1u<<x; // bit0 (x=0) is 0
    v.push_back(t); best[t]=0;}
  best[0]=0;
  rec(0);
  map<int,int> cnt; long tot=0;
  for(unsigned f=0;f<(1u<<M);f+=2){ // normal functions: bit0=0
    cnt[best[f]]++; }
  for(auto&p:cnt) printf("n=%d size<=%d%s : %d normal functions (of %u)\n",n,p.first,p.first==99?"(none found within K)":"",p.second,1u<<(M-1));
}
