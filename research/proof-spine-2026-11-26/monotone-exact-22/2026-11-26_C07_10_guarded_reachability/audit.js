// Run with node audit.js; no dependencies.
function audit(){
 const assert=(v,m)=>{if(!v)throw Error(m||"assert")};
 const range=n=>Array.from({length:n},(_,i)=>i);
 const bit=(k,i)=>Math.floor(k/2**i)%2;
 const canon=a=>[...new Set(a)].sort((x,y)=>x-y);
 const merge=(a,b)=>{const c=canon([...a,...b]);return c.some(x=>c.includes(-x))?null:c};
 const subset=(a,b)=>a.every(x=>b.includes(x));
 const truth=(l,M)=>{let v=M.get(Math.abs(l));assert(v!==undefined,"missing id "+l);return l>0?v:1-v};
 const hash=s=>{let h=2166136261;for(let i=0;i<s.length;i++)h=Math.imul(h^s.charCodeAt(i),16777619);return(h>>>0).toString(16)};
 const build=(kind,k,pin=false)=>{
   let next=0;const fresh=()=>++next;const zero=fresh(),one=fresh(),pins=[[zero,0],[one,1]],boundary=[],priv=[],rows=[],comp=[],groups=[];
   const cm=new Map();function physical(l){if(l>0)return l;const x=-l;if(!cm.has(x)){const y=fresh();cm.set(x,y);comp.push([x,y]);rows.push([x,y,zero,one])}return cm.get(x)}
   const pub=()=>{const x=fresh();boundary.push(x);return x};
   function group(B){let g={B:[...B],P:[],N:[]};groups.push(g);return g}
   function p(g){const x=fresh();g.P.push(x);priv.push(x);return x}
   function nae(g,L){const R=L.map(physical),w=fresh();assert(new Set([...R,w]).size===4);rows.push([...R,w]);g.N.push({L,R,w})}
   function or3(g,a,b,c){const z=p(g);nae(g,[a,b,z]);nae(g,[-z,c,zero])}
   function or4(L){const g=group(L.map(Math.abs));const r=p(g);or3(g,L[0],L[1],r);or3(g,L[2],L[3],-r)}
   let original=[];
   if(kind==="chain"){const A=range(k+1).map(pub);for(let j=0;j<k;j++){const g=group([A[j],A[j+1]]),T=range(3).map(()=>p(g));for(let i=0;i<3;i++)for(const a of g.B)nae(g,[a,T[i],T[(i+1)%3]])}if(pin)pins.push([A[0],0],[A[k],1])}
   else {const X=range(7).map(pub),s=pub(),u=pub(),v=pub(),w=pub();let lines=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]];if(kind==="gate-sat")lines=lines.slice(0,6);original=lines.map(L=>L.map(i=>X[i]));for(const L of original){or4([-s,...L]);or4([-s,...L.map(x=>-x)])}or4([-s,u,v,w])}
   return {kind,k,pin,n:next,boundary,priv,pins,rows,comp,groups,original}
 };
 function laneA(S,d,tick){
   const P=new Set(S.priv),B=new Set(S.boundary),fixed=new Map(S.pins.filter(([x])=>!B.has(x))),vertices=S.priv.flatMap(x=>[x,-x]),edges=new Map(vertices.map(x=>[x,[]])),forbid=[];
   // Original parity gives completion bit; each NAE exactly forbids all-zero and all-one.
   for(const G of S.groups)for(const {L} of G.N)for(const polarity of [1,-1]){
     let C=L.map(l=>l*polarity);if(C.some(l=>fixed.has(Math.abs(l))&&truth(l,fixed)))continue;
     C=C.filter(l=>!fixed.has(Math.abs(l)));let Q=C.filter(l=>P.has(Math.abs(l))),guard=canon(C.filter(l=>B.has(Math.abs(l))).map(l=>-l));
     assert(Q.length<=2&&Q.length+guard.length===C.length);
     if(merge(guard,[])===null)continue;
     if(!Q.length)forbid.push(guard);
     else if(Q.length===1)edges.get(-Q[0]).push({v:Q[0],g:guard});
     else {edges.get(-Q[0]).push({v:Q[1],g:guard});edges.get(-Q[1]).push({v:Q[0],g:guard})}
   }
   for(const [x,v] of S.pins)if(B.has(x))forbid.push([v?-x:x]);
   let all=new Map(),states=0,overflow=0;
   for(const start of vertices){
     const M=new Map(),queue=[];function add(v,g){const key=g.join(",");if(!M.has(v))M.set(v,new Map());if(!M.get(v).has(key)){M.get(v).set(key,g);queue.push([v,g]);states++;tick()}}
     add(start,[]);
     for(let i=0;i<queue.length;i++){const [v,g]=queue[i];for(const e of edges.get(v)){tick();const h=merge(g,e.g);if(h&&h.length<=d)add(e.v,h)}}
     for(const [v,g] of queue)for(const e of edges.get(v)){tick();const h=merge(g,e.g);if(h&&![...(M.get(e.v)||new Map()).values()].some(z=>subset(z,h)))overflow++}
     all.set(start,M)
   }
   if(overflow)return {states,overflow,cnf:null};
   for(const x of S.priv)for(const g of (all.get(x).get(-x)||new Map()).values())for(const h of (all.get(-x).get(x)||new Map()).values()){tick();const c=merge(g,h);if(c)forbid.push(c)}
   return {states,overflow,cnf:[...new Map(forbid.map(g=>[g.join(","),g.map(l=>-l)])).values()]};
 }
 function twoSAT(C,ids,tick){
   if(C.some(c=>!c.length))return false;
   const V=ids.flatMap(x=>[x,-x]),adj=new Map(V.map(x=>[x,[]]));
   for(const c of C){assert(c.length<=2);let [a,b=a]=c;adj.get(-a).push(b);adj.get(-b).push(a);tick()}
   const reach=(a,b)=>{let seen=new Set([a]),q=[a];for(let i=0;i<q.length;i++){tick();if(q[i]===b)return true;for(const v of adj.get(q[i]))if(!seen.has(v)){seen.add(v);q.push(v)}}return false};
   return !ids.some(x=>reach(x,-x)&&reach(-x,x))
 }
 function simplify(C,ids,tick){if(C===null)return null;let H=C.filter(c=>c.length<=2);for(const c of C.filter(c=>c.length>2)){tick();if(twoSAT([...H,...c.map(l=>[-l])],ids,tick))return null}return H}
 function B(S,M,tick){
   for(const [x,v] of S.pins)if(M.has(x)&&M.get(x)!==v)return false;
   if(S.kind==="chain"){for(let i=0;i<S.k;i++){tick();if(M.get(S.boundary[i])!==M.get(S.boundary[i+1]))return false}return true}
   const [s,u,v,w]=S.boundary.slice(7).map(x=>M.get(x));if(!s)return true;
   for(const L of S.original){tick();const q=L.reduce((a,x)=>a+M.get(x),0);if(q===0||q===3)return false}
   return !!(u||v||w)
 }
 function local(S,G,M,tick){
   for(let mask=0;mask<2**G.P.length;mask++){
     tick();const V=new Map(M);for(const [x,v] of S.pins)if(!S.boundary.includes(x))V.set(x,v);
     G.P.forEach((x,i)=>V.set(x,bit(mask,i)));
     for(const [x,y] of S.comp)if(V.has(x))V.set(y,1-V.get(x));
     let ok=true;for(const {R,w} of G.N){tick();const z=2-R.reduce((a,x)=>a+V.get(x),0);if(z!==0&&z!==1){ok=false;break}V.set(w,z)}
     if(ok)return V
   }return null
 }
 function C(S,M,tick){
   for(const [x,v] of S.pins)if(M.has(x)&&M.get(x)!==v)return null;
   const W=new Map(M);for(const [x,v] of S.pins)W.set(x,v);
   for(const G of S.groups){const V=local(S,G,M,tick);if(!V)return null;for(const [x,v] of V){if(W.has(x))assert(W.get(x)===v);W.set(x,v)}}
   for(const [x,y] of S.comp)W.set(y,1-W.get(x));
   assert(W.size===S.n,"witness size");
   for(const R of S.rows){tick();assert(R.reduce((a,x)=>a+W.get(x),0)===2,"bad source witness")}
   return W
 }
 function imported(S,tick){
   let clauses=S.pins.filter(([x])=>S.boundary.includes(x)).map(([x,v])=>[v?x:-x]);
   // Each local imported exact support checked from original integer rows; retained clauses are reclosed if 2CNF.
   let reclosures=0;
   for(const G of S.groups){for(let m=0;m<2**G.B.length;m++){const M=new Map(G.B.map((x,i)=>[x,bit(m,i)]));if(!local(S,G,M,tick))clauses.push(G.B.map((x,i)=>bit(m,i)?-x:x))}
     if(clauses.every(c=>c.length<=2)){twoSAT(clauses,S.boundary,tick);reclosures++}
   }return {clauses,reclosures}
 }
 const satCNF=(C,M)=>C.every(c=>c.some(l=>truth(l,M)));
 let results=[];
 for(const S0 of [...[1,2,4,8,16,32,64].flatMap(k=>[build("chain",k),build("chain",k,true)]),build("gate-sat",0),build("gate-unsat",0)]){
   const raw=JSON.stringify(S0),N=8*raw.length,cap=N**3,cost={A:0,B:0,C:0,I:0};const tick=k=>()=>{if(++cost[k]>cap)throw Error("cap "+k)};
   const copy=()=>JSON.parse(raw),S=copy();
   const A=laneA(copy(),2,tick("A")),H=simplify(A.cnf,S.boundary,tick("A"));
   const words=S.boundary.length<=11?range(2**S.boundary.length):range(36);
   const values=(j)=>new Map(S.boundary.map((x,i)=>[x,S.boundary.length<=11?bit(j,i):j===0?0:j===1?1:((Math.imul(j+1,1103515245)^Math.imul(i+5,2654435761))>>>(i%24))&1]));
   let Bvals=words.map(j=>B(copy(),values(j),tick("B")));
   let Cvals=words.map(j=>!!C(copy(),values(j),tick("C")));
   assert(Bvals.every((v,i)=>v===Cvals[i]),"B vs C");
   const I=imported(copy(),tick("I"));let IH=simplify(I.clauses,S.boundary,tick("I"));
   let accepted=0;for(let i=0;i<words.length;i++){const M=values(words[i]),b=Bvals[i];if(b)accepted++;if(A.cnf)assert(satCNF(A.cnf,M)===b,"A");if(H)assert(satCNF(H,M)===b,"H");assert(satCNF(I.clauses,M)===b,"I");if(IH)assert(satCNF(IH,M)===b,"IH")}
   let maj=null;if(S.kind.startsWith("gate")){let xword=words.find(j=>bit(j,7)&&Bvals[j]);if(xword!==undefined){const base=xword%256;const triple=[base+256,base+512,base+1024];assert(triple.every(j=>Bvals[j])&&!Bvals[base]);maj={accepted:triple,rejected:base}}else assert(Bvals.every((v,j)=>v===(bit(j,7)===0)))}
   const Adecision=H?twoSAT(H,S.boundary,tick("A")):"UNKNOWN";const Idecision=IH?twoSAT(IH,S.boundary,tick("I")):"UNKNOWN";
   if(S.kind==="chain"){assert(Adecision===!S.pin&&Idecision===!S.pin)}
   results.push({kind:S.kind,k:S.k,pin:S.pin,vars:S.n,rows:S.rows.length,boundary:S.boundary.length,N,fingerprint:hash(raw),cap,words:words.length,accepted,states:A.states,overflow:A.overflow,conflictClauses:A.cnf?.length??null,binaryClauses:H?.length??null,Adecision,Idecision,importedClauses:I.clauses.length,reclosures:I.reclosures,cost,majorityWitness:maj})
 }
 return {mode:"sequential identical JSON source copies; fixed N^3 counted high-level operation cap per lane, not bit-operation meter; sampled larger boundaries",results}
}
console.log(JSON.stringify(audit(),null,2));
