function audit(){
const assert=(x,msg)=>{if(!x)throw Error(msg)};
const xorSet=(a,b)=>{for(const x of b){if(a.has(x))a.delete(x);else a.add(x)}return a};
const key=a=>[...new Set(a)].sort((a,b)=>a-b).join(",");
const prod=(a,b)=>{let s=new Set();for(const u of a)for(const v of b)xorSet(s,[key([...u.split(",").filter(Boolean).map(Number),...v.split(",").filter(Boolean).map(Number)])]);return s};
function indicator(c){let s=new Set([""]);for(const l of c)s=prod(s,new Set(l>0?["",String(l)]:[String(-l)]));return s}
function span(gs){const piv=new Map();let ops=0;for(let i=0;i<gs.length;i++){let s=new Set(gs[i]),p=new Set([i]);while(s.size){let j=[...s].sort().at(-1);if(!piv.has(j)){piv.set(j,[s,p]);break}let [a,b]=piv.get(j);xorSet(s,a);xorSet(p,b);ops++}}let s=new Set([""]),p=new Set();while(s.size){let j=[...s].sort().at(-1);if(!piv.has(j))return {rank:piv.size,ops,certificate:null};let [a,b]=piv.get(j);xorSet(s,a);xorSet(p,b);ops++}let replay=new Set();for(let i of p)xorSet(replay,gs[i]);assert(replay.size===1&&replay.has(""),"certificate replay");return {rank:piv.size,ops,certificate:[...p].sort((a,b)=>a-b)}}
function build(k,r){let n=2*k,pins=new Map();for(let i=r;i<k;i++)pins.set(i+1,i%2);let original=[],active=[];for(let v=0;v<n;v++){let ids=[v%k+1,k+v+1,k+(v+n-1)%n+1];for(let w=0;w<8;w++){let b=ids.map((_,i)=>w>>i&1);if((b[0]^b[1]^b[2])===+(v===0))continue;let lits=ids.map((e,i)=>b[i]?-e:e);let id=original.length;original.push({id,v,lits});if(lits.some(l=>pins.has(Math.abs(l))&&pins.get(Math.abs(l))===+(l>0)))continue;active.push({id,v,lits:lits.filter(l=>!pins.has(Math.abs(l)))})}}return {k,r,n,pins,original,active}}
function values(g,p,y){let a=[0];for(let i=0;i<g.k;i++)a.push(g.pins.has(i+1)?g.pins.get(i+1):p[i]);return a.concat(y)}
const word=(i,n)=>Array.from({length:n},(_,j)=>i>>j&1);
function failed(c,a){return c.lits.every(l=>a[Math.abs(l)]!==+(l>0))}
function scan(g,a){let q=0;for(const c of g.active){q++;if(failed(c,a))return [c,q]}throw Error("no failed clause")}
function syndrome(g,a){return Array.from({length:g.n},(_,v)=>+(v===0)^a[v%g.k+1]^a[g.k+v+1]^a[g.k+(v+g.n-1)%g.n+1])}
function suffix(g,p,v0){let a=values(g,p,[]),y=[],prev=0;for(let v=0;v<g.n;v++){let b=+(v===0)^a[v%g.k+1]^+(v===v0)^prev;y.push(b);prev=b}assert(prev===0,"cycle closure");return y}
function adaptive(g,a){let l=0,h=g.n,msg=0,visits=0;while(h-l>1){let m=(l+h)>>1,A=0,B=0;for(let v=l;v<m;v++){A^=a[v%g.k+1];B^=+(v===0)^a[g.k+v+1]^a[g.k+(v+g.n-1)%g.n+1];visits++}msg+=2;if(A^B)h=m;else l=m}msg++;let c=g.active.find(c=>c.v===l&&failed(c,a));assert(c,"adaptive local Hall cube");return {id:c.id,vertex:l,msg,visits}}
function fnv(s){let h=14695981039346656037n;for(let i=0;i<s.length;i++){h^=BigInt(s.charCodeAt(i));h=h*1099511628211n&((1n<<64n)-1n)}return h.toString(16).padStart(16,"0")}
let seed=2611262045;function bit(){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed>>>31}
let result={family:[],pairChecks:0,assignmentChecks:0,localMatchingChecks:0,hostile:null,seed:2611262045};
function hasMatching(enabled){let w=enabled.length;const dfs=(r,used)=>r===w||enabled.some((b,j)=>!(used>>j&1)&&(r!==0||b)&&dfs(r+1,used|1<<j));return dfs(0,0)}
for(let k of [3,4,5,6,8,16,32,64,128,256]){
 for(let r of [...new Set(k<=6?Array.from({length:k+1},(_,i)=>i):[0,Math.floor(k/2),k])]){
 let g=build(k,r);assert(g.active.every(c=>c.lits.length>=2),"initial UP");let canonical=JSON.stringify({k,r,pins:[...g.pins],clauses:g.original.map(c=>c.lits)});
 // A: compile independently from literal clauses and check all-cube XOR.
 let polys=g.active.map(c=>indicator(c.lits)),sum=new Set();for(let p of polys)xorSet(sum,p);assert(sum.size===1&&sum.has(""),"odd cover");
 // B: distinct prefix pairs, constructive common suffix, independent original clause check.
 let pairs=0;
 if(k<=6){for(let i=0;i<2**r;i++)for(let j=i+1;j<2**r;j++){
 let p=word(i,r),q=word(j,r),v=p.findIndex((b,i)=>b!==q[i]);let y=suffix(g,p,v),a=values(g,p,y),b=values(g,q,y);
 let A=g.active.filter(c=>failed(c,a)),B=g.active.filter(c=>failed(c,b));assert(A.length===1&&A[0].v===v,"singleton");assert(B.length&&B.every(c=>!A.some(d=>d.id===c.id)),"disjoint outputs");pairs++;
 }}
 // C and integrated: local matching equivalence and independent clause scan vs adaptive parity.
 if(k<=6){for(let c of g.active){let w=c.lits.length;for(let j=0;j<2**w;j++){let e=word(j,w);assert(hasMatching(e)===e.some(Boolean),"local block");result.localMatchingChecks++}}}
 let trials=k<=4?2**(r+2*k):64, maxMsg=0,maxVisits=0,scanQueries=0;
 for(let t=0;t<trials;t++){
 let p=k<=4?word(t,r):Array.from({length:r},bit),y=k<=4?word(t>>r,2*k):Array.from({length:2*k},bit),a=values(g,p,y);
 let [c,q]=scan(g,a),d=adaptive(g,a),s=syndrome(g,a);
 assert(s.reduce((a,b)=>a^b,0)===1&&s[c.v]&&s[d.vertex],"scan and syndrome");
 assert(g.original[d.id].v===d.vertex&&failed(g.original[d.id],a),"original certificate");
 maxMsg=Math.max(maxMsg,d.msg);maxVisits=Math.max(maxVisits,d.visits);scanQueries+=q;
 }
 result.pairChecks+=pairs;result.assignmentChecks+=trials;
 result.family.push({k,r,originalVars:3*k,originalClauses:8*k,pins:[...g.pins],activeClauses:g.active.length,sourceFNV64:fnv(canonical),minimumCutStates:(1n<<BigInt(r)).toString(),pairs,trials,maxMsg,maxVisits,scanQueries});
 }}
 // Nonaffine 2-CNF hostile control, no units: (not x or a),(not x or not a),(not y or b),(not y or not b),(x or y).
 const H=[[-1,3],[-1,-3],[-2,4],[-2,-4],[1,2]],C=H.map((lits,id)=>({lits,id})),P=H.map(indicator),D=span(P);assert(D.certificate===null,"hostile parity obstruction");
 let odd=[3,1,2].map(i=>[0,...word(i,4)]),neg=new Set();for(let a of odd)for(let c of C)if(failed(c,a))xorSet(neg,[c.id]);assert(neg.size===0,"odd dual");
 let pairs=[],Q=P.slice();for(let i=0;i<P.length;i++)for(let j=i+1;j<P.length;j++){pairs.push([i,j]);Q.push(prod(P[i],P[j]))}let J=span(Q);assert(J.certificate!==null,"degree-two overlap cover");let maxOverlap=0;for(let i=0;i<16;i++){let a=[0,...word(i,4)],n=C.filter(c=>failed(c,a)).length;assert(n>0,"hostile UNSAT");maxOverlap=Math.max(maxOverlap,n)}
 result.hostile={clauses:H,exhaustive:16,maxOverlap,oddDualAssignments:odd.map(a=>a.slice(1)),linear:D,intersection:J,pairs};return result
}
console.log(JSON.stringify(audit(),null,2));
