#define main referee393_main_disabled
#include "lspv5_393_double_cross_resolution.cpp"
#undef main

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

// REFEREE395: exact source-authenticated test for
//   RES(C1, RES(RES(C2,D1),D2)),
// where C1,C2 are first cross-cut resolvents and D1,D2 are side-local.
// The support ceilings 4,5,6 are forced backwards from a final support <=3.

struct Pair395 { unsigned l=0,r=0; };
struct Info395 { std::vector<Pair395> masks; };
using Catalog395=std::map<uint32_t,Info395>;

static void add395(Info395&info,unsigned l,unsigned r){
  for(const auto&m:info.masks)
    if((m.l&l)==m.l&&(m.r&r)==m.r)return;
  info.masks.erase(std::remove_if(info.masks.begin(),info.masks.end(),
    [l,r](const Pair395&m){return (m.l&l)==l&&(m.r&r)==r;}),info.masks.end());
  info.masks.push_back({l,r});
}

static uint64_t mask_count395(const Catalog395&cat){
  uint64_t n=0;for(const auto&[_,i]:cat)n+=i.masks.size();return n;
}

struct StepCounts395 {
  uint64_t input_mask_states=0,candidate_queries=0,strict=0,small=0;
  uint64_t legal_mask_unions=0;
};

static Catalog395 extend395(const Catalog395&in,unsigned output_ceiling,
                            const SideClosure&L,const SideClosure&R,
                            StepCounts395&counts){
  Catalog395 out;
  std::map<std::pair<unsigned,bool>,std::vector<std::pair<uint32_t,const MaskInfo*>>> cache;
  for(const auto&[a,ainfo]:in){
    const unsigned support=clause_support(a),s=pc(support);
    for(const Pair395&am:ainfo.masks){
      counts.input_mask_states++;
      for(unsigned side=0;side<2;side++){
        const bool right=side;
        const Catalog&local=right?R.catalog:L.catalog;
        auto key=std::make_pair(support,right);
        auto it=cache.find(key);
        if(it==cache.end()){
          std::vector<std::pair<uint32_t,const MaskInfo*>> candidates;
          const unsigned outside_budget=output_ceiling+1-s;
          for(const auto&[d,di]:local)
            if(unsigned(pc(clause_support(d)&~support))<=outside_budget)
              candidates.push_back({d,&di});
          it=cache.emplace(key,std::move(candidates)).first;
        }
        for(const auto&[d,di]:it->second){
          counts.candidate_queries++;
          const int z=strict_resolve_global(a,d);if(z<0)continue;
          counts.strict++;
          const uint32_t b=uint32_t(z);if(unsigned(pc(clause_support(b)))>output_ceiling)continue;
          counts.small++;
          const unsigned used=right?am.r:am.l;
          for(unsigned dm:di->minimal_masks){
            if(used&dm)continue;
            counts.legal_mask_unions++;
            if(right)add395(out[b],am.l,am.r|dm);
            else add395(out[b],am.l|dm,am.r);
          }
        }
      }
    }
  }
  return out;
}

struct Witness395{
  bool exists=false;uint32_t c1=0,p2=0,out=0;
  unsigned c1l=0,c1r=0,p2l=0,p2r=0,total=999;
};

int main(){
  const auto start=std::chrono::steady_clock::now();
  SideClosure L=close_side(false),R=close_side(true);
  uint64_t all_cross=0,cross4_patterns=0,cross456_patterns=0;
  Catalog395 cross4,cross456;
  for(const auto&[l,li]:L.catalog)for(const auto&[r,ri]:R.catalog){
    const int z=strict_resolve_global(l,r);if(z<0)continue;all_cross++;
    const uint32_t c=uint32_t(z);const unsigned s=pc(clause_support(c));
    if(s<4||s>6)continue;
    cross456_patterns++;if(s==4)cross4_patterns++;
    for(unsigned lm:li.minimal_masks)for(unsigned rm:ri.minimal_masks){
      add395(cross456[c],lm,rm);
      if(s==4)add395(cross4[c],lm,rm);
    }
  }

  StepCounts395 s1,s2;
  Catalog395 post1=extend395(cross456,5,L,R,s1);
  Catalog395 post2=extend395(post1,4,L,R,s2);

  uint64_t final_clause_queries=0,final_hits=0,final_strict_small=0,final_disjoint=0;
  std::set<uint32_t> outputs;Witness395 best;
  for(const auto&[c1,c1info]:cross4){
    for(uint32_t p2:signed_clauses_on_support(clause_support(c1))){
      final_clause_queries++;
      auto it=post2.find(p2);if(it==post2.end())continue;final_hits++;
      const int z=strict_resolve_global(c1,p2);if(z<0)continue;
      const uint32_t out=uint32_t(z);if(pc(clause_support(out))>3)continue;
      final_strict_small++;outputs.insert(out);
      for(const Pair395&a:c1info.masks)for(const Pair395&b:it->second.masks){
        if((a.l&b.l)||(a.r&b.r))continue;
        final_disjoint++;
        const unsigned total=pc(a.l)+pc(a.r)+pc(b.l)+pc(b.r);
        if(!best.exists||total<best.total)
          best={true,c1,p2,out,a.l,a.r,b.l,b.r,total};
      }
    }
  }

  rusage ru{};getrusage(RUSAGE_SELF,&ru);
  const double seconds=std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count();
  std::cout<<"{\n"
    <<"  \"run\": \"LSPV-5/REFEREE395 two-post-cross chain test\",\n"
    <<"  \"status\": \"COMPUTATIONAL_EXACT_FINITE\",\n"
    <<"  \"scope\": \"RES(C1,RES(RES(C2,D1),D2)); C1,C2 first cross, D1,D2 side-local\",\n"
    <<"  \"left_unique_clauses\": "<<L.catalog.size()<<",\n"
    <<"  \"right_unique_clauses\": "<<R.catalog.size()<<",\n"
    <<"  \"all_first_cross_resolvents\": "<<all_cross<<",\n"
    <<"  \"support_four_first_cross_patterns\": "<<cross4_patterns<<",\n"
    <<"  \"support_four_to_six_first_cross_patterns\": "<<cross456_patterns<<",\n"
    <<"  \"support_four_unique_cross_clauses\": "<<cross4.size()<<",\n"
    <<"  \"support_four_cross_minimal_mask_pairs\": "<<mask_count395(cross4)<<",\n"
    <<"  \"support_four_to_six_unique_cross_clauses\": "<<cross456.size()<<",\n"
    <<"  \"support_four_to_six_cross_minimal_mask_pairs\": "<<mask_count395(cross456)<<",\n"
    <<"  \"post1_input_mask_states\": "<<s1.input_mask_states<<",\n"
    <<"  \"post1_candidate_queries\": "<<s1.candidate_queries<<",\n"
    <<"  \"post1_strict_patterns\": "<<s1.strict<<",\n"
    <<"  \"post1_support_at_most_five_patterns\": "<<s1.small<<",\n"
    <<"  \"post1_legal_mask_unions\": "<<s1.legal_mask_unions<<",\n"
    <<"  \"post1_unique_clauses\": "<<post1.size()<<",\n"
    <<"  \"post1_minimal_mask_pairs\": "<<mask_count395(post1)<<",\n"
    <<"  \"post2_input_mask_states\": "<<s2.input_mask_states<<",\n"
    <<"  \"post2_candidate_queries\": "<<s2.candidate_queries<<",\n"
    <<"  \"post2_strict_patterns\": "<<s2.strict<<",\n"
    <<"  \"post2_support_at_most_four_patterns\": "<<s2.small<<",\n"
    <<"  \"post2_legal_mask_unions\": "<<s2.legal_mask_unions<<",\n"
    <<"  \"post2_unique_clauses\": "<<post2.size()<<",\n"
    <<"  \"post2_minimal_mask_pairs\": "<<mask_count395(post2)<<",\n"
    <<"  \"final_clause_queries\": "<<final_clause_queries<<",\n"
    <<"  \"final_post2_catalog_hits\": "<<final_hits<<",\n"
    <<"  \"final_strict_support_at_most_three_patterns\": "<<final_strict_small<<",\n"
    <<"  \"final_distinct_support_at_most_three_outputs\": "<<outputs.size()<<",\n"
    <<"  \"final_source_disjoint_realizations\": "<<final_disjoint<<",\n"
    <<"  \"falsifier_found\": "<<(best.exists?"true":"false")<<",\n"
    <<"  \"best_witness\": {\n"
    <<"    \"first_cross\": "<<clause_text(best.c1)<<",\n"
    <<"    \"two_post_sibling\": "<<clause_text(best.p2)<<",\n"
    <<"    \"output\": "<<clause_text(best.out)<<",\n"
    <<"    \"first_left_mask\": "<<best.c1l<<",\n"
    <<"    \"first_right_mask\": "<<best.c1r<<",\n"
    <<"    \"sibling_left_mask\": "<<best.p2l<<",\n"
    <<"    \"sibling_right_mask\": "<<best.p2r<<",\n"
    <<"    \"total_source_leaves\": "<<(best.exists?best.total:0)<<"\n"
    <<"  },\n"
    <<"  \"wall_seconds\": "<<std::fixed<<std::setprecision(6)<<seconds<<",\n"
    <<"  \"max_rss_kib\": "<<ru.ru_maxrss<<"\n"
    <<"}\n";
}
