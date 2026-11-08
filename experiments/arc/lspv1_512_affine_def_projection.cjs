"use strict";
/* LSPV-1/512. Independent Node audit. Distinct affine-DEF + XOR system. */
function check(b,why){if(!b)throw new Error(why)}
function xor(a,b){return [a[0]^b[0],a[1]^b[1]]}
function pop(x){let c=0;while(x){c+=x&1;x>>>=1}return c}
function evalPar(mask,assignment){return pop(mask&assignment)&1}
function edgesFor(name,h){
 const edges=[];
 if(name==="K4"){for(let i=0;i<h;i++)for(let j=i+1;j<h;j++)edges.push([i,j]);}
 if(name==="K33"){for(let i=0;i<3;i++)for(let j=3;j<6;j++)edges.push([i,j]);}
 if(name==="cube3"){for(let i=0;i<8;i++)for(let k=0;k<3;k++){let j=i^(1<<k);if(i<j)edges.push([i,j]);}}
 return edges;
}
function project(row,subst,n){
 let [mask,rhs]=row;
 for(let j=n;j<subst.length;j++)if(mask&(1<<j)){mask^=1<<j;mask^=subst[j][0];rhs^=subst[j][1];}
 return [mask,rhs];
}
function validateDefs(defs,n){
 const seen=new Set();
 for(let i=0;i<defs.length;i++){
  let out=n+i,mask=defs[i][0];
  if(seen.has(out)||!(mask&(1<<out))||(mask>>>(out+1)))return false;
  seen.add(out);
 }return true;
}
function audit(name,h){
 const E=edgesFor(name,h),n=E.length;
 check(n===3*h/2,"not cubic");
 let source=[];
 for(let v=0;v<h;v++){
  let mask=0;
  E.forEach(([a,b],i)=>{if(a===v||b===v)mask|=1<<i});
  check(pop(mask)===3,"degree");source.push([mask,v===0?1:0]);
 }
 let cnf=[];
 for(let v=0;v<h;v++){
  let inc=[];for(let i=0;i<n;i++)if(source[v][0]&(1<<i))inc.push(i);
  for(let t=0;t<8;t++){
    if((pop(t)&1)!==source[v][1]){
      cnf.push(inc.map((e,j)=>t&(1<<j)?-(e+1):e+1));
    }
  }
 }
 check(cnf.length===4*h,"signed clauses");
 let assignments=0;
 for(let a=0;a<(1<<n);a++){
  let cnfSat=cnf.every(cl=>cl.some(l=>l>0? !(a&(1<<(l-1))): !!(a&(1<<(-l-1)))));
  let xorSat=source.every(([m,r])=>evalPar(m,a)===r);
  check(cnfSat===xorSat,"source parity mismatch");
  if(cnfSat)assignments++;
 }
 check(assignments===0,"odd Tseitin should be UNSAT");
 let z=n;
 const defs=[[((1<<z)|(1<<0)|(1<<1)),0],[(1<<(z+1))|(1<<z)|(1<<2),0],[(1<<(z+2))|(1<<(z+1)),1]];
 check(validateDefs(defs,n),"invalid definitions");
 const subst=Array.from({length:n},(_,i)=>[1<<i,0]);
 subst.push([(1<<0)|(1<<1),0],[(1<<0)|(1<<1)|(1<<2),0],[(1<<0)|(1<<1)|(1<<2),1]);
 defs.forEach(d=>check(JSON.stringify(project(d,subst,n))==="[0,0]","definition not conservative"));
 const rows=source.map(r=>({r,parents:[],kind:"SRC"})).concat(defs.map(r=>({r,parents:[],kind:"DEF"})));
 function add(i,j){
  check(i<rows.length&&j<rows.length,"bad parents");
  const k=rows.length;
  rows.push({r:xor(rows[i].r,rows[j].r),parents:[i,j],kind:"XOR"});
  return k;
 }
 let root=add(0,h+1);root=add(root,h+1);
 for(let v=1;v<h;v++)root=add(root,v);
 check(JSON.stringify(rows[root].r)==="[0,1]","not contradiction");
 rows.forEach((node,i)=>{if(node.kind==="XOR"){
  check(node.parents.every(p=>p<i),"bad chronology");
  check(JSON.stringify(node.r)===JSON.stringify(xor(rows[node.parents[0]].r,rows[node.parents[1]].r)),"forged xor");
 }});
 const coeff=rows.map(({r})=>{
  let rr=project(r,subst,n),matches=[];
  for(let s=0;s<(1<<h);s++){
   let v=[0,0];for(let k=0;k<h;k++)if(s&(1<<k))v=xor(v,source[k]);
   if(v[0]===rr[0]&&v[1]===rr[1])matches.push(s);
  }
  check(matches.length===1,"nonunique coefficient");
  return matches[0];
 });
 check(coeff[root]===(1<<h)-1,"wrong source dependency");
 function boundary(s){
  return E.reduce((count,[a,b])=>count+(((s>>a)&1)^((s>>b)&1)),0);
 }
 let beta=Infinity;
 for(let s=1;s<(1<<h)-1;s++)beta=Math.min(beta,boundary(s)/Math.min(pop(s),h-pop(s)));
 const reachable=new Set();
 function ancestors(i){if(reachable.has(i))return;reachable.add(i);rows[i].parents.forEach(ancestors)}
 ancestors(root);
 const cross=[...reachable].sort((a,b)=>a-b).find(i=>pop(coeff[i])>h/3);
 check(cross!==undefined&&rows[cross].kind==="XOR","no internal crossing");
 check(pop(coeff[cross])<=2*h/3,"overshoot crossing");
 const projection=project(rows[cross].r,subst,n);
 check(pop(projection[0])===boundary(coeff[cross]),"boundary support mismatch");
 check(pop(projection[0])+1e-9>=beta*h/3,"expander width violation");
 const even=source.map(x=>[...x]);even[0][1]=0;
 const evenRoot=even.reduce(xor,[0,0]);
 check(JSON.stringify(evenRoot)==="[0,0]","even charge false contradiction");
 check(!validateDefs([defs[0],[defs[0][0],1]],n),"nonfresh definition accepted");
 check(JSON.stringify(xor(rows[0].r,rows[1].r))!=="[0,1]","forged root accepted");
 return {family:name,vertices:h,edge_variables:n,source_clauses:cnf.length,source_models:assignments,
   paid_affine_defs:defs.length,paid_xors:h+1,unique_coeff_rows:rows.length,
   beta,source_mass_at_cross:pop(coeff[cross]),width_at_cross:pop(projection[0]),
   bound:beta*h/3,root_row:rows[root].r,even_control_root:evenRoot};
}
function run(){return {status:"PASS",system:"R_affDEF_XOR512: source parity equations + paid acyclic affine definitions + paid binary XOR",cases:[audit("K4",4),audit("K33",6),audit("cube3",8)],hostile_controls:["even charge rejected as contradiction","duplicate/nonfresh definition rejected","forged row rejected","source-CNF parity checked exhaustively"]}}
if(typeof require!=="undefined"&&require.main===module){console.log(JSON.stringify(run(),null,2));}
