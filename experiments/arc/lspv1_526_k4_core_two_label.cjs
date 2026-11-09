/* LSPV-1/526 independent original CORE two-label and malformed-source finite control.
   Not an asymptotic proof and not a native R_mix341 checker. */
"use strict";
function run(){
 const edges=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]];
 function CNF(charges){
  const cls=[];for(let e=0;e<edges.length;e++)cls.push([3*e+1,3*e+2,3*e+3]);
  for(let v=0;v<4;v++){const inc=edges.map((uv,e)=>uv.includes(v)?{e,s:uv[0]===v?1:-1}:null).filter(Boolean);
   if(inc.length!==3)throw Error("not cubic");
   for(let i=0;i<3;i++)for(let j=0;j<3;j++)for(let k=0;k<3;k++){
    const a=[i,j,k],sum=inc.reduce((t,q,z)=>t+q.s*a[z],0);
    if(((sum-charges[v])%3+3)%3!==0)cls.push(inc.map((q,z)=>-(3*q.e+a[z]+1)));
   }
  }
  if(cls.length!==78||cls.some(c=>c.length!==3))throw Error("not original proper width3 CORE");
  return cls;
 }
 function strictValidate(clauses,declared=18,expected=78){
  if(!Array.isArray(clauses)||clauses.length!==expected)throw Error("wrong DIMACS header");
  const all=new Set();for(const c of clauses){
   if(!Array.isArray(c)||c.length!==3||c.some(z=>!Number.isInteger(z)||z===0||Math.abs(z)>declared)||new Set(c.map(Math.abs)).size!==3)throw Error("malformed proper triple");
   all.add(c.join(","));}
  if(all.size!==expected)throw Error("duplicate source");return true;
 }
 let output={graph:"K4",original_edge_groups:6,original_Boolean_variables:18,charge_controls:{},malformed:{},checked_ternary_flows:0};
 for(const [label,b] of [["zero",[0,0,0,0]],["nonzero",[1,0,0,0]]]){
  let F=CNF(b);strictValidate(F);let sat=0;
  for(let t=0;t<729;t++){let v=t,bits=Array(19).fill(false),values=[];
   for(let e=0;e<6;e++){let k=v%3;v=Math.floor(v/3);values.push(k);bits[3*e+k+1]=true;}
   if(F.every(c=>c.some(l=>l>0?bits[l]:!bits[-l])))sat++;
   output.checked_ternary_flows++;
  }
  output.charge_controls[label]={source_clauses:F.length,onehot_flow_solutions:sat};
  if(sat!==(label==="zero"?27:0))throw Error("wrong K4 charge control");
 }
 const ok=CNF([0,0,0,0]);
 for(const [name,change] of [["zero_literal",x=>x[0][0]=0],["wrong_width",x=>x[0].pop()],["repeated_ID",x=>x[0][1]=x[0][0]],["out_of_range",x=>x[0][0]=25],["duplicate_source",x=>x[1]=x[0].slice()],["bad_clause_count",x=>x.pop()]]){const x=ok.map(c=>c.slice());change(x);try{strictValidate(x);output.malformed[name]="MISSED";}catch(e){output.malformed[name]="REJECTED";}}
 if(Object.values(output.malformed).some(x=>x!=="REJECTED"))throw Error("malformed accepted");
 return output;
}
if(typeof module!=="undefined")module.exports={run};
if(typeof require!=="undefined"&&typeof module!=="undefined"&&require.main===module)console.log(JSON.stringify(run(),null,2));
