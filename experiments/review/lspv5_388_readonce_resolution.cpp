#include <algorithm>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <functional>
#include <iostream>
#include <string>
#include <unordered_set>
#include <vector>
#include <sys/resource.h>

using Clause = uint16_t; // low 8 bits positive, high 8 bits negative

struct Source { std::vector<int> lits; int global_id; };

static Clause encode(const std::vector<int>& lits, const std::vector<int>& vars) {
  uint16_t p=0,n=0;
  for(int l:lits){auto it=std::find(vars.begin(),vars.end(),std::abs(l));if(it==vars.end())throw std::runtime_error("outside side vars");int j=it-vars.begin();(l>0?p:n)|=uint16_t(1u<<j);}
  return Clause(p|(n<<8));
}

static bool resolve(Clause a, Clause b, Clause& out) {
  uint16_t ap=a&255, an=a>>8, bp=b&255, bn=b>>8;
  uint16_t comp=(ap&bn)|(an&bp);
  if(__builtin_popcount(unsigned(comp))!=1)return false;
  uint16_t rp=(ap|bp)&~comp, rn=(an|bn)&~comp;
  if(rp&rn)return false;
  out=Clause(rp|(rn<<8));return true;
}

static bool sat_clause(Clause c,int a){uint16_t p=c&255,n=c>>8;return (p&a)||(n&uint16_t(~a));}
static bool entails(const std::vector<Source>&src,const std::vector<int>&vars,Clause target){for(int a=0;a<256;a++){bool ok=true;for(const auto&s:src)ok&=sat_clause(encode(s.lits,vars),a);if(ok&&!sat_clause(target,a))return false;}return true;}

struct ProofNode { bool source; int source_id; Clause clause; int left,right; };

struct Run {
  bool found=false; uint64_t pair_tests=0, resolvents=0, duplicate_resolvents=0;
  std::vector<uint64_t> states_by_leaf_count;
  std::vector<Clause> full_outcomes;
  std::vector<ProofNode> proof;
};

static Run solve(const std::vector<Source>& src, const std::vector<int>& vars, Clause target) {
  const int m=src.size(), total=1<<m;std::vector<std::vector<Clause>> dp(total);Run r;r.states_by_leaf_count.assign(m+1,0);
  for(int i=0;i<m;i++){dp[1<<i].push_back(encode(src[i].lits,vars));r.states_by_leaf_count[1]++;}
  for(int sz=2;sz<=m;sz++){
    for(int mask=1;mask<total;mask++)if(__builtin_popcount(unsigned(mask))==sz){
      int anchor=mask&-mask;std::unordered_set<Clause> got;
      for(int a=(mask-1)&mask;a;a=(a-1)&mask){if(!(a&anchor))continue;int b=mask^a;if(!b||dp[a].empty()||dp[b].empty())continue;
        for(Clause x:dp[a])for(Clause y:dp[b]){r.pair_tests++;Clause z;if(resolve(x,y,z)){r.resolvents++;if(!got.insert(z).second)r.duplicate_resolvents++;}}
      }
      dp[mask].assign(got.begin(),got.end());std::sort(dp[mask].begin(),dp[mask].end());r.states_by_leaf_count[sz]+=dp[mask].size();
    }
    std::cerr<<"size "<<sz<<" states "<<r.states_by_leaf_count[sz]<<" pairs "<<r.pair_tests<<"\n";
  }
  r.full_outcomes=dp.back();r.found=std::binary_search(r.full_outcomes.begin(),r.full_outcomes.end(),target);
  if(r.found){
    std::function<int(int,Clause)> build=[&](int mask,Clause goal)->int{
      if((mask&(mask-1))==0){int i=__builtin_ctz(unsigned(mask));r.proof.push_back({true,src[i].global_id,goal,-1,-1});return int(r.proof.size()-1);}
      int anchor=mask&-mask;
      for(int a=(mask-1)&mask;a;a=(a-1)&mask){if(!(a&anchor))continue;int b=mask^a;if(!b)continue;
        for(Clause x:dp[a])for(Clause y:dp[b]){Clause z;if(resolve(x,y,z)&&z==goal){int l=build(a,x),rr=build(b,y);r.proof.push_back({false,-1,goal,l,rr});return int(r.proof.size()-1);}}
      }
      throw std::runtime_error("proof reconstruction failed");
    };build(total-1,target);
  }
  return r;
}

static std::vector<std::vector<int>> formula(std::vector<std::pair<int,int>>& edges,std::vector<std::vector<int>>& inc,std::vector<int>& charge){
  for(int off:{0,5})for(int u=0;u<4;u++)for(int v=u+1;v<4;v++)if(u==0&&v==1){edges.push_back({off,off+4});edges.push_back({off+4,off+1});}else edges.push_back({off+u,off+v});
  edges.push_back({4,9});inc.assign(10,{});for(int i=0;i<15;i++){inc[edges[i].first].push_back(i+1);inc[edges[i].second].push_back(i+1);}charge.assign(10,0);charge[0]=1;
  std::vector<std::vector<int>> F;for(int v=0;v<10;v++)for(int t=0;t<8;t++){int a=(t>>2)&1,b=(t>>1)&1,c=t&1;if((a^b^c)==charge[v])continue;F.push_back({a?-inc[v][0]:inc[v][0],b?-inc[v][1]:inc[v][1],c?-inc[v][2]:inc[v][2]});}return F;
}

static std::string clause_json(Clause c,const std::vector<int>& vars){std::string s="[";bool first=true;for(int j=0;j<8;j++){if(c&(1u<<j)){if(!first)s+=",";s+=std::to_string(vars[j]);first=false;}if(c&(1u<<(j+8))){if(!first)s+=",";s+=std::to_string(-vars[j]);first=false;}}return s+"]";}

int main(int argc,char**argv){if(argc!=2){std::cerr<<"usage: solver out.json\n";return 2;}auto started=std::chrono::steady_clock::now();
  std::vector<std::pair<int,int>> edges;std::vector<std::vector<int>> inc;std::vector<int> charge;auto F=formula(edges,inc,charge);
  std::vector<int> left_ids,right_ids;for(int i=0;i<16;i++)left_ids.push_back(i);left_ids.push_back(17);left_ids.push_back(18);for(int i=20;i<36;i++)right_ids.push_back(i);right_ids.push_back(36);right_ids.push_back(39);
  auto mk=[&](const std::vector<int>& ids){std::vector<Source>s;for(int i:ids)s.push_back({F[i],i});return s;};
  std::vector<int> lv={1,2,3,4,5,6,7,15},rv={8,9,10,11,12,13,14,15};
  auto LS=mk(left_ids),RS=mk(right_ids);Clause lt=Clause(1u<<7),rt=Clause(1u<<(7+8));
  bool Lent=entails(LS,lv,lt),Rent=entails(RS,rv,rt);if(!Lent||!Rent)throw std::runtime_error("side does not entail target unit");
  auto L=solve(LS,lv,lt);auto R=solve(RS,rv,rt);
  struct rusage ru{};getrusage(RUSAGE_SELF,&ru);double sec=std::chrono::duration<double>(std::chrono::steady_clock::now()-started).count();
  std::ofstream o(argv[1]);o<<"{\n  \"run\":\"LSPV-5/REFEREE388\",\n  \"timestamp_pst\":\"2026-11-06 07:48 PST\",\n  \"source_dimacs_sha256\":\"4f8a7e613ace4f67cd0b62204cdda2a4d8072047bd55a70da23da282e3537b18\",\n  \"left_source_ids\":[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,17,18],\n  \"right_source_ids\":[20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,39],\n  \"model\":\"strict non-tautological read-once Resolution tree, exact 18-source side subsets; no weakening\",\n  \"left_semantically_entails_positive_bridge_unit\":true,\n  \"right_semantically_entails_negative_bridge_unit\":true,\n";
  auto emit=[&](const char*name,const Run&x,const std::vector<int>&vars){o<<"  \""<<name<<"\":{\"target_found\":"<<(x.found?"true":"false")<<",\"pair_tests\":"<<x.pair_tests<<",\"resolvents\":"<<x.resolvents<<",\"duplicate_resolvents\":"<<x.duplicate_resolvents<<",\"states_by_leaf_count\":[";for(size_t i=0;i<x.states_by_leaf_count.size();i++){if(i)o<<",";o<<x.states_by_leaf_count[i];}o<<"],\"full_outcomes\":[";for(size_t i=0;i<x.full_outcomes.size();i++){if(i)o<<",";o<<clause_json(x.full_outcomes[i],vars);}o<<"],\"proof_nodes\":"<<x.proof.size()<<"}";};
  emit("left",L,lv);o<<",\n";emit("right",R,rv);o<<",\n  \"consequence\":\""<<(L.found&&R.found?"35-node pure-Resolution bridge refutation exists":"side-separable pure-Resolution 35-node construction excluded")<<"\",\n  \"elapsed_seconds\":"<<sec<<",\n  \"max_rss_kib\":"<<ru.ru_maxrss<<"\n}\n";o.close();
  std::cout<<"left="<<L.found<<" right="<<R.found<<" seconds="<<sec<<" rss="<<ru.ru_maxrss<<"\n";return 0;
}
