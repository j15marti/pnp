#include <algorithm>
#include <array>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <functional>
#include <iostream>
#include <map>
#include <stdexcept>
#include <vector>
using namespace std;
int main(int argc,char**argv){try{
 if(argc!=4)throw runtime_error("usage: partition8 N PIVOT OUTPUT_PREFIX");
 int n=stoi(argv[1]),pivot=stoi(argv[2]);string prefix=argv[3];
 if(n<3||n>6||(pivot!=0&&pivot!=1))throw runtime_error("N=3..6, PIVOT=0 first uncovered or 1 minimum choices");
 vector<uint64_t> masks;vector<array<int,3>> vars;vector<int> pats;
 vector<vector<int>> incident(1<<n);
 for(int a=0;a<n;a++)for(int b=a+1;b<n;b++)for(int c=b+1;c<n;c++)for(int s=0;s<8;s++){
  uint64_t mask=0;int v[3]={a,b,c};
  for(int x=0;x<(1<<n);x++){bool yes=true;for(int j=0;j<3;j++)yes&=((x>>v[j])&1)==((s>>j)&1);if(yes)mask|=uint64_t(1)<<x;}
  int q=masks.size();masks.push_back(mask);vars.push_back({a,b,c});pats.push_back(s);
  for(int x=0;x<(1<<n);x++)if(mask&(uint64_t(1)<<x))incident[x].push_back(q);
 }
 uint64_t full=n==6?~uint64_t(0):(uint64_t(1)<<(1<<n))-1,total=0,states=0;
 array<unsigned char,8> picked{};map<pair<int,int>,uint64_t> hist;map<int,uint64_t> active;
 ofstream binary(prefix+".bin",ios::binary);auto start=chrono::steady_clock::now();
 function<void(uint64_t,int)> dfs=[&](uint64_t covered,int depth){states++;
  if(covered==full){if(depth!=8)throw runtime_error("depth");total++;auto sorted=picked;sort(sorted.begin(),sorted.end());binary.write(reinterpret_cast<char*>(sorted.data()),8);
   int pos[6]={},neg[6]={};for(int q:picked)for(int j=0;j<3;j++)(((pats[q]>>j)&1)?neg:pos)[vars[q][j]]++;
   int I=0,sq=0,used=0;for(int v=0;v<n;v++){I+=abs(pos[v]-neg[v]);int d=pos[v]+neg[v];sq+=d*d;used+=d>0;}hist[{I,n*sq-576}]++;active[used]++;return;
  }
  int x=__builtin_ctzll(full^covered);
  if(pivot==1){int best=1000;for(int a=0;a<(1<<n);a++)if(!(covered&(uint64_t(1)<<a))){int cnt=0;for(int q:incident[a])cnt+=!(covered&masks[q]);if(cnt<best){best=cnt;x=a;}if(!cnt)return;}}
  for(int q:incident[x])if(!(covered&masks[q])){picked[depth]=q;dfs(covered|masks[q],depth+1);}
 };dfs(0,0);
 ofstream out(prefix+".json");out<<"{\"n\":"<<n<<",\"m\":8,\"clauses\":"<<masks.size()<<",\"pivot\":"<<pivot<<",\"unsat\":"<<total<<",\"states\":"<<states<<",\"seconds\":"<<chrono::duration<double>(chrono::steady_clock::now()-start).count()<<",\"active_variables\":{";bool first=true;for(auto [a,c]:active){if(!first)out<<",";first=false;out<<"\""<<a<<"\":"<<c;}out<<"}}\n";
 ofstream h(prefix+"_profiles.csv");h<<"n,m,I,V_times_n,unsat\n";for(auto [iv,c]:hist)h<<n<<",8,"<<iv.first<<","<<iv.second<<","<<c<<"\n";
 cerr<<"n="<<n<<" pivot="<<pivot<<" unsat="<<total<<" states="<<states<<"\n";
}catch(const exception&e){cerr<<e.what()<<"\n";return 1;}}
