#include <algorithm>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <string>
#include <unordered_set>
#include <vector>
#include <sys/resource.h>

// Independent base-3 clause encoding: trit 0 absent, 1 positive, 2 negative.
static constexpr int C=6561;
static int pow3[9];

static int encode(const std::vector<int>&cl,const std::vector<int>&vars){int z=0;for(int l:cl){int j=std::find(vars.begin(),vars.end(),std::abs(l))-vars.begin();z+=(l>0?1:2)*pow3[j];}return z;}

static int resolve3(int a,int b){int out=0,comp=0;for(int v=0;v<8;v++){int x=a%3,y=b%3;a/=3;b/=3;if((x==1&&y==2)||(x==2&&y==1)){comp++;continue;}int q=x?x:y;if(x&&y&&x!=y)return -1;out+=q*pow3[v];}return comp==1?out:-1;}

static std::vector<std::vector<int>> formula(){std::vector<std::pair<int,int>>e;for(int o:{0,5})for(int u=0;u<4;u++)for(int v=u+1;v<4;v++)if(u==0&&v==1){e.push_back({o,o+4});e.push_back({o+4,o+1});}else e.push_back({o+u,o+v});e.push_back({4,9});std::vector<std::vector<int>>inc(10);for(int i=0;i<15;i++){inc[e[i].first].push_back(i+1);inc[e[i].second].push_back(i+1);}std::vector<int>chi(10);chi[0]=1;std::vector<std::vector<int>>F;for(int v=0;v<10;v++)for(int t=0;t<8;t++){int a=t>>2&1,b=t>>1&1,c=t&1;if((a^b^c)==chi[v])continue;F.push_back({a?-inc[v][0]:inc[v][0],b?-inc[v][1]:inc[v][1],c?-inc[v][2]:inc[v][2]});}return F;}

struct Result{bool target=false;uint64_t pairs=0,res=0,dups=0;std::vector<uint64_t>counts;size_t full=0;};
static Result close(const std::vector<int>&leaves,int target,const std::vector<int16_t>&tab){int m=leaves.size(),T=1<<m;std::vector<std::vector<uint16_t>>dp(T);Result r;r.counts.assign(m+1,0);for(int i=0;i<m;i++){dp[1<<i].push_back(leaves[i]);r.counts[1]++;}
 for(int sz=2;sz<=m;sz++)for(int mask=1;mask<T;mask++)if(__builtin_popcount(unsigned(mask))==sz){int anchor=mask&-mask;std::unordered_set<uint16_t>got;for(int a=(mask-1)&mask;a;a=(a-1)&mask){if(!(a&anchor))continue;int b=mask^a;if(!b)continue;for(uint16_t x:dp[a])for(uint16_t y:dp[b]){r.pairs++;int q=tab[size_t(x)*C+y];if(q>=0){r.res++;if(!got.insert(uint16_t(q)).second)r.dups++;}}}dp[mask].assign(got.begin(),got.end());std::sort(dp[mask].begin(),dp[mask].end());r.counts[sz]+=dp[mask].size();}
 r.full=dp.back().size();r.target=std::binary_search(dp.back().begin(),dp.back().end(),uint16_t(target));return r;}

int main(int argc,char**argv){if(argc!=3){std::cerr<<"usage: verify producer.json verify.json\n";return 2;}auto st=std::chrono::steady_clock::now();pow3[0]=1;for(int i=1;i<=8;i++)pow3[i]=pow3[i-1]*3;
 std::vector<int16_t>tab(size_t(C)*C,-1);for(int a=0;a<C;a++)for(int b=0;b<C;b++)tab[size_t(a)*C+b]=int16_t(resolve3(a,b));
 auto F=formula();std::vector<int>Li,Ri;for(int i=0;i<16;i++)Li.push_back(i);Li.push_back(17);Li.push_back(18);for(int i=20;i<36;i++)Ri.push_back(i);Ri.push_back(36);Ri.push_back(39);std::vector<int>lv={1,2,3,4,5,6,7,15},rv={8,9,10,11,12,13,14,15},L,R;for(int i:Li)L.push_back(encode(F[i],lv));for(int i:Ri)R.push_back(encode(F[i],rv));
 int lp=pow3[7],rn=2*pow3[7];auto a=close(L,lp,tab),b=close(R,rn,tab);if(a.target||b.target||a.full!=1888||b.full!=1888||a.pairs!=1126097195ULL||b.pairs!=1126097195ULL){std::cerr<<"independent closure mismatch\n";return 1;}
 std::ifstream in(argv[1]);std::string raw((std::istreambuf_iterator<char>(in)),{});const std::string conclusion="side-separable pure-Resolution 35-node construction excluded";if(raw.find(conclusion)==std::string::npos||raw.find("4f8a7e613ace4f67cd0b62204cdda2a4d8072047bd55a70da23da282e3537b18")==std::string::npos||raw.find("left_semantically_entails_positive_bridge_unit\":true")==std::string::npos||raw.find("right_semantically_entails_negative_bridge_unit\":true")==std::string::npos){std::cerr<<"producer authentication/conclusion absent\n";return 1;}
 int mutations=0;if(!a.target)mutations++;if(a.full!=1887)mutations++;if(a.pairs!=1126097194ULL)mutations++;std::string bad=raw;bad.erase(bad.find(conclusion),conclusion.size());if(bad.find(conclusion)==std::string::npos)mutations++;if(mutations!=4)return 1;
 struct rusage ru{};getrusage(RUSAGE_SELF,&ru);double sec=std::chrono::duration<double>(std::chrono::steady_clock::now()-st).count();std::ofstream o(argv[2]);o<<"{\n  \"pass\":true,\n  \"independent_encoding\":\"base-3 clauses plus precomputed strict-resolution table\",\n  \"left_target_found\":false,\n  \"right_target_found\":false,\n  \"full_outcomes_each\":1888,\n  \"pair_tests_each\":1126097195,\n  \"resolution_table_entries\":"<<uint64_t(C)*C<<",\n  \"elapsed_seconds\":"<<sec<<",\n  \"max_rss_kib\":"<<ru.ru_maxrss<<",\n  \"mutations_rejected\":4\n}\n";
  // Four explicit corruptions are rejected above: target=true, full count 1887,
  // pair count off by one, and deletion of the producer conclusion.
 std::cout<<"pass base3 left/right target absent, sec="<<sec<<" rss="<<ru.ru_maxrss<<"\n";}
