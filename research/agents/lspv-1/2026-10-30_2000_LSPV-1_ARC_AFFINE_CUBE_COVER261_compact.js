'use strict';
// ARC-AFFINE-CUBE-COVER261 independent compact checker (Node.js >=18).
// Every computation finite and deterministic; no SAT oracle or package.
function pc(a){return a.reduce((s,x)=>s^x,0);}
function bits(v,n){return Array.from({length:n},(_,i)=>(v>>i)&1);}
function make(b,contradiction=false){let F=[];for(let j=0;j<b;j++){let p=j%2;for(let a=0;a<8;a++){let v=bits(a,3);if(pc(v)!==p)F.push(v.map((t,k)=>(t?-1:1)*(3*j+k+1)));}}if(contradiction){for(let a=0;a<8;a++){let v=bits(a,3);if(pc(v)===0)F.push(v.map((t,k)=>(t?-1:1)*(k+1)));}}return F;}
function sat(F,a){return F.every(C=>C.some(l=>a[Math.abs(l)-1]===(l>0?1:0)));}
function restrict(F,r){return F.map(C=>C.some(l=>r[Math.abs(l)-1]===(l>0?1:0))?null:C.filter(l=>r[Math.abs(l)-1]<0)).filter(x=>x!==null);}
function cube(i,n){let a=[];for(let k=0;k<n;k++){a.push(i%3-1);i=Math.floor(i/3);}return a;}
function mass(b,r){let p=1;for(let j=0;j<b;j++){let a=r.slice(3*j,3*j+3),k=a.filter(x=>x>=0).length;if(k===3){if(pc(a)!==(j&1))return 0;}else p*=2**(2-k);}return p;}
function extremes(F,i,j){let result={SS:false,SU:false,US:false,UU:false};let vars=[...new Set([...F[i],...F[j]].map(x=>Math.abs(x)-1))];for(let mask=0;mask<(1<<vars.length);mask++){let a=Array(Math.max(...vars)+1).fill(0);vars.forEach((v,k)=>a[v]=(mask>>k)&1);let t=[F[i],F[j]].map(C=>C.filter(l=>a[Math.abs(l)-1]===(l>0?1:0)).length);for(let key of Object.keys(result))if(t[0]===(key[0]==='S'?3:0)&&t[1]===(key[1]==='S'?3:0))result[key]=true;}return result;}
function predicted(F,i,j){let ret={};for(let x of ['S','U'])for(let y of ['S','U']){let req=new Map(),ok=true;for(let [z,k] of [[i,x],[j,y]])for(let l of F[z]){let v=Math.abs(l),bit=(l>0?1:0)^(z==='U'?1:0);if(req.has(v)&&req.get(v)!==bit)ok=false;req.set(v,bit);}ret[x+y]=ok;}return ret;}
let summary=[];
for(let b of [2,3]){
 let n=3*b,F=make(b),G=make(b,true),models=[];
 for(let m=0;m<(1<<n);m++)if(sat(F,bits(m,n)))models.push(m);
 if(models.length!==4**b||bits(0,n).every(x=>x===1))throw Error('model count');
 if(sat(F,Array(n).fill(0))||sat(F,Array(n).fill(1)))throw Error('endpoint');
 if(Array.from({length:1<<n},(_,m)=>bits(m,n)).some(a=>sat(G,a)))throw Error('UNSAT companion');
 let checked=0;for(let H of [F,G])for(let i=0;i<H.length;i++)for(let j=i+1;j<H.length;j++){
 let A=extremes(H,i,j),B=predicted(H,i,j);
 for(let k of Object.keys(A)){if(A[k]!==B[k])throw Error('SS/SU/US/UU '+k);checked++;}
 }
 let cubes=0,nonempty=0,failed=0,max=0;
 for(let i=0;i<3**n;i++){let r=cube(i,n),R=restrict(F,r),m=mass(b,r);
 let brute=models.filter(x=>bits(x,n).every((v,k)=>r[k]<0||v===r[k])).length;
 if(brute!==m)throw Error('mass');
 if(m){nonempty++;if(m>2**Math.floor(R.length/2))throw Error('cover bound');max=Math.max(max,m);}
 cubes++;
 }
 let proofBlockers=0;for(let H of [F,G])for(let C of H){let rho={};for(let l of C)rho[Math.abs(l)-1]=l<0?1:0;
 for(let m=0;m<1<<n;m++){let a=bits(m,n);if(Object.keys(rho).every(k=>a[k]===rho[k])){if(sat(H,a))throw Error('invalid clause blocker');proofBlockers++;}}
 }
 summary.push({blocks:b,models:models.length,cubes,nonempty_cubes:nonempty,pair_extreme_modes_checked:checked,source_blocker_extensions_checked:proofBlockers,max_cube_model_mass:max,lower_bound_at_zero_remaining_clauses:4**b,failures:failed});
}
console.log(JSON.stringify({run_id:'ARC-AFFINE-CUBE-COVER261',status:'COMPUTATIONAL verification of restricted exact theorem',summary},null,2));