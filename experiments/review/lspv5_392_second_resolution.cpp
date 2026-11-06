#include <algorithm>
#include <array>
#include <chrono>
#include <cstdint>
#include <iomanip>
#include <iostream>
#include <limits>
#include <map>
#include <set>
#include <string>
#include <sys/resource.h>
#include <vector>

// REFEREE392: exact source-disjoint test for
//   (left-local clause RES right-local clause) RES side-local clause.
// Only clause-producing historical rules are relevant; AND3/XOR do not
// produce clauses consumable by strict Resolution.

using U16 = uint16_t;

static int pc(unsigned x) { return __builtin_popcount(x); }

template<class T> static void uniq(std::vector<T>& v) {
  std::sort(v.begin(), v.end());
  v.erase(std::unique(v.begin(), v.end()), v.end());
}

static U16 clause_code(unsigned pos, unsigned neg) {
  return U16(pos | (neg << 8));
}

static int strict_resolve_local(U16 a, U16 b) {
  const unsigned ap=a&255u, an=(a>>8)&255u;
  const unsigned bp=b&255u, bn=(b>>8)&255u;
  const unsigned piv=(ap&bn)|(an&bp);
  if (pc(piv)!=1) return -1;
  const unsigned rp=(ap|bp)&~piv, rn=(an|bn)&~piv;
  if (rp&rn) return -1;
  return int(clause_code(rp,rn));
}

static int strict_resolve_global(uint32_t a, uint32_t b) {
  const unsigned ap=a&0xffffu, an=a>>16;
  const unsigned bp=b&0xffffu, bn=b>>16;
  const unsigned piv=(ap&bn)|(an&bp);
  if (pc(piv)!=1) return -1;
  const unsigned rp=(ap|bp)&~piv, rn=(an|bn)&~piv;
  if (rp&rn) return -1;
  return int(uint32_t(rp|(rn<<16)));
}

static std::array<std::array<int,3>,18> side(bool right) {
  if (!right) return {{{1,3,4},{1,-3,-4},{-1,3,-4},{-1,-3,4},
    {2,5,-6},{2,-5,6},{-2,5,6},{-2,-5,-6},
    {3,5,-7},{3,-5,7},{-3,5,7},{-3,-5,-7},
    {4,6,-7},{4,-6,7},{-4,6,7},{-4,-6,-7},
    {1,-2,15},{-1,2,15}}};
  return {{{8,10,-11},{8,-10,11},{-8,10,11},{-8,-10,-11},
    {9,12,-13},{9,-12,13},{-9,12,13},{-9,-12,-13},
    {10,12,-14},{10,-12,14},{-10,12,14},{-10,-12,-14},
    {11,13,-14},{11,-13,14},{-11,13,14},{-11,-13,-14},
    {8,9,-15},{-8,-9,-15}}};
}

static std::vector<int> side_vars(bool right) {
  return right ? std::vector<int>{8,9,10,11,12,13,14,15}
               : std::vector<int>{1,2,3,4,5,6,7,15};
}

static std::vector<U16> encode_side(bool right) {
  const auto src=side(right); const auto vars=side_vars(right);
  std::vector<U16> out;
  for (auto c:src) {
    unsigned pos=0,neg=0;
    for (int x:c) {
      const unsigned v=std::lower_bound(vars.begin(),vars.end(),std::abs(x))-vars.begin();
      (x>0?pos:neg)|=1u<<v;
    }
    out.push_back(clause_code(pos,neg));
  }
  return out;
}

static uint32_t global_key(U16 c, bool right) {
  const auto vars=side_vars(right);
  const unsigned lp=c&255u, ln=(c>>8)&255u;
  unsigned gp=0,gn=0;
  for (unsigned i=0;i<8;i++) {
    if ((lp>>i)&1u) gp|=1u<<(vars[i]-1);
    if ((ln>>i)&1u) gn|=1u<<(vars[i]-1);
  }
  return uint32_t(gp|(gn<<16));
}

static std::string clause_text(uint32_t c) {
  std::string s="["; bool first=true;
  const unsigned p=c&0xffffu,n=c>>16;
  for (unsigned v=0;v<15;v++) {
    if ((p>>v)&1u) { if(!first)s+=","; s+=std::to_string(v+1); first=false; }
    if ((n>>v)&1u) { if(!first)s+=","; s+="-"+std::to_string(v+1); first=false; }
  }
  return s+"]";
}

struct MaskInfo { std::vector<unsigned> minimal_masks; };
using Catalog=std::map<uint32_t,MaskInfo>;
struct State { std::vector<U16> clauses; };

static void add_minimal(MaskInfo& info, unsigned mask) {
  for (unsigned m:info.minimal_masks) if ((m&mask)==m) return;
  info.minimal_masks.erase(std::remove_if(info.minimal_masks.begin(),info.minimal_masks.end(),
    [mask](unsigned m){return (m&mask)==mask;}),info.minimal_masks.end());
  info.minimal_masks.push_back(mask);
}

struct SideClosure {
  std::vector<State> dp;
  Catalog catalog;
  uint64_t pair_tests=0;
  uint64_t subset_clause_occurrences=0;
};

static SideClosure close_side(bool right) {
  const auto src=encode_side(right); const unsigned n=18,full=(1u<<n)-1;
  SideClosure z; z.dp.resize(1u<<n);
  for (unsigned i=0;i<n;i++) z.dp[1u<<i].clauses.push_back(src[i]);
  for (unsigned size=1;size<=n;size++) {
    for (unsigned sub=1;sub<=full;sub++) if (unsigned(pc(sub))==size) {
      if (size>1) {
        State cur;
        const unsigned anchor=sub&-sub;
        for (unsigned a=(sub-1)&sub;a;a=(a-1)&sub) {
          if (!(a&anchor)) continue;
          const unsigned b=sub^a; if(!b)continue;
          const auto&A=z.dp[a].clauses; const auto&B=z.dp[b].clauses;
          z.pair_tests+=uint64_t(A.size())*B.size();
          for(U16 x:A)for(U16 y:B){int q=strict_resolve_local(x,y);if(q>=0)cur.clauses.push_back(U16(q));}
        }
        uniq(cur.clauses); z.dp[sub]=std::move(cur);
      }
      z.subset_clause_occurrences+=z.dp[sub].clauses.size();
      for(U16 c:z.dp[sub].clauses) add_minimal(z.catalog[global_key(c,right)],sub);
    }
  }
  return z;
}

static bool disjoint_masks(const MaskInfo&a,const MaskInfo&b,unsigned&am,unsigned&bm) {
  for(unsigned x:a.minimal_masks)for(unsigned y:b.minimal_masks)if(!(x&y)){am=x;bm=y;return true;}
  return false;
}

struct Witness {
  bool exists=false, sibling_right=false;
  uint32_t left=0,right=0,first=0,sibling=0,second=0;
  unsigned parent_mask=0,sibling_mask=0,other_mask=0,total_sources=999;
};

static void consider(Witness&w,bool sib_right,uint32_t l,uint32_t r,uint32_t first,
                     uint32_t sib,uint32_t second,unsigned pm,unsigned sm,unsigned om) {
  const unsigned total=pc(pm)+pc(sm)+pc(om);
  if(!w.exists||total<w.total_sources||
     (total==w.total_sources&&std::array<uint32_t,5>{l,r,first,sib,second}<
       std::array<uint32_t,5>{w.left,w.right,w.first,w.sibling,w.second})) {
    w={true,sib_right,l,r,first,sib,second,pm,sm,om,total};
  }
}

int main() {
  const auto start=std::chrono::steady_clock::now();
  SideClosure L=close_side(false),R=close_side(true);
  uint64_t cross_pairs=0,support4=0,candidate_clause_tests=0;
  uint64_t semantic_second_res=0,disjoint_second_res=0;
  std::array<uint64_t,2> disjoint_by_side{};
  std::set<uint32_t> second_outputs;
  Witness best;
  for(const auto&[lk,li]:L.catalog)for(const auto&[rk,ri]:R.catalog){
    const int q=strict_resolve_global(lk,rk); if(q<0)continue;
    cross_pairs++;const uint32_t first=uint32_t(q);
    const unsigned support=(first&0xffffu)|(first>>16);
    if(pc(support)!=4)continue;
    support4++;
    std::array<unsigned,4> vars{};unsigned nv=0;
    for(unsigned v=0;v<15;v++)if((support>>v)&1u)vars[nv++]=v;
    for(unsigned side_id=0;side_id<2;side_id++){
      const bool sr=side_id==1;const Catalog&cat=sr?R.catalog:L.catalog;
      const MaskInfo&parent=sr?ri:li;const MaskInfo&other=sr?li:ri;
      for(unsigned code=1;code<81;code++){
        unsigned t=code,p=0,n=0;
        for(unsigned j=0;j<4;j++,t/=3){unsigned d=t%3;if(d==1)p|=1u<<vars[j];if(d==2)n|=1u<<vars[j];}
        const uint32_t sib=p|(n<<16);candidate_clause_tests++;
        auto it=cat.find(sib);if(it==cat.end())continue;
        const int z=strict_resolve_global(first,sib);if(z<0)continue;
        const uint32_t second=uint32_t(z);
        if(pc((second&0xffffu)|(second>>16))>3)continue;
        semantic_second_res++;
        unsigned pm=0,sm=0;
        if(!disjoint_masks(parent,it->second,pm,sm))continue;
        disjoint_second_res++;disjoint_by_side[side_id]++;second_outputs.insert(second);
        consider(best,sr,lk,rk,first,sib,second,pm,sm,other.minimal_masks.front());
      }
    }
  }
  rusage ru{};getrusage(RUSAGE_SELF,&ru);
  const double seconds=std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count();
  std::cout<<"{\n"
    <<"  \"run\": \"LSPV-5/REFEREE392 one-additional-Resolution source-disjoint test\",\n"
    <<"  \"status\": \"COMPUTATIONAL_EXACT_FINITE\",\n"
    <<"  \"scope\": \"first cross-cut strict RES followed by one strict RES with a side-local source-disjoint sibling\",\n"
    <<"  \"left_unique_clauses\": "<<L.catalog.size()<<",\n"
    <<"  \"right_unique_clauses\": "<<R.catalog.size()<<",\n"
    <<"  \"left_subset_clause_occurrences\": "<<L.subset_clause_occurrences<<",\n"
    <<"  \"right_subset_clause_occurrences\": "<<R.subset_clause_occurrences<<",\n"
    <<"  \"left_resolution_pair_tests\": "<<L.pair_tests<<",\n"
    <<"  \"right_resolution_pair_tests\": "<<R.pair_tests<<",\n"
    <<"  \"cross_strict_resolution_pairs\": "<<cross_pairs<<",\n"
    <<"  \"cross_support_four_pairs\": "<<support4<<",\n"
    <<"  \"candidate_side_clause_tests\": "<<candidate_clause_tests<<",\n"
    <<"  \"semantic_second_resolution_patterns\": "<<semantic_second_res<<",\n"
    <<"  \"source_disjoint_second_resolution_patterns\": "<<disjoint_second_res<<",\n"
    <<"  \"source_disjoint_by_sibling_side\": ["<<disjoint_by_side[0]<<","<<disjoint_by_side[1]<<"],\n"
    <<"  \"distinct_support_at_most_three_outputs\": "<<second_outputs.size()<<",\n"
    <<"  \"falsifier_found\": "<<(best.exists?"true":"false")<<",\n"
    <<"  \"best_witness\": {\n"
    <<"    \"sibling_side\": \""<<(best.sibling_right?"right":"left")<<"\",\n"
    <<"    \"left_parent\": "<<clause_text(best.left)<<",\n"
    <<"    \"right_parent\": "<<clause_text(best.right)<<",\n"
    <<"    \"first_resolvent\": "<<clause_text(best.first)<<",\n"
    <<"    \"sibling\": "<<clause_text(best.sibling)<<",\n"
    <<"    \"second_resolvent\": "<<clause_text(best.second)<<",\n"
    <<"    \"same_side_parent_source_mask\": "<<best.parent_mask<<",\n"
    <<"    \"sibling_source_mask\": "<<best.sibling_mask<<",\n"
    <<"    \"other_side_source_mask\": "<<best.other_mask<<",\n"
    <<"    \"total_source_leaves\": "<<(best.exists?best.total_sources:0)<<"\n"
    <<"  },\n"
    <<"  \"wall_seconds\": "<<std::fixed<<std::setprecision(6)<<seconds<<",\n"
    <<"  \"max_rss_kib\": "<<ru.ru_maxrss<<"\n"
    <<"}\n";
}
