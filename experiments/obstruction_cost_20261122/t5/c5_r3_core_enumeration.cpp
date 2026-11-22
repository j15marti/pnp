#include <algorithm>
#include <array>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <set>
#include <string>
#include <vector>
using Mask=__uint128_t;
struct Row { std::string name; Mask accepts; };
const Mask FULL=(Mask(1)<<125)-1;
std::vector<Row> rows;
std::array<unsigned long long,48> cores{},nodes{};
std::array<std::vector<int>,48> witness;
std::vector<int> chosen;
std::chrono::steady_clock::time_point begin_time;
bool stopped=false;
unsigned long long checks=0;
bool c5(int a,int b,int c) {
  if(a==b||a==c||b==c)return false;
  int s=(1<<a)|(1<<b)|(1<<c);
  for(int i=0;i<5;++i)
    if(s==((1<<i)|(1<<((i+1)%5))|(1<<((i+2)%5))))return true;
  return false;
}
void make_rows() {
  std::set<int> supports;
  for(int a=0;a<5;++a)for(int b=a+1;b<5;++b) {
    int s=0;for(int x=0;x<5;++x)if(c5(x,a,b))s|=1<<x;
    supports.insert(s);
  }
  for(int v=0;v<3;++v)for(int s:supports) {
    Mask m=0;for(int x=0;x<5;++x)for(int y=0;y<5;++y)for(int z=0;z<5;++z) {
      int a[3]={x,y,z}; if(s&(1<<a[v]))m|=Mask(1)<<(25*x+5*y+z);
    }
    rows.push_back({"U"+std::to_string(v)+":"+std::to_string(s),m});
  }
  for(int u=0;u<3;++u)for(int v=u+1;v<3;++v)for(int a=0;a<5;++a) {
    Mask m=0;for(int x=0;x<5;++x)for(int y=0;y<5;++y)for(int z=0;z<5;++z) {
      int t[3]={x,y,z}; if(c5(t[u],t[v],a))m|=Mask(1)<<(25*x+5*y+z);
    }
    rows.push_back({"B"+std::to_string(u)+std::to_string(v)+":"+std::to_string(a),m});
  }
  Mask m=0;for(int x=0;x<5;++x)for(int y=0;y<5;++y)for(int z=0;z<5;++z)
    if(c5(x,y,z))m|=Mask(1)<<(25*x+5*y+z);
  rows.push_back({"T012",m});
}
void dfs(int start, Mask common, const std::vector<Mask>& private_sets) {
  ++nodes[chosen.size()];
  if((++checks&65535)==0 &&
     std::chrono::duration<double>(std::chrono::steady_clock::now()-begin_time).count()>25.0) {
    stopped=true;return;
  }
  for(int j=start;j<(int)rows.size()&&!stopped;++j) {
    Mask new_private=common&~rows[j].accepts;
    if(!new_private)continue;
    std::vector<Mask> next_private;next_private.reserve(private_sets.size()+1);
    bool redundant=false;
    for(Mask p:private_sets) {
      Mask q=p&rows[j].accepts;
      if(!q){redundant=true;break;}
      next_private.push_back(q);
    }
    if(redundant)continue;
    next_private.push_back(new_private);
    chosen.push_back(j);
    Mask next=common&rows[j].accepts;
    if(!next) {
      auto k=chosen.size();++cores[k];
      if(witness[k].empty())witness[k]=chosen;
    } else dfs(j+1,next,next_private);
    chosen.pop_back();
  }
}
int main(int argc,char**argv) {
  make_rows();
  int first=argc>1?std::stoi(argv[1]):0,last=argc>2?std::stoi(argv[2]):46;
  begin_time=std::chrono::steady_clock::now();
  int completed=first-1;
  for(int j=first;j<last&&!stopped;++j) {
    chosen={j};dfs(j+1,rows[j].accepts,{FULL&~rows[j].accepts});
    if(!stopped)completed=j;
  }
  double seconds=std::chrono::duration<double>(std::chrono::steady_clock::now()-begin_time).count();
  std::cout<<"{\n\"complete\":"<<(stopped?"false":"true")<<",\"first_root\":"<<first
    <<",\"last_root_exclusive\":"<<last<<",\"completed_through_root\":"<<completed
    <<",\"seconds\":"<<seconds<<",\"atoms\":"<<rows.size()<<",\"rows\":[";
  for(int j=0;j<(int)rows.size();++j){if(j)std::cout<<",";std::cout<<"\""<<rows[j].name<<"\"";}
  std::cout<<"],\"core_counts\":{";
  bool sep=false;for(int k=1;k<48;++k)if(cores[k]){if(sep)std::cout<<",";sep=true;std::cout<<"\""<<k<<"\":"<<cores[k];}
  std::cout<<"},\"irredundant_satisfiable_prefix_counts\":{";
  sep=false;for(int k=1;k<48;++k)if(nodes[k]){if(sep)std::cout<<",";sep=true;std::cout<<"\""<<k<<"\":"<<nodes[k];}
  std::cout<<"},\"first_core_by_size\":{";
  sep=false;for(int k=1;k<48;++k)if(!witness[k].empty()) {
    if(sep)std::cout<<",";sep=true;std::cout<<"\""<<k<<"\":[";
    for(int t=0;t<k;++t){if(t)std::cout<<",";std::cout<<witness[k][t];}std::cout<<"]";
  }
  std::cout<<"}}\n";
}
