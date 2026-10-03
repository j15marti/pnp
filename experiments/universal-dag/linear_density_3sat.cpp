#include <bits/stdc++.h>
using namespace std;

struct Clause { int v[3]; int s[3]; };
struct Stats { uint64_t nodes=0, decisions=0, conflicts=0; };

static inline int litval(const Clause& c,int j,const vector<int8_t>& a){
    int x=a[c.v[j]];
    if(x<0) return -1;
    return c.s[j] ? x : 1-x;
}

bool unit_propagate(const vector<Clause>& F, vector<int8_t>& a, Stats& st){
    bool changed=true;
    while(changed){
        changed=false;
        for(auto &c:F){
            bool sat=false; int un=0, last=-1;
            for(int j=0;j<3;j++){
                int z=litval(c,j,a);
                if(z==1){ sat=true; break; }
                if(z<0){un++; last=j;}
            }
            if(sat) continue;
            if(un==0){ st.conflicts++; return false; }
            if(un==1){
                int val=c.s[last]?1:0;
                int v=c.v[last];
                if(a[v]>=0 && a[v]!=val){ st.conflicts++; return false; }
                if(a[v]<0){ a[v]=val; changed=true; }
            }
        }
    }
    return true;
}

bool all_sat(const vector<Clause>&F,const vector<int8_t>&a){
    for(auto &c:F){
        bool sat=false;
        for(int j=0;j<3;j++){
            int z=litval(c,j,a);
            if(z==1){sat=true;break;}
        }
        if(!sat) return false;
    }
    return true;
}

int choose_var(const vector<Clause>&F,const vector<int8_t>&a){
    int n=a.size(); vector<int> score(n,0);
    for(auto &c:F){
        bool sat=false;
        for(int j=0;j<3;j++){ int z=litval(c,j,a); if(z==1){sat=true;break;} }
        if(sat) continue;
        for(int j=0;j<3;j++) if(a[c.v[j]]<0) score[c.v[j]]++;
    }
    int best=-1, bs=-1;
    for(int v=0;v<n;v++) if(a[v]<0 && score[v]>bs){bs=score[v];best=v;}
    return best;
}

bool dpll(const vector<Clause>&F, vector<int8_t> a, Stats& st){
    st.nodes++;
    if(!unit_propagate(F,a,st)) return false;
    if(all_sat(F,a)) return true;
    int v=choose_var(F,a);
    if(v<0) return false;
    st.decisions++;
    a[v]=1; if(dpll(F,a,st)) return true;
    a[v]=0; return dpll(F,a,st);
}

vector<Clause> gen_formula(int n,int m,mt19937_64&rng){
    unordered_set<uint64_t> seen; seen.reserve(m*2+1);
    vector<Clause> F; F.reserve(m);
    uniform_int_distribution<int> D(0,n-1), S(0,1);
    while((int)F.size()<m){
        int x=D(rng),y=D(rng),z=D(rng);
        if(x==y||x==z||y==z) continue;
        array<int,3> vv{x,y,z}; sort(vv.begin(),vv.end());
        int pat=S(rng)|(S(rng)<<1)|(S(rng)<<2);
        uint64_t key=pat;
        for(int j=0;j<3;j++) key=key*64+vv[j];
        if(!seen.insert(key).second) continue;
        Clause c;
        for(int j=0;j<3;j++){c.v[j]=vv[j]; c.s[j]=(pat>>j)&1;}
        F.push_back(c);
    }
    return F;
}

double quantile(vector<uint64_t> v,double q){
    if(v.empty())return 0;
    sort(v.begin(),v.end());
    double x=q*(v.size()-1);
    size_t i=floor(x),j=ceil(x);
    if(i==j)return v[i];
    return v[i]*(j-x)+v[j]*(x-i);
}

int main(int argc,char**argv){
    int samples=100; if(argc>1) samples=stoi(argv[1]);
    uint64_t seed=20261003ULL; if(argc>2) seed=stoull(argv[2]);
    vector<int> ns={8,12,16,20,24,28,32};
    vector<double> alphas={1.0,4.0/3.0,2.0,3.0,4.0,4.25,4.5,5.0};

    cout<<"n,alpha,m,samples,sat_frac,median_nodes,p90_nodes,max_nodes,median_decisions,p90_decisions,mean_nodes\n";
    for(int n:ns){
        long long M=8LL*n*(n-1)*(n-2)/6;
        for(double alpha:alphas){
            int m=max(1,(int)llround(alpha*n));
            if(m>M) continue;
            vector<uint64_t> nodes,decisions;
            nodes.reserve(samples); decisions.reserve(samples);
            int sat=0; long double sum=0;
            for(int s=0;s<samples;s++){
                mt19937_64 rng(seed ^ (uint64_t)n*0x9e3779b97f4a7c15ULL ^
                               (uint64_t)m*0xbf58476d1ce4e5b9ULL ^
                               (uint64_t)s*0x94d049bb133111ebULL);
                auto F=gen_formula(n,m,rng);
                vector<int8_t>a(n,-1); Stats st;
                bool ok=dpll(F,a,st);
                sat+=ok;
                nodes.push_back(st.nodes);
                decisions.push_back(st.decisions);
                sum+=st.nodes;
            }
            cout<<n<<","<<fixed<<setprecision(4)<<alpha<<","<<m<<","<<samples<<","
                <<setprecision(4)<<(double)sat/samples<<","
                <<(uint64_t)llround(quantile(nodes,.5))<<","
                <<(uint64_t)llround(quantile(nodes,.9))<<","
                <<*max_element(nodes.begin(),nodes.end())<<","
                <<(uint64_t)llround(quantile(decisions,.5))<<","
                <<(uint64_t)llround(quantile(decisions,.9))<<","
                <<setprecision(3)<<(double)(sum/samples)<<"\n";
        }
    }
}
