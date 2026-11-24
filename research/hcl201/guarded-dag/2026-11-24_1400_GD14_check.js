function experiment(){
  const stats={closureSweeps:0,forcedPins:0,gaussianXors:0,candidateSets:0,reachChecks:0,syndromeTransitions:0,verifiedWitnesses:0,referenceWords:0};
  const bit=i=>1n<<BigInt(i);
  function pivot(a){return a.toString(2).length-1}
  function reduce(a,b,B){for(const [p,[v,w]] of [...B].sort((x,y)=>y[0]-x[0]))if(a&bit(p)){a^=v;b^=w;stats.gaussianXors++}return [a,b]}
  function add(B,a,b){[a,b]=reduce(a,b,B);if(!a)return b===0;B.set(pivot(a),[a,b]);return true}
  function lift(rows){const B=new Map();for(const [a,b] of rows)if(!add(B,a,b))return null;let x=0n;for(const [p,[a,b]] of [...B].sort((x,y)=>x[0]-y[0]))if(parity(a&x)!==b)x|=bit(p);return x}
  function parity(a){let p=0;while(a){a&=a-1n;p^=1}return p}
  function enabled(e,x){return e.rows.every(([a,b])=>parity(a&x)===b)}
  function reach(es,s,t){stats.reachChecks++;const adj=new Map();for(const e of es){if(!adj.has(e.u))adj.set(e.u,[]);adj.get(e.u).push(e.v)}let q=[s],seen=new Set(q);for(let i=0;i<q.length;i++){if(q[i]===t)return true;for(const v of adj.get(q[i])||[])if(!seen.has(v)){seen.add(v);q.push(v)}}return false}
  function verify(I,x){if(x===null||!I.pins.every(([a,b])=>parity(a&x)===b)||reach(I.edges.filter(e=>enabled(e,x)),I.s,I.t))throw Error("bad source witness");stats.verifiedWitnesses++}
  function closure(I){const B=new Map();for(const [a,b] of I.pins)if(!add(B,a,b))return {label:false};while(true){stats.closureSweeps++;let E=[];for(const e of I.edges){const R=new Map();let ok=true;for(let [a,b] of e.rows){[a,b]=reduce(a,b,B);if(!add(R,a,b)){ok=false;break}}if(ok)E.push({...e,rows:[...R.values()]})}const fixed=E.filter(e=>!e.rows.length), opt=E.filter(e=>e.rows.length);
    if(reach(fixed,I.s,I.t))return {label:false};if(!reach(E,I.s,I.t))return {label:true,x:lift([...B.values()])};let changed=false;for(const e of opt)if(e.rows.length===1&&reach([...fixed,e],I.s,I.t)){const [a,b]=e.rows[0];if(!add(B,a,b^1))return {label:false};stats.forcedPins++;changed=true;break}
    if(!changed)return {B,fixed,opt};}}
  function registry(opt){let global=new Map(),deps=[],j=0;const blocks=[];for(const e of opt){let ids=[];for(const [row] of e.rows){let a=row,h=bit(j);ids.push(j++);while(a){let p=pivot(a);if(!global.has(p)){global.set(p,[a,h]);break}const [v,w]=global.get(p);a^=v;h^=w;stats.gaussianXors++}if(!a)deps.push(h)}blocks.push(ids)}return {deps,blocks,rank:global.size}}
  function localOptions(e,ids,deps){let table=new Map([[0,[0n]]]);for(let j=0;j<ids.length;j++){let col=0;for(let k=0;k<deps.length;k++)if(deps[k]&bit(ids[j]))col|=1<<k;let next=new Map();for(const [s,ws] of table)for(const w of ws)for(let b=0;b<2;b++){let t=s^(b?col:0),v=w^(b?bit(j):0n);if(!next.has(t))next.set(t,[]);let a=next.get(t);if(a.length<2&&!a.includes(v))a.push(v)}table=next}let on=0n;for(let j=0;j<e.rows.length;j++)if(e.rows[j][1])on|=bit(j);let yes=[],no=[];for(const [s,ws] of table){if(ws.includes(on))yes.push([s,on]);const v=ws.find(w=>w!==on);if(v!==undefined)no.push([s,v])}
    // The enabled word may not be one of the two representatives.
    let ss=0;for(let k=0;k<deps.length;k++){let p=0;for(let j=0;j<ids.length;j++)if((on&bit(j))&&(deps[k]&bit(ids[j])))p^=1;ss|=p<<k}yes=[[ss,on]];return {yes,no};}
  function* subsets(n,k,start=0,arr=[]){if(!k){yield arr.slice();return}for(let i=start;i<=n-k;i++){arr.push(i);yield* subsets(n,k-1,i+1,arr);arr.pop()}}
  function solve(I,cap=8){let c=closure(I);if(c.label!==undefined){if(c.label)verify(I,c.x);return {label:c.label,closed:true,x:c.x}}let {B,fixed,opt}=c;const {deps,blocks,rank}=registry(opt),delta=deps.length;if(delta>cap)return {label:null,delta,rank};let options=opt.map((e,i)=>localOptions(e,blocks[i],deps));
    for(let k=0;k<=Math.min(delta,opt.length);k++)for(const a of subsets(opt.length,k)){stats.candidateSets++;const selected=new Set(a);if(reach([...fixed,...a.map(i=>opt[i])],I.s,I.t))continue;let dp=new Map([[0,[]]]);for(let i=0;i<opt.length&&dp.size;i++){let next=new Map();for(const [s,words] of dp)for(const [v,w] of (selected.has(i)?options[i].yes:options[i].no)){stats.syndromeTransitions++;let t=s^v;if(!next.has(t))next.set(t,[...words,w])}dp=next}if(dp.has(0)){const words=dp.get(0),rows=[...B.values()];for(let i=0;i<opt.length;i++)for(let j=0;j<opt[i].rows.length;j++)rows.push([opt[i].rows[j][0],Number((words[i]>>BigInt(j))&1n)]);const x=lift(rows);verify(I,x);return {label:true,delta,rank,enabled:k,x}}}
    return {label:false,delta,rank};}
  function reference(I){for(let x=0n;x<bit(I.n);x++){stats.referenceWords++;if(I.pins.every(([a,b])=>parity(a&x)===b)&&!reach(I.edges.filter(e=>enabled(e,x)),I.s,I.t))return true}return false}
  const groups={};function check(name,I,expected=null,cap=8){let ref=expected===null?reference(I):expected,a=solve(I,cap);let g=groups[name]??={SAT:0,UNSAT:0,terminal:0,closure:0,capUnknown:0};g[ref?"SAT":"UNSAT"]++;if(a.label===null)g.capUnknown++;else {if(a.label!==ref)throw Error("label mismatch "+name);g[a.closed?"closure":"terminal"]++}return a}
  function makeCNF(n,clauses){return {n,s:0,t:1,pins:[],edges:clauses.map(C=>({u:0,v:1,rows:C.map(l=>[bit(Math.abs(l)-1),l<0?1:0])}))}}
  const cube=Array.from({length:8},(_,i)=>[1,2,3].map((v,j)=>i&(1<<j)?-v:v));
  for(let mask=0;mask<256;mask++)check("cube",makeCNF(3,cube.filter((_,i)=>mask&(1<<i))),null,8);
  const lines=[[1,2,3],[1,4,5],[1,6,7],[2,4,6],[2,5,7],[3,4,7],[3,5,6]];
  const fano=lines.flatMap(C=>[C,C.map(x=>-x)]);check("fano",makeCNF(7,fano),null,8);for(let i=0;i<14;i++)check("fano",makeCNF(7,fano.filter((_,j)=>j!==i)),null,8);
  let seed=314159;function rnd(k){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%k}
  for(let i=0;i<180;i++){let n=5+rnd(2),edges=[];for(let j=0;j<3+rnd(5);j++){let rows=[];for(let q=0;q<1+rnd(3);q++)rows.push([BigInt(1+rnd((1<<n)-1)),rnd(2)]);edges.push({u:rnd(5),v:rnd(5),rows})}let pins=i%3===0?[[BigInt(1+rnd((1<<n)-1)),rnd(2)]]:[];check("random",{n,s:0,t:4,edges,pins},null,8)}
  // Two independent odd parity groups. Each group has q local words and q-1 free bits.
  // All A edges are s->v; B edges v->t. A safe B edge is redirected to a dead vertex.
  let scales=[];for(const q of [3,8,16,32,64])for(const sat of [false,true]){let edges=[];for(let g=0;g<2;g++){let sum=0n;for(let i=0;i<q;i++){let row=i===q-1?sum:bit(g*(q-1)+i);if(i<q-1)sum^=row;edges.push({u:g?1:0,v:g?(sat&&i===0?3:2):1,rows:[[row,i===q-1?0:1]]})}}let I={n:2*(q-1),s:0,t:2,pins:[],edges};let a=check("scale",I,sat);if(a.delta!==2||a.label!==sat)throw Error("scale");scales.push({q,sat,delta:a.delta,rank:a.rank,enabled:a.enabled??null})}
  // Verify bounded-occurrence compilation on original cube/Fano source witnesses.
  // Split each occurrence, add implication cycle; test all source words and their synchronized lifts.
  let splitChecks=0;function split(C,n){let count=0,uses=Array.from({length:n},()=>[]),D=C.map(cl=>cl.map(l=>{let v=++count;uses[Math.abs(l)-1].push(v);return l>0?v:-v}));for(const a of uses)if(a.length>1)for(let j=0;j<a.length;j++)D.push([-a[j],a[(j+1)%a.length]]);let occ=Array(count).fill(0);for(const c of D)for(const l of c)occ[Math.abs(l)-1]++;if(occ.some(x=>x>3))throw Error("occ");for(let x=0;x<(1<<n);x++){const val=l=>Boolean(x&(1<<(Math.abs(l)-1)))===(l>0);let y=0n;for(let i=0;i<n;i++)if(x&(1<<i))for(const v of uses[i])y|=bit(v-1);let good=D.every(c=>c.some(l=>Boolean(y&bit(Math.abs(l)-1))===(l>0)));if(good!==C.every(c=>c.some(val)))throw Error("split");splitChecks++}return {count,D,uses}}
  for(let m=0;m<256;m++)split(cube.filter((_,i)=>m&(1<<i)),3);split(fano,7);for(let i=0;i<14;i++)split(fano.filter((_,j)=>j!==i),7);
  return {seed:314159,groups,scales,splitChecks,stats};
}
console.log(JSON.stringify(experiment(),null,2));
