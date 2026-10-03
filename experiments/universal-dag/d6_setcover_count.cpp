#include <bits/stdc++.h>
using namespace std;

struct Bits { uint64_t w[3]={0,0,0}; };
inline bool test(const Bits&b,int i){ return (b.w[i>>6]>>(i&63))&1ULL; }
inline void setb(Bits&b,int i){ b.w[i>>6]|=1ULL<<(i&63); }
inline int popc(const Bits&b,int words){
  int s=0; for(int i=0;i<words;i++) s+=__builtin_popcountll(b.w[i]); return s;
}

unsigned long long C[281][16];
int N,MCLAUSE,WORDS,SEL;
vector<uint64_t> cmask;
vector<vector<int>> containsA;
uint64_t FULL;
unsigned long long nodes=0;

unsigned long long rec(uint64_t cov,int k,Bits forb){
  nodes++;
  int r=SEL-k;
  if(cov==FULL){
    int avail=MCLAUSE-popc(forb,WORDS);
    if(r<0||r>avail) return 0;
    return C[avail][r];
  }
  if(r<=0) return 0;
  int unc=(1<<N)-__builtin_popcountll(cov);
  int clause_cover=1<<(N-3);
  if(unc>clause_cover*r) return 0;

  int besta=-1,bestc=INT_MAX;
  int A=1<<N;
  for(int a=0;a<A;a++) if(!((cov>>a)&1ULL)){
    int c=0;
    for(int ci:containsA[a]) if(!test(forb,ci)) c++;
    if(c<bestc){ bestc=c; besta=a; if(c==0) break; }
  }
  if(bestc==0) return 0;

  unsigned long long total=0;
  Bits running=forb;
  for(int ci:containsA[besta]){
    if(test(running,ci)) continue;
    Bits child=running;
    setb(child,ci);
    total += rec(cov|cmask[ci],k+1,child);
    setb(running,ci);
  }
  return total;
}

int main(int argc,char**argv){
  if(argc!=3){ cerr<<"usage: dn_setcover_count n m\n"; return 2; }
  N=stoi(argv[1]); SEL=stoi(argv[2]);
  MCLAUSE=8*(N*(N-1)*(N-2)/6);
  WORDS=(MCLAUSE+63)/64;
  if(N>6||WORDS>3){ cerr<<"this compact implementation supports n<=6\n"; return 2; }

  for(int n=0;n<=MCLAUSE;n++){
    C[n][0]=1;
    for(int k=1;k<=min(n,15);k++) C[n][k]=C[n-1][k-1]+C[n-1][k];
  }

  vector<array<int,3>> tri;
  for(int i=0;i<N;i++) for(int j=i+1;j<N;j++) for(int k=j+1;k<N;k++)
    tri.push_back({i,j,k});

  int A=1<<N;
  containsA.assign(A,{});
  for(auto T:tri) for(int pat=0;pat<8;pat++){
    uint64_t m=0;
    int ci=cmask.size();
    for(int a=0;a<A;a++){
      bool ok=true;
      for(int z=0;z<3;z++) if(((a>>T[z])&1)!=((pat>>z)&1)){ ok=false; break; }
      if(ok){ m|=1ULL<<a; containsA[a].push_back(ci); }
    }
    cmask.push_back(m);
  }

  FULL=(A==64)?~0ULL:((1ULL<<A)-1);
  Bits b;
  auto st=chrono::steady_clock::now();
  auto ans=rec(0,0,b);
  double sec=chrono::duration<double>(chrono::steady_clock::now()-st).count();

  cout<<"N "<<N<<" m "<<SEL<<" clauses "<<MCLAUSE
      <<" total "<<C[MCLAUSE][SEL]
      <<" unsat "<<ans
      <<" nodes "<<nodes
      <<" sec "<<sec<<"\n";
}
