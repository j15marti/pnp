'use strict';
// LSPV-4 345. Standalone source-authenticated bit-PHP reproducer.
// No solver imports. The streaming logspace theorem is mathematical;
// this compact Node program explicitly materializes small test sources.
const crypto=require('crypto');
function check(v,s){if(!v)throw Error(s);}
function bphp(h){
 const ell=Math.log2(h),p=h+1,m=h*p*(p-1)/2;
 check(Number.isInteger(ell),'power of two');
 let clauses=[],s='p cnf '+(p*ell)+' '+m+'\n';
 for(let i=0;i<p;i++)for(let j=i+1;j<p;j++)for(let c=0;c<h;c++){
   let a=[];
   for(const q of [i,j])for(let b=0;b<ell;b++){
     const v=q*ell+b+1;a.push((c>>b)&1?-v:v);
   }
   clauses.push(a);s+=a.join(' ')+' 0\n';
 }
 return {h,n:p*ell,m,ell,s,clauses};
}
function models(n,cs){
 let ans=0;
 for(let v=0;v<2**n;v++){
   if(cs.every(c=>c.some(l=>Boolean((v>>(Math.abs(l)-1))&1)===(l>0))))ans++;
 }
 return ans;
}
function run(){
 const sizes=[[2,52],[4,508],[8,6061],[16,62990]];
 let out=[],flips=0;
 for(const [h,len] of sizes){
  const z=bphp(h);
  check(z.s.length===len,'source exact bytes '+h);
  if(h<=4){
   check(models(z.n,z.clauses)===0,'original UNSAT '+h);
   for(let j=0;j<z.m;j++)for(let k=0;k<z.clauses[j].length;k++){
    const c=z.clauses.map(x=>x.slice());c[j][k]=-c[j][k];
    check(models(z.n,c)===(h===2?1:6),'signed repair '+h+'/'+j+'/'+k);
    flips++;
   }
  }
  out.push({h,variables:z.n,clauses:z.m,source_bytes:len,
            sha256:crypto.createHash('sha256').update(z.s).digest('hex')});
 }
 check(flips===172,'172 finite sign-flip controls');
 console.log(JSON.stringify({run:'LSPV4_BPHP_STREAM_ATLAS345',
    status:'PASS finite controls; NOT a native FLMV trace or Rmix worst-case lower bound',
    originals:out,exhaustively_verified_sign_flips:flips},null,2));
}
run();
