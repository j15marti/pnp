"use strict";
/* LSPV-1/479. Pang 2026 Thm 1.1 quantitative parameter control.
 * Numerical c choices are illustrative, NOT published expander constants.
 * No native R_mix341 checker or SAT-algorithm lower bound.
 */
function audit(){
 let assertions=0,eligible=0,ineligible=0,rows=[],models={};
 const ok=(v,msg)=>{assertions++;if(!v)throw Error(msg)};
 const ps=[3,5,7],cs=[0.05,0.2],epss=[0.25,0.5,0.75];
 const hs=[1e8,1e12,1e16,1e24,1e32,1e48,1e64,1e80];
 for(const p of ps)for(const c of cs)for(const epsilon of epss){
  const kappa=(1-epsilon)/((p-1)*Math.log(176/c));
  ok(kappa>0&&kappa<1,"kappa");
  for(const h of hs){
   const r=Math.floor(kappa*Math.log(h));
   if(r<1){ineligible++;continue;}
   const n=5.5*h,D=Math.floor(c*h)-1;
   if(D<Math.max(32*(p-1)**2*r,24)){ineligible++;continue;}
   eligible++;
   const logActual=Math.log(D)-Math.log(32*p*p*r)+(p-1)*r*Math.log(D/(16*n));
   const logFloor=Math.log(c)-Math.log(64*p*p*r)+epsilon*Math.log(h);
   ok(logActual+1e-9>=logFloor,"Pang logarithmic bound");
   ok(r<=kappa*Math.log(h),"floor bound");
   ok(D>=c*h/2,"degree parameter");
   ok(D/(16*n)>=c/176,"source-variable ratio");
   rows.push({p,c,epsilon,h,r,lower_log_S:+logActual.toFixed(3),comparison_log:+logFloor.toFixed(3)});
  }
 }
 const edges=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]];
 const sat=(C,assignment)=>C.some(l=>assignment[l.v]===l.pos);
 const clauses=charges=>{
  const out=[];
  for(let v=0;v<4;v++){
   const ids=edges.map((e,j)=>e.includes(v)?j:-1).filter(j=>j>=0);
   for(let mask=0;mask<8;mask++){
    const bits=ids.map((_,k)=>(mask>>k)&1);
    if((bits[0]^bits[1]^bits[2])===charges[v])continue;
    out.push(ids.map((j,k)=>({v:j,pos:!Boolean(bits[k])})));
   }
  }return out;
 };
 for(const [label,ch]of [["odd",[1,0,0,0]],["even",[0,0,0,0]]]){
  const F=clauses(ch);ok(F.length===16,"source count");
  let count=0,sectionChecks=0;
  for(let mask=0;mask<64;mask++){
   const assign=edges.map((_,i)=>Boolean((mask>>i)&1));
   const f=F.every(C=>sat(C,assign));if(f)count++;
   for(const C of F){
    const l3=C[2],a=assign[l3.v],alphaPos=l3.pos;
    const P=[C[0],C[1],{v:6,pos:alphaPos}];
    const Q=[C[0],C[2],{v:6,pos:!alphaPos}];
    const extension=[...assign,a];
    ok((sat(P,extension)&&sat(Q,extension))===sat(C,assign),"positive-alias signed section");
    sectionChecks++;
   }
  }
  ok(count===(label==="odd"?0:8),"original parity model count");
  models[label]={source_clauses:F.length,models:count,section_checks:sectionChecks};
 }
 ok(eligible>30,"coverage");
 return {status:"PASS",type:"arithmetic sanity controls for published theorem application",illustrative_c_not_certified:true,assertions,eligible,ineligible,illustrative_rows:rows.slice(0,12),max_r:Math.max(...rows.map(r=>r.r)),tseitin_k4:models,limitations:"No native R_mix341 checker, no measured expander PC-degree constant, no asymptotic finite computation."};
}
if(typeof module!=="undefined"&&module.exports)module.exports={audit};
if(typeof require!=="undefined"&&require.main===module)console.log(JSON.stringify(audit(),null,2));
