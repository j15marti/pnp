/* LSPV-1/475: independent F2/F3/F5 polynomial-evaluation rank control.
   This is NOT the historical R_mix341 accepted-byte checker. */
"use strict";
const outcome=(function(){
let assertions=0;
function verify(ok,message){assertions++;if(!ok)throw Error(message);}
function combinations(arr,k,fn,b=[],i=0){if(k===0){fn(b.slice());return;}for(let j=i;j<=arr.length-k;j++){b.push(arr[j]);combinations(arr,k-1,fn,b,j+1);b.pop();}}
function clauses(n,widths){let out=[];for(let w of widths)combinations([...Array(n).keys()],w,vars=>{for(let s=0;s<(1<<w);s++)out.push(vars.map((v,i)=>((s>>i)&1)?v+1:-v-1));});return out;}
function peel(F,n){F=F.slice();while(F.length){let d=Array(n).fill(0);for(let c of F)for(let lit of c)d[Math.abs(lit)-1]++;let G=F.filter(c=>c.every(lit=>d[Math.abs(lit)-1]>1));if(G.length===F.length)return false;F=G;}return true;}
function models(F,n){let a=[];for(let x=0;x<(1<<n);x++)if(F.every(c=>c.some(lit=>((x>>(Math.abs(lit)-1))&1)===(lit>0?1:0))))a.push(x);return a;}
function monomials(n){let a=[[]];for(let i=0;i<n;i++)a.push([i]);for(let i=0;i<n;i++)for(let j=i+1;j<n;j++)a.push([i,j]);return a;}
function imod(x,p){return (x%p+p)%p;}
function independentColumns(F,n,p){let sols=models(F,n),poly=monomials(n),basis=new Map();
 for(let mon of poly){let v=sols.map(x=>mon.every(i=>(x>>i)&1)?1:0);
   for(let [j,w] of basis)if(v[j]){let z=v[j];v=v.map((a,i)=>imod(a-z*w[i],p));}
   let j=v.findIndex(z=>z!==0);if(j===-1)continue;
   let inv=1;while(imod(inv*v[j],p)!==1)inv++;
   basis.set(j,v.map(z=>imod(z*inv,p)));
 }
 return [basis.size,poly.length,sols.length];
}
function valid(F,n){return F.every(c=>(c.length===3||c.length===4)&&new Set(c.map(Math.abs)).size===c.length&&c.every(l=>Number.isSafeInteger(l)&&l!==0&&Math.abs(l)<=n));}
let n4=clauses(4,[3]),tested4=0,rankTests=0,fields=[2,3,5];
for(let k=0;k<=4;k++)combinations(n4,k,F=>{if(!peel(F,4))return;tested4++;for(let p of fields){const [r,d]=independentColumns(F,4,p);verify(r===d,"bad rank n4 "+p);rankTests++;}});
let seed=4752026;
function rand(){seed=(Math.imul(1664525,seed)+1013904223)>>>0;return seed;}
let sampling=[];
for(let [n,widths,goal] of [[5,[3],900],[6,[3,4],900]]){
  let cs=clauses(n,widths), accepted=0,trials=0;
  while(accepted<goal&&trials<100000){trials++;let k=rand()%5,F=[],ids=new Set();
    while(F.length<k){let id=rand()%cs.length;if(ids.has(id))continue;ids.add(id);F.push(cs[id]);}
    if(!peel(F,n))continue;
    verify(valid(F,n),"invalid source");accepted++;
    for(let p of fields){let [r,d]=independentColumns(F,n,p);verify(r===d,"bad rank mixed "+n+"/"+p);rankTests++;}
  }sampling.push({n,accepted,trials});verify(accepted===goal,"sampler shortage");
}
let bad=[[1,2,3],[-1,2,3]];
verify(!peel(bad,3),"negative falsely peelable");
for(let p of fields){const [r,d,m]=independentColumns(bad,3,p);verify(r===6&&d===7&&m===6,"negative missing quadratic row");}
for(let f of [[[1,1,2]],[[0,2,3]],[[1,2,7]],[[1,2]],[[1,2,3,3]]])verify(!valid(f,6),"bad source accepted");
return {schema:"LSPV1_475_MULTIFIELD_JS",fields,exhaustive_n4_peelable:tested4,sampling,rankTests,assertions,negative_resolvent:[2,3],malformed_rejected:5};
})();
if(typeof console!=="undefined")console.log(JSON.stringify(outcome,null,2));
outcome;