#include <bits/stdc++.h>
using namespace std;
struct E{int u,v;};
int main(){
    vector<E> ed; map<pair<int,int>,int> id;
    for(int v=0;v<16;v++)for(int d=0;d<4;d++){
        int w=v^(1<<d); if(v<w){id[{v,w}]=ed.size();ed.push_back({v,w});}
    }
    int inc[16][4];
    for(int v=0;v<16;v++)for(int d=0;d<4;d++){
        int w=v^(1<<d); auto p=minmax(v,w); inc[v][d]=id[p];
    }
    int ord[16][4]={
      {1,3,0,2},{2,0,3,1},{2,0,3,1},{1,3,0,2},
      {2,3,1,0},{0,3,1,2},{0,1,3,2},{2,1,3,0},
      {2,0,3,1},{1,3,0,2},{1,3,0,2},{2,0,3,1},
      {0,1,3,2},{2,1,3,0},{2,3,1,0},{0,3,1,2}
    };
    auto direct=[&](uint32_t m){
        for(int v=0;v<16;v++){
            bool c=0; for(int d=0;d<4;d++) if((m>>inc[v][d])&1U){c=1;break;}
            if(!c)return false;
        } return true;
    };
    auto bp=[&](uint32_t m){
        int q=0; array<int,32> reads{};
        for(int v=0;v<16;v++){
            bool c=0;
            for(int j=0;j<4;j++){
                int e=inc[v][ord[v][j]]; q++; reads[e]++;
                if((m>>e)&1U){c=1;break;}
            }
            if(!c){
                int rep=0;for(int x:reads)rep+=(x>1);
                return tuple<bool,int,int>(false,q,rep);
            }
        }
        int rep=0;for(int x:reads)rep+=(x>1);
        return tuple<bool,int,int>(true,q,rep);
    };
    unsigned long long total=0,covers=0,bad=0; int maxq=0,maxrep=0;
    uint64_t x=(1ULL<<8)-1, lim=1ULL<<32;
    while(x<lim){
        uint32_t m=(uint32_t)x; auto [g,q,r]=bp(m); bool f=direct(m);
        total++;covers+=f;bad+=(f!=g);maxq=max(maxq,q);maxrep=max(maxrep,r);
        uint64_t c=x&-x,y=x+c;if(y>=lim)break;x=(((x^y)>>2)/c)|y;
    }
    cout<<"weight8_total="<<total<<" edgecovers="<<covers<<" mismatches="<<bad
        <<" max_queries="<<maxq<<" max_repeated_variables="<<maxrep<<"\n";
}
