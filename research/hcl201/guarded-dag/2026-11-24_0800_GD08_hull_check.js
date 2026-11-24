function experiment(){
const bit=i=>1n<<BigInt(i), pop=x=>{let n=0;while(x){x&=x-1n;n++}return n}, par=x=>pop(x)%2,piv=x=>x.toString(2).length-1;
function red(x,B){while(x&&B.has(piv(x)))x^=B.get(piv(x));return x}
function add(x,B){x=red(x,B);if(x)B.set(piv(x),x)}
function gauss(E){let B=new Map;for(let [a,b] of E){while(a&&B.has(piv(a))){let [r,s]=B.get(piv(a));a^=r;b^=s}if(!a){if(b)return null}else B.set(piv(a),[a,b])}return B}
function reduce(a,b,B){for(let k of [...B.keys()].sort((x,y)=>y-x))if(a&bit(k)){let [r,s]=B.get(k);a^=r;b^=s}return[a,b]}
function lift(E){let B=gauss(E),x=0n;if(!B)throw Error("lift");for(let k of [...B.keys()].sort((a,b)=>a-b)){let [r,s]=B.get(k);if(par(r&x)!==s)x|=bit(k)}return x}
function run(n,v,groups,pins=[],dom=false){
function extendHull(dst,ys){for(let y of ys){let d=red(y^dst.rep,dst.span);if(d){dst.span.set(piv(d),d);dst.hull.push(y)}}}
let B=gauss(pins),deleted=0,forced=0;const empty=()=>({count:0n,w:0,p:0,peak:0,attempts:0,deleted,forced,merges:0,pruned:0,compare:0,witness:null});if(!B)return empty();
groups=groups.map(g=>g.flatMap(e=>{let q=e.eq.map(([a,b])=>reduce(a,b,B));if(!gauss(q)){deleted++;return []}q=q.filter(([a])=>a!==0n);if(!q.length)forced++;return [{...e,eq:q}]}));
let sink=v-1,always=1n;for(let g of groups)for(let e of g)if(!e.eq.length&&(always&bit(e.u)))always|=bit(e.v);if(always&bit(sink))return empty();
let obs=[],events=[],D=new Map,checks=[];
for(let g of groups){let rows=[],es=[];for(let e of g){let ids=[];for(let [a,b] of e.eq){let idx=obs.length;obs.push(a);rows.push(idx);ids.push([rows.length-1,b]);let z=a,c=bit(idx);while(z&&D.has(piv(z))){let [r,t]=D.get(piv(z));z^=r;c^=t}if(z)D.set(piv(z),[z,c]);else checks.push(c)}es.push({u:e.u,v:e.v,ids})}events.push({rows,es})}
let H=obs.map((_,i)=>checks.reduce((a,c,j)=>c&bit(i)?a|bit(j):a,0n)),m=events.length,suffix=Array(m+1),last=Array(v).fill(-1),latestIn=Array(v).fill(-1);suffix[m]=new Map;
for(let i=m-1;i>=0;i--){let M=new Map(suffix[i+1]);for(let j of events[i].rows)add(H[j],M);suffix[i]=M}
for(let i=0;i<m;i++)for(let e of events[i].es){if(e.u>=e.v)throw Error("topological IDs");last[e.u]=i;latestIn[e.v]=i}
for(let i=0;i<m;i++){let seenOut=new Set;for(let e of events[i].es){if(latestIn[e.u]>i||seenOut.has(e.v))throw Error("invalid schedule");seenOut.add(e.u)}}
let prefix=new Map,w=0,p=0,peak=1,attempts=0,merges=0,pruned=0,compare=0,possible=1n,states=new Map([["0/1",{s:0n,r:1n,c:1n,path:[],rep:0n,hull:[],span:new Map}]]);
for(let i=0;i<m;i++){let {rows,es}=events[i];for(let j of rows)add(H[j],prefix);w=Math.max(w,prefix.size+suffix[i+1].size-checks.length);let live=bit(sink);for(let j=0;j<v;j++)if(last[j]>i)live|=bit(j);for(let e of es)possible|=bit(e.v);p=Math.max(p,pop(live&possible&~bit(sink)));let next=new Map;
if(rows.length>20)throw Error("large event");
for(let a of states.values())for(let b=0;b<2**rows.length;b++){attempts++;let s=a.s,r=a.r;for(let j=0;j<rows.length;j++)if(b&(1<<j))s^=H[rows[j]];if(red(s,suffix[i+1]))continue;
for(let e of es)if((r&bit(e.u))&&e.ids.every(([j,t])=>((b>>j)&1)===t))r|=bit(e.v);
if(r&bit(sink))continue;r&=live;let key=s+"/"+r,old=next.get(key),y=0n;for(let j=0;j<rows.length;j++)if(b&(1<<j))y|=bit(rows[j]);let rep=a.rep|y,hs=a.hull.map(z=>z|y);if(old){old.c+=a.c;merges++;extendHull(old,[rep,...hs]);continue}let dst={s,r,c:a.c,path:[...a.path,b],rep,hull:[],span:new Map};extendHull(dst,hs);next.set(key,dst)}
if(dom){let by=new Map;for(let [k,a] of next){let l=by.get(a.s)||[];l.push([k,a]);by.set(a.s,l)}for(let l of by.values())for(let [k,a] of l){if(!next.has(k))continue;for(let [kk,b] of l){if(k===kk||!next.has(kk))continue;compare++;if((a.r&b.r)===a.r){next.delete(kk);pruned++}}}}
states=next;peak=Math.max(peak,states.size)}
let count=0n,witness=null,actual=[];for(let a of states.values()){if(a.s)throw Error("syndrome");count+=a.c;if(witness===null){let E=[...pins];for(let i=0;i<m;i++)events[i].rows.forEach((j,k)=>E.push([obs[j],(a.path[i]>>k)&1]));witness=lift(E);if(!dom){for(let y of [a.rep,...a.hull])actual.push(lift([...pins,...obs.map((r,i)=>[r,Number((y>>BigInt(i))&1n)])]));let K=gauss([...pins.map(([r])=>[r,0]),...obs.map(r=>[r,0])]);for(let j=0;j<n;j++)if(!K.has(j)){let z=bit(j);for(let k of [...K.keys()].sort((a,b)=>a-b))if(par(K.get(k)[0]&z))z|=bit(k);actual.push(witness^z)}}}}
if(!dom)count*=2n**BigInt(n-B.size-D.size);return {count:dom?null:count,w,p,peak,attempts,deleted,forced,merges,pruned,compare,witness,actual}}
function accepts(x,v,g,pins){if(pins.some(([a,b])=>par(a&x)!==b))return false;let R=1n;for(let group of g)for(let e of group)if((R&bit(e.u))&&e.eq.every(([a,b])=>par(a&x)===b))R|=bit(e.v);return !(R&bit(v-1))}
const edge=(u,v,eq)=>({u,v,eq}),star=clauses=>clauses.map(eq=>[edge(0,1,eq)]);
let seed=917204;function rand(n){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return (seed>>>8)%n}
let totals={cases:0,sat:0,unsat:0,reference:0,attempts:0,dominanceAttempts:0,dominancePruned:0,dominanceComparisons:0,merges:0,deleted:0,forced:0,witnesses:0,peak:0},controls=[];
function check(label,n,v,g,pins=[]){let t=0n,models=[];for(let x=0n;x<bit(n);x++){totals.reference++;if(accepts(x,v,g,pins)){t++;models.push(x)}}let z=run(n,v,g,pins),d=run(n,v,g,pins,true);if(z.count!==t||Boolean(t)!==(d.witness!==null)||Boolean(t)!==(z.witness!==null)||(t&&(!accepts(z.witness,v,g,pins)||!accepts(d.witness,v,g,pins))))throw Error(label+" mismatch "+t+" "+z.count);if(t){let A=new Map,C=new Map;for(let x of models)add(x^models[0],A);for(let x of z.actual){if(!accepts(x,v,g,pins))throw Error("invalid feature witness");add(x^models[0],C)}if(A.size!==C.size||[...A.values()].some(x=>red(x,C)))throw Error("hull mismatch");totals.hullChecks=(totals.hullChecks||0)+1;totals.hullWitnesses=(totals.hullWitnesses||0)+z.actual.length}totals.cases++;totals[t?"sat":"unsat"]++;totals.witnesses+=t?2:0;for(let k of ["attempts","merges","deleted","forced"])totals[k]+=z[k]||0;totals.dominanceAttempts+=d.attempts;totals.dominancePruned+=d.pruned||0;totals.dominanceComparisons+=d.compare||0;totals.peak=Math.max(totals.peak,z.peak);return {label,count:String(t),w:z.w,p:z.p,peak:z.peak,attempts:z.attempts,decisionPeak:d.peak,pruned:d.pruned||0}}
for(let k=0;k<160;k++){let n=3+rand(5),v=3+rand(5),g=[];for(let u=0;u<v-1;u++)for(let j=u+1;j<v;j++)if(rand(5)<3){let q=[];for(let h=0,l=rand(4);h<l;h++)q.push([BigInt(1+rand(2**n-1)),rand(2)]);g.push([edge(u,j,q)])}let pins=[];if(k%3===0)pins.push([BigInt(1+rand(2**n-1)),rand(2)]);check("random"+k,n,v,g,pins)}
let fano=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]],guards=fano.flatMap(f=>[0,1].map(b=>f.map(j=>[bit(j),b])));
controls.push(check("Fano",7,2,star(guards)));for(let i=0;i<14;i++)controls.push(check("Fano owner "+i,7,2,star(guards.filter((_,j)=>i!==j))));
let wires=[];for(let i=0;i<5;i++)for(let j=i+1;j<5;j++)wires.push([i,j]);for(let k=0;k<30;k++){let g=[];for(let v=0;v<5;v++){let ids=wires.map((e,i)=>e.includes(v)?i:-1).filter(i=>i>=0),s=rand(16),E=rand(2);for(let b=0;b<16;b++){let a=b^s,ok=E?(a===0||a===15):pop(BigInt(a))===2;if(!ok)g.push(ids.map((j,l)=>[bit(j),(b>>l)&1]))}}check("signed K5 "+k,10,2,star(g))}
controls.push(check("correlated opposite guards",1,3,[[edge(0,1,[[1n,0]])],[edge(1,2,[[1n,1]])]]));
let scaling=[];for(let h of [4,8,16,32,64]){let g=[];for(let j=0;j<h;j++)g.push(...star([[[bit(3*j),0],[bit(3*j+1),0],[bit(3*j+2),0]],[[bit(3*j),1],[bit(3*j+1),1],[bit(3*j+2),1]]]));let z=run(3*h,2,g);if(z.count!==6n**BigInt(h)||!accepts(z.witness,2,g,[]))throw Error("scaling");scaling.push({h,n:3*h,w:z.w,p:z.p,peak:z.peak,attempts:z.attempts,count:String(z.count)})}
let frontier=[];for(let h of [2,4,6,8]){let g=[];for(let i=0;i<h;i++)g.push([edge(0,1+2*i,[[bit(i),0]]),edge(0,2+2*i,[[bit(i),1]])]);for(let i=0;i<h;i++)g.push([edge(1+2*i,2*h+1,[[bit(h+i),1]]),edge(2+2*i,2*h+1,[[bit(h+i),1]])]);let z=run(2*h,2*h+2,g),d=run(2*h,2*h+2,g,[],true);if(z.count!==bit(h)||d.witness===null)throw Error("frontier");frontier.push({h,w:z.w,p:z.p,peak:z.peak,decisionPeak:d.peak,pruned:d.pruned,attempts:z.attempts})}
return {seed:917204,totals,controls,scaling,frontier}
}
console.log(JSON.stringify(experiment(),null,2));
