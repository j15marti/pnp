// LSPV-1/392 independent constructive sign-flip verifier. Usage: node file.js results.json
"use strict";
function make(h){
  const c=[], id=(p,j)=>1+p*h+j;
  for(let p=0;p<=h;p++)c.push({kind:"pigeon",p,lit:Array.from({length:h},(_,j)=>id(p,j))});
  for(let j=0;j<h;j++)for(let p=0;p<=h;p++)for(let q=p+1;q<=h;q++)
    c.push({kind:"collision",p,q,j,lit:[-id(p,j),-id(q,j)]});
  return c;
}
function satisfies(clauses,assignment){
 return clauses.every(c=>c.some(l=>(!!assignment[Math.abs(l)])===(l>0)));
}
function witness(h,row){
  const assigned=Array(h+1).fill(-1);
  if(row.kind==="pigeon"){
    let k=0;for(let p=0;p<=h;p++)if(p!==row.p)assigned[p]=k++;
  }else{
    assigned[row.p]=row.j;assigned[row.q]=row.j;
    const holes=Array.from({length:h},(_,j)=>j).filter(j=>j!==row.j);
    let k=0;for(let p=0;p<=h;p++)if(p!==row.p&&p!==row.q)assigned[p]=holes[k++];
  }
  const a=Array((h+1)*h+1).fill(false);
  for(let p=0;p<=h;p++)if(assigned[p]>=0)a[1+p*h+assigned[p]]=true;
  return a;
}
function audit(raw,checkMutations=true){
 if(!raw||raw.schema!=="LSPV1-392-v1"||!Array.isArray(raw.cases)||raw.cases.length!==3)throw Error("schema");
 let checks=0,total=0;
 const expect=[[1,2,3,4,208],[2,6,9,18,608],[3,12,22,48,1600]];
 for(let k=0;k<3;k++){
   const [h,v,m,lit,bits]=expect[k],a=raw.cases[k], rows=make(h);
   if(a.h!==h||a.variables!==v||a.clauses!==m||a.signs!==lit
      ||a.SAT_sign_flips!==lit||a.UNSAT_models!==0||a.input_bits!==bits
      ||rows.length!==m)throw Error("metadata");
   checks+=8;
   const src=rows.map(r=>r.lit);
   for(let i=0;i<rows.length;i++){
     const ass=witness(h,rows[i]);
     for(let j=0;j<rows[i].lit.length;j++){
       const changed=src.map(x=>x.slice());changed[i][j]*=-1;
       if(!satisfies(changed,ass))throw Error("constructed SAT neighbor not valid");
       if(satisfies(src,ass))throw Error("source accidentally SAT at witness");
       checks+=2;total++;
     }
   }
   for(let i=0;i<rows.length;i++)
     for(let j=0;j<rows[i].lit.length;j++)
       if(rows[i].lit[j]===0)throw Error("zero literal");
   checks+=lit;
 }
 if(raw.malformed_rejections!==8||raw.checks!==109||raw.lookalikes.length!==3)throw Error("summary");
 checks+=3;
 const altered=JSON.parse(JSON.stringify(raw));altered.cases[2].SAT_sign_flips=47;
 if(checkMutations){
   let rejected=false;
   try{audit(altered,false)}catch(e){rejected=true}
   if(!rejected)throw Error("tampered metadata unexpectedly accepted");
   checks++;
 }
 return {verifier:"independent constructive witness checker",passed:true,checks,flips_verified:total,seed:null};
}
if(typeof require!=="undefined"&&typeof module!=="undefined"&&require.main===module){
 const fs=require("fs"),data=JSON.parse(fs.readFileSync(process.argv[2],"utf8"));
 process.stdout.write(JSON.stringify(audit(data),null,2)+"\n");
}
