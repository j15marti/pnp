module.exports=function fused(C,api,cap=2000000){
 const {up,canon,key}=api,db=C.slice(),seen=new Set(db.map(key)),proof=[],m={scans:0,lits:0,cap};let probes=0,rounds=0,rootChecks=0,skips=0,status="UNKNOWN",reason="fixed point",binaryUnits=0,unaryUnits=0;
 function add(cl){cl=canon(cl);let k=key(cl);if(seen.has(k))return false;seen.add(k);db.push(cl);proof.push(cl);return true}
 function root(){rootChecks++;let a=up(db,[],m);if(a.conflict){add([]);status="UNSAT";reason="root UP";}return a}
 function close(cl){
  if(cl.length===2){let [u,v]=cl;for(let [a,b] of [[u,v],[v,u]])if(seen.has(key(canon([a,-b])))&&add([a]))binaryUnits++}
  let a=root();if(a.conflict)return a;
  for(let v of cl.map(Math.abs))if(!a.A.has(v))for(let b of [0,1]){probes++;if(up(db,[[v,b]],m).conflict){if(add([b?-v:v]))unaryUnits++;a=root();if(a.conflict)return a;break}}
  return a
 }
 try{outer:for(;;){rounds++;let a=root();if(a.conflict)break;let vars=[...a.score].sort((a,b)=>b[1]-a[1]||a[0]-b[0]).map(x=>x[0]),old=proof.length;
  for(let v of vars)for(let b of [0,1]){if(a.A.has(v)){skips++;continue}probes++;if(up(db,[[v,b]],m).conflict){let cl=[b?-v:v];if(add(cl))unaryUnits++;a=root();if(a.conflict)break outer}}
  for(let i=0;i<vars.length;i++)for(let j=i+1;j<vars.length;j++)for(let b of [0,1])for(let c of [0,1]){
   let u=vars[i],v=vars[j],cl=canon([b?-u:u,c?-v:v]);if(seen.has(key(cl))||a.A.has(u)||a.A.has(v)){skips++;continue}probes++;
   if(up(db,[[u,b],[v,c]],m).conflict){add(cl);a=close(cl);if(a.conflict)break outer}
  }
  if(proof.length===old)break;
 }}catch(e){if(e.message!=="cap")throw e;reason="scan cap"}
 // independent literal-array verifier, no call to discovery propagation.
 let scan=0,lits=0,verify=C.slice();for(let cl of proof){let a=new Map(cl.map(l=>[Math.abs(l),Number(l<0)])),contradiction=false,changed=true;
  while(changed&&!contradiction){changed=false;for(let d of verify){scan++;let n=0,last=0,sat=false;for(let l of d){lits++;let z=a.get(Math.abs(l));if(z===undefined){n++;last=l}else if(z===Number(l>0)){sat=true;break}}
    if(sat)continue;if(n===0){contradiction=true;break}if(n===1){a.set(Math.abs(last),Number(last>0));changed=true}
  }}if(!contradiction)throw Error("not RUP");verify.push(cl)}
 return {status,reason,probes,rounds,rootChecks,skips,binaryUnits,unaryUnits,metrics:m,verification:{scans:scan,lits},proof,peakClauses:db.length};
};
