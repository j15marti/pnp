function runRT14(){
const out={assertions:0,gateWords:0,compiledCases:0,sat:0,unsat:0,sourceWords:0,starChecks:0,closureScans:0,closurePins:0,guardNodes:0,peakDepth:0,greedyChecks:0,momentChecks:0,trellisTransitions:0,trellisPeak:0,neighbors:[],seed:20261124};
function ok(x,m){out.assertions++;if(!x)throw Error(m);}
let seed=out.seed>>>0;function rand(n){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return (seed>>>8)%n;}
function par(x){x>>>=0;let p=0;while(x){p^=1;x&=x-1;}return p;}
function top(x){return 31-Math.clz32(x);}
function basis(){return Array(30).fill(null);}
function reduce(B,m,b=0){while(m){let p=top(m);if(!B[p])break;b^=B[p][1];m^=B[p][0];}return [m,b];}
function add(B,m,b=0){let [r,s]=reduce(B,m,b);if(!r)return s?-1:0;B[top(r)]=[r,s];return 1;}
function rank(B){return B.filter(Boolean).length;}
function value(B){let w=0;for(let p=0;p<B.length;p++)if(B[p]&&(par(B[p][0]&w)^B[p][1]))w|=1<<p;return w;}
const bit=i=>({m:1<<i,c:0}),zero={m:0,c:0};
const ev=(f,w)=>par(f.m&w)^f.c;
function lifts(x,y,z){out.starChecks++;const a=x+2*z,b=1+2*y;let allowed=[];for(let h=0;h<4;h++)if(![0,a,b,a^b].includes(h))allowed.push(h);return allowed;}
for(let x=0;x<2;x++)for(let y=0;y<2;y++)for(let z=0;z<2;z++){out.gateWords++;ok(lifts(x,y,z).length===(z===(x&y)?2:0),"gate truth and multiplicity");}
function closure(B,G){
for(;;){let changed=false;
for(const g of G){out.closureScans++;const legal=[];
for(let v=0;v<8;v++){const C=B.slice();let feasible=true;for(let j=0;j<3;j++)if(add(C,g[j].m,((v>>j)&1)^g[j].c)<0){feasible=false;break;}if(feasible&&lifts(v&1,(v>>1)&1,(v>>2)&1).length)legal.push(v);}
if(!legal.length)return false;
for(let mask=1;mask<8;mask++){let s=par(legal[0]&mask);if(legal.some(v=>par(v&mask)!==s))continue;let m=0,c=s;for(let j=0;j<3;j++)if(mask&(1<<j)){m^=g[j].m;c^=g[j].c;}let a=add(B,m,c);ok(a>=0,"closure consistency");if(a>0){out.closurePins++;changed=true;break;}}
if(changed)break;}
if(!changed)return true;}
}
function greedy(G,B){let C=B.map(x=>x?[x[0],0]:null), pins=[];for(const [x,y] of G){if(!reduce(C,x.m)[0]||!reduce(C,y.m)[0])continue;for(const f of [x,y])if(add(C,f.m)>0)pins.push(f.m);}for(const [x,y] of G)ok(!reduce(C,x.m)[0]||!reduce(C,y.m)[0],"cover");return pins;}
function literalFalse(l){return {m:1<<(Math.abs(l)-1),c:l>0?1:0};}
function compile(n,F){let G=[];F.forEach((cl,j)=>{let [a,b,c]=cl.map(literalFalse),p=bit(n+j);G.push([a,b,p],[p,c,zero]);});return G;}
function source(n,F){let count=0;for(let w=0;w<(1<<n);w++){out.sourceWords++;if(F.every(cl=>cl.some(l=>!ev(literalFalse(l),w))))count++;}return count;}
function solve(n,F){const G=compile(n,F), d=n+F.length, B=basis();let root=closure(B,G);let rootRank=rank(B),pins=root?greedy(G,B):[],cnt=0,first=null,peak=0;
function dfs(C,j,depth){out.guardNodes++;peak=Math.max(peak,depth);out.peakDepth=Math.max(out.peakDepth,depth);
if(!closure(C,G))return;
while(j<pins.length&&!reduce(C,pins[j])[0])j++;
if(j===pins.length){let w=value(C);ok(G.every(g=>lifts(...g.map(f=>ev(f,w))).length===2),"leaf source lift");cnt+=2**(d-rank(C));if(first===null)first=w;return;}
for(let b=0;b<2;b++){const D=C.slice();ok(add(D,pins[j],b)>0,"independent conditional pin");dfs(D,j+1,depth+1);}}
if(root)dfs(B,0,0);
let expected=source(n,F);ok(cnt===expected,"compiled projected count");if(first!==null)ok(F.every(cl=>cl.some(l=>!ev(literalFalse(l),first))),"source witness");out.compiledCases++;out[cnt?"sat":"unsat"]++;return {count:cnt,rootRank,coverRank:pins.length,peak};}
let F=[];for(let w=0;w<8;w++)F.push([1,2,3].map((v,i)=>w&(1<<i)?-v:v));
let n=3;
for(let j=0;j<=3;j++){let base=solve(n,F);ok(base.count===0&&base.rootRank===0,"critical root affine stagnation");let maxCover=base.coverRank;
for(let i=0;i<F.length;i++){let H=F.map(c=>c.slice());H[i][0]*=-1;let r=solve(n,H);ok(r.count>0&&r.rootRank===0,"signed SAT neighbor closure stagnation");maxCover=Math.max(maxCover,r.coverRank);}
out.neighbors.push({n,m:F.length,neighbors:F.length,rootCoverRank:base.coverRank,maxCover});let [a,b,c]=F.pop();let z=++n,d=++n;F.push([a,b,z],[-z,c,d],[-z,c,-d]);}
for(let j=0;j<36;j++){let n=3+rand(3),m=1+rand(9),F=[];for(let i=0;i<m;i++){let ar=[];while(ar.length<3){let v=1+rand(n);if(!ar.some(l=>Math.abs(l)===v))ar.push(rand(2)?v:-v);}F.push(ar);}solve(n,F);}
for(let j=0;j<80;j++){let d=2+rand(4),m=1+rand(6),G=Array.from({length:m},()=>[{m:rand(1<<d),c:0},{m:rand(1<<d),c:0},zero]),B=basis();let best=d;
for(let w=0;w<(1<<m);w++){let C=basis();for(let i=0;i<m;i++)add(C,G[i][(w>>i)&1].m);best=Math.min(best,rank(C));}
let r=greedy(G,B).length;ok(best<=r&&r<=2*best,"rank cover approximation");out.greedyChecks++;}
for(let j=0;j<120;j++){let d=1+rand(5),rows=Array.from({length:8},()=>rand(1<<d)),off=rand(256),h=rand(1<<d),B=basis(),rels=[];
for(let i=0;i<8;i++){let v=rows[i],q=1<<i;while(v&&B[top(v)]){q^=B[top(v)][1];v^=B[top(v)][0];}if(v)B[top(v)]=[v,q];else rels.push(q);}
let v=h,lambda=0;while(v&&B[top(v)]){lambda^=B[top(v)][1];v^=B[top(v)][0];}
let cols=rows.map((_,i)=>rels.reduce((s,r,k)=>s|(((r>>i)&1)<<k),0)),suffix=Array(5);suffix[4]=basis();for(let i=3;i>=0;i--){suffix[i]=suffix[i+1].slice();add(suffix[i],cols[2*i]);add(suffix[i],cols[2*i+1]);}
let D=new Map([[0,1]]);for(let i=0;i<4;i++){let E=new Map();for(let [key,c] of D){let syn=key>>4,mask=key&15;for(let y=0;y<4;y++){out.trellisTransitions++;let s=syn^((y&1)?cols[2*i]:0)^((y&2)?cols[2*i+1]:0);if(reduce(suffix[i+1],s)[0])continue;let t=(s<<4)|(mask|(1<<(y^((off>>(2*i))&3))));let sign=par(lambda&(y<<(2*i)))?-1:1;E.set(t,(E.get(t)||0)+sign*c);}}D=E;out.trellisPeak=Math.max(out.trellisPeak,D.size);}
let exact=v?0:(D.get(15)||0)*2**(d-rank(B)), brute=0;for(let w=0;w<(1<<d);w++){let y=rows.reduce((s,r,i)=>s|(par(r&w)<<i),0)^off,mask=0;for(let i=0;i<4;i++)mask|=1<<((y>>(2*i))&3);if(mask===15)brute+=par(h&w)?-1:1;}
ok(exact===brute,"MS14 signed trellis");out.momentChecks++;}
return out;
}
console.log(JSON.stringify(runRT14(),null,2));
