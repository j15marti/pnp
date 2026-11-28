function canon(c){return [...new Set(c)].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b)}

function ck(c){return c.join(",")}

function indexed(C,meter){
 const occ=new Map(), units=[], all=new Set();
 for(let i=0;i<C.length;i++){
  if(C[i].length===1)units.push([C[i][0],i]);
  for(let l of C[i]){meter("index");all.add(Math.abs(l));if(!occ.has(l))occ.set(l,[]);occ.get(l).push(i)}
 }
 function prop(g){
  const a=new Set(),q=[],reason=new Map();let conflict=null, no=false;
  function push(l,r){if(a.has(-l)){no=true;conflict=r;return}if(!a.has(l)){a.add(l);q.push(l);reason.set(l,r)}}
  for(let l of g)push(l,-1);if(no)return{no,a,reason,conflict};
  if(C.some(c=>c.length===0))return{no:true,a,reason,conflict:C.findIndex(c=>c.length===0)};
  for(let [l,i] of units){meter("units");push(l,i);if(no)return{no,a,reason,conflict}}
  for(let z=0;z<q.length;z++){
   for(let i of occ.get(-q[z])||[]){meter("clauses");let n=0,last=0,sat=false;
    for(let l of C[i]){meter("lits");if(a.has(l)){sat=true;break}if(!a.has(-l)){n++;last=l}}
    if(sat)continue;if(n===0)return{no:true,a,reason,conflict:i};
    if(n===1){push(last,i);if(no)return{no,a,reason,conflict}}
   }
  }
  return{no:false,a,reason,conflict};
 }
 return {prop,vars:[...all].sort((a,b)=>a-b)};
}

function reverseLearn(base,mode,cap=900000,batch=12){
 let C=[],seen=new Set();for(let c of base){c=canon(c);if(!c.some(l=>c.includes(-l))&&!seen.has(ck(c))){seen.add(ck(c));C.push(c)}}
 const initial=C.length,counts={index:0,units:0,clauses:0,lits:0,mask:0,candidates:0,emit:0,sort:0,init:0},proof=[],history=[];let events=0,epochs=0,probes=0,pairProbes=0,peak=C.length,why="stalled",status="UNKNOWN",maxMasks=0;
 const meter=(k,n=1)=>{counts[k]+=n;events+=n;if(events>cap)throw Error("cap")};
 function add(c,kind,parent){c=canon(c);if(c.some(l=>c.includes(-l))||seen.has(ck(c)))return false;meter("emit");C.push(c);seen.add(ck(c));proof.push({c,kind,parent});peak=Math.max(peak,C.length);return true}
 try{for(;;){
  epochs++;let P=indexed(C,meter),root=P.prop([]);probes++;if(root.no){add([],"root",null);status="UNSAT";why="root UP";break}
  const vars=P.vars.filter(v=>!root.a.has(v)&&!root.a.has(-v)),rank=new Map();
  for(let c of C)for(let l of c){meter("init");rank.set(Math.abs(l),(rank.get(Math.abs(l))||0)+1)}
  vars.sort((a,b)=>rank.get(b)-rank.get(a)||a-b);meter("sort",vars.length*Math.ceil(Math.log2(Math.max(2,vars.length))));
  const L=vars.flatMap(v=>[v,-v]),m=L.length;let U=[],failed=[];
  for(let i=0;i<m;i++){probes++;let a=P.prop([L[i]]);U.push(a);if(a.no&&!seen.has(ck([-L[i]])))failed.push(i)}
  if(failed.length){for(let i of failed.slice(0,batch))add([-L[i]],"failed-single",[L[i]]);history.push({epoch:epochs,units:Math.min(batch,failed.length),pairs:0,events});continue}
  if(!m){why="no free variables";break}
  let cand=[],pairSet=new Set(),kindCounts={union:0,opposition:0,pair:0,implication:0};
  function record(i,j,kind,source){meter("candidates");if(i===j||L[i]===-L[j])return;let c=canon([-L[i],-L[j]]),k=ck(c);if(seen.has(k)||pairSet.has(k)||c.some(l=>seen.has(ck([l]))))return;pairSet.add(k);cand.push({c,kind,parent:source,priority:i*m+j});kindCounts[kind]++}
  if(mode==="pairs"){
   outer:for(let i=0;i<m;i++)for(let j=i+1;j<m;j++){if(L[i]===-L[j])continue;let c=canon([-L[i],-L[j]]);if(seen.has(ck(c)))continue;pairProbes++;let a=P.prop([L[i],L[j]]);if(a.no){record(i,j,"pair",[L[i],L[j]]);if(cand.length>=batch)break outer}}
  }else{
   let F=new Map(),all=(1n<<BigInt(m))-1n;
   // F[l] = singleton guard indices which force clause literal l false.
   for(let j=0;j<m;j++)for(let q of U[j].a){meter("mask");F.set(-q,(F.get(-q)||0n)|(1n<<BigInt(j)))}
   maxMasks=Math.max(maxMasks,F.size);
   function maskFor(i,c,skip=0){let b=all;for(let l of c)if(l!==skip&&!U[i].a.has(-l)){meter("mask");b&=F.get(l)||0n;if(!b)break}return b}
   function emitMask(i,b,kind,src){
    // Test only positions in b; avoid charging unbounded implicit enumeration.
    b&=all^((1n<<BigInt(i+1))-1n);meter("mask");
    while(b){let j=(b&-b).toString(2).length-1;meter("mask");record(i,j,kind,src);b&=b-1n;if(cand.length>=batch)return true}
    return false;
   }
   outer:for(let i=0;i<m;i++){
    let b=0n;for(let q of U[i].a){meter("mask");b|=F.get(q)||0n}if(emitMask(i,b,"union",["opposite literal",L[i]]))break;
    let pos=new Map(),neg=new Map();
    for(let k=0;k<C.length;k++){
     let c=C[k];let b=maskFor(i,c);if(emitMask(i,b,"union",["clause",k,L[i]]))break outer;
     if(mode==="reverse1")for(let l of c){
       let a=maskFor(i,c,l);if(!a)continue;let X=l>0?pos:neg,Y=l>0?neg:pos,v=Math.abs(l),prev=Y.get(v)||0n;meter("mask");
       if(emitMask(i,a&prev,"opposition",["opposite units",v,L[i],k]))break outer;
       X.set(v,(X.get(v)||0n)|a);meter("mask");
     }
    }
   }
  }
  if(!cand.length){why="candidate pool saturated";break}
  for(let c of cand.slice(0,batch))add(c.c,c.kind,c.parent);
  history.push({epoch:epochs,units:0,pairs:Math.min(batch,cand.length),kindCounts,events});
 }
 }catch(e){if(e.message!=="cap")throw e;why="event cap"}
 return {mode,status,why,initial,proof,history,counts,events,epochs,probes,pairProbes,peak,maxMasks,cap};
}

function replay(base,proof,cap=20000000){
 const C=[],seen=new Set();for(let c of base){c=canon(c);if(!c.some(l=>c.includes(-l))&&!seen.has(ck(c))){seen.add(ck(c));C.push(c)}}
 let visits=0,steps=0,reasonRows=0,cores=[];
 for(let step of proof){let g=step.c.map(l=>-l),a=new Map(g.map(l=>[Math.abs(l),+(l>0)])),why=new Map(),hit=-1,changed=true;
  while(changed&&hit<0){changed=false;for(let i=0;i<C.length;i++){let c=C[i],free=[],sat=false;for(let l of c){if(++visits>cap)throw Error("replay cap");let v=Math.abs(l);if(!a.has(v))free.push(l);else if(a.get(v)===(l>0?1:0)){sat=true;break}}if(sat)continue;if(!free.length){hit=i;break}if(free.length===1){let l=free[0];a.set(Math.abs(l),+(l>0));why.set(l,i);changed=true}}}
  if(hit<0)throw Error("invalid RUP "+JSON.stringify(step));
  let stack=[hit],ids=new Set();while(stack.length){let i=stack.pop();if(ids.has(i))continue;ids.add(i);for(let l of C[i])if(why.has(-l))stack.push(why.get(-l))}
  reasonRows+=ids.size;cores.push([...ids].sort((a,b)=>a-b));
  if(seen.has(ck(step.c)))throw Error("duplicate");C.push(step.c);seen.add(ck(step.c));steps++;
 }
 return {steps,visits,reasonRows,cores,unsat:proof.some(s=>s.c.length===0)};
}

function forwardCoverControl(){
 let F=[[-1,-2,3],[-1,-2,-3]],guards=[1,2],a=indexed(F,()=>{}),A=a.prop([1]),B=a.prop([2]),P=a.prop(guards);
 let union=new Set([...A.a,...B.a]),wave0=F.some(c=>c.every(l=>union.has(-l)))||[...union].some(l=>union.has(-l)),left=F.map(c=>c.filter(l=>!union.has(-l)));
 if(wave0||!P.no||left[0][0]!==-left[1][0])throw Error("control");
 return {F,guards,singleClosures:[...A.a,...B.a],wave0,oppositeUnits:left,pairUP:P.no};
}
module.exports={canon,ck,indexed,reverseLearn,replay,forwardCoverControl};
