#include <algorithm>
#include <array>
#include <cstdint>
#include <fstream>
#include <functional>
#include <iostream>
#include <map>
#include <numeric>
#include <set>
#include <stdexcept>
#include <tuple>
#include <vector>
using namespace std;
struct Node{int q,lo,hi;};
using Row=array<uint8_t,8>;
uint64_t choose(int n,int k){if(k<0||k>n)return 0;uint64_t v=1;for(int j=1;j<=k;j++)v=v*(n-j+1)/j;return v;}
int main(int argc,char**argv){try{
 if(argc!=5)throw runtime_error("usage: partition8_dag N PARTITIONS.bin OUTPUT_PREFIX SWAP_PASSES");
 int n=stoi(argv[1]),passes=stoi(argv[4]),C=8*n*(n-1)*(n-2)/6;string prefix=argv[3];
 if(n<3||n>6||passes<0)throw runtime_error("invalid argument");
 ifstream in(argv[2],ios::binary);if(!in)throw runtime_error("input");vector<Row> rows;Row row;while(in.read(reinterpret_cast<char*>(row.data()),8))rows.push_back(row);if(!in.eof()||in.gcount()!=0)throw runtime_error("partial record");
 for(auto r:rows)if(!is_sorted(r.begin(),r.end())||adjacent_find(r.begin(),r.end())!=r.end()||r[7]>=C)throw runtime_error("row");
 vector<array<uint64_t,3>> bits(rows.size());for(size_t i=0;i<rows.size();i++)for(int q:rows[i])bits[i][q/64]|=uint64_t(1)<<(q%64);
 vector<int> round;for(int s=0;s<8;s++)for(int t=0;t<C/8;t++)round.push_back(t*8+s);
 vector<int> grouped(C);iota(grouped.begin(),grouped.end(),0);
 int best=100000000,trial=0;vector<int> bestorder;
 ofstream log(prefix+"_search.csv");log<<"method,trial,nodes,allocated_nodes\n";
 auto run=[&](const vector<int>& order,string method){
  vector<Node> nodes={{-1,0,0},{-1,1,1}};map<tuple<int,int,int>,int> unique;
  auto mk=[&](int q,int lo,int hi){if(lo==hi)return lo;auto key=make_tuple(q,lo,hi);auto it=unique.find(key);if(it!=unique.end())return it->second;int id=nodes.size();nodes.push_back({q,lo,hi});unique[key]=id;return id;};
  function<int(int,int,const vector<int>&)> rec=[&](int i,int r,const vector<int>& ids){
   if(ids.empty())return 0;
   if(ids.size()==choose(C-i,r))return 1;
   int q=order[i];vector<int> lo,hi;lo.reserve(ids.size());hi.reserve(ids.size());
   for(int id:ids)((bits[id][q/64]>>(q%64))&1?hi:lo).push_back(id);
   return mk(q,rec(i+1,r,lo),rec(i+1,r-1,hi));
  };
  vector<int> ids(rows.size());iota(ids.begin(),ids.end(),0);int root=rec(0,8,ids);
  vector<bool> seen(nodes.size());int count=0;function<void(int)> walk=[&](int id){if(id<2||seen[id])return;seen[id]=true;count++;walk(nodes[id].lo);walk(nodes[id].hi);};walk(root);
  log<<method<<","<<trial++<<","<<count<<","<<nodes.size()-2<<"\n";log.flush();
  if(count<best){best=count;bestorder=order;ofstream f(prefix+".dag");f<<n<<" 8 "<<C<<" "<<root<<" "<<nodes.size()<<"\n";for(int q:order)f<<q<<" ";f<<"\n";for(size_t id=2;id<nodes.size();id++){auto v=nodes[id];f<<id<<" "<<v.q<<" "<<v.lo<<" "<<v.hi<<"\n";}cerr<<"n="<<n<<" best="<<best<<" "<<method<<"\n";}
 };
 run(round,"sign_round_robin");run(grouped,"grouped");
 vector<int> gray;for(int s=0;s<8;s++)for(int t=0;t<C/8;t++)gray.push_back(t*8+(s^(s>>1)));run(gray,"gray_round_robin");
 vector<int> minpoint(C),maxpoint(C);int qid=0;
 for(int a=0;a<n;a++)for(int b=a+1;b<n;b++)for(int c=b+1;c<n;c++)for(int s=0;s<8;s++){
  int lo=((s&1)<<a)|(((s>>1)&1)<<b)|(((s>>2)&1)<<c),fixed=(1<<a)|(1<<b)|(1<<c);
  minpoint[qid]=lo;maxpoint[qid]=lo|(((1<<n)-1)^fixed);qid++;
 }
 for(int reverse_tie=0;reverse_tie<2;reverse_tie++){
  auto o=grouped;sort(o.begin(),o.end(),[&](int a,int b){return minpoint[a]!=minpoint[b]?minpoint[a]<minpoint[b]:(reverse_tie?a>b:a<b);});run(o,reverse_tie?"min_point_reverse_tie":"min_point");
 }
 auto reversed=grouped;reverse(reversed.begin(),reversed.end());run(reversed,"reverse_grouped");
 auto order=bestorder;for(int pass=0;pass<passes;pass++){bool change=false;for(int i=0;i<C-1;i++){auto cand=order;swap(cand[i],cand[i+1]);int before=best;run(cand,"adjacent");if(best<before){order=bestorder;change=true;}}if(!change)break;}
 cout<<"best_nodes="<<best<<" trials="<<trial<<"\n";
}catch(const exception&e){cerr<<e.what()<<"\n";return 1;}}
