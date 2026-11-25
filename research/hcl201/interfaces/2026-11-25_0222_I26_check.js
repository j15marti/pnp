
// Node: node CHECK.js BS19_results.json. Also callable as runI26(parsed).
function runI26(data) {
 const bit=i=>1n<<BigInt(i), has=(x,i)=>Number((x>>BigInt(i))&1n);
 function parity(x){let p=0;while(x){x&=x-1n;p^=1}return p}
 function system(rows,d,need=false){
  const B=new Map();let bad=false;
  for(let [v,r] of rows){while(v){const i=(v&-v).toString(2).length-1;
   if(!B.has(i)){B.set(i,[v,r]);break}const b=B.get(i);v^=b[0];r^=b[1]}
   if(!v&&r){bad=true;break}}
  if(bad)return {bad:true,rank:B.size};
  if(!need)return {bad:false,rank:B.size};
  const piv=[...B.keys()].sort((a,b)=>b-a);
  function complete(v,hom){for(const i of piv){const [row,r]=B.get(i);if(parity(row&v)^(hom?0:r))v^=bit(i)}return v}
  const free=[];for(let i=0;i<d;i++)if(!B.has(i))free.push(complete(bit(i),true));
  return {bad:false,rank:B.size,point:complete(0n,false),free};
 }
 function distinct(vs){const B=new Map();for(let v of vs){while(v){let i=(v&-v).toString(2).length-1;if(!B.has(i)){B.set(i,v);break}v^=B.get(i)}}return [...B.values()]}
 function gauss(point,free,q){
  const c=q(point),Q=v=>q(point^v)^c, P=(v,w)=>Q(v^w)^Q(v)^Q(w);
  let V=free.slice(),sign=c,exp=0;
  while(V.length){const u=V.shift();let j=V.findIndex(v=>P(u,v));
   if(j<0){if(Q(u))return 0n;exp++;continue}
   const v=V.splice(j,1)[0];sign^=Q(u)&Q(v);exp++;
   V=V.map(w=>w^(P(w,v)?u:0n)^(P(w,u)?v:0n));
  }return (sign?-1n:1n)*bit(exp);
 }
 function circuit(n,C,nae=true,pins=[]){
  const F=[];let nv=n;
  function OR(lits){let a=lits[0];for(let j=1;j<lits.length;j++){let z=++nv;F.push({kind:"OR",vars:[Math.abs(a)-1,Math.abs(lits[j])-1,z-1],neg:[a<0,lits[j]<0]});a=z}
   F.push({kind:"pin",vars:[Math.abs(a)-1],b:a>0?1:0});
  }
  for(const c of C){OR(c);if(nae)OR(c.map(x=>-x))}
  for(const [i,b] of pins)F.push({kind:"pin",vars:[i-1],b});
  return {nv,F};
 }
 function dual({nv,F},cap){
  let d=0;const wire=Array(nv).fill(0n),A=[],G=[],P=[];
  for(const f of F){const ix=f.vars.map(v=>{wire[v]^=bit(d);return d++});
    if(f.kind==="pin")P.push({i:ix[0],b:f.b});
    else {G.push({ix,neg:f.neg,kind:f.kind});A.push(bit(ix[2]))}}
  const R=wire.map(v=>[v,0]),base=system(R,d),rank=system(R.concat(A.map(v=>[v,0])),d).rank-base.rank;
  const out={wireVars:nv,factors:F.length,gates:G.length,modeBits:d,activationRank:rank,cap};
  if(rank>cap)return {...out,status:"DECLINE"};
  const root=system(R,d,true);
  const proj=v=>G.reduce((s,g,j)=>has(v,g.ix[2])?s^bit(j):s,0n);
  const images=distinct(root.free.map(proj));if(images.length!==rank)throw Error("rank");
  let modes=[0n];for(const v of images)modes=modes.concat(modes.map(w=>w^v));
  let total=0n,nz=0,neg=0,consistent=0;
  for(const t of modes){let rows=R.slice(),active=0;
   for(let j=0;j<G.length;j++){let [a,b,s]=G[j].ix, tbit=has(t,j);rows.push([bit(s),tbit]);
     if(!tbit){rows.push([bit(a),0],[bit(b),0])}else active++}
   const sol=system(rows,d,true);if(sol.bad)continue;consistent++;
   function q(v){let z=0;for(const p of P)z^=p.b&has(v,p.i);
    for(let j=0;j<G.length;j++)if(has(t,j)){const g=G[j],a=has(v,g.ix[0]),b=has(v,g.ix[1]);
     z^=(a&b)^(g.kind==="OR"?(1^a^b):0)^(g.neg[0]?a:0)^(g.neg[1]?b:0)}
    return z}
   const contribution=gauss(sol.point,sol.free,q)*bit(2*G.length-active);
   if(contribution){nz++;if(contribution<0n)neg++}total+=contribution;
  }
  const div=bit(d-nv);if(total%div)throw Error("normalization");
  return {...out,status:"COUNT",groups:modes.length,consistent,nonzeroGroups:nz,negativeGroups:neg,count:String(total/div)};
 }
 function val(w,l){return ((w>>(Math.abs(l)-1))&1)^(l<0?1:0)}
 function ok(w,C,nae,pins=[]){return pins.every(([i,b])=>val(w,i)===b)&&C.every(c=>{let v=c.map(l=>val(w,l));return v.some(x=>x)&&( !nae||v.some(x=>!x))})}
 // Paid local coordinate closure of explicit source clauses and pins. Restart after a deduction.
 function close(n,C,nae,pins=[]){let D=Array(n).fill(3),scans=0,pinsFound=0;
  for(const [i,b] of pins){D[i-1]&=1<<b;if(!D[i-1])return {unsat:true,scans,pinsFound}}
  for(;;){let change=false;
   outer:for(const c of C){scans++;let scope=[...new Set(c.map(Math.abs))],support=Array(scope.length).fill(0),cnt=0;
    for(let a=0;a<1<<scope.length;a++){if(scope.some((v,i)=>!(D[v-1]&(1<<((a>>i)&1)))))continue;
     const z=c.map(l=>((a>>scope.indexOf(Math.abs(l)))&1)^(l<0?1:0));if(!z.some(x=>x)||nae&&!z.some(x=>!x))continue;
     cnt++;scope.forEach((v,i)=>support[i]|=1<<((a>>i)&1))}
    if(!cnt)return {unsat:true,scans,pinsFound};
    for(let i=0;i<scope.length;i++){let v=scope[i]-1;if(D[v]!==support[i]){D[v]=support[i];pinsFound++;change=true;break outer}}
   }if(!change)return {unsat:false,scans,pinsFound,domains:D}}
 }
 let assertions=0;function check(c){assertions++;if(!c)throw Error("assertion "+assertions)}
 function ref(n,C,nae,pins=[]){let count=0,first=null;for(let w=0;w<1<<n;w++)if(ok(w,C,nae,pins)){count++;if(first===null)first=w}return {count,first}}
 const controls=[];
 function trial(name,n,C,nae=true,pins=[]){let closure=close(n,C,nae,pins),D=dual(circuit(n,C,nae,pins),10),R=ref(n,C,nae,pins);
  check(D.status==="COUNT"&&BigInt(D.count)===BigInt(R.count));check(!closure.unsat||R.count===0);controls.push({name,...D,ref:R.count,closure});}
 trial("OR-all-four UNSAT",2,[[1,2],[1,-2],[-1,2],[-1,-2]],false);
 trial("OR-three SAT",2,[[1,2],[1,-2],[-1,2]],false);
 trial("NAE2 inconsistent",2,[[1,2],[1,-2]]);
 trial("NAE2 consistent",2,[[1,2],[-1,-2]]);
 trial("pinned NAE3 SAT",3,[[1,2,3]],true,[[1,0]]);
 trial("pinned NAE3 UNSAT",3,[[1,2,3]],true,[[1,0],[2,0],[3,0]]);
 for(const n of [4,6,8,10]){trial("monotone cycle "+n,n,Array.from({length:n},(_,i)=>[i+1,(i+1)%n+1]),false);
  let t=controls.at(-1);check(t.activationRank===n&&t.nonzeroGroups>=2**(n/2));}
 let seed=123456789;function rand(k){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%k}
 for(let i=0;i<24;i++){let C=[];for(let j=0;j<2;j++){let s=[];while(s.length<3){let k=1+rand(5);if(!s.some(x=>Math.abs(x)===k))s.push((rand(7)<3?-1:1)*k)}C.push(s)}trial("random "+i,5,C)}
 const k=data.common.find(x=>x.K===16),C=k.residual.C,ids=[...new Set(C.flat().map(Math.abs))].sort((a,b)=>a-b),local=C.map(c=>c.map(l=>Math.sign(l)*(ids.indexOf(Math.abs(l))+1)));
 const raw=data.source.O.map(o=>o.t.map(v=>v+1));const rawClosure=close(data.source.n,raw,true);
 const kClosure=close(ids.length,local,true), K=dual(circuit(ids.length,local),10), BW=dual(circuit(data.source.n,raw),10);
 const R=ref(ids.length,local,true);check(R.count===246);check(!kClosure.unsat&&kClosure.pinsFound===0);check(!rawClosure.unsat&&rawClosure.pinsFound===0);
 // Full reference reconstruction of each actual residual model through authenticated elimination logs.
 let lifts=0,firstLift=null;
 for(let w=0;w<1<<ids.length;w++)if(ok(w,local,true)){
   let z=0;ids.forEach((v,i)=>{if((w>>i)&1)z|=1<<(v-1)});
   for(const l of k.residual.log.slice().reverse()){
     let feasible=[];for(let b=0;b<2;b++){let t=(z&~(1<<(l.v-1)))|(b<<(l.v-1));if(ok(t,l.bucket.map(c=>[l.v,...c]),true))feasible.push(t)}
     check(feasible.length>0);z=feasible[0];
   }check(ok(z,raw,true));lifts++;if(firstLift===null)firstLift=z;
 }
 check(lifts===R.count);
 // Actual K16 owner slices, relabel locally and compare the real dual contraction.
 const slices=[];
 for(const row of C.slice(0,5)){const sc=[...new Set(row.map(Math.abs))],c=row.map(l=>Math.sign(l)*(sc.indexOf(Math.abs(l))+1));const d=dual(circuit(sc.length,[c]),10),r=ref(sc.length,[c],true);check(d.status==="COUNT"&&Number(d.count)===r.count);slices.push({sourceRow:row,...d,ref:r.count})}

 // Private gate cancellation: direct independent transform of every actual wide signed NAE owner.
 let collapsedChecks=0,collapsedModes=0,collapsedNonzero=0,rawModes=0,rawNonzero=0;
 function collapse(rows,isRaw){for(const row of rows){const k=row.length,sz=1<<k;let neg=0;row.forEach((l,i)=>{if(l<0)neg|=1<<i});
   for(let a=0;a<sz;a++){let sum=0;for(let x=0;x<sz;x++){let y=x^neg;if(y!==0&&y!==sz-1)sum+=parity(BigInt(x&a))?-1:1}
     const formula=(a===0?sz:0)-(parity(BigInt(a&neg))?-1:1)*(1+(parity(BigInt(a))?-1:1));check(sum===formula);collapsedChecks++;if(isRaw){rawModes++;if(sum)rawNonzero++}else{collapsedModes++;if(sum)collapsedNonzero++}
   }
 }}
 collapse(C,false);collapse(raw,true);


 // Exact native NAE dual support: the binary incidence-graph cycle space.
 function cycleDual(n,rows,cap=12){
  let d=0,vr=Array(n).fill(0n),owners=[];
  for(const c of rows){if(c.length<2||new Set(c.map(Math.abs)).size!==c.length)throw Error("noncanonical owner");
   let mask=0n,neg=0n;
   for(const l of c){const b=bit(d++);mask^=b;vr[Math.abs(l)-1]^=b;if(l<0)neg^=b}
   owners.push({mask,neg,k:c.length})}
  const constraints=vr.concat(owners.map(o=>o.mask)).map(v=>[v,0]);
  const rank=system(constraints,d).rank,dim=d-rank;
  const out={vars:n,owners:rows.length,incidences:d,incidenceRank:rank,cycleDimension:dim,cap};
  if(dim>cap)return {...out,status:"DECLINE"};
  const basis=system(constraints,d,true).free;check(basis.length===dim);
  let states=[0n];for(const b of basis)states=states.concat(states.map(s=>s^b));
  let total=0n,positive=0,negative=0,absolute=0n;
  for(const s of states){let weight=1n;for(const o of owners){let a=s&o.mask;
    check(parity(a)===0);if(!a)weight*=bit(o.k)-2n;else weight*=parity(s&o.neg)?2n:-2n}
    check(weight!==0n);if(weight>0n){positive++;absolute+=weight}else{negative++;absolute-=weight}total+=weight
  }
  let divisor=bit(Math.max(0,d-n)),numerator=total*bit(Math.max(0,n-d));check(numerator%divisor===0n);
  return {...out,status:"COUNT",modes:states.length,positive,negative,signedNumerator:String(total),absoluteNumerator:String(absolute),count:String(numerator/divisor)};
 }
 const fano=[[1,2,3],[1,4,5],[1,6,7],[2,4,6],[2,5,7],[3,4,7],[3,5,6]];
 let fanoControls=[];
 function testCycle(name,rows,expected){let c=cycleDual(7,rows);check(c.status==="COUNT"&&Number(c.count)===expected);check(ref(7,rows,true).count===expected);fanoControls.push({name,...c})}
 testCycle("Fano root",fano,0);
 for(let i=0;i<7;i++)for(let j=0;j<3;j++){let C=fano.map(c=>c.slice());C[i][j]*=-1;testCycle("Fano sign "+i+":"+j,C,10)}
 const cycleK=cycleDual(ids.length,local),cycleBW=cycleDual(data.source.n,raw);

 return {assertions,fanoControls,cycleK,cycleBW,collapsedChecks,collapsedModes,collapsedNonzero,rawModes,rawNonzero,controls,controlSAT:controls.filter(x=>x.ref>0).length,controlUNSAT:controls.filter(x=>!x.ref).length,
  sameSource:{ids,K,BW,kClosure,rawClosure,reference:R,lifts,firstLift,slices},limitations:"Actual full gate mode contractions decline cap 10; exact source reference enumerates 2^14 words. No global matching execution, native lift, full portfolio, kernel or measured CM."};
}
if(typeof module!=="undefined"){module.exports=runI26;if(require.main===module){const fs=require("fs");console.log(JSON.stringify(runI26(JSON.parse(fs.readFileSync(process.argv[2],"utf8"))),null,2))}}
