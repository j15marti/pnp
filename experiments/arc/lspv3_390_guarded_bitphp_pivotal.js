#!/usr/bin/env node
"use strict";
// LSPV-3/390 self-contained public finite verifier. No SAT library, no randomness.
const crypto=require("crypto");
let checks=0;
function ok(v,msg){if(!v)throw Error(msg);checks++}
const gam=z=>{if(z<1)throw Error("gamma");let s=z.toString(2);return "0".repeat(s.length-1)+s};
const w=v=>Math.max(1,Math.floor(Math.log2(v))+1);
function construct(ell){
  const n=2**ell,V=(n+1)*ell+1,cs=[],tags=[];
  for(let i=0;i<=n;i++)for(let j=i+1;j<=n;j++)for(let h=0;h<n;h++){
    const c=[[1,V]];
    for(const p of [i,j])for(let r=0;r<ell;r++)c.push([(h>>r)&1,p*ell+r+1]);
    cs.push(c);tags.push([i,j,h]);
  }
  cs.push([[0,V]]);
  let bits="1011"+gam(V+1)+gam(cs.length+1); const sites=[];
  for(const c of cs){bits+=gam(c.length+1);for(const [s,id] of c){
    sites.push(bits.length);bits+=String(s)+id.toString(2).padStart(w(V),"0");
  }}
  return {n,V,cs,tags,bits,sites};
}
function parse(s){
  if(!s.startsWith("1011"))throw Error("tag");
  let p=4;
  function g(){
    let z=0;while(p<s.length&&s[p]==="0"){p++;z++}
    if(p+z>=s.length||s[p]!=="1")throw Error("gamma");
    let y=parseInt(s.slice(p,p+z+1),2);p+=z+1;return y;
  }
  const V=g()-1,m=g()-1;if(V<1||V>100000||m<0||m>100000)throw Error("header");
  const cs=[],sites=[];
  for(let j=0;j<m;j++){const k=g()-1;if(k<0||k>100000)throw Error("width");let c=[];
    for(let z=0;z<k;z++){
      if(p+1+w(V)>s.length)throw Error("short literal");
      const sign=Number(s[p]);sites.push(p);const id=parseInt(s.slice(p+1,p+1+w(V)),2);
      if(!Number.isInteger(sign)||sign<0||sign>1||id<1||id>V)throw Error("literal");
      c.push([sign,id]);p+=1+w(V);
    }cs.push(c);
  }
  if(p!==s.length)throw Error("extra input");
  return {V,cs,sites};
}
function val(cs,v){return cs.every(c=>c.some(([s,id])=>v[id]!==s))}
function assignment(ell,n,V,i,j,h){
  const holes=Array.from({length:n},(_,z)=>z).filter(z=>z!==h);
  const alloc=Array(n+1).fill(-1);alloc[i]=alloc[j]=h;
  let k=0;for(let p=0;p<=n;p++)if(alloc[p]===-1)alloc[p]=holes[k++];
  let v=Array(V+1).fill(0);
  for(let p=0;p<=n;p++)for(let r=0;r<ell;r++)v[p*ell+r+1]=(alloc[p]>>r)&1;
  v[V]=1;return v;
}
let output=[];
for(const ell of [1,2,3]){
  const {n,V,cs,tags,bits,sites}=construct(ell);
  const x=parse(bits);ok(x.V===V&&JSON.stringify(x.cs)===JSON.stringify(cs),"original parse");
  ok(JSON.stringify(x.sites)===JSON.stringify(sites),"source coordinates");
  let cur=0;
  for(let a=0;a<tags.length;a++){
    const v=assignment(ell,n,V,...tags[a]);
    const failed=cs.map((c,z)=>val([c],v)?-1:z).filter(z=>z>=0);
    ok(failed.length===1&&failed[0]===a,"exact selected collision");
    for(let j=0;j<cs[a].length;j++){
      const p=sites[cur],flip=bits.slice(0,p)+(bits[p]==="1"?"0":"1")+bits.slice(p+1);
      const y=parse(flip);
      ok(y.cs[a][j][0]!==cs[a][j][0]&&val(y.cs,v),"same-length SAT neighbor");
      cur++;
    }
  }
  let p=sites[cur],unitFlip=bits.slice(0,p)+"1"+bits.slice(p+1);
  ok(val(parse(unitFlip).cs,Array(V+1).fill(0)),"unit signed neighbor");
  ok(++cur===sites.length,"all coordinates pivotal");
  for(const malformed of ["",bits+"1",bits.slice(0,-1),"0011"+bits.slice(4),
    bits.slice(0,sites[0]+1)+"0".repeat(w(V))+bits.slice(sites[0]+1+w(V))]){
    let rejected=false;try{parse(malformed)}catch(e){rejected=true}
    ok(rejected,"reject malformed");
  }
  output.push({ell,n,clauses:cs.length,source_bits:bits.length,pivotal_signs:sites.length,
    all_flip_SAT_neighbors:cur,source_sha256:crypto.createHash("sha256").update(bits).digest("hex")});
}
console.log(JSON.stringify({status:"PASS",checks,rows:output},null,2));
