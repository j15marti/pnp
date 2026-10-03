#include <bits/stdc++.h>
using namespace std;
struct Node{int var=-1,lo=0,hi=0;};

int main(int argc,char**argv){
    if(argc!=2){cerr<<"usage: verify_d4_fbdd <d4_fbdd_301.csv>\n";return 2;}
    ifstream f(argv[1]); if(!f){cerr<<"open failed\n";return 2;}
    string line; getline(f,line);
    vector<Node> a(303);
    int id,v,l,h; char c;
    while(f>>id>>c>>v>>c>>l>>c>>h) a[id]={v,l,h};
    const int root=302;

    vector<pair<int,int>> edges;
    for(int i=0;i<4;i++)for(int j=i+1;j<4;j++)for(int k=j+1;k<4;k++){
        int T[3]={i,j,k};
        for(int pat=0;pat<8;pat++){
            vector<int> vs;
            for(int x=0;x<16;x++){
                bool ok=true;
                for(int z=0;z<3;z++)
                    if(((x>>T[z])&1)!=((pat>>z)&1)){ok=false;break;}
                if(ok)vs.push_back(x);
            }
            if(vs.size()!=2) return 3;
            edges.push_back({min(vs[0],vs[1]),max(vs[0],vs[1])});
        }
    }

    vector<unsigned long long> memo(303,ULLONG_MAX);
    function<unsigned long long(int)> labs=[&](int u)->unsigned long long{
        if(u<2)return 0;
        if(memo[u]!=ULLONG_MAX)return memo[u];
        auto n=a[u];
        auto below=labs(n.lo)|labs(n.hi);
        if((below>>n.var)&1ULL){
            cerr<<"READ_ONCE_FAIL node "<<u<<" var "<<n.var<<"\n"; exit(4);
        }
        return memo[u]=below|(1ULL<<n.var);
    };
    auto used=labs(root);

    auto eval=[&](uint32_t x){
        int u=root,steps=0;
        while(u>=2){
            auto n=a[u];
            u=((x>>n.var)&1U)?n.hi:n.lo;
            if(++steps>32) exit(5);
        }
        return pair<int,int>{u,steps};
    };

    unsigned long long total=0,pos=0,neg=0; int maxd=0;
    uint64_t x=(1ULL<<8)-1, limit=1ULL<<32;
    while(x<limit){
        uint32_t m=(uint32_t)x;
        int deg[16]={0}; bool pm=true;
        for(int e=0;e<32;e++) if((m>>e)&1U){
            auto [p,q]=edges[e];
            if(++deg[p]>1 || ++deg[q]>1) pm=false;
        }
        if(pm) for(int z=0;z<16;z++) if(deg[z]!=1){pm=false;break;}
        auto [y,d]=eval(m); maxd=max(maxd,d);
        if(y!=(int)pm){
            cerr<<"MISMATCH mask="<<m<<" expected="<<pm<<" got="<<y<<"\n";
            return 6;
        }
        total++; pos+=pm; neg+=!pm;
        uint64_t low=x&-x, r=x+low;
        if(r>=limit)break;
        x=(((r^x)>>2)/low)|r;
    }
    cout<<"PASS\n";
    cout<<"promised_inputs "<<total<<"\n";
    cout<<"perfect_matchings "<<pos<<"\n";
    cout<<"nonmatchings "<<neg<<"\n";
    cout<<"internal_nodes 301\n";
    cout<<"max_depth "<<maxd<<"\n";
    cout<<"queried_variables_global "<<__builtin_popcountll(used)<<"\n";
}
