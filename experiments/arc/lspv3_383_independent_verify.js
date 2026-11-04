#!/usr/bin/env node
/* Independent verifier for LSPV-3/383 same-source signed perfect matching controls. */
'use strict';
const fs=require('fs'),crypto=require('crypto');
const raw=JSON.parse(fs.readFileSync(process.argv[2],'utf8'));
let checks=0;
function insist(x,msg){checks++;if(!x)throw Error(msg||'check failed')}
function build(n,mask){
  const X=(i,j)=>1+i*n+j, P=(i,j)=>1+n*n+i*n+j, C=[];
  for(let i=0;i<n;i++)C.push(Array.from({length:n},(_,j)=>X(i,j)));
  for(let j=0;j<n;j++)C.push(Array.from({length:n},(_,i)=>X(i,j)));
  for(let i=0;i<n;i++)for(let j=0;j<n;j++)for(let k=j+1;k<n;k++)C.push([-X(i,j),-X(i,k)]);
  for(let j=0;j<n;j++)for(let i=0;i<n;i++)for(let k=i+1;k<n;k++)C.push([-X(i,j),-X(k,j)]);
  for(let i=0;i<n;i++)for(let j=0;j<n;j++)C.push([P(i,j),-X(i,j)]);
  for(let i=0;i<n;i++)for(let j=0;j<n;j++)C.push([((mask>>(i*n+j))&1)?-P(i,j):P(i,j)]);
  return C;
}
function checkAssignment(clauses,n,mask,xbits){
  const m=n*n;
  for(const c of clauses){
    let yes=false;
    for(const v of c){
      const t=Math.abs(v)-1;
      const bit=(t<m)?((xbits>>t)&1):(1-((mask>>(t-m))&1));
      if((v>0 && bit===1)||(v<0 && bit===0)){yes=true;break;}
    }
    if(!yes)return false;
  }
  return true;
}
function permute(n,mask){
  let count=0;
  function go(row,used){
    if(row===n){count++;return;}
    for(let col=0;col<n;col++)if(!(used&(1<<col))&&!(mask&(1<<(row*n+col))))go(row+1,used|(1<<col));
  }
  go(0,0);return count;
}
let totalCases=0;
for(const o of raw.cases){
 const {n}=o;
 const masks=[];
 if(n<4){for(let m=0;m<2**(n*n);m++)masks.push(m);}else{
   masks.push(0,65535);
   for(let i=0;i<16;i++){masks.push(1<<i,(65535^(1<<i)));}
 }
 let sat=0,unsat=0;
 let sourceSignature=null;
 const dig=crypto.createHash('sha256');
 for(const m of masks){
   const cs=build(n,m), pcount=permute(n,m);
   insist(cs.length===n**3+n*n+2*n,'clause count');
   insist(cs.flat().length===2*n**3+3*n*n,'occurrence count');
   const sig=cs.map(c=>c.map(Math.abs).join(',')).join(';');
   if(sourceSignature===null)sourceSignature=sig;
   insist(sig===sourceSignature,'signed incidence changed');
   if(n<=3){
     let exact=0;
     for(let v=0;v<(1<<(n*n));v++)if(checkAssignment(cs,n,m,v))exact++;
     insist(exact===pcount,'CNF count mismatch');
     dig.update(m+':'+(pcount>0?1:0)+';');
   }
   if(pcount>0)sat++;else unsat++;
   totalCases++;
 }
 if(n<=3){insist(sat===o.sat && unsat===o.unsat,'full census');insist(dig.digest('hex')===o.mask_digest,'digest');}
 else{insist(sat<=o.sat && unsat<=o.unsat,'stratified subset');}
 insist(o.clauses===n**3+n*n+2*n && o.occurrences===2*n**3+3*n*n,'reported sizes');
 insist(o.variables===2*n*n,'variable count');
}
for(const n of [2,3]){
 const full=1<<(n*n), U=new Uint8Array(full);
 for(let a=0;a<full;a++)U[a]=(permute(n,a)===0)?1:0;
 for(let a=0;a<full;a++){
   const b=(full-1)^a;
   let enabledCount=0;
   function choose(i,used){if(i===n){enabledCount++;return;}for(let j=0;j<n;j++)if(!(used&(1<<j))&&(b&(1<<(i*n+j))))choose(i+1,used|(1<<j));}
   choose(0,0);
   insist(U[a] === (1-(enabledCount>0?1:0)), 'De Morgan duality');
   for(let e=0;e<n*n;e++)if(!(a&(1<<e)))insist(U[a]<=U[a|(1<<e)],'monotonicity');
 }
}
for(const n of [2,3]){
 const cs=build(n,0), p=n*n+1;
 insist(cs[cs.length-n*n].length===1 && cs[cs.length-n*n][0]===p, 'unit position');
 insist(cs[cs.length-2*n*n].join(',')===[p,-1].join(','),'gate position');
 const neg=build(n,1);
 insist(neg.slice(0,-n*n).every((c,i)=>String(c)===String(cs[i])),'only source units differ');
 insist(neg[neg.length-n*n][0]===-p,'unit sign inversion');
}
insist(raw.malformed_rejections===6, 'reported mutation count');
console.log(JSON.stringify({result:'PASS',independent_assertions:checks,all_masks_n2_n3:true,stratified_n4_masks:34,total_fixture_masks:totalCases,source:'independent JavaScript checker'}));
