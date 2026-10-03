#include <bits/stdc++.h>
#include <omp.h>
using namespace std;
using U128=__uint128_t;

struct B{uint64_t w[8]={0};};
inline bool tst(const B&b,int i){return (b.w[i>>6]>>(i&63))&1ULL;}
inline void setb(B&b,int i){b.w[i>>6]|=1ULL<<(i&63);}
inline int popb(const B&b,int words){int s=0;for(int i=0;i<words;i++)s+=__builtin_popcountll(b.w[i]);return s;}
inline int pc(U128 x){return __builtin_popcountll((uint64_t)x)+__builtin_popcountll((uint64_t)(x>>64));}

int N,M,K,A,WORDS;
vector<U128> cm;
vector<vector<int>> ca;
vector<array<int,3>> clauseT;
vector<int> clausePat;
U128 FULL;
unsigned long long Cb[449][11];

struct R{unsigned long long count=0,nodes=0;};

R rec(U128 cov,int k,B forb){
  R out; out.nodes=1;
  int r=K-k;
  if(cov==FULL){
    int av=M-popb(forb,WORDS);
    if(r>=0&&r<=av) out.count=Cb[av][r];
    return out;
  }
  if(r<=0) return out;
  int unc=A-pc(cov);
  int setsize=1<<(N-3);
  if(unc>setsize*r) return out;

  int besta=-1,bestc=INT_MAX;
  U128 rem=FULL^cov;
  while(rem){
    uint64_t lo=(uint64_t)rem;
    int a;
    if(lo) a=__builtin_ctzll(lo);
    else a=64+__builtin_ctzll((uint64_t)(rem>>64));
    rem&=~(U128(1)<<a);
    int c=0;
    for(int ci:ca[a]) if(!tst(forb,ci)) c++;
    if(c<bestc){bestc=c;besta=a;if(!c)break;}
  }
  if(!bestc) return out;

  B run=forb;
  for(int ci:ca[besta]){
    if(tst(run,ci)) continue;
    B child=run;
    setb(child,ci);
    R z=rec(cov|cm[ci],k+1,child);
    out.count+=z.count;
    out.nodes+=z.nodes;
    setb(run,ci);
  }
  return out;
}

long long Cs(int n,int k){
  if(k<0||k>n) return 0;
  long long r=1;
  for(int i=1;i<=k;i++) r=r*(n-k+i)/i;
  return r;
}

int findc(array<int,3>T,int p){
  for(int i=0;i<M;i++) if(clauseT[i]==T&&clausePat[i]==p) return i;
  return -1;
}

struct O{int kk,h,rep;unsigned long long mult;R r;};

int main(int argc,char**argv){
  if(argc!=3){cerr<<"usage: count_pair_orbits n m\n";return 2;}
  N=stoi(argv[1]); K=stoi(argv[2]);
  A=1<<N;
  M=8*(N*(N-1)*(N-2)/6);
  WORDS=(M+63)/64;
  if(N>7||K>10) return 2;

  for(int n=0;n<=M;n++){
    Cb[n][0]=1;
    for(int k=1;k<=K&&k<=n;k++) Cb[n][k]=Cb[n-1][k-1]+Cb[n-1][k];
  }

  vector<array<int,3>>tr;
  for(int i=0;i<N;i++)for(int j=i+1;j<N;j++)for(int k=j+1;k<N;k++)tr.push_back({i,j,k});
  ca.assign(A,{});
  for(auto T:tr)for(int pat=0;pat<8;pat++){
    U128 m=0;
    int ci=cm.size();
    for(int a=0;a<A;a++){
      bool ok=true;
      for(int z=0;z<3;z++) if(((a>>T[z])&1)!=((pat>>z)&1)){ok=false;break;}
      if(ok){m|=U128(1)<<a;ca[a].push_back(ci);}
    }
    cm.push_back(m);
    clauseT.push_back(T);
    clausePat.push_back(pat);
  }
  FULL=(A==128)?~U128(0):((U128(1)<<A)-1);

  vector<O>os;
  for(int kk=0;kk<=3;kk++)for(int h=0;h<=kk;h++){
    if(kk==3&&h==0) continue;
    if(3-kk>N-3) continue;
    vector<int>vv;
    for(int i=0;i<kk;i++) vv.push_back(i);
    for(int j=0;j<3-kk;j++) vv.push_back(3+j);
    sort(vv.begin(),vv.end());
    array<int,3>T{vv[0],vv[1],vv[2]};
    int p=0,ones=0;
    for(int z=0;z<3;z++) if(T[z]<3&&ones<h){p|=1<<z;ones++;}
    int rep=findc(T,p);
    unsigned long long mult=Cs(3,kk)*Cs(N-3,3-kk)*Cs(kk,h)*(1ULL<<(3-kk));
    os.push_back({kk,h,rep,mult,{}});
  }

  int root=0;
  auto st=chrono::steady_clock::now();
  #pragma omp parallel for schedule(dynamic,1)
  for(int q=0;q<(int)os.size();q++){
    int c=os[q].rep;
    B forb;
    setb(forb,root);
    setb(forb,c);
    os[q].r=rec(cm[root]|cm[c],2,forb);
  }

  unsigned long long wc=0,nodes=0,ms=0;
  for(auto&o:os){wc+=o.mult*o.r.count;nodes+=o.r.nodes;ms+=o.mult;}
  unsigned long long fixed=wc/(K-1);
  unsigned long long total=fixed*(unsigned long long)M/K;
  double sec=chrono::duration<double>(chrono::steady_clock::now()-st).count();

  cout<<"N "<<N<<" m "<<K<<" multsum "<<ms
      <<" weighted_pair_incidence "<<wc
      <<" fixed_clause "<<fixed
      <<" total "<<total
      <<" nodes "<<nodes
      <<" sec "<<sec<<"\n";
  for(auto&o:os)
    cout<<"k "<<o.kk<<" h "<<o.h<<" mult "<<o.mult
        <<" rep "<<o.rep<<" paircount "<<o.r.count
        <<" nodes "<<o.r.nodes<<"\n";
}
