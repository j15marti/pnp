#include <bits/stdc++.h>
using namespace std;

struct Clause { int v[3]; int s[3]; };
struct Stats { unsigned long long nodes=0, decisions=0, conflicts=0; };

vector<Clause> gen_formula(int n,int m,mt19937_64&rng){
    unordered_set<unsigned long long> seen; seen.reserve(m*2+1);
    vector<Clause> F; F.reserve(m);
    uniform_int_distribution<int> D(0,n-1), S(0,1);
    while((int)F.size()<m){
        int x=D(rng),y=D(rng),z=D(rng);
        if(x==y||x==z||y==z) continue;
        array<int,3> vv{x,y,z}; sort(vv.begin(),vv.end());
        int pat=S(rng)|(S(rng)<<1)|(S(rng)<<2);
        unsigned long long key=pat;
        for(int j=0;j<3;j++) key=key*(unsigned long long)n+vv[j];
        if(!seen.insert(key).second) continue;
        Clause c;
        for(int j=0;j<3;j++){c.v[j]=vv[j];c.s[j]=(pat>>j)&1;}
        F.push_back(c);
    }
    return F;
}
static inline int litval(const Clause&c,int j,const vector<int8_t>&a){
    int x=a[c.v[j]]; if(x<0)return -1; return c.s[j]?x:1-x;
}
bool unitprop(const vector<Clause>&F,vector<int8_t>&a,Stats&st){
    bool ch=true;
    while(ch){
        ch=false;
        for(auto &c:F){
            bool sat=false; int un=0,last=-1;
            for(int j=0;j<3;j++){int z=litval(c,j,a); if(z==1){sat=true;break;} if(z<0){un++;last=j;}}
            if(sat)continue;
            if(un==0){st.conflicts++;return false;}
            if(un==1){
                int val=c.s[last]?1:0,v=c.v[last];
                if(a[v]>=0&&a[v]!=val){st.conflicts++;return false;}
                if(a[v]<0){a[v]=val;ch=true;}
            }
        }
    }
    return true;
}
bool allsat(const vector<Clause>&F,const vector<int8_t>&a){
    for(auto &c:F){bool sat=false;for(int j=0;j<3;j++)if(litval(c,j,a)==1){sat=true;break;}if(!sat)return false;}
    return true;
}
int choosevar(const vector<Clause>&F,const vector<int8_t>&a){
    vector<int> sc(a.size());
    for(auto &c:F){
        bool sat=false;for(int j=0;j<3;j++)if(litval(c,j,a)==1){sat=true;break;}
        if(sat)continue;for(int j=0;j<3;j++)if(a[c.v[j]]<0)sc[c.v[j]]++;
    }
    int b=-1,bs=-1;for(int v=0;v<(int)a.size();v++)if(a[v]<0&&sc[v]>bs){bs=sc[v];b=v;}return b;
}
bool dpll(const vector<Clause>&F,vector<int8_t>a,Stats&st){
    st.nodes++; if(!unitprop(F,a,st))return false; if(allsat(F,a))return true;
    int v=choosevar(F,a); if(v<0)return false; st.decisions++;
    a[v]=1;if(dpll(F,a,st))return true;a[v]=0;return dpll(F,a,st);
}
double qtile(vector<unsigned long long> v,double q){
    sort(v.begin(),v.end());double x=q*(v.size()-1);size_t i=floor(x),j=ceil(x);
    if(i==j)return v[i];return v[i]*(j-x)+v[j]*(x-i);
}
int main(int argc,char**argv){
    int samples=100;if(argc>1)samples=stoi(argv[1]);
    const unsigned long long seed=20261003ULL;
    vector<int> ns={64,96,128};
    vector<double> alphas={3.0,4.0,4.25,4.5,5.0,5.25,6.0,8.0};
    cout<<"n,alpha,m,samples,unsat,sat_frac,median_nodes,p90_nodes,mean_nodes\n";
    for(int n:ns)for(double alpha:alphas){
        int m=llround(alpha*n),unsat=0;vector<unsigned long long> nodes;long double sum=0;
        for(int s=0;s<samples;s++){
            mt19937_64 rng(seed ^ (unsigned long long)n*0x9e3779b97f4a7c15ULL ^
                           (unsigned long long)m*0xbf58476d1ce4e5b9ULL ^
                           (unsigned long long)s*0x94d049bb133111ebULL);
            auto F=gen_formula(n,m,rng);vector<int8_t>a(n,-1);Stats st;bool sat=dpll(F,a,st);
            unsat+=!sat;nodes.push_back(st.nodes);sum+=st.nodes;
        }
        cout<<n<<","<<fixed<<setprecision(2)<<alpha<<","<<m<<","<<samples<<","<<unsat<<","
            <<setprecision(6)<<(double)(samples-unsat)/samples<<","
            <<(unsigned long long)llround(qtile(nodes,.5))<<","
            <<(unsigned long long)llround(qtile(nodes,.9))<<","
            <<setprecision(3)<<(double)(sum/samples)<<"\n";
    }
}
