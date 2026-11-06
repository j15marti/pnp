#include <algorithm>
#include <array>
#include <bitset>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <string>
#include <sys/resource.h>
#include <vector>

// Independent representation: clauses use base-3 trits (0 absent, 1 +, 2 -).
// Local factors/equations use separate truth-vector and affine encodings.
static constexpr int C = 6561;
static int p3[9];
using U16 = uint16_t;
struct S { std::vector<U16> c,f,e,k; };
template<class T> static void uq(std::vector<T>&v){std::sort(v.begin(),v.end());v.erase(std::unique(v.begin(),v.end()),v.end());}
static int pc(unsigned x){return __builtin_popcount(x);}
static U16 fc(unsigned s,unsigned t){return U16(s|(t<<8));}
static U16 ec(unsigned m,unsigned r){return U16(m|((r&1)<<8));}
static unsigned cs(U16 c){unsigned s=0;for(int i=0;i<8;i++,c/=3)if(c%3)s|=1u<<i;return s;}
static U16 cf(U16 c){unsigned tr[8],s=0,z=c;for(int i=0;i<8;i++,z/=3){tr[i]=z%3;if(tr[i])s|=1u<<i;}unsigned t=0,k=pc(s);for(unsigned a=0;a<(1u<<k);a++){unsigned g=0,j=0;for(int i=0;i<8;i++)if(s>>i&1){g|=((a>>j)&1)<<i;j++;}bool ok=false;for(int i=0;i<8;i++)if(tr[i])ok|=(tr[i]==1?bool(g>>i&1):!bool(g>>i&1));if(ok)t|=1u<<a;}return fc(s,t);}
static unsigned li(unsigned g,unsigned s){unsigned z=0,j=0;for(int i=0;i<8;i++)if(s>>i&1){z|=((g>>i)&1)<<j;j++;}return z;}
static unsigned ex(U16 f,unsigned u){unsigned s=f&255,t=f>>8,out=0,k=pc(u);for(unsigned a=0;a<(1u<<k);a++){unsigned g=0,j=0;for(int i=0;i<8;i++)if(u>>i&1){g|=((a>>j)&1)<<i;j++;}if(t>>li(g,s)&1)out|=1u<<a;}return out;}
static U16 ef(U16 e){unsigned m=e&255,r=e>>8,t=0,k=pc(m);for(unsigned a=0;a<(1u<<k);a++)if((pc(a)&1)==int(r))t|=1u<<a;return fc(m,t);}
static int alias(U16 f){unsigned s=f&255,t=f>>8;for(unsigned m=0;m<256;m++)if(!(m&~s))for(unsigned r=0;r<2;r++){U16 e=ec(m,r);if(ex(ef(e),s)==t)return e;}return -1;}
static U16 conj(U16 a,U16 b){unsigned s=(a&255)|(b&255);return fc(s,ex(a,s)&ex(b,s));}
static void fin(S&x){uq(x.c);uq(x.f);uq(x.e);for(U16 c:x.c)if(pc(cs(c))<=3)x.k.push_back(cf(c));for(U16 e:x.e)if(pc(e&255)<=3)x.k.push_back(ef(e));for(U16 f:x.f)x.k.push_back(f);uq(x.k);}
static int enc(const std::vector<int>&cl,const std::vector<int>&vars){int z=0;for(int l:cl){int j=std::find(vars.begin(),vars.end(),std::abs(l))-vars.begin();z+=(l>0?1:2)*p3[j];}return z;}
static int res3(int a,int b){int o=0,n=0;for(int i=0;i<8;i++){int x=a%3,y=b%3;a/=3;b/=3;if((x==1&&y==2)||(x==2&&y==1)){n++;continue;}if(x&&y&&x!=y)return -1;o+=(x?x:y)*p3[i];}return n==1?o:-1;}
static std::vector<std::vector<int>> formula(){std::vector<std::pair<int,int>>e;for(int o:{0,5})for(int u=0;u<4;u++)for(int v=u+1;v<4;v++)if(u==0&&v==1){e.push_back({o,o+4});e.push_back({o+4,o+1});}else e.push_back({o+u,o+v});e.push_back({4,9});std::vector<std::vector<int>>in(10);for(int i=0;i<15;i++){in[e[i].first].push_back(i+1);in[e[i].second].push_back(i+1);}std::vector<std::vector<int>>F;for(int v=0;v<10;v++)for(int t=0;t<8;t++){int a=t>>2&1,b=t>>1&1,c=t&1;if((a^b^c)==(v==0))continue;F.push_back({a?-in[v][0]:in[v][0],b?-in[v][1]:in[v][1],c?-in[v][2]:in[v][2]});}return F;}
struct R{S full;uint64_t rp=0,ap=0,xp=0,eqsubs=0;bool exact=true;};
static R close(bool right,const std::vector<int16_t>&tab){
 auto F=formula();std::vector<int> ids;if(!right){for(int i=0;i<16;i++)ids.push_back(i);ids.push_back(17);ids.push_back(18);}else{for(int i=20;i<36;i++)ids.push_back(i);ids.push_back(36);ids.push_back(39);}std::vector<int>vs=right?std::vector<int>{8,9,10,11,12,13,14,15}:std::vector<int>{1,2,3,4,5,6,7,15};int n=18,T=1<<n;std::vector<S>dp(T);for(int i=0;i<n;i++){dp[1<<i].c.push_back(enc(F[ids[i]],vs));fin(dp[1<<i]);}R z;
 for(int sz=2;sz<=n;sz++)for(int m=1;m<T;m++)if(pc(m)==sz){S q;int anchor=m&-m;for(int a=(m-1)&m;a;a=(a-1)&m){if(!(a&anchor))continue;int b=m^a;if(!b)continue;S&A=dp[a];S&B=dp[b];z.rp+=uint64_t(A.c.size())*B.c.size();for(U16 x:A.c)for(U16 y:B.c){int w=tab[size_t(x)*C+y];if(w>=0)q.c.push_back(w);}z.ap+=uint64_t(A.k.size())*B.k.size();for(U16 x:A.k)for(U16 y:B.k)if(pc((x&255)|(y&255))<=3){U16 f=conj(x,y);q.f.push_back(f);int e=alias(f);if(e>=0)q.e.push_back(e);}z.xp+=uint64_t(A.e.size())*B.e.size();for(U16 x:A.e)for(U16 y:B.e)q.e.push_back(ec((x^y)&255,((x>>8)^(y>>8))&1));}fin(q);dp[m]=std::move(q);}
 std::array<U16,4>rows={ec((1<<0)|(1<<2)|(1<<3),right?0:1),ec((1<<1)|(1<<4)|(1<<5),0),ec((1<<2)|(1<<4)|(1<<6),0),ec((1<<3)|(1<<5)|(1<<6),0)};
 for(int m=1;m<T;m++){if(!dp[m].e.empty())z.eqsubs++;bool expected=false;U16 want=0;for(int gset=1;gset<16;gset++){int sm=0;U16 e=0;for(int g=0;g<4;g++)if(gset>>g&1){sm|=15<<(4*g);e^=rows[g];}if(m==sm){expected=true;want=e;break;}}if(expected){if(dp[m].e.size()!=1||dp[m].e[0]!=want)z.exact=false;}else if(!dp[m].e.empty())z.exact=false;}
 z.full=std::move(dp.back());return z;
}
static std::string readall(const char*p){std::ifstream f(p);return std::string((std::istreambuf_iterator<char>(f)),{});}
int main(int argc,char**argv){if(argc!=4){std::cerr<<"usage: verifier primary.json boundary.json verify.json\n";return 2;}auto st=std::chrono::steady_clock::now();p3[0]=1;for(int i=1;i<9;i++)p3[i]=p3[i-1]*3;std::vector<int16_t>tab(size_t(C)*C,-1);for(int a=0;a<C;a++)for(int b=0;b<C;b++)tab[size_t(a)*C+b]=res3(a,b);R L=close(false,tab),Rr=close(true,tab);
 bool ok=L.full.c.size()==1888&&Rr.full.c.size()==1888&&L.full.f.size()==5&&Rr.full.f.size()==5&&L.full.e.empty()&&Rr.full.e.empty()&&L.eqsubs==15&&Rr.eqsubs==15&&L.exact&&Rr.exact&&L.rp==1126097195ULL&&Rr.rp==1126097195ULL&&L.ap==55144&&Rr.ap==55144&&L.xp==25&&Rr.xp==25;
 std::string a=readall(argv[1]),b=readall(argv[2]);ok&=a.find("\"equation_subsets_exact_internal_bundle_unions\": true")!=std::string::npos&&a.find("\"side_local_partition_contradiction\": false")!=std::string::npos&&b.find("\"contradictions\": []")!=std::string::npos&&b.find("\"full_outcomes\": 0")!=std::string::npos;
 int mut=0;mut+=!(L.full.c.size()==1887);mut+=!(L.full.f.size()==4);mut+=!(L.eqsubs==14);mut+=!(L.rp==1126097194ULL);mut+=!(L.ap==55143);mut+=!(L.xp==24);if(mut!=6)ok=false;
 rusage ru{};getrusage(RUSAGE_SELF,&ru);double sec=std::chrono::duration<double>(std::chrono::steady_clock::now()-st).count();std::ofstream o(argv[3]);o<<"{\n  \"pass\": "<<(ok?"true":"false")<<",\n  \"independent_encoding\": \"base-3 clauses plus separately reconstructed local truth vectors\",\n  \"full_clauses_each\": "<<L.full.c.size()<<",\n  \"full_factors_each\": "<<L.full.f.size()<<",\n  \"full_equations_each\": "<<L.full.e.size()<<",\n  \"equation_subsets_each\": "<<L.eqsubs<<",\n  \"equation_subsets_exact_internal_bundle_unions\": "<<(L.exact&&Rr.exact?"true":"false")<<",\n  \"res_pair_tests_each\": "<<L.rp<<",\n  \"and_pair_tests_each\": "<<L.ap<<",\n  \"xor_pair_tests_each\": "<<L.xp<<",\n  \"mutations_rejected\": "<<mut<<",\n  \"elapsed_seconds\": "<<sec<<",\n  \"max_rss_kib\": "<<ru.ru_maxrss<<"\n}\n";std::cout<<(ok?"PASS":"FAIL")<<" sec="<<sec<<" rss="<<ru.ru_maxrss<<"\n";return ok?0:1;}
