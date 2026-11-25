/* BW11 reproducible checks. node this_file.js */
function run(){
 const A=[0,1,2,3], d=4; let seed=20261124, ledger={assertions:0,events:0,eventChecks:0,dpTransitions:0,edgeChecks:0,closureScans:0,pins:0,searchNodes:0,peakDPStates:0};
 const check=(x)=>{ledger.assertions++;if(!x)throw Error("assertion "+ledger.assertions)};
 const rand=()=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed};
 const C=(x)=>[x,0,0,0,0], xor=(a,b)=>a.map((x,i)=>x^b[i]), J=x=>((x>>1)&1)|(((x&1)^((x>>1)&1))<<1), val=(a,z)=>a.reduce((s,v,i)=>s^((i===0||((z>>(i-1))&1))?v:0),0);
 const sample=()=>Array.from({length:d+1},()=>rand()>>>30);
 const neq=(a)=>[1,2,3].map(b=>[a,b]);
 function events(edges){
  const ds=edges.map(([s,t])=>xor(s,t)), base=ds[0];
  const r=edges.reduce((v,[s,t],i)=>xor(v,xor(s,ds[i].map(J))),C(0));
  const out=ds.map(a=>[a,0]);
  for(let i=1;i<ds.length;i++)out.push(...neq(xor(ds[i],base)));
  out.push([r,0],[xor(r,base),0]);ledger.events+=out.length;return out;
 }
 function accept(ev,z){for(const [a,b] of ev){ledger.eventChecks++;if(val(a,z)===b)return true}return false}
 function lift(edges,z){
  let map=new Map([[0,[]]]);
  for(const [a,b] of edges){const s=val(a,z),t=val(b,z),next=new Map();
   for(const [p,path] of map)for(const x of A){ledger.dpTransitions++;if(x!==s&&x!==t&&!next.has(p^x))next.set(p^x,[...path,x])}
   map=next;ledger.peakDPStates=Math.max(ledger.peakDPStates,map.size);
  }
  if(!map.has(0))return null;
  let x=[0];for(const q of map.get(0))x.push(x[x.length-1]^q);
  check(x.at(-1)===0);
  for(let i=0;i<edges.length;i++){const q=x[i]^x[i+1];for(const s of edges[i]){ledger.edgeChecks++;check(q!==val(s,z))}}
  return x.slice(0,-1);
 }
 function brute(edges,z){const n=edges.length, x=Array(n).fill(0), es=edges.map(e=>e.map(a=>val(a,z)));
  function rec(i){if(i===n)return !es[n-1].includes(x[n-1]^x[0]);for(const a of A){x[i]=a;if(!es[i-1].includes(x[i-1]^a)&&rec(i+1))return true}return false}return rec(1);
 }
 let bridgeCases=0, bridgeTight={};
 const subsets=t=>Array.from({length:16},(_,i)=>A.filter(x=>(i>>x)&1)).filter(a=>a.length===t);
 for(let t=1;t<=4;t++){bridgeTight[t]=0;for(const S of subsets(t))for(const L of subsets(t)){
  const F=A.filter(p=>L.every(v=>S.includes(p^v)));
  let want=t===1?[S[0]^L[0]]:t===2?((S[0]^S[1])===(L[0]^L[1])?S.map(s=>s^L[0]):[]):t===3?A.filter(p=>p===(A.find(a=>!S.includes(a))^A.find(a=>!L.includes(a)))):A;
  // Triple forbidden set is complement of three translated missing colors; the remaining color is missing(S) XOR missing(L).
  check(JSON.stringify(F)===JSON.stringify(want.sort((a,b)=>a-b)));if(F.length===t)bridgeTight[t]++;bridgeCases++;
 }}
 let random={sat:0,unsat:0}, scaling=[];
 for(let k=0;k<180;k++){
  const n=3+k%6, edges=Array.from({length:n},()=>[sample(),sample()]);
  if(k%3===0){for(let i=0;i<n;i++)edges[i]=[edges[i][0],xor(edges[i][0],C(1))]}
  const ev=events(edges);
  for(let z=0;z<16;z++){let a=accept(ev,z),b=brute(edges,z),w=lift(edges,z);check(a===b&&a===(w!==null));random[a?"sat":"unsat"]++}
 }
 for(const n of [3,5,17,65,257,1025]){
  const edges=Array.from({length:n},()=>[C(0),C(1)]);let e=events(edges);check(!accept(e,0)&&lift(edges,0)===null);
  edges[n-1]=[C(0),C(2)];e=events(edges);check(accept(e,0)&&lift(edges,0)!==null);scaling.push({n,rawEvents:e.length,root:"UNSAT",neighbor:"SAT"});
 }
 // Clause-to-rim compiler with one actual chart selector per variable. d may vary: the local test below uses explicit literal values to verify the source lift, then tests all 8 symbolic words separately.
 function literalRim(lits){
  const edges=Array.from({length:5},()=>[C(0),C(1)]);
  lits.forEach((l,i)=>{const a=C(l>0?1:2);a[Math.abs(l)]=3;edges[i+1]=[C(0),a]});return edges;
 }
 let clauseFibers={sat:0,unsat:0};
 for(let s=0;s<8;s++){const lits=[1,2,3].map((v,i)=>s>>i&1?-v:v);const edges=literalRim(lits),ev=events(edges);
  for(let z=0;z<8;z++){const truth=lits.some(l=>Boolean(z>>(Math.abs(l)-1)&1)===(l>0));check(accept(ev,z)===truth);check((lift(edges,z)!==null)===truth);clauseFibers[truth?"sat":"unsat"]++}
 }
 const fano=[[1,2,3],[1,4,5],[1,6,7],[2,4,6],[2,5,7],[3,4,7],[3,5,6]].flatMap(a=>[a,a.map(x=>-x)]);
 function solve(n,cs){function rec(x){ledger.searchNodes++;while(true){let changed=false;for(const cl of cs){ledger.closureScans++;if(cl.some(l=>x[Math.abs(l)]!==-1&&x[Math.abs(l)]===Number(l>0)))continue;const u=cl.filter(l=>x[Math.abs(l)]===-1);if(!u.length)return null;if(u.length===1){x[Math.abs(u[0])]=Number(u[0]>0);ledger.pins++;changed=true;break}}if(!changed)break}let i=x.findIndex((v,j)=>j>0&&v===-1);if(i<0)return x;for(const b of [0,1]){let y=x.slice();y[i]=b;let w=rec(y);if(w)return w}return null}return rec(Array(n+1).fill(-1))}
 function reference(n,cs){let count=0;for(let z=0;z<1<<n;z++)if(cs.every(c=>c.some(l=>Boolean(z>>(Math.abs(l)-1)&1)===(l>0))))count++;return count}
 let benchmarks={cube:{sat:0,unsat:0},fano:{sat:0,unsat:0,counts:[]}}, verifiedRimLifts=0;
 function audit(n,cs,key){const cnt=reference(n,cs),w=solve(n,cs);check(Boolean(w)===Boolean(cnt));benchmarks[key][w?"sat":"unsat"]++;if(key==="fano")benchmarks[key].counts.push(cnt);
  if(w)for(const c of cs){const local=c.map((l,i)=>l>0?i+1:-(i+1)),z=c.reduce((s,l,i)=>s|(w[Math.abs(l)]<<i),0);check(accept(events(literalRim(local)),z));check(lift(literalRim(local),z)!==null);verifiedRimLifts++}
 }
 const cube=Array.from({length:8},(_,s)=>[1,2,3].map((v,i)=>s>>i&1?-v:v));
 for(let m=0;m<256;m++)audit(3,cube.filter((_,i)=>m>>i&1),"cube");
 audit(7,fano,"fano");for(let i=0;i<fano.length;i++)audit(7,fano.filter((_,j)=>i!==j),"fano");
 return {seed:20261124,bridgeCases,bridgeTight,random,scaling,clauseFibers,benchmarks,verifiedRimLifts,ledger,scope:"explicit double-cycle packet evaluator, four-state lift, finite brute reference, clause unit closure and DPLL; no general multigraph discovery or physical compiler"};
}
console.log(JSON.stringify(run(),null,2));
