module.exports=function experiment(b,p,api){
 const {up,canon,key,solve}=api;
 function probe(input,cap=2000000){
  let C=input.slice(),seen=new Set(C.map(key)),proof=[],m={scans:0,lits:0,cap},probes=0,rounds=0,rootChecks=0,status="UNKNOWN",root;
  function add(c){c=canon(c);let k=key(c);if(seen.has(k))return false;seen.add(k);C.push(c);proof.push(c);return true}
  try{for(;;){rounds++;rootChecks++;root=up(C,[],m);if(root.conflict){add([]);status="UNSAT";break}let vars=[...root.score.keys()].sort((a,b)=>a-b),before=proof.length;
   for(let v of vars)for(let bit of [0,1]){probes++;let r=up(C,[[v,bit]],m),neg=bit?-v:v;
    if(r.conflict){add([neg]);rootChecks++;root=up(C,[],m);if(root.conflict){add([]);status="UNSAT";break}}
    else for(let [u,z] of r.A)if(u!==v&&!root.A.has(u))add([neg,z?u:-u]);
    if(status==="UNSAT")break;
   }if(status==="UNSAT")break;if(proof.length===before)break;}
  }catch(e){if(e.message!=="cap")throw e}
  return {C,proof,metrics:{...m,probes,rounds,rootChecks,status}};
 }
 function independent(C,proof){
   let db=C.map(c=>c.slice()),scans=0,lits=0,passes=0;
   for(let c of proof){let A=new Map();for(let l of c){if(A.has(Math.abs(l))&&A.get(Math.abs(l))!==Number(l<0))throw Error("taut");A.set(Math.abs(l),Number(l<0))}
    let conflict=false,change=true;while(change&&!conflict){change=false;passes++;for(let d of db){scans++;let sat=false,n=0,last=0;for(let l of d){lits++;let a=A.get(Math.abs(l));if(a===undefined){n++;last=l}else if(a===Number(l>0)){sat=true;break}}
    if(sat)continue;if(n===0){conflict=true;break}if(n===1){A.set(Math.abs(last),Number(last>0));change=true}}}
    if(!conflict)throw Error("not RUP "+c);db.push(c)
   }return {scans,lits,passes,steps:proof.length}
 }
 function treeProof(t,guard=[],a=[]){if(t!==null){treeProof(t[1],[...guard,t[0]],a);treeProof(t[2],[...guard,-t[0]],a)}a.push(canon(guard));return a}
 function lane(input){
  let r=probe(input),finish=r.metrics.status==="UNSAT"?null:solve(r.C,2000000),proof=r.proof.slice();
  if(finish?.status==="UNSAT")proof.push(...treeProof(finish.tree));
  let verification=independent(input,proof);
  return {status:proof.at(-1)?.length===0?"UNSAT":"UNKNOWN",proof,metrics:r.metrics,finish,verification,peakClauses:r.C.length}
 }
 let solo=lane(p.C),baseline=solve(p.C,2000000);return {solo,baseline,lane,independent};
};
