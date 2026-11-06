#!/usr/bin/env node
// Independent LSPV4/450 referee: builds clauses by forbidden truth triples,
// and gauge by tree-leaf elimination, not the producer's prefix formula.
// Usage: node lspv4_450_hamiltonian_gauge_referee.mjs raw.json
import fs from 'node:fs';
const f=JSON.parse(fs.readFileSync(process.argv[2]||'raw.json','utf8'));
let A=0;function ck(ok,label){A++;if(!ok)throw new Error('assertion '+A+': '+label)}
const edges=n=>[...Array(n)].map((_,i)=>[i,(i+1)%n]).concat([...Array(n/2)].map((_,i)=>[i,i+n/2]);
function makeClauses(n,charge){const E=edges(n),rows=[];
 for(let v=0;v<n;v++){
  const inc=E.map(([a,b],idx)=>(a===v||b===v)?idx:-1).filter(x=>x>=0).sort((a,b)=>a-b);
  ck(inc.length===3,'degree cubic');
  for(let p=0;p<=1;p++)for(let q=0;q<=1;q++){
   const r=(charge[v]^1)^p^q;
   rows.push(inc.map((id,t)=>[id,([p,q,r][t]===0?1:-1)]));
  }
 }
 return rows;
}
const sorter=rs=>rs.map(cl=>cl.map(([id,s])=>id+':'+s).sort().join('|')).sort().join(';');
function cofact(F,n,values){const B=[];
 for(const cl of F){const next=[];let sat=false;
  for(const [id,s] of cl){const ix=id-n;
   if(ix>=0&&ix<values.length){const val=values[ix];if((val===1&&s===1)||(val===0&&s===-1)){sat=true;break}}
   else next.push([id,s]);
  }
  if(!sat)B.push(next);
 }return B;
}
function charges(n,k,alpha,beta){const d=Array(n).fill(0);
 for(let j=0;j<k;j++){const p=alpha[j]^beta[j];d[j]^=p;d[j+n/2]^=p;}
 return d;
}
function treeGauge(n,k,alpha,beta){
 const d=charges(n,k,alpha,beta),z=Array(3*n/2).fill(0);
 for(let v=n-1;v>=1;v--){z[v-1]=d[v];d[v-1]^=d[v];d[v]=0;}
 ck(d[0]===0,'root parity');return z;
}
function originalCoEq(rows,vals){return rows.every(cl=>cl.some(([id,s])=>s===1?vals[id]===1:vals[id]===0))}
const totals={total_cases:0,clauses:0,host_assignment_tests:0,incidence_checks:0,canonical_mismatch:0};
let state=45020261106;function rnd(){state=(Math.imul(state,1664525)+1013904223)>>>0;return state&1;}
for(const rec of f.records){
 const {H:n,k,alpha,beta}=rec,charges0=Array(n).fill(0),E=edges(n);
 const z=treeGauge(n,k,alpha,beta);
 ck(z.slice(0,n).join(',')===rec.cycle_gauge.join(','),'independent tree witness');
 for(let j=0;j<n;j++){
  const a=E.reduce((sum,e,id)=>sum^((e[0]===j||e[1]===j)?z[id]:0),0);
  ck(a===charges(n,k,alpha,beta)[j],'incidence equality');totals.incidence_checks++;
 }
 for(let parity=0;parity<2;parity++){
  charges0[0]=parity;
  const orig=makeClauses(n,charges0),F=cofact(orig,n,alpha),G=cofact(orig,n,beta);
  const flipped=F.map(cl=>cl.map(([id,s])=>[id,z[id]?-s:s]));
  ck(sorter(flipped)===sorter(G),'signed source multiset equivalence');
  for(let ii=0;ii<20;ii++){
   const values=Array(E.length).fill(0).map(()=>rnd()),trans=values.map((v,id)=>v^z[id]);
   ck(originalCoEq(F,values)===originalCoEq(G,trans),'truth-preserving bijection');
   totals.host_assignment_tests++;
  }
  totals.clauses+=F.length;
 }
 ck(k>=0&&k<=n/2,'descriptor bound');
 ck(rec.cofactor_clauses===4*n-4*k,'residual count');
 ck(rec.ternary===4*(n-2*k)&&rec.binary===4*k,'clause width count');
 let broken=z.slice();broken[0]^=1;
 const d=charges(n,k,alpha,beta);
 const checkInc=(candidate,v)=>E.reduce((p,[u,w],id)=>p ^ ((u===v||w===v)?candidate[id]:0),0)===d[v];
 ck(!checkInc(broken,0),'bad gauge incidence fails at vertex 0');
 ck(!checkInc(broken,1),'bad gauge incidence fails at vertex 1');
 totals.total_cases++;
}
ck(totals.total_cases===240,'raw count');
console.log(JSON.stringify({run:'LSPV4_450',status:'PASS',assertions:A,...totals},null,2));
