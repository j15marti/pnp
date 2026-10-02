#include <bits/stdc++.h>
using namespace std;

// Exact finite baseline for simple full 3-CNF formulas.
// Each clause chooses 3 distinct variables and one falsifying sign pattern.
// For each m-clause set, record the union of assignments falsified by its clauses.

int main(int argc,char**argv){
 int n=4,m=8;
 if(argc>1) n=stoi(argv[1]);
 if(argc>2) m=stoi(argv[2]);
 if(n<3 || n>5){ cerr<<"baseline supports 3<=n<=5\n"; return 2; }
 int A=1<<n;
 vector<uint32_t> clauses;
 for(int i=0;i<n;i++) for(int j=i+1;j<n;j++) for(int k=j+1;k<n;k++){
   int vars[3]={i,j,k};
   for(int pat=0;pat<8;pat++){
     uint32_t mask=0;
     for(int a=0;a<A;a++){
       bool match=true;
       for(int t=0;t<3;t++) if(((a>>vars[t])&1)!=((pat>>t)&1)){match=false;break;}
       if(match) mask|=(1u<<a);
     }
     clauses.push_back(mask);
   }
 }
 int C=clauses.size();
 if(m<0 || m>C){cerr<<"bad m\n"; return 2;}
 long double combos=1; for(int i=1;i<=m;i++) combos=combos*(C-m+i)/i;
 if(combos>2e8L){cerr<<"refusing >2e8 combinations in exact baseline\n"; return 3;}
 unordered_map<uint32_t,uint64_t> freq; freq.reserve(1<<min(A,20));
 vector<int> c(m); iota(c.begin(),c.end(),0);
 uint64_t total=0,unsat=0; uint32_t full=(A==32?0xFFFFFFFFu:((1u<<A)-1));
 if(m==0){freq[0]=1;total=1;} else while(true){
   uint32_t cov=0; for(int q:c) cov|=clauses[q];
   freq[cov]++; total++; if(cov==full) unsat++;
   int p=m-1; while(p>=0 && c[p]==C-m+p) p--; if(p<0) break;
   c[p]++; for(int q=p+1;q<m;q++) c[q]=c[q-1]+1;
 }
 map<int,uint64_t> distinct_by_covered;
 for(auto &kv:freq) distinct_by_covered[__builtin_popcount(kv.first)]++;
 cout<<"n "<<n<<" m "<<m<<" possible_clauses "<<C<<" total_formulas "<<total
     <<" distinct_semantic_masks "<<freq.size()<<" unsat_formulas "<<unsat<<"\n";
 for(auto [pc,cnt]:distinct_by_covered) cout<<"covered_assignments "<<pc<<" distinct_masks "<<cnt<<"\n";
}
