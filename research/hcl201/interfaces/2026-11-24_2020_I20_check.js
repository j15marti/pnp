const run = function run(){
const R={seed:20261124,tests:0,SAT:0,UNSAT:0,UNKNOWN:0,referenceSAT:0,referenceUNSAT:0,assertions:0,closurePasses:0,forcedPins:0,groupProbes:0,tupleVisits:0,absorptions:[0,0,0,0],nativeTests:0,scaling:[]};
let seed=R.seed;const rand=n=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n};
const ck=(x)=>{R.assertions++;if(!x)throw Error("assertion "+R.assertions)};
const bit=i=>1n<<BigInt(i);
const reduce=(x,B)=>{for(const [p,v] of B)if(x&p)x^=v;return x};
function insert(x,B){x=reduce(x,B);if(!x)return false;let p=bit(x.toString(2).length-1);B.push([p,x]);B.sort((a,b)=>a[0]>b[0]?-1:1);return true}
const basis=xs=>{let B=[];for(const x of xs)insert(x,B);return B};
function allmatch(n,E){let out=[];function rec(mask,x,t){if(!mask){out.push({x,t});return}let v=0;while(!(mask&bit(v)))v++;for(const e of E){let w=e.u===v?e.v:e.v===v?e.u:-1;if(w>=0&&(mask&bit(w)))rec(mask^bit(v)^bit(w),x^bit(e.id),t^e.t)}}rec((1n<<BigInt(n))-1n,0n,0n);return out}
function comps(n,E){let adj=Array.from({length:n},()=>[]);for(const e of E){adj[e.u].push(e.v);adj[e.v].push(e.u)}let seen=new Set(),out=[];for(let i=0;i<n;i++)if(!seen.has(i)){let v=[i];seen.add(i);for(let j=0;j<v.length;j++)for(const w of adj[v[j]])if(!seen.has(w)){seen.add(w);v.push(w)}let ids=new Map(v.map((x,i)=>[x,i]));out.push({n:v.length,E:E.filter(e=>ids.has(e.u)).map(e=>({...e,u:ids.get(e.u),v:ids.get(e.v)}))})}return out}
const xor=(a,f)=>a.reduce((x,v)=>x^f(v),0n);
function closure(F,target){let pins=new Map();for(;;){R.closurePasses++;if(F.some(s=>!s.length))return false;let anchors=F.map(s=>s[0]), baseX=xor(anchors,v=>v.x),baseT=xor(anchors,v=>v.t),cols=[];
for(let i=0;i<F.length;i++){let B=[];for(let v of F[i])if(insert(v.x^anchors[i].x,B))cols.push({x:v.x^anchors[i].x,t:v.t^anchors[i].t})}
let B=[],nulls=[];for(let c of cols){let {x,t}=c;for(let [p,v,w] of B)if(t&p){t^=v;x^=w}if(!t)nulls.push(x);else{let p=bit(t.toString(2).length-1);B.push([p,t,x]);B.sort((a,b)=>a[0]>b[0]?-1:1)}}
let t=target^baseT,x=baseX;for(let [p,v,w] of B)if(t&p){t^=v;x^=w}if(t)return false;
let varying=nulls.reduce((a,b)=>a|b,0n),universe=F.flat().reduce((a,b)=>a|b.x,0n),fixed=universe&~varying;
let changed=false;for(let i=0;i<F.length&&!changed;i++){let old=F[i];for(let j=0;j<old.length;j++){let bad=(old[j].x^x)&fixed&old.reduce((a,b)=>a|b.x,0n);if(bad){let p=bad&-bad;F[i]=old.filter(v=>(v.x&p)===(x&p));pins.set(p,x&p);R.forcedPins++;changed=true;break}}}
if(!changed)return true;
}}
function solve(F,target,cap=3){F=F.map(s=>s.slice());if(!closure(F,target))return {status:"UNSAT"};let A=F.map(s=>s[0]),base=xor(A,v=>v.t),d=target^base;let packets=F.map((s,i)=>{let B=[],w=[{x:s[0].x,t:0n}];for(let v of s)if(insert(v.t^s[0].t,B))w.push({x:v.x,t:v.t^s[0].t});return {i,w,B}}),W=[],archive=[];
function checkHull(){return !reduce(d,basis([...W.map(p=>p[1]),...packets.flatMap(p=>p.B.map(v=>v[1]))]))}
function probe(group){R.groupProbes++;let V=basis(group.flatMap(p=>p.B.map(v=>reduce(v[1],W))));let map=new Map();function rec(j,t,x){if(j===group.length){R.tupleVisits++;let key=reduce(t,W);if(!map.has(key))map.set(key,{t,x});return}for(let v of group[j].w)rec(j+1,t^v.t,x^v.x)}rec(0,0n,0n);if(BigInt(map.size)!==(1n<<BigInt(V.length)))return false;
archive.push({map,W:W.map(p=>p.slice()),ids:group.map(p=>p.i)});for(let p of group)for(let v of p.B)insert(v[1],W);
let ids=new Set(group.map(p=>p.i));packets=packets.filter(p=>!ids.has(p.i));R.absorptions[group.length]++;return true}
while(true){ck(checkHull());let changed=false;for(let k=1;k<=cap&&!changed;k++){function pick(start,g){if(g.length===k)return probe(g);for(let i=start;i<=packets.length-(k-g.length);i++)if(pick(i+1,[...g,packets[i]]))return true;return false}changed=pick(0,[])}if(!changed)break}
if(reduce(d,W))return {status:"UNKNOWN"};let x=xor(packets,p=>A[p.i].x);for(let i=archive.length-1;i>=0;i--){let a=archive[i],v=a.map.get(reduce(d,a.W));ck(!!v);d^=v.t;x^=v.x}ck(d===0n);return {status:"SAT",x}}
function audit(F,target,reference=true,expected=null,cap=3){let out=solve(F,target,cap);R.tests++;R[out.status]++;let ref=expected;if(reference){let S=new Set([0n]);for(let s of F){let T=new Set();for(let x of S)for(let v of s)T.add(x^v.t);S=T}ref=S.has(target)}if(ref)R.referenceSAT++;else R.referenceUNSAT++;ck(out.status==="UNKNOWN"||((out.status==="SAT")===ref));if(out.status==="SAT"){let t=0n,x=0n;for(let s of F){let universe=s.reduce((a,b)=>a|b.x,0n),v=s.find(v=>v.x===(out.x&universe));ck(!!v);t^=v.t;x^=v.x}ck(t===target&&x===out.x)}return out.status}
function k4(tags,id){let E=[],pairs=[[0,1],[2,3],[0,2],[1,3],[0,3],[1,2]];pairs.forEach(([u,v],i)=>E.push({u,v,id:id+i,t:i%2===0?tags[i/2]:0n}));return allmatch(4,E)}
function tri(i,j){let a=bit(j),b=bit(j+1),c=bit(j+2),d=bit(j+3);return [k4([0n,a,b],i),k4([0n,c,d],i+6),k4([0n,a^c,b^d],i+12)]}
let f=tri(0,0);for(let t=0;t<16;t++)ck(audit(f,BigInt(t))==="SAT");ck(audit(f,7n,true,null,1)==="UNKNOWN");ck(audit(f,7n,true,null,2)==="UNKNOWN");
for(let t=0;t<4;t++)audit([k4([0n,1n,2n],0)],BigInt(t));
for(let it=0;it<100;it++){let F=[],id=0;for(let k=0;k<1+it%4;k++){let n=it%3===0?6:4,E=[];for(let u=0;u<n;u++)for(let v=u+1;v<n;v++)if(rand(5)!==0)E.push({u,v,id:id++,t:BigInt(rand(16))});F.push(allmatch(n,E))}for(let t=0;t<16;t++)audit(F,BigInt(t))}
for(let k of [4,16,32]){let F=[];for(let j=0;j<k;j++)F.push(...tri(18*j,4*j));let t=bit(4*k)-1n;let old=R.groupProbes;ck(audit(F,t,false,true)==="SAT");ck(audit(F,t^bit(4*k),false,false)==="UNSAT");R.scaling.push({blocks:k*3,rank:4*k,probes:R.groupProbes-old})}
for(let type=0;type<4;type++)for(let sign=0;sign<16;sign++){
let E=[],n=8;const add=(u,v,t=0n)=>E.push({u,v,id:E.length,t});
for(let v=0;v<2;v++){let p=4*v;if(type&(1<<v)){let a=n++,b=n++;for(let k=0;k<4;k++){add(a,p+k);add(b,p+k)}}else{add(p,p+1,bit(v));add(p+2,p+3,bit(v))}}
for(let k=0;k<4;k++)if(sign&(1<<k)){let a=n++;add(k,a);add(a,4+k)}else add(k,4+k);
let F=comps(n,E).map(c=>allmatch(c.n,c.E));let truth=false;for(let x=0;x<16;x++){let y=x^sign;let good=(v,w)=>(type&(1<<v))?w.toString(2).split("1").length===3:w===0||w===15;if(good(0,x)&&good(1,y))truth=true}
audit(F,0n,true);let exact=F.reduce((S,s)=>{let T=new Set();for(let a of S)for(let b of s)T.add(a^b.t);return T},new Set([0n]));ck(exact.has(0n)===truth);R.nativeTests++;
}
return R;
};
console.log(JSON.stringify(run(),null,2));
