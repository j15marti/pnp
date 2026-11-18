// TMR-2/077 independent complete-source PC engine, g++ -std=c++17 -O2.
// Usage: ./tmr2_t5_girth_pc077 < canonical_t5_source.txt > pc_rows.txt
// Prints every ordered pair's five row masks, preserving exact source values.
#include <bits/stdc++.h>
using namespace std;
using Row=array<uint8_t,5>;
int main(){
  ios::sync_with_stdio(false);cin.tie(nullptr);
  string head;
  if(!getline(cin,head)){cerr<<"NO_HEADER\n";return 2;}
  istringstream h(head); string p,t;int n,m; string trailing;
  if(!(h>>p>>t>>n>>m)||p!="p"||t!="t5"||n<1||m<0||(h>>trailing)){cerr<<"INVALID_HEADER\n";return 2;}
  vector<pair<int,int>> arcs; string line;
  for(int i=0;i<n;i++){
    if(!getline(cin,line)||line!=("v "+to_string(i))){cerr<<"INVALID_VERTEX\n";return 2;}
  }
  for(int j=0;j<m;j++){
    if(!getline(cin,line)){cerr<<"MISSING_ARC\n";return 2;}
    istringstream a(line);string op; int u,v;
    if(!(a>>op>>u>>v)||op!="a"||u<0||v<0||u>=n||v>=n||u==v||(a>>trailing)){
      cerr<<"INVALID_ARC\n";return 2;}
    arcs.push_back({u,v});
  }
  if(getline(cin,line)||!is_sorted(arcs.begin(),arcs.end())||adjacent_find(arcs.begin(),arcs.end())!=arcs.end()){
    cerr<<"NOT_CANONICAL\n";return 2;}
  auto allowed=[&](int a,int b){int d=(b-a+5)%5;return d==1||d==3;};
  vector<Row> r(n*n); const Row all={31,31,31,31,31};
  for(int i=0;i<n;i++)for(int j=0;j<n;j++) {
    r[i*n+j]=(i==j?Row{1,2,4,8,16}:all);
  }
  for(auto [i,j]:arcs){
    for(int a=0;a<5;a++){
      uint8_t fw=0,bw=0;
      for(int b=0;b<5;b++){
        if(allowed(a,b))fw|=(1<<b);
        if(allowed(b,a))bw|=(1<<b);
      }
      r[i*n+j][a] &= fw;
      r[j*n+i][a] &= bw;
    }
  }
  long long deleted=0;int rounds=0;bool consistent=true;
  for(;;){
    long long changed=0;
    for(int k=0;k<n;k++) for(int i=0;i<n;i++) for(int j=0;j<n;j++){
      const Row x=r[i*n+k]; const Row y=r[k*n+j]; Row &out=r[i*n+j];
      for(int a=0;a<5;a++){
        int z=x[a],new_mask=0;
        while(z){int bit=__builtin_ctz(z);new_mask|=y[bit];z&=z-1;}
        int invalid=out[a]&~new_mask;
        if(invalid){changed+=__builtin_popcount((unsigned)invalid);out[a]&=new_mask;}
      }
    }
    rounds++;deleted+=changed;
    if(!changed)break;
    if(rounds>20){cerr<<"NOT_CONVERGED\n";return 4;}
  }
  for(const auto &x:r){if(all_of(x.begin(),x.end(),[](uint8_t z){return z==0;})){consistent=false;break;}}
  cout<<n<<' '<<rounds<<' '<<deleted<<' '<<(consistent?1:0)<<'\n';
  for(auto &x:r){for(int a=0;a<5;a++)cout<<(a?" ":"")<<int(x[a]);cout<<'\n';}
}
