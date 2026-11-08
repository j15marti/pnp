"use strict";
/* LSPV-2/496, finite independent JS proof-control. Promise only. Node >=18. */
function primes(k){const out=[];for(let n=2;out.length<k;n++){let ok=true;for(let d=2;d*d<=n;d++)if(n%d===0){ok=false;break;}if(ok)out.push(n);}return out;}
function fp(a,b,p){if(a.length!==b.length)throw Error("length");let h=0;for(let side=0;side<2;side++){let seq=side?b:a;let power=1;for(let bit of seq){if(bit!==0&&bit!==1)throw Error("not bit");h=(h+(side?-1:1)*bit*power+p)%p;power=power*2%p;}}return h;}
function vec(n,m){return Array.from({length:m},(_,i)=>(n>>i)&1);}
function graph(which){
 const H=which==="k33"?6:8,edges=[];
 if(which==="k33")for(let x=0;x<3;x++)for(let y=3;y<6;y++)edges.push([x,y]);
 else if(which==="cube")for(let x=0;x<8;x++)for(let z=0;z<3;z++){let y=x^(1<<z);if(x<y)edges.push([x,y]);}
 else throw Error("which");
 function parity(n){let a=0;while(n){a^=n&1;n>>=1;}return a;}
 const left=Array.from({length:H},(_,i)=>i).filter(i=>which==="k33"?i<3:parity(i)===0);
 const match=which==="k33"?[[0,3],[1,4],[2,5]]:edges.filter(([x,y])=>(x^y)===1);
 return {H,edges,left,match};
}
function cnf(which,a,b){
 const {H,edges,left,match}=graph(which),m=H/2, L=new Set(left),inc=Array.from({length:H},()=>[]);
 if(a.length!==m||b.length!==m)throw Error("m");
 const tags=new Map(match.map((e,i)=>[e.join(":"),i]));let next=H+1;
 for(const e of edges){let i=tags.get(e.join(":"));if(i===undefined){for(const v of e)inc[v].push(next);next++;}
 else for(const v of e)inc[v].push(2*i+1+(L.has(v)?a[i]:b[i]));}
 let clauses=[];const order=left.concat(Array.from({length:H},(_,i)=>i).filter(x=>!L.has(x)));
 for(const v of order){const ids=inc[v].slice().sort((x,y)=>x-y),ch=v===0?1:0;if(new Set(ids).size!==3)throw Error("repeated literal");
 for(let b0=0;b0<8;b0++){const z=[b0&1,(b0>>1)&1,(b0>>2)&1];
 if((z[0]^z[1]^z[2])!==ch)clauses.push(ids.map((id,j)=>z[j]?-id:id));}}
 return clauses;
}
function satAffine(clauses){
 const ids=[...new Set(clauses.flat().map(Math.abs))].sort((a,b)=>a-b),index=new Map(ids.map((id,i)=>[id,i]));
 const basis=new Map();
 for(let k=0;k<clauses.length;k+=4){
  const block=clauses.slice(k,k+4),own=block[0].map(Math.abs);
  if(new Set(own).size!==3||block.length!==4)throw Error("invalid block");
  const p=new Set(block.map(c=>c.map(x=>x<0?1:0).reduce((a,b)=>a^b,0)));
  if(p.size!==1)throw Error("bad parity clauses");
  let rhs=1-[...p][0],row=own.reduce((r,id)=>r^(1n<<BigInt(index.get(id))),0n);
  while(row!==0n){const least=(row&(-row)).toString();
   if(!basis.has(least)){basis.set(least,[row,rhs]);break;}
   const [r,z]=basis.get(least);row^=r;rhs^=z;}
  if(row===0n&&rhs) return false;
 }
 return true;
}
function test(){
 let checks=0,pairs=0,sat=0,unsat=0,bad=0,worst=0;
 for(const which of ["k33","cube"]){
 const m=graph(which).match.length;let K=1;while(K<4*m)K*=2;const P=primes(K);
 for(let ai=0;ai<(1<<m);ai++)for(let bi=0;bi<(1<<m);bi++){
  const a=vec(ai,m),b=vec(bi,m),isSAT=ai!==bi,C=cnf(which,a,b);
  if(C.length!==8*m||C.some(c=>c.length!==3||new Set(c.map(Math.abs)).size!==3))throw Error("invalid CNF");checks++;
  if(new Set(C.map(c=>c.join(","))).size!==C.length)throw Error("repeated clause");checks++;
  if(satAffine(C)!==isSAT)throw Error("GF2 parity mismatch");checks++;
  let missed=0;for(const p of P){if((fp(a,b,p)!==0)!==isSAT)missed++;checks++;}
  if(!isSAT&&missed)throw Error("false SAT on UNSAT diagonal");
  if(isSAT){if(missed>m)throw Error("prime factor bound");sat++;bad+=missed;worst=Math.max(worst,missed);checks++;}
  else unsat++;pairs++;
 }
 }
 // All small fixed-prime CRT portfolios have an exact sharp threshold.
 for(let m=3;m<=8;m++){const plist=primes(6);let product=1;
  for(let j=0;j<plist.length;j++){product*=plist[j];
   if(product<(1<<m)){const z=vec(product,m),zero=vec(0,m);
    if(!plist.slice(0,j+1).every(p=>fp(z,zero,p)===0))throw Error("CRT lower control");
    checks++;
   }else{for(let d=1;d<(1<<m);d++)if(plist.slice(0,j+1).every(p=>d%p===0))throw Error("CRT upper control");checks++;break;}
  }
 }
 if(fp([1,0,0],[1,1,0],2)!==0)throw Error("missed collision");checks++;
 for(const corrupt of [[0,2,0],[0,-1,1]]){let caught=false;try{fp(corrupt,[0,0,0],5);}catch(_){caught=true;}if(!caught)throw Error("malformed accepted");checks++;}
 return {status:"PASS",model:"independent exact finite seeded randomized promise test",checks,pairs,sat,unsat,collision_samples_total:bad,worst_bad_primes_per_pair:worst,graphs:["k33","cube"],native_FLMV:false};
}
if(typeof module!=="undefined"&&require.main===module)console.log(JSON.stringify(test(),null,2));
