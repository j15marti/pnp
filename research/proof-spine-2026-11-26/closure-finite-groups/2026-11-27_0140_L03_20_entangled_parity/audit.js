function audit(){
 const check=(x,m)=>{if(!x)throw Error(m)};
 const parity=x=>{let p=0;while(x){p^=1;x&=x-1}return p};
 const add=(B,x)=>{while(x){let i=31-Math.clz32(x);if(B[i])x^=B[i];else{B[i]=x;return}}};
 const out=[];
 for(const n of [5,7,9,17]){
  const q=3*n, mod=i=>(i+q)%q,a=i=>2*mod(i),b=i=>2*mod(i)+1;
  const scope=e=>[a(e),a(e+1),b(e),b(e+1),b(e+2)];
  const rows=Array.from({length:n},(_,r)=>[r,r+n,r+2*n]);
  const cols=Array.from({length:n},(_,c)=>[c,(c-1+n)%n+n,(c-2+n)%n+2*n]);
  let fingerprint=2166136261;
  const hash=x=>{fingerprint=Math.imul(fingerprint^x,16777619)>>>0};
  const groups=[...rows,...cols].map((edges,id)=>{
   let S=[...new Set(edges.flatMap(scope))].sort((x,y)=>x-y);
   let ps=edges.map(e=>scope(e).map(v=>S.indexOf(v)));
   let bad=[],good=[],all=1<<S.length;hash(id);hash(S.length);S.forEach(hash);
   for(let w=0;w<all;w++){
    const bit=j=>(w>>j)&1;
    let v=ps.map(([i,j,k,l,m])=>(bit(i)^(bit(k)&bit(l)))^(bit(j)^(bit(l)&bit(m))));
    if(v.reduce((s,x)=>s+x,0)!==1){bad.push(w);hash(w)}else good.push(w);
   }
   return {id,edges,S,ps,bad,good,all};
  });
  const parentClauses=groups.reduce((s,g)=>s+g.bad.length,0);
  const parentLiterals=groups.reduce((s,g)=>s+g.bad.length*g.S.length,0);
  for(const r of n===5?[0,7,q]:[q]){
   let goodChecks=0,badChecks=0,rawAffineRanks=[],residualClauses=0,units=0;
   // A. Source table restriction, exact unary closure and local affine bases.
   for(const g of groups){
    const active=g.S.map((v,i)=>((v%2===0)||(v>>1)<r)?i:-1).filter(i=>i>=0);
    let pin=0;for(let i=0;i<g.S.length;i++)if(!active.includes(i))pin|=1<<i;
    const keep=w=>(w&pin)===0;
    let allowed=g.good.filter(keep);
    check(allowed.length>0,"local contradiction");
    let any=0,all=(1<<g.S.length)-1,B=[];
    for(const w of allowed){any|=w;all&=w;add(B,w^allowed[0])}
    for(const i of active)check(((any>>i)&1)===1&&((all>>i)&1)===0,"forced unary");
    rawAffineRanks.push([B.filter(Boolean).length,active.length]);
    let bad=g.bad.filter(keep);residualClauses+=bad.length;if(active.length===1)units+=bad.length;
   }
   check(units===0,"UP not stable");
   // B. Separate original-word verification using expanded ANF, plus coefficient cancellation.
   let terms=new Set([0]); // constant 1 per row, n odd
   const toggle=x=>terms.has(x)?terms.delete(x):terms.add(x);
   // stable term identities: a and unordered b products. n odd gives 1.
   for(let i=0;i<q;i++){
    for(const j of [i,mod(i+1)]){
     toggle("a"+j);
     if(j<r&&mod(j+1)<r)toggle("b"+[j,mod(j+1)].sort((a,b)=>a-b).join(","));
    }
   }
   check(terms.size===1&&terms.has(0),"global ANF sum");
   for(const g of groups){
    const bad=new Set(g.bad);
    const gbit=(w,v)=>(w>>g.S.indexOf(v))&1;
    for(let w=0;w<g.all;w++){
     let pinOK=true;for(const v of g.S)if(v%2&&v>>1>=r&&gbit(w,v)){pinOK=false;break}
     if(!pinOK)continue;
     let values=g.edges.map(i=>gbit(w,a(i))^gbit(w,a(i+1))^(gbit(w,b(i))&gbit(w,b(i+1)))^(gbit(w,b(i+1))&gbit(w,b(i+2))));
     const isBad=values.reduce((s,x)=>s+x,0)!==1;
     check(isBad===bad.has(w),"source table/ANF mismatch");
     if(isBad)badChecks++;else{goodChecks++;check(values.reduce((s,x)=>s^x,0)===1,"row parity");}
    }
   }
   // C. Outer matching enumeration with a fixed cap; independently checks positive quotient and parity.
   let matches=0,tries=0,syndromes=new Set(),stop=false;
   const visit=(row,used,mask)=>{
    if(row===n){matches++;check(parity(mask)===1,"odd matching");syndromes.add(((mask&1)?1:0)|((mask&(1<<n))?2:0));return}
    for(let k=0;k<3;k++){if(++tries>1000000){stop=true;return}const col=(row+k)%n;if(!(used&(1<<col)))visit(row+1,used|(1<<col),mask|(1<<(row+k*n)));if(stop)return}
   };
   if(q<=27)visit(0,0,0); // explicit finite reference only
   let support=null;
   if(n===5){
    const image=new Set();let tested=0;const bm=r===0?0:(1<<r)-1;
    for(let am=0;am<(1<<q);am++){
     let h=0;for(let i=0;i<q;i++)h|=((((am>>i)&1)^(((bm>>i)&1)&((bm>>mod(i+1))&1))))<<i;
     let x=0;for(let i=0;i<q;i++)x|=(((h>>i)^(h>>mod(i+1)))&1)<<i;
     check(parity(x)===0,"decoder parity");image.add(x);tested++;
    }
    check(image.size===1<<(q-1),"full even image");
    let proj=0;for(let i=0;i<q;i++){let S=new Set();for(const x of image)S.add((x&((1<<i)-1))|((x>>(i+1))<<i));check(S.size===1<<(q-1),"proper marginal");proj+=S.size}
    support={tested,image:image.size,oneDeletionProjectionEntries:proj};
   }
   // integrated: diagonal perfect matching in outer graph, all matchings odd by row exact-one.
   check(rows.every((row,i)=>row[0]===i)&&cols.every((col,i)=>col[0]===i),"diagonal matching");
   const fullRank=rawAffineRanks.filter(([x,y])=>x===y).length;
   if(r===q)check(fullRank===2*n,"unexpected local affine relation");
   if(q<=27){check(!stop&&matches>0,"reference cap");check(syndromes.has(0)&&syndromes.has(1)&&syndromes.has(2)&&!syndromes.has(3),"two-bit hostile check")}
   out.push({n,q,released:r,originalVariables:2*q,parentClauses,parentLiterals,parentFingerprint:fingerprint.toString(16),residualClauses,goodChecks,badChecks,groupCount:2*n,fullLocalAffineHullGroups:fullRank,localRanks:rawAffineRanks,unitClosureStable:true,quadraticCertificate:"sum of n row parity equations = 1",matchingReference:q<=27?{matches,tries,syndromes:[...syndromes].sort()}:null,decoderReference:support,properScopeRelaxation:"UNKNOWN (outer diagonal feasible)",hybrid:"UNSAT"});
  }
 }
 return {schema:1,source:"0-based raw a_i=2i,b_i=2i+1; cyclic q=3n; row r uses r,r+n,r+2n; column c uses c,n+(c-1 mod n),2n+(c-2 mod n); full blocking clauses on union scopes",jobs:out};
}
console.log(JSON.stringify(audit(),null,2));
