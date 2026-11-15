// Exactly executed audit function, V8 ES2020.
const runAudit = function runAudit(){
 "use strict";
 let assertions=0,checks=0;
 function assert(p,msg){assertions++;if(!p)throw new Error("FAIL "+msg);}
 function universe(maxN){const a=[];for(let n=0;n<=maxN;n++)for(let i=0;i<2**n;i++)a.push(i.toString(2).padStart(n,"0"));return a;}
 function padded(s,j){return (s+"#".repeat(j+1)).slice(0,j);}
 const U=universe(7),tag=s=>(s==="010"||s==="1101"||s==="1110000")?1:0;
 let toyN=0,toyMax=0,toyMin=99;
 for(const x of U){
   let d=-1;
   for(let j=0;j<=x.length+1;j++){
     const pre=padded(x,j);
     if(U.every(y=>padded(y,j)!==pre||tag(y)===tag(x))){d=j;break;}
   }
   assert(d>=1&&d<=x.length+1,"toy depth "+x);
   for(const y of U){ checks++;if(padded(y,d)===padded(x,d))assert(tag(y)===tag(x),"prefix correct");}
   assert(U.some(y=>padded(y,d-1)===padded(x,d-1)&&tag(y)!==tag(x)),"depth sharp");
   toyN++;toyMax=Math.max(toyMax,d);toyMin=Math.min(toyMin,d);
 }
 function ids(t){return [2**(t-1),2**(t-1)+1,2**(t-1)+2];}
 function make(t,yes){
   const v=ids(t);const masks=[1,2,3,4,5,6,7,yes?1:0];
   while(masks.length<t)masks.push(7);
   let s="1".repeat(t)+"0"+"1".repeat(t)+"0";
   for(const mask of masks){for(let h=0;h<3;h++)s+=v[h].toString(2).padStart(t,"0")+((mask>>(2-h))&1);}
   return {s,masks,v};
 }
 function parse(s){
   if(!/^[01]+$/.test(s))return null;
   let i=0,b=0,M=0;
   while(i<s.length&&s[i]==="1"){i++;b++;}
   if(b<3||s[i]!=="0")return null;i++;
   while(i<s.length&&s[i]==="1"){i++;M++;}
   if(M<1||s[i]!=="0")return null;i++;
   if(s.length-i!==3*M*(b+1))return null;
   let clauses=[];
   for(let j=0;j<M;j++){
     let row=[];
     for(let h=0;h<3;h++){
       let bin=s.slice(i,i+b);i+=b;let id=parseInt(bin,2),sign=Number(s[i++]);
       if(id===0||id>=2**b||!(sign===0||sign===1))return null;
       row.push([id,sign]);
     }
     if(new Set(row.map(z=>z[0])).size!==3)return null;
     clauses.push(row);
   }
   return {b,M,clauses};
 }
 function sat3(masks){for(let a=0;a<8;a++)if(masks.every(m=>m!==a))return true;return false;}
 let prism=[];
 for(let t=9;t<=20;t++){
   let no=make(t,false),yes=make(t,true);
   let N=3*t*t+5*t+2,P=26*(t+1);
   assert(no.s.length===N&&yes.s.length===N,"size "+t);
   assert(no.s.slice(0,P-1)===yes.s.slice(0,P-1),"prefix "+t);
   assert(no.s[P-1]!==yes.s[P-1],"distinguished bit "+t);
   assert(no.s.slice(P)===yes.s.slice(P),"suffix "+t);
   assert(!!parse(no.s)&&!!parse(yes.s),"strict sources "+t);
   assert(!parse(yes.s+"0"),"invalid extension");
   assert(!sat3(no.masks)&&sat3(yes.masks),"labels "+t);
   assert(no.masks.slice(0,8).every((m,i)=>m===[1,2,3,4,5,6,7,0][i]),"core "+t);
   for(let m=1;m<=7;m++){const alt=[1,2,3,4,5,6,7,m,...new Array(t-8).fill(7)];assert(sat3(alt),"alternative SAT "+t);}
   prism.push({t,N,P,d_negative:P,d_positive:N+1,naive_negative_goal_residual:N-P});
 }
 function nae(k){
   let clauses=[],n=3*k+k*(k-1)/2;
   function NAE(a,b,c){clauses.push([[a,0],[b,0],[c,0]]);clauses.push([[a,1],[b,1],[c,1]]);}
   for(let i=0;i<k;i++)NAE(i+1,k+i+1,2*k+i+1);
   let z=3*k+1;
   for(let i=0;i<k;i++)for(let j=i+1;j<k;j++)NAE(i+1,j+1,z++);
   let counts=Array(n+1).fill(0);
   for(const C of clauses)for(const [id] of C)counts[id]++;
   const assignment=counts.map(c=>c>2?0:1);
   function clauseTrue(C,a){return C.some(([id,sign])=>(a[id]^sign)===1);}
   assert(clauses.every(C=>clauseTrue(C,assignment)),"NAE witness "+k);
   assert(!clauses.every(C=>clauseTrue(C,counts.map(()=>0))),"allzero no "+k);
   assert(!clauses.every(C=>clauseTrue(C,counts.map(()=>1))),"allone no "+k);
   const b=Math.max(3,Math.ceil(Math.log2(n+1))),M=clauses.length;
   let s="1".repeat(b)+"0"+"1".repeat(M)+"0";
   for(const C of clauses)for(const [id,sign] of C)s+=id.toString(2).padStart(b,"0")+sign;
   assert(!!parse(s),"NAE source valid "+k);
   assert(!parse(s+"0"),"NAE extension invalid");
   return {k,encoded_length:s.length,rank:2**k,depth:s.length+1};
 }
 let rankSamples=[];
 for(let k=2;k<=16;k++)rankSamples.push(nae(k));
 let tariffRows=[
 {rule:"work_recompute_reread",cost:1,delta:[0,0,0,0,0,0,0]},
 {rule:"first_required_frontier_scan",cost:1,delta:[0,0,0,0,0,1,0]},
 {rule:"halt_after_required_scan",cost:1,delta:[0,0,0,0,0,0,1]},
 {rule:"scan_required_frontier_and_halt",cost:1,delta:[0,0,0,0,0,1,1]}
 ];
 let tariffs=0,feasible=0,violations=0;
 for(let q=1;q<=16;q++)for(let a=0;a<=q;a++)for(let b=0;b<=q;b++){
   let good=tariffRows.every(row=>a*row.delta[5]+b*row.delta[6]<=q*row.cost);
   assert(good===(a+b<=q),"exact cone q="+q);
   if(good)feasible++;else violations++;tariffs++;
 }
 for(const s of [...prism,...rankSamples]){
   const d=s.d_positive??s.depth;
   let optimum=0;
   for(let a=0;a<=16;a++)for(let b=0;b<=16;b++)if(a+b<=16)optimum=Math.max(optimum,d*a+b);
   assert(optimum===d*16,"LP dual primal "+d);
 }
 return {id:"TMR4_PREFIX_DEPTH079",scientific_status:"PROVED/RESTRICTED symbolic; COMPUTATIONAL finite audit",test_parameters:{toy_max_length:7,prism_t_range:[9,20],nae_k_range:[2,16],rational_grid_denominators:[1,16]},assertions,failed:0,toy:{strings:toyN,comparisons:checks,minDepth:toyMin,maxDepth:toyMax},prism,nae_samples:rankSamples,tariff_columns:["CNF","aff","sep","fus","Gamma","interface","machine"],tariff_rows:tariffRows,rational_grid:{cases:tariffs,feasible,violations},certificate:["0","0","0","0","0","1","0"],cone:"lambda_interface>=0,lambda_machine>=0,lambda_interface+lambda_machine<=1",note:"No physical Turing machine compiled. Exact symbolic theorem for local-head model; finite controls not asymptotic proofs."};
};
console.log(JSON.stringify(runAudit(),null,2));
