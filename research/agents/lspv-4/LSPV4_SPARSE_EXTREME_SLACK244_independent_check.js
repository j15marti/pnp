"use strict";
/* LSPV-4 SPARSE-EXTREME-SLACK244: independent JS verification.
   No Python import, SAT oracle, external package, or unknown answer bit. */
const A=require("node:assert/strict");
const B=[[1,3,5],[1,-3,6],[-1,4,5],[-1,-4,6],[2,3,-5],[2,-3,-6],[-2,4,-5],[-2,-4,-6]];
const ring=r=>Array.from({length:r},(_,j)=>B.map((c,k)=>c.map((z,p)=>Math.sign(z)*(6*(k===0&&p===0?(j+r-1)%r:j)+Math.abs(z))))).flat();
const target=(C,mode)=>Object.fromEntries(C.map(z=>[Math.abs(z),mode==="S"?Number(z>0):Number(z<0)]));
const count=(C,a)=>C.filter(z=>a[Math.abs(z)-1]===Number(z>0)).length;
const resolve=(A0,B0,p)=>{let a=new Set(A0),b=new Set(B0);if(!a.has(p))[a,b]=[b,a];
 A.ok(a.has(p)&&b.has(-p));const R=[...new Set([...a].filter(z=>z!==p).concat([...b].filter(z=>z!==-p)))];
 A.ok(R.every(z=>!R.includes(-z)));return R.sort((x,y)=>Math.abs(x)-Math.abs(y)||x-y)};
function sparse(F,n){let occ=Array.from({length:n},()=>[]),same=0,opp=0,flags=new Map();
 F.forEach((C,j)=>C.forEach(z=>occ[Math.abs(z)-1].push([j,z>0])));
 for(const rows of occ){A.equal(rows.length,4);A.equal(rows.filter(x=>x[1]).length,2);
  for(let i=0;i<4;i++)for(let k=i+1;k<4;k++){let x=rows[i],y=rows[k];
   A.notEqual(x[0],y[0]);let key=Math.min(x[0],y[0])+","+Math.max(x[0],y[0]);
   let fl=flags.get(key)||[false,false];if(x[1]===y[1]){fl[0]=true;same++}else{fl[1]=true;opp++}flags.set(key,fl)}}
 A.equal(same,2*n);A.equal(opp,4*n);A.ok(flags.size<=6*n);return flags}
function dag(F,r){let j=r-1,P0=resolve(F[2],F[3],4),P1=resolve(F[1],P0,1),P2=resolve(F[0],P1,3),
 P3=j===0?P0:resolve(F[8*j+2],F[8*j+3],6*j+4),
 R=resolve(P2,P3,6*j+1),want=[5,6,6*j+5,6*j+6].filter((z,i,a)=>a.indexOf(z)===i).sort((a,b)=>a-b);
 A.deepEqual(R,want);return R}
let modes=0,full=0,proven=0,rows=[];
for(let r=1;r<=12;r++){let F=ring(r),n=6*r,m=8*r,flags=sparse(F,n);
 A.equal(F.length,m);A.equal(new Set(F.map(C=>C.slice().sort((a,b)=>a-b).join(","))).size,m);
 for(let j=0;j<m;j++){let T=target(F[j],"S"),U=target(F[j],"U");
   A.ok(Object.keys(T).every(v=>1-T[v]===U[v]));
   for(let k=j+1;k<m;k++){let fl=flags.get(j+","+k)||[false,false];
    for(const mode of ["SS","SU","US","UU"]){let a=target(F[j],mode[0]),b=target(F[k],mode[1]);
     let observed=Object.keys(a).every(v=>!(v in b)||a[v]===b[v]);
     A.equal(observed,mode==="SS"||mode==="UU"?!fl[1]:!fl[0]);modes++}}}
 if(r<=2)for(let mask=0;mask<2**n;mask++){let a=Array.from({length:n},(_,i)=>(mask>>i)&1);
   let b=a.map(v=>1-v);A.ok(F.every(C=>count(C,a)+count(C,b)===3));full++;
   for(let i=0;i<n;i++){let c=a.slice();c[i]^=1;
    F.forEach(C=>{let delta=C.filter(z=>Math.abs(z)-1===i).reduce((s,z)=>s+(a[i]===Number(z>0)?-1:1),0);
      A.equal(count(C,c)-count(C,a),delta)})}}
 let learned=dag(F,r);proven++;
 let pin=Array.from({length:n},()=>null);for(let j=0;j<r;j++){pin[6*j+4]=0;pin[6*j+5]=0}
 let Z=0,e=0,w=0,H2=0,H3=0;
 for(const C of F){let c=C.filter(z=>pin[Math.abs(z)-1]!==null&&pin[Math.abs(z)-1]===Number(z>0)).length;
  let u=C.filter(z=>pin[Math.abs(z)-1]===null).length;
  if(c===0){Z++;A.equal(u,2)}else e+=u;H2+=Number(c>=2);H3+=Number(c===3)}
 let d=m/2-H2-H3;A.equal(d,4*r);A.equal(e,8*r);A.equal(w,0);A.equal(2*d,w+e);
 let witness=Array.from({length:n},(_,i)=>[1,0,1,0,1,0][i%6]);A.ok(F.every(C=>count(C,witness)>0));
 if(r<=2)for(let mask=0;mask<2**n;mask++){let a=Array.from({length:n},(_,i)=>(mask>>i)&1);
  if(learned.every(z=>a[z-1]===0))A.ok(F.some(C=>count(C,a)===0))}
 rows.push({r,n,m,nondefault_pairs:flags.size,w,d,e,source_DAG_steps:r===1?4:5})}
console.log(JSON.stringify({result:"PASS",pair_modes:modes,coherent_complements:full,source_DAGs:proven,rows},null,2));
