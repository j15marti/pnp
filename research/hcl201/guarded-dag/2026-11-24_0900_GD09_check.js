/* GD09 deterministic standalone JS; run node FILE.js */
function run(){
const B=i=>1n<<BigInt(i), bit=(x,i)=>Number((x>>BigInt(i))&1n);
function par(x){let p=0;while(x){p^=1;x&=x-1n}return p}
function add(m,x,w=0n){while(x){let i=x.toString(2).length-1;if(m.has(i)){let [a,b]=m.get(i);x^=a;w^=b}else{m.set(i,[x,w]);return true}}return false}
function red(m,x,w=0n){while(x){let i=x.toString(2).length-1;if(!m.has(i))return [x,w];let [a,b]=m.get(i);x^=a;w^=b}return [0n,w]}
function span(xs){let m=new Map;for(let x of xs)add(m,x);return m}
function solveLinear(rows,word,D){let m=new Map;for(let i=0;i<rows.length;i++){let [a,b]=red(m,rows[i],BigInt(bit(word,i)));if(!a){if(b)throw Error("inconsistent lift")}else add(m,a,b)}let x=0n;for(let [i,[a,b]] of [...m].sort((a,b)=>a[0]-b[0]))if(par(a&x)!==Number(b))x|=B(i);return x}
function orth(m,n){let piv=new Set(m.keys()), out=[];for(let i=0;i<n;i++)if(!piv.has(i)){let x=B(i);for(let [j,[a]] of [...m].sort((a,b)=>a[0]-b[0]))if(par(a&x))x|=B(j);out.push(x)}return out}
function make(n,v,edges){const D=n+v-2, src=0,sink=v-1;let factors=[];
for(let e of edges){let forms=e.rows.slice(), r=forms.length, u=e.u===src?1:e.u===sink?0:null, z=e.v===src?1:e.v===sink?0:null;let ui=-1,zi=-1;if(u===null){ui=forms.length;forms.push(B(n+e.u-1))}if(z===null){zi=forms.length;forms.push(B(n+e.v-1))}let allowed=[];for(let a=0;a<2**forms.length;a++){let g=e.on.includes(a%(2**r));let l=u===null?((a>>ui)&1):u,t=z===null?((a>>zi)&1):z;if(!g||!l||t)allowed.push(BigInt(a))}factors.push({forms,allowed})}
return {n,D,factors,edges,v}}
function nonreach(P,x){let r=new Set([0]);let changed=true;while(changed){changed=false;for(let e of P.edges)if(r.has(e.u)&&!r.has(e.v)){let y=e.rows.reduce((a,b,i)=>a+(par(b&x)<<i),0);if(e.on.includes(y)){r.add(e.v);changed=true}}}return !r.has(P.v-1)}
function core(P,probe,stats){
let fs=P.factors.slice();if(probe)fs.push({forms:[probe[0]],allowed:[BigInt(probe[1])]});
if(!fs.length)fs=[{forms:[],allowed:[0n]}];
let rows=[], offsets=[], bases=new Map, rel=[];
for(let f of fs){offsets.push(rows.length);for(let a of f.forms){let i=rows.length;rows.push(a);let [z,w]=red(bases,a,B(i));if(z)add(bases,z,w);else rel.push(w)}}
let tags=rows.map((_,i)=>rel.reduce((a,w,j)=>bit(w,i)?a|B(j):a,0n));
let blocks=fs.map((f,i)=>f.allowed.map(a=>{let s=0n;for(let j=0;j<f.forms.length;j++)if(bit(a,j))s^=tags[offsets[i]+j];return {s,y:a<<BigInt(offsets[i])}}));
function affineClosure(){while(true){if(blocks.some(a=>!a.length))return false;let edited=false;
for(let i=0;i<blocks.length&&!edited;i++){let h=new Map,t=0n;for(let j=0;j<blocks.length;j++)if(i!==j){let a=blocks[j];t^=a[0].s;for(let z of a){stats.closureRows++;add(h,z.s^a[0].s)}}for(let k=0;k<blocks[i].length;k++){stats.closureProbes++;if(red(h,t^blocks[i][k].s)[0]){blocks[i].splice(k,1);stats.deletions++;edited=true;break}}}if(!edited)return true}}
if(!affineClosure())return null;
function node(l,r){let lo=offsets[l],hi=r===fs.length?rows.length:offsets[r];let outside=span(tags.filter((_,i)=>i<lo||i>=hi)),inside=span(tags.slice(lo,hi)),both=span(tags);let w=inside.size+outside.size-both.size;stats.width=Math.max(stats.width,w);stats.spanBuilds+=3;
let out=new Map;function put(s,y){stats.attempts++;if(!red(outside,s)[0]&&!out.has(s))out.set(s,y)}
if(r-l===1){for(let a of blocks[l])put(a.s,a.y)}else{let mid=(l+r)>>1,L=node(l,mid),R=node(mid,r);for(let [s,y] of L)for(let [t,z] of R)put(s^t,y^z)}
stats.peak=Math.max(stats.peak,out.size);stats.states+=out.size;return out}
let root=node(0,fs.length);if(!root.has(0n))return null;let y=root.get(0n),z=solveLinear(rows,y,P.D);for(let i=0;i<rows.length;i++)if(par(rows[i]&z)!==bit(y,i))throw Error("bad lift");let x=z&(B(P.n)-1n);
if(!nonreach(P,x)||probe&&par(probe[0]&x)!==probe[1])throw Error("bad original witness");stats.lifts++;return x}
function stats(){return {calls:0,closureRows:0,closureProbes:0,deletions:0,spanBuilds:0,width:0,attempts:0,states:0,peak:0,lifts:0}}
function hull(P){let s=stats(),ask=p=>{s.calls++;return core(P,p,s)},x0=ask(null),W=new Map,C=new Map;
if(x0===null)return {x0,W,C,s};while(W.size+C.size<P.n){let a=orth(W,P.n).find(a=>red(C,a)[0]);if(a===undefined)throw Error("no probe");let y=ask([a,1^par(a&x0)]);if(y===null){if(!add(C,a))throw Error("dependent cert")}else if(!add(W,y^x0))throw Error("dependent witness")}
return {x0,W,C,s}}
let seed=20109;function rnd(n){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n}
let counts={cases:0,SAT:0,UNSAT:0,reference:0,identityChecks:0,stats:stats()},controls=[],scaling=[];
function check(name,P,record=false){let H=hull(P),xs=[];for(let x=0n;x<B(P.n);x++){counts.reference++;if(nonreach(P,x))xs.push(x)}if((H.x0===null)!==(!xs.length))throw Error(name+" verdict");if(xs.length){let W=span(xs.map(x=>x^xs[0]));if(W.size!==H.W.size||red(W,H.x0^xs[0])[0])throw Error(name+" hull rank/base");for(let [a] of H.W.values())if(red(W,a)[0])throw Error(name+" hull subspace");for(let [a] of H.C.values())for(let x of xs){counts.identityChecks++;if(par(a&(x^H.x0)))throw Error(name+" false identity")}}
counts.cases++;counts[xs.length?"SAT":"UNSAT"]++;for(let k of Object.keys(H.s))counts.stats[k]=["peak","width"].includes(k)?Math.max(counts.stats[k],H.s[k]):counts.stats[k]+H.s[k];if(record)controls.push({name,models:xs.length,rank:H.W.size,...H.s});return H}
function E(u,v,rows,on){return {u,v,rows,on}}
const triples=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]];
let fe=triples.flatMap(t=>[E(0,1,t.map(B),[0]),E(0,1,t.map(B),[7])]);check("Fano",make(7,2,fe),true);for(let i=0;i<14;i++)check("Fano owner "+i,make(7,2,fe.filter((_,j)=>j!==i)),true);
function color(n,drop){let es=[];for(let i=0;i<n;i++)for(let j=i+1;j<n;j++)if(drop!==i+","+j)es.push(E(0,1,[B(2*i)^B(2*j),B(2*i+1)^B(2*j+1)],[0]));return make(2*n,2,es)}
check("K5",color(5,""),true);check("K5-e",color(5,"0,1"),true);
for(let t=0;t<80;t++){let n=2+rnd(5),v=3+rnd(5),es=[];for(let j=0;j<4+rnd(10);j++){let u=rnd(v-1),z=1+rnd(v-1);if(t%2===0){u=rnd(v-1);z=u+1+rnd(v-u-1)}let rs=[BigInt(1+rnd((1<<n)-1)),BigInt(1+rnd((1<<n)-1))];es.push(E(u,z,rs,[rnd(4)]))}if(t%8===0)es.push(E(0,v-1,[],[0]));check("random "+t,make(n,v,es))}
for(let t=0;t<30;t++){let n=4+rnd(3),es=[];for(let j=0;j<3;j++){let rr=Array.from({length:4},()=>B(rnd(n))),sign=rnd(16),kind=rnd(2);let on=[];for(let a=0;a<16;a++){let z=a^sign,ones=z.toString(2).replace(/0/g,"").length;if(kind?ones!==2:ones!==0&&ones!==4)on.push(a)}es.push(E(0,1,rr,on))}check("signed E4/B4 "+t,make(n,2,es))}
function lanes(h,unsat){let v=2*h+2,es=[];for(let i=0;i<h;i++){let a=1+2*i,b=a+1,t=v-1;es.push(E(0,a,[B(i)],[0]),E(0,b,[B(i)],[1]),E(a,t,[B(i)],[unsat&&i===0?0:1]),E(b,t,[B(i)],[unsat&&i===0?1:0]))}return make(h,v,es)}
for(let h of [4,8,16,32])for(let u of [false,true]){let P=lanes(h,u),s=stats(),x=core(P,null,s);if((x===null)!==u)throw Error("lane");scaling.push({h,unsat:u,originalOrderAntichain:"2^"+h,...s});if(h<=8)check("lanes "+h+" "+u,P)}
return {seed:20109,counts,controls,scaling,discrepancies:0}
}
console.log(JSON.stringify(run(),null,2));
