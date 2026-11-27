module.exports=function pairLane(C,api,cap=2000000){
 const {up,canon,key}=api,db=C.slice(),seen=new Set(db.map(key)),proof=[],m={scans:0,lits:0,cap};let probes=0,rounds=0,rootChecks=0,skips=0,status="UNKNOWN",reason="fixed point";
 function add(cl){cl=canon(cl);let k=key(cl);if(seen.has(k))return false;seen.add(k);db.push(cl);proof.push(cl);return true}
 function root(){rootChecks++;let a=up(db,[],m);if(a.conflict){add([]);status="UNSAT";reason="root UP";}return a}
 try{outer:for(;;){rounds++;let a=root();if(a.conflict)break;let vars=[...a.score].sort((a,b)=>b[1]-a[1]||a[0]-b[0]).map(x=>x[0]),old=proof.length;
  for(let i=0;i<vars.length;i++)for(let j=i+1;j<vars.length;j++)for(let b of [0,1])for(let c of [0,1]){
   let u=vars[i],v=vars[j],cl=canon([b?-u:u,c?-v:v]);if(seen.has(key(cl))||a.A.has(u)||a.A.has(v)){skips++;continue}probes++;
   if(up(db,[[u,b],[v,c]],m).conflict){add(cl);a=root();if(a.conflict)break outer}
  }
  // Root forced variables and one-literal failed probes separately, all RUP.
  for(let v of vars)for(let b of [0,1]){if(a.A.has(v)){skips++;continue}probes++;if(up(db,[[v,b]],m).conflict){add([b?-v:v]);a=root();if(a.conflict)break outer}}
  if(proof.length===old)break;
 }}catch(e){if(e.message!=="cap")throw e;reason="scan cap"}
 let m2={scans:0,lits:0,cap:10000000},verify=C.slice();for(let cl of proof){if(!up(verify,cl.map(l=>[Math.abs(l),Number(l<0)]),m2).conflict)throw Error("not RUP");verify.push(cl)}
 return {status,reason,probes,rounds,rootChecks,skips,metrics:m,verification:m2,proof,peakClauses:db.length};
};
