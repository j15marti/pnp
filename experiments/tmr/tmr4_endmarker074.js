const result=(function audit(){
"use strict";
let checks=0, rows=[], samples=[], exhaustive=0;
function ok(x,s){checks++;if(!x)throw Error("CHECK_FAILED: "+s);}
function prism(m){
 const es=[],s=new Set(),v=Array.from({length:2*m},()=>[]);
 function add(a,b){let x=Math.min(a,b),y=Math.max(a,b),k=x+":"+y;if(!s.has(k)){s.add(k);es.push([x,y]);}}
 for(let r=0;r<2;r++)for(let i=0;i<m;i++)add(r*m+i,r*m+(i+1)%m);
 for(let i=0;i<m;i++)add(i,m+i);
 es.forEach(([u,w],j)=>{v[u].push(j+1);v[w].push(j+1);});
 ok(es.length===3*m && v.every(z=>z.length===3),"cubic graph");
 return v;
}
function block(ids,t){
 const out=[];for(let a=0;a<8;a++){
   let bits=[(a>>2)&1,(a>>1)&1,a&1];
   if((bits[0]^bits[1]^bits[2])===t)continue;
   out.push(ids.map((z,i)=>bits[i]?-z:z));
 }
 if(t)out.sort((a,b)=>a.every(x=>x>0)?1:b.every(x=>x>0)?-1:0);
 return out;
}
function source(m){
 const v=prism(m),f=[];
 v.forEach((ids,j)=>f.push(...block(ids,j===2*m-1?1:0)));
 const fplus=f.map(c=>c.slice());
 ok(f.length===8*m && f[f.length-1].every(x=>x>0),"last clause positive");
 fplus[f.length-1][2]=-fplus[f.length-1][2];
 return {minus:f,plus:fplus};
}
function enc(c,b){
 let s="1".repeat(b)+"0"+"1".repeat(c.length)+"0";
 for(let row of c)for(let x of row){
 const u=Math.abs(x);ok(u>=1&&u<2**b,"literal width");
 s+=u.toString(2).padStart(b,"0")+(x<0?"1":"0");
 }
 return s;
}
function valid(s){
 if(typeof s!=="string"||!/^[01]+$/.test(s))return false;
 const b=s.indexOf("0");if(b<1)return false;
 const j=s.indexOf("0",b+1);if(j<=b+1)return false;
 const M=j-b-1,start=j+1;if(s.length-start!==3*M*(b+1))return false;
 for(let i=0;i<M;i++){const ids=[];
 for(let t=0;t<3;t++){const pos=start+(3*i+t)*(b+1),u=parseInt(s.slice(pos,pos+b),2);if(!u)return false;ids.push(u);}
 if(new Set(ids).size!==3)return false;
 }return true;
}
function truth(c,a){return c.every(row=>row.some(x=>(((a>>(Math.abs(x)-1))&1)===(x>0?1:0))))}
function p(N,r,halt,member){return member?[Math.max(0,N-r),halt?0:1]:[0,0];}
function addRow(id,N,r,r2,halt2,cost=1){
 const q=p(N,r,false,true),q2=p(N,r2,!!halt2,true);
 const dI=q[0]-q2[0],dM=q[1]-q2[1];
 ok(dI>=0&&dI<=1&&dM>=0&&dM<=1,"local source/terminal discharge");
 ok(dI+dM<=2,"two coordinate bound");
 rows.push({rule:id,cost,delta_CNF:0,delta_XOR:0,delta_sep:0,delta_fus:0,delta_Gamma:0,delta_interface:dI,delta_machine:dM,N,r,r2,terminal:!!halt2});
}
for(let m=3;m<=12;m++){
 const {minus,plus}=source(m),b=Math.ceil(Math.log2(3*m+1)),x=enc(minus,b),y=enc(plus,b),N=(24*m+1)*(b+1)+8*m+1;
 ok(x.length===N&&y.length===N,"exact source length");
 ok(x.slice(0,-1)===y.slice(0,-1)&&x.at(-1)==="0"&&y.at(-1)==="1","exact final-bit pair");
 ok(valid(x)&&valid(y),"strict grammar both members");
 for(const t of ["0","1","00","11"]){ok(!valid(y+t),"strict suffix invalid");}
 ok(truth(plus,0),"SAT control all-zero witness");
 if(m<=5){let z=false;for(let a=0;a<2**(3*m);a++){if(truth(minus,a)){z=true;break;}}ok(!z,"UNSAT exhaustive prism");exhaustive++;}
 for(let r=-1;r<=N;r++){
   // Scans and other work: include a paid step with no new original cell.
   addRow("CACHE_REREAD_OR_WORK",N,r,r,false);
   if(r<N){addRow("FIRST_READ_LOCAL",N,r,r+1,false);}
   if(r===N){addRow("HALT_AFTER_ENDMARKER",N,r,r,true);}
   if(r===N-1){addRow("FUSED_ENDMARKER_READ_AND_ACCEPT",N,r,N,true);}
 }
 // A strict proper 3-CNF input extended by an extra bit must be invalid.
 const q0=p(N,-1,false,true),qGoal=p(N,N,true,true);
 ok(q0[0]===N+1&&q0[1]===1&&qGoal.every(t=>t===0),"endmarker potential initial/goal");
 // Nonmembers get zero even at a premature arbitrary halt.
 ok(p(N,-1,false,false).every(t=>t===0)&&p(N,-1,true,false).every(t=>t===0),"nonmember conservative zero");
 samples.push({m,clauses:8*m,input_bits:N,sat_prefix_extension_invalid:true,source_hamming_distance:1,terminal_ingress_floor:N+1,previous_last_bit_floor:N});
}
let joint=rows.filter(x=>x.rule==="FUSED_ENDMARKER_READ_AND_ACCEPT");
ok(joint.length===samples.length,"real fused class modeled");
for(let d=1;d<=16;d++){
 for(let a=0;a<=d;a++)for(let b=0;b<=d;b++){
   const feasible=rows.every(x=>a*x.delta_interface+b*x.delta_machine<=d*x.cost);
   ok(feasible===(a+b<=d),"exact two-weight cone grid");
 }
}
for(let z of rows){
 ok(z.delta_interface<=z.cost,"lambda (1,0) certificate");
 ok(z.delta_machine<=z.cost,"lambda (0,1) certificate");
 ok(z.delta_interface+z.delta_machine<=2*z.cost,"sum bound");
}
const symbolic=[
 {rule:"SCAN_HEAD_NO_NEW_FRONTIER",cost:1,delta_interface:0,delta_machine:0},
 {rule:"FIRST_READ_ONE_CELL",cost:1,delta_interface:1,delta_machine:0},
 {rule:"HALT_AFTER_ENDMARKER",cost:1,delta_interface:0,delta_machine:1},
 {rule:"FUSED_FIRST_ENDMARKER_AND_ACCEPT",cost:1,delta_interface:1,delta_machine:1},
 {rule:"NONMEMBER_ANY_LOCAL_STEP",cost:1,delta_interface:0,delta_machine:0},
 {rule:"NONLOCAL_SOURCE_JUMP",cost:1,delta_interface:2,delta_machine:0,model:"DIFFERENT MODEL: random-access illegal in qualified local-head model"}
];
return {id:"ENDMARKER074",result_type:"COMPUTATIONAL",status:"PROVED/RESTRICTED symbolic statement separately",time_zone:"America/Los_Angeles",assertions:checks,failures:0,rows_checked:rows.length,lp_denominators_tested:16,source_samples:samples,small_unsat_exhaustions:exhaustive,exact_rational_certificate:{columns:["CNF","XOR","sep","fus","Gamma","interface","machine"],lambda:["0","0","0","0","0","1","0"],dual_fusion_constraint:"lambda_interface + lambda_machine <= 1"},symbolic_tariff_rows:symbolic,model_limit:"Only fixed finite total correct local-head deterministic multitape SAT deciders; not random access; no superpolynomial implication",rows};
})();
const {rows,...summary}=result;
console.log(JSON.stringify(summary,null,2));
