#include <bits/stdc++.h>
using namespace std;
using U128=__uint128_t;

// D7M8-PAIR1 deterministic all-pairs witness certificate generator.
// Emits one opposite-output swap witness for every unordered pair of the
// 280 clause-presence inputs. Under the weight-eight promise, an UNSAT
// formula is an exact partition into eight 16-point falsifying subcubes;
// replacing one selected clause by any distinct absent clause makes it SAT.

struct Clause{array<int,3>T; int pat; U128 mask;};
struct W{bool set=false; int in=-1,out=-1; array<int,8> F{};};

int main(){
  const int n=7,M=280;
  vector<Clause>C; vector<vector<int>>contains(128);
  for(int a=0;a<n;a++)for(int b=a+1;b<n;b++)for(int c=b+1;c<n;c++){
    array<int,3>T={a,b,c};
    for(int pat=0;pat<8;pat++){
      U128 m=0;
      for(int x=0;x<128;x++){
        bool ok=true;
        for(int z=0;z<3;z++) if(((x>>T[z])&1)!=((pat>>z)&1)){ok=false;break;}
        if(ok)m|=(U128(1)<<x);
      }
      int ci=C.size(); C.push_back({T,pat,m});
      for(int x=0;x<128;x++) if((m>>x)&1) contains[x].push_back(ci);
    }
  }

  U128 FULL=~U128(0);
  vector<vector<W>> w(M,vector<W>(M));
  vector<int> ch; long long covers=0;

  function<void(U128)> rec=[&](U128 cov){
    if(cov==FULL){
      if(ch.size()!=8)return;
      covers++;
      array<int,8>F; bitset<M> bs;
      for(int q=0;q<8;q++){F[q]=ch[q];bs.set(ch[q]);}
      for(int i:ch) for(int j=0;j<M;j++) if(!bs.test(j)){
        int a=min(i,j),b=max(i,j);
        if(!w[a][b].set)w[a][b]={true,i,j,F};
      }
      return;
    }
    if(ch.size()>=8)return;
    U128 rem=FULL&~cov;
    int x=0; while(((rem>>x)&1)==0)x++;
    for(int ci:contains[x]) if((C[ci].mask&cov)==0){
      ch.push_back(ci); rec(cov|C[ci].mask); ch.pop_back();
    }
  };
  rec(0);

  cout<<"pair_a,pair_b,unsat_in,sat_out,f0,f1,f2,f3,f4,f5,f6,f7\n";
  int rows=0;
  for(int a=0;a<M;a++)for(int b=a+1;b<M;b++){
    auto &q=w[a][b];
    if(!q.set){cerr<<"missing pair "<<a<<" "<<b<<"\n";return 2;}
    cout<<a<<","<<b<<","<<q.in<<","<<q.out;
    for(int z:q.F)cout<<","<<z;
    cout<<"\n"; rows++;
  }
  cerr<<"covers "<<covers<<" rows "<<rows<<"\n";
}
