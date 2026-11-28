function triggerMask(C,L,U,i,F,occ,meter){
 const all=(1n<<BigInt(L.length))-1n;let mask=0n,touched=new Set(),A=U[i].a;
 for(let q of A){meter("mask");mask|=F.get(q)||0n;for(let k of occ.get(-q)||[]){meter("touch");touched.add(k)}}
 for(let k of touched){let c=C[k];if(c.some(l=>A.has(l)))continue;let rem=c.filter(l=>!A.has(-l));if(!rem.length)throw Error("singleton conflict");
  // If all missing literals become false, or all but one become false and the last remains untrue,
  // this clause can produce the first extra unit (or contradiction) in the combined closure.
  let b=all;for(let l of rem){meter("mask");b&=F.get(l)||0n;if(!b)break}mask|=b;
  for(let j=0;j<rem.length;j++){let l=rem[j],p=all;for(let k2=0;k2<rem.length;k2++)if(k2!==j){meter("mask");p&=F.get(rem[k2])||0n;if(!p)break}
   meter("mask");p&=all^(F.get(-l)||0n);mask|=p;
  }
 }
 return mask&(all^((1n<<BigInt(i+1))-1n));
}

function learnTrigger(base,mode,cap=900000,batch=12){
 let C=[],seen=new Set();for(let c of base){c=canon(c);if(!c.some(l=>c.includes(-l))&&!seen.has(ck(c))){seen.add(ck(c));C.push(c)}}
 let counts={index:0,units:0,clauses:0,lits:0,mask:0,touch:0,candidates:0,emit:0,sort:0,init:0},events=0,epochs=0,probes=0,pairProbes=0,excluded=0,proof=[],history=[],peak=C.length,status="UNKNOWN",why="stalled",initial=C.length;
 function meter(k,n=1){counts[k]+=n;events+=n;if(events>cap)throw Error("cap")}
 function add(c,kind,guard){c=canon(c);if(seen.has(ck(c))||c.some(l=>c.includes(-l)))return false;meter("emit");C.push(c);seen.add(ck(c));proof.push({c,kind,parent:guard});peak=Math.max(peak,C.length);return true}
 try{for(;;){
  epochs++;let P=indexed(C,meter),root=P.prop([]);probes++;if(root.no){add([],"root",[]);status="UNSAT";why="root UP";break}
  let rank=new Map();for(let c of C)for(let l of c){meter("init");rank.set(Math.abs(l),(rank.get(Math.abs(l))||0)+1)}
  let L=P.vars.filter(v=>!root.a.has(v)&&!root.a.has(-v)).sort((a,b)=>rank.get(b)-rank.get(a)||a-b).flatMap(v=>[v,-v]),m=L.length;meter("sort",m*Math.ceil(Math.log2(Math.max(2,m))));
  let U=[],failed=[];for(let i=0;i<m;i++){probes++;let a=P.prop([L[i]]);U.push(a);if(a.no&&!seen.has(ck([-L[i]])))failed.push(i)}
  if(failed.length){for(let i of failed.slice(0,batch))add([-L[i]],"failed-single",[L[i]]);history.push({epoch:epochs,units:Math.min(batch,failed.length),pairs:0,events});continue}
  let F=new Map(),occ=new Map();
  if(mode!=="all"){
   for(let j=0;j<m;j++)for(let q of U[j].a){meter("mask");F.set(-q,(F.get(-q)||0n)|(1n<<BigInt(j)))}
   for(let k=0;k<C.length;k++)for(let l of C[k]){meter("index");if(!occ.has(l))occ.set(l,[]);occ.get(l).push(k)}
  }
  let cand=[],before=pairProbes,beforeExcluded=excluded;
  outer:for(let i=0;i<m;i++){
   let mask=mode==="all"?null:triggerMask(C,L,U,i,F,occ,meter);
   for(let j=i+1;j<m;j++){
    if(L[i]===-L[j])continue;let cl=canon([-L[i],-L[j]]);if(seen.has(ck(cl)))continue;
    meter("candidates");
    if(mode!=="all"){meter("mask");if(!(mask&(1n<<BigInt(j)))){excluded++;continue}}
    pairProbes++;let x=P.prop([L[i],L[j]]);if(x.no){cand.push({c:cl,guard:[L[i],L[j]]});if(cand.length>=batch)break outer}
   }
  }
  if(!cand.length){why="all eligible pair conflicts exhausted";break}
  for(let x of cand)add(x.c,"trigger-pair",x.guard);
  history.push({epoch:epochs,units:0,pairs:cand.length,pairProbes:pairProbes-before,excluded:excluded-beforeExcluded,events});
 }}catch(e){if(e.message!=="cap")throw e;why="event cap"}
 return {mode,status,why,initial,proof,history,counts,events,epochs,probes,pairProbes,excluded,peak,cap}
}

function checkFilter(C,cap=500000){
 let steps=0,tick=()=>{if(++steps>cap)throw Error("audit cap")},P=indexed(C,tick),L=P.vars.flatMap(v=>[v,-v]),U=L.map(l=>P.prop([l])),F=new Map(),occ=new Map(),audit={pairs:0,conflicts:0,eligible:0,falseNegatives:0};
 if(U.some(a=>a.no))return {status:"singleton contradiction; no two-guard admission",steps};
 for(let j=0;j<L.length;j++)for(let q of U[j].a)F.set(-q,(F.get(-q)||0n)|(1n<<BigInt(j)));
 for(let k=0;k<C.length;k++)for(let l of C[k]){if(!occ.has(l))occ.set(l,[]);occ.get(l).push(k)}
 for(let i=0;i<L.length;i++){let b=triggerMask(C,L,U,i,F,occ,tick);for(let j=i+1;j<L.length;j++){if(L[i]===-L[j])continue;audit.pairs++;let eligible=!!(b&(1n<<BigInt(j)));if(eligible)audit.eligible++;let no=P.prop([L[i],L[j]]).no;if(no){audit.conflicts++;if(!eligible)audit.falseNegatives++}}}
 if(audit.falseNegatives)throw Error("filter false negative");
 return {...audit,steps};
}
module.exports={triggerMask,learnTrigger,checkFilter};
