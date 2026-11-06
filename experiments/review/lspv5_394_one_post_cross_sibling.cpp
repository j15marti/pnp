#define main referee393_main_disabled
#include "lspv5_393_double_cross_resolution.cpp"
#undef main

// REFEREE394: exact source-authenticated test for
//   RES(C1, RES(C2,D)),
// where C1 and C2 are first cross-cut resolvents and D is side-local.

struct PairMask { unsigned left=0,right=0; };
struct PostInfo { std::vector<PairMask> minimal_masks; };
using PostCatalog=std::map<uint32_t,PostInfo>;

static void add_minimal_pair(PostInfo&info,unsigned left,unsigned right){
  for(const auto&m:info.minimal_masks)
    if((m.left&left)==m.left&&(m.right&right)==m.right)return;
  info.minimal_masks.erase(std::remove_if(info.minimal_masks.begin(),info.minimal_masks.end(),
    [left,right](const PairMask&m){
      return (m.left&left)==left&&(m.right&right)==right;
    }),info.minimal_masks.end());
  info.minimal_masks.push_back({left,right});
}

static unsigned clause_support(uint32_t c){return (c&0xffffu)|(c>>16);}

static std::vector<uint32_t> signed_clauses_on_support(unsigned support){
  std::vector<unsigned> vars;
  for(unsigned v=0;v<15;v++)if((support>>v)&1u)vars.push_back(v);
  unsigned pow3=1;for(size_t i=0;i<vars.size();i++)pow3*=3;
  std::vector<uint32_t> out;out.reserve(pow3-1);
  for(unsigned code=1;code<pow3;code++){
    unsigned t=code,p=0,n=0;
    for(size_t j=0;j<vars.size();j++,t/=3){
      const unsigned d=t%3;
      if(d==1)p|=1u<<vars[j];
      if(d==2)n|=1u<<vars[j];
    }
    out.push_back(uint32_t(p|(n<<16)));
  }
  return out;
}

struct FinalWitness{
  bool exists=false;
  uint32_t c1=0,post=0,out=0;
  unsigned c1l=0,c1r=0,postl=0,postr=0,total=999;
};

int main(){
  const auto start=std::chrono::steady_clock::now();
  SideClosure L=close_side(false),R=close_side(true);
  std::vector<Cross> cross4,cross45;
  uint64_t all_cross=0;
  for(const auto&[lk,li]:L.catalog)for(const auto&[rk,ri]:R.catalog){
    const int q=strict_resolve_global(lk,rk);if(q<0)continue;
    all_cross++;const uint32_t c=uint32_t(q);const int s=pc(clause_support(c));
    if(s==4)cross4.push_back({c,lk,rk,&li,&ri});
    if(s==4||s==5)cross45.push_back({c,lk,rk,&li,&ri});
  }

  PostCatalog post;
  uint64_t post_candidate_queries=0,post_catalog_hits=0,post_strict=0;
  uint64_t post_support_at_most_four=0,post_legal_mask_unions=0;
  std::map<std::pair<unsigned,bool>,std::vector<std::pair<uint32_t,const MaskInfo*>>> candidate_cache;
  for(const Cross&c:cross45){
    const unsigned support=clause_support(c.clause);
    for(unsigned side_id=0;side_id<2;side_id++){
      const bool right=side_id==1;
      const Catalog&cat=right?R.catalog:L.catalog;
      const MaskInfo&same=right?*c.right_masks:*c.left_masks;
      const MaskInfo&other=right?*c.left_masks:*c.right_masks;
      auto&candidates=candidate_cache[{support,right}];
      if(candidates.empty()){
        const unsigned outside_budget=5-pc(support);
        for(const auto&[d,masks]:cat)
          if(unsigned(pc(clause_support(d)&~support))<=outside_budget)
            candidates.push_back({d,&masks});
      }
      for(const auto&[d,dmasks]:candidates){
        post_candidate_queries++;
        post_catalog_hits++;
        const int z=strict_resolve_global(c.clause,d);if(z<0)continue;post_strict++;
        const uint32_t out=uint32_t(z);
        if(pc(clause_support(out))>4)continue;
        post_support_at_most_four++;
        for(unsigned sm:same.minimal_masks)for(unsigned dm:dmasks->minimal_masks){
          if(sm&dm)continue;
          for(unsigned om:other.minimal_masks){
            post_legal_mask_unions++;
            if(right)add_minimal_pair(post[out],om,sm|dm);
            else add_minimal_pair(post[out],sm|dm,om);
          }
        }
      }
    }
  }

  uint64_t post_mask_pairs=0;for(const auto&[_,info]:post)post_mask_pairs+=info.minimal_masks.size();
  uint64_t final_clause_queries=0,final_catalog_hits=0,final_strict_small=0,final_disjoint=0;
  std::set<uint32_t>final_outputs;FinalWitness best;
  for(const Cross&c1:cross4){
    for(uint32_t sibling:signed_clauses_on_support(clause_support(c1.clause))){
      final_clause_queries++;
      auto it=post.find(sibling);if(it==post.end())continue;final_catalog_hits++;
      const int z=strict_resolve_global(c1.clause,sibling);if(z<0)continue;
      const uint32_t out=uint32_t(z);if(pc(clause_support(out))>3)continue;
      final_strict_small++;final_outputs.insert(out);
      for(unsigned c1l:c1.left_masks->minimal_masks)
        for(unsigned c1r:c1.right_masks->minimal_masks)
          for(const PairMask&m:it->second.minimal_masks){
            if((c1l&m.left)||(c1r&m.right))continue;
            final_disjoint++;
            const unsigned total=pc(c1l)+pc(c1r)+pc(m.left)+pc(m.right);
            if(!best.exists||total<best.total)
              best={true,c1.clause,sibling,out,c1l,c1r,m.left,m.right,total};
          }
    }
  }

  rusage ru{};getrusage(RUSAGE_SELF,&ru);
  const double seconds=std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count();
  std::cout<<"{\n"
    <<"  \"run\": \"LSPV-5/REFEREE394 one-post-cross sibling test\",\n"
    <<"  \"status\": \"COMPUTATIONAL_EXACT_FINITE\",\n"
    <<"  \"scope\": \"RES(C1,RES(C2,D)) with C1,C2 first cross resolvents and D side-local\",\n"
    <<"  \"left_unique_clauses\": "<<L.catalog.size()<<",\n"
    <<"  \"right_unique_clauses\": "<<R.catalog.size()<<",\n"
    <<"  \"all_first_cross_resolvents\": "<<all_cross<<",\n"
    <<"  \"support_four_first_cross_resolvents\": "<<cross4.size()<<",\n"
    <<"  \"support_four_or_five_first_cross_resolvents\": "<<cross45.size()<<",\n"
    <<"  \"post_candidate_side_clause_queries\": "<<post_candidate_queries<<",\n"
    <<"  \"post_catalog_hits\": "<<post_catalog_hits<<",\n"
    <<"  \"post_strict_resolution_patterns\": "<<post_strict<<",\n"
    <<"  \"post_support_at_most_four_patterns\": "<<post_support_at_most_four<<",\n"
    <<"  \"post_legal_mask_unions_before_minimization\": "<<post_legal_mask_unions<<",\n"
    <<"  \"post_unique_clauses\": "<<post.size()<<",\n"
    <<"  \"post_minimal_mask_pairs\": "<<post_mask_pairs<<",\n"
    <<"  \"final_clause_queries\": "<<final_clause_queries<<",\n"
    <<"  \"final_post_catalog_hits\": "<<final_catalog_hits<<",\n"
    <<"  \"final_strict_support_at_most_three_patterns\": "<<final_strict_small<<",\n"
    <<"  \"final_distinct_support_at_most_three_outputs\": "<<final_outputs.size()<<",\n"
    <<"  \"final_source_disjoint_realizations\": "<<final_disjoint<<",\n"
    <<"  \"falsifier_found\": "<<(best.exists?"true":"false")<<",\n"
    <<"  \"best_witness\": {\n"
    <<"    \"first_cross\": "<<clause_text(best.c1)<<",\n"
    <<"    \"post_cross_sibling\": "<<clause_text(best.post)<<",\n"
    <<"    \"output\": "<<clause_text(best.out)<<",\n"
    <<"    \"first_left_mask\": "<<best.c1l<<",\n"
    <<"    \"first_right_mask\": "<<best.c1r<<",\n"
    <<"    \"post_left_mask\": "<<best.postl<<",\n"
    <<"    \"post_right_mask\": "<<best.postr<<",\n"
    <<"    \"total_source_leaves\": "<<(best.exists?best.total:0)<<"\n"
    <<"  },\n"
    <<"  \"wall_seconds\": "<<std::fixed<<std::setprecision(6)<<seconds<<",\n"
    <<"  \"max_rss_kib\": "<<ru.ru_maxrss<<"\n"
    <<"}\n";
}
