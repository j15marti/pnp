#include <algorithm>
#include <array>
#include <chrono>
#include <cstdint>
#include <iomanip>
#include <iostream>
#include <map>
#include <set>
#include <string>
#include <sys/resource.h>
#include <vector>

// REFEREE393: exact source-disjoint test for
//   RES( RES(left-local,right-local), RES(left-local,right-local) ).
// At the authenticated q=35 floor, clauses are produced only by strict RES.

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
          for(U16 x:A)for(U16 y:B){
            int q=strict_resolve_local(x,y);
            if(q>=0)cur.clauses.push_back(U16(q));
          }
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
  for(unsigned x:a.minimal_masks)for(unsigned y:b.minimal_masks)if(!(x&y)){
    am=x;bm=y;return true;
  }
  return false;
}

static unsigned minimum_overlap(const MaskInfo&a,const MaskInfo&b) {
  unsigned best=999;
  for(unsigned x:a.minimal_masks)for(unsigned y:b.minimal_masks)
    best=std::min(best,unsigned(pc(x&y)));
  return best;
}

struct Cross {
  uint32_t clause=0,left_parent=0,right_parent=0;
  const MaskInfo* left_masks=nullptr;
  const MaskInfo* right_masks=nullptr;
};

struct Witness {
  bool exists=false;
  uint32_t a=0,b=0,out=0;
  unsigned al=0,ar=0,bl=0,br=0,total_sources=999;
};

int main() {
  const auto start=std::chrono::steady_clock::now();
  SideClosure L=close_side(false),R=close_side(true);
  uint64_t all_cross=0;
  std::vector<Cross> cross4;
  for(const auto&[lk,li]:L.catalog)for(const auto&[rk,ri]:R.catalog){
    const int q=strict_resolve_global(lk,rk); if(q<0)continue;
    all_cross++;
    const uint32_t c=uint32_t(q);
    if(pc((c&0xffffu)|(c>>16))==4)
      cross4.push_back({c,lk,rk,&li,&ri});
  }

  uint64_t pair_tests=0,strict_pairs=0,semantic_small=0,disjoint_small=0;
  uint64_t left_disjoint_small=0,right_disjoint_small=0;
  unsigned minimum_total_overlap=999;
  std::set<uint32_t> small_outputs;
  Witness best;
  for(size_t i=0;i<cross4.size();i++)for(size_t j=i+1;j<cross4.size();j++){
    pair_tests++;
    const int z=strict_resolve_global(cross4[i].clause,cross4[j].clause);
    if(z<0)continue;
    strict_pairs++;
    const uint32_t out=uint32_t(z);
    if(pc((out&0xffffu)|(out>>16))>3)continue;
    semantic_small++;small_outputs.insert(out);
    unsigned al=0,bl=0,ar=0,br=0;
    const bool ld=disjoint_masks(*cross4[i].left_masks,*cross4[j].left_masks,al,bl);
    const bool rd=disjoint_masks(*cross4[i].right_masks,*cross4[j].right_masks,ar,br);
    left_disjoint_small+=ld;right_disjoint_small+=rd;
    minimum_total_overlap=std::min(minimum_total_overlap,
      minimum_overlap(*cross4[i].left_masks,*cross4[j].left_masks)+
      minimum_overlap(*cross4[i].right_masks,*cross4[j].right_masks));
    if(!ld||!rd)continue;
    disjoint_small++;
    const unsigned total=pc(al)+pc(bl)+pc(ar)+pc(br);
    if(!best.exists||total<best.total_sources){
      best={true,cross4[i].clause,cross4[j].clause,out,al,ar,bl,br,total};
    }
  }

  rusage ru{};getrusage(RUSAGE_SELF,&ru);
  const double seconds=std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count();
  std::cout<<"{\n"
    <<"  \"run\": \"LSPV-5/REFEREE393 double-cross strict-Resolution test\",\n"
    <<"  \"status\": \"COMPUTATIONAL_EXACT_FINITE\",\n"
    <<"  \"scope\": \"one strict RES between two support-four first cross-cut strict resolvents with exact left/right source-disjointness\",\n"
    <<"  \"left_unique_clauses\": "<<L.catalog.size()<<",\n"
    <<"  \"right_unique_clauses\": "<<R.catalog.size()<<",\n"
    <<"  \"left_subset_clause_occurrences\": "<<L.subset_clause_occurrences<<",\n"
    <<"  \"right_subset_clause_occurrences\": "<<R.subset_clause_occurrences<<",\n"
    <<"  \"left_resolution_pair_tests\": "<<L.pair_tests<<",\n"
    <<"  \"right_resolution_pair_tests\": "<<R.pair_tests<<",\n"
    <<"  \"all_first_cross_resolvents\": "<<all_cross<<",\n"
    <<"  \"support_four_first_cross_resolvents\": "<<cross4.size()<<",\n"
    <<"  \"unordered_double_cross_pair_tests\": "<<pair_tests<<",\n"
    <<"  \"strict_double_cross_pairs\": "<<strict_pairs<<",\n"
    <<"  \"semantic_support_at_most_three_pairs\": "<<semantic_small<<",\n"
    <<"  \"semantic_pairs_with_left_disjoint_ancestry\": "<<left_disjoint_small<<",\n"
    <<"  \"semantic_pairs_with_right_disjoint_ancestry\": "<<right_disjoint_small<<",\n"
    <<"  \"source_disjoint_support_at_most_three_pairs\": "<<disjoint_small<<",\n"
    <<"  \"minimum_total_reused_source_count\": "<<(semantic_small?minimum_total_overlap:0)<<",\n"
    <<"  \"distinct_support_at_most_three_outputs\": "<<small_outputs.size()<<",\n"
    <<"  \"falsifier_found\": "<<(best.exists?"true":"false")<<",\n"
    <<"  \"best_witness\": {\n"
    <<"    \"first_cross_resolvent\": "<<clause_text(best.a)<<",\n"
    <<"    \"sibling_cross_resolvent\": "<<clause_text(best.b)<<",\n"
    <<"    \"output\": "<<clause_text(best.out)<<",\n"
    <<"    \"first_left_mask\": "<<best.al<<",\n"
    <<"    \"first_right_mask\": "<<best.ar<<",\n"
    <<"    \"sibling_left_mask\": "<<best.bl<<",\n"
    <<"    \"sibling_right_mask\": "<<best.br<<",\n"
    <<"    \"total_source_leaves\": "<<(best.exists?best.total_sources:0)<<"\n"
    <<"  },\n"
    <<"  \"wall_seconds\": "<<std::fixed<<std::setprecision(6)<<seconds<<",\n"
    <<"  \"max_rss_kib\": "<<ru.ru_maxrss<<"\n"
    <<"}\n";
}
