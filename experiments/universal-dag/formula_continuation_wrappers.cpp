#define main formula_continuation_original_main
#include "/mnt/data/formula_continuation_quotient.cpp"
#undef main
int main(){
    Family b=make_2sat3(); SmallExact E0(b); E0.optimize_order();
    Family dead=b; Constraint d; d.falsify=0; d.label="DEAD_TAUTOLOGY"; dead.cs.push_back(d); SmallExact ED(dead); ED.optimize_order();
    Family copy=b; copy.cs.push_back(copy.cs[0]); copy.cs.back().label="COPY_CLAUSE0"; SmallExact EC(copy); EC.optimize_order();
    cout<<"variant,constraints,exact_min_peak\n";
    cout<<"BASE,"<<E0.M<<","<<*max_element(E0.profile.begin(),E0.profile.end())<<"\n";
    cout<<"DEAD,"<<ED.M<<","<<*max_element(ED.profile.begin(),ED.profile.end())<<"\n";
    cout<<"COPY,"<<EC.M<<","<<*max_element(EC.profile.begin(),EC.profile.end())<<"\n";
    cerr<<"DEAD profile:";for(int x:ED.profile)cerr<<" "<<x;cerr<<"\nCOPY profile:";for(int x:EC.profile)cerr<<" "<<x;cerr<<"\n";
}
