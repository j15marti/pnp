/* LSPV-1/526: exact original CORE -> (0+Y=Y) proof-DAG splice.
   PROVED/RESTRICTED: signed-AND2 ER2-OWNER plus ordinary oriented RES,
   NOT an execution of historical R_mix341. Run from repository root:
   node experiments/arc/lspv1_526_core_zero_port.cjs > /tmp/packet526.json
*/
"use strict";
function compose(base, core, ext) {
 const canon=a=>{const b=[...new Set(a)].sort((x,y)=>Math.abs(x)-Math.abs(y)||x-y);if(b.some(v=>b.includes(-v)))throw Error("tautological clause");return b};
 const vid=x=>{const a=Math.abs(x);if(a===4)throw Error("old padding variable escaped");return Math.sign(x)*(a<=3?a:a<=7?a-1:a+2)};
 const ref=i=>i===0?18:i===7?32:i===8?44:i===9?56:i>=10?i+47:(()=>{throw Error("padding SOURCE accessed: "+i)})();
 if(base.proof.lines.length!==118||core.lines.length!==165||ext.proof.lines.length!==190)throw Error("unexpected pinned packet lengths");
 const lines=core.lines.map(l=>({...l})),owners=core.owners.map(g=>({...g}));
 for(const old of ext.proof.lines.slice(118)){
  const x={id:lines.length,kind:old.kind,clause:canon(old.clause.map(vid))};
  if(x.id!==ref(old.id))throw Error("line-map index mismatch");
  if(x.kind==="FACET"){x.owner=old.owner;x.tag=old.tag;}
  else if(x.kind==="RES"){x.left=ref(old.left);x.right=ref(old.right);x.pivot=vid(old.pivot);}
  else throw Error("new source/rule not permitted");
  lines.push(x);
 }
 for(const g of ext.proof.defs.slice(19))owners.push({...g,id:vid(g.id),a:vid(g.a),b:vid(g.b),facets:g.facets.map(ref)});
 const targets=ext.targets.map(t=>({k:t.k,bit:vid(t.bit),input:vid(t.input),positive:ref(t.positive),negative:ref(t.negative)}));
 const counts={sources:lines.filter(l=>l.kind==="SOURCE").length,facets:lines.filter(l=>l.kind==="FACET").length,res:lines.filter(l=>l.kind==="RES").length,defs:owners.length,paid:0,records:lines.length};
 counts.paid=counts.defs+counts.res;
 if(JSON.stringify(counts)!==JSON.stringify({sources:21,facets:102,res:114,defs:34,paid:148,records:237}))throw Error("paid work/record mismatch");
 return {name:"LSPV1_526_CORE_ZERO_PORT",status:"PROVED/RESTRICTED",calculus:"signed-AND2 ER2-OWNER/Resolution, NOT historical R_mix341",family:"local original proper 21-clause cubic mod3 Tseitin CORE, signed orientation +++ and charge 0",source:core.source,lines,owners,base_goals:core.targets,targets,counts,
 upstream_blobs:["3fa42e25e02d05b9a915458a7f780e59fd828c12","c8c62a5eb9a64a6c6949217473ba5075558500c8","1d6334fa5712f374bd0455445cd1bb40ac6a2fe0"]};
}
function main(){
 const fs=require("fs"),vm=require("vm"),crypto=require("crypto");
 const f=["experiments/arc/lspv1_524_strict3_inverse_cancellation.js","experiments/arc/lspv3_523_core_inverse_lift.cjs","experiments/arc/lspv1_525_zero_sum.cjs"];
 const sha=["3fa42e25e02d05b9a915458a7f780e59fd828c12","c8c62a5eb9a64a6c6949217473ba5075558500c8","1d6334fa5712f374bd0455445cd1bb40ac6a2fe0"];
 const txt=f.map((name,i)=>{let s=fs.readFileSync(name,"utf8");const h=crypto.createHash("sha1").update("blob "+Buffer.byteLength(s)+"\0").update(s).digest("hex");if(h!==sha[i])throw Error("upstream SHA mismatch "+name);return s;});
 const sandbox={require,module:{exports:{}},console};const base=vm.runInNewContext(txt[0]+";main()",sandbox),lift=vm.runInNewContext(txt[1]+";lift",sandbox),extend=vm.runInNewContext(txt[2]+";extend",sandbox);
 return compose(base,lift(base),extend(base));
}
if(typeof module!=="undefined")module.exports={main,compose};
if(typeof require!=="undefined" && typeof module!=="undefined"&&require.main===module)console.log(JSON.stringify(main(),null,2));
