#include <bits/stdc++.h>
#include <omp.h>
using namespace std;
using U128=__uint128_t;

struct B{uint64_t w[8]={0};};
inline bool tst(const B&b,int i){return (b.w[i>>6]>>(i&63))&1ULL;}
inline void setb(B&b,int i){b.w[i>>6]|=1ULL<<(i&63);}
inline int pc(U128 x){return __builtin_popcountll((uint64_t)x)+__builtin_popcountll((uint64_t)(x>>64));}

int N,M,K,A;
vector<U128> cm;
vector<vector<int>>ca;
vector<array<int,3>> clauseT;
vector<int> clausePat;
vector<unsigned> varmask;
U128 FULL;

struct R{unsigned long long count=0,full=0,nodes=0;};

bool has_private(int ci,const array<uint8_t,128>&cnt){
  U128 x=cm[ci];
  while(x){
    uint64_t lo=(uint64_t)x;
    int a;
    if(lo) a=__builtin_ctzll(lo);
    else a=64+__builtin_ctzll((uint64_t)(x>>64));
    x&=~(U128(1)<<a);
    if(cnt[a]==1) return true;
  }
  return false;
}

void addmask(int ci,array<uint8_t,128>&cnt){
  U128 x=cm[ci];
  while(x){
    uint64_t lo=(uint64_t)x;
    int a;
    if(lo) a=__builtin_ctzll(lo);
    else a=64+__builtin_ctzll((uint64_t)(x>>64));
    x&=~(U128(1)<<a);
    cnt[a]++;
  }
}

R rec(U128 cov,int k,B forb,vector<int>&sel,array<uint8_t,128>&cnt){
  R out; out.nodes=1;
  if(cov==FULL){
    if(k==K){
      out.count=1;
      unsigned vm=0;
      for(int ci:sel) vm|=varmask[ci];
      if(__builtin_popcount(vm)==N) out.full=1;
    }
    return out;
  }
  if(k>=K) return out;
  int unc=A-pc(cov);
  if(unc>(1<<(N-3))*(K-k)) return out;

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
    auto c2=cnt;
    addmask(ci,c2);
    bool ok=true;
    for(int sj:sel) if(!has_private(sj,c2)){ok=false;break;}
    if(ok&&!has_private(ci,c2)) ok=false;
    if(ok){
      B child=run;
      setb(child,ci);
      sel.push_back(ci);
      R z=rec(cov|cm[ci],k+1,child,sel,c2);
      sel.pop_back();
      out.count+=z.count;
      out.full+=z.full;
      out.nodes+=z.nodes;
    }
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
  if(argc!=3){cerr<<"usage: min_pair_orbits n m\n";return 2;}
  N=stoi(argv[1]); K=stoi(argv[2]);
  A=1<<N;
  M=8*(N*(N-1)*(N-2)/6);
  if(N>7||K>10) return 2;

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
    varmask.push_back((1u<<T[0])|(1u<<T[1])|(1u<<T[2]));
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
    array<uint8_t,128>cnt{};
    addmask(root,cnt);
    addmask(c,cnt);
    vector<int>sel{root,c};
    if(has_private(root,cnt)&&has_private(c,cnt))
      os[q].r=rec(cm[root]|cm[c],2,forb,sel,cnt);
  }

  unsigned long long wc=0,wf=0,nodes=0;
  for(auto&o:os){
    wc+=o.mult*o.r.count;
    wf+=o.mult*o.r.full;
    nodes+=o.r.nodes;
  }
  unsigned long long fixed=wc/(K-1);
  unsigned long long fixedfull=wf/(K-1);
  unsigned long long total=fixed*(unsigned long long)M/K;
  unsigned long long totalfull=fixedfull*(unsigned long long)M/K;
  double sec=chrono::duration<double>(chrono::steady_clock::now()-st).count();

  cout<<"N "<<N<<" m "<<K
      <<" minimal "<<total
      <<" fullsupport "<<totalfull
      <<" fixed "<<fixed
      <<" nodes "<<nodes
      <<" sec "<<sec<<"\n";
  for(auto&o:os)
    cout<<"k "<<o.kk<<" h "<<o.h<<" mult "<<o.mult
        <<" count "<<o.r.count<<" full "<<o.r.full
        <<" nodes "<<o.r.nodes<<"\n";
}
