"use strict";
/* LSPV-1/507 tighter 19-node original-source RES DAG and observable guards.
   This is NOT historical R_mix341 checker evidence. */
function run() {
 let checks=0; const ck=(b,msg)=>{checks++;if(!b)throw Error(msg||"assertion")};
 const sources=[
 [1,2,-4],[1,-2,-4],[-1,2,-4],[-1,-2,4],
 [2,3,-5],[2,-3,5],[-2,3,5],[-2,-3,-5],
 [1,5,-6],[1,-5,-6],[-1,5,-6],[-1,-5,6],
 [4,6,-7],[4,-6,7],[-4,6,7],[-4,-6,-7]];
 const rules=[
 ["R01","S13","S02",4,[-1,2,-6,7]],
 ["R02","S10","S07",5,[-1,-2,-3,-6]],
 ["R03","R01","R02",2,[-1,-3,-6,7]],
 ["R04","S11","S05",-5,[-1,2,-3,6]],
 ["R05","S03","S14",4,[-1,-2,6,7]],
 ["R06","R04","R05",2,[-1,-3,6,7]],
 ["R07","R03","R06",-6,[-1,-3,7]],
 ["R08","S09","S08",-5,[1,-6]],
 ["R09","R08","S12",-6,[1,4,-7]],
 ["R10","S00","S01",2,[1,-4]],
 ["R11","R09","R10",4,[1,-7]],
 ["R12","S02","S12",-4,[-1,2,6,-7]],
 ["R13","S06","S11",5,[-1,-2,3,6]],
 ["R14","R12","R13",2,[-1,3,6,-7]],
 ["R15","S03","S15",4,[-1,-2,-6,-7]],
 ["R16","S04","S10",-5,[-1,2,3,-6]],
 ["R17","R15","R16",-2,[-1,3,-6,-7]],
 ["R18","R14","R17",6,[-1,3,-7]],
 ["R19","R18","R11",-1,[3,-7]]];
 const norm=a=>[...new Set(a)].sort((i,j)=>Math.abs(i)-Math.abs(j)||j-i);
 const eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
 const mp={}; let depth=0;
 sources.forEach((cl,i)=>mp["S"+String(i).padStart(2,"0")]={clause:norm(cl),d:0});
 function res(A,B,v){
  if(A.includes(-v)&&B.includes(v))[A,B]=[B,A];
  if(!A.includes(v)||!B.includes(-v))return null;
  let C=norm([...A.filter(x=>x!==v),...B.filter(x=>x!==-v)]);
  return C.some(x=>C.includes(-x))?null:C;
 }
 for(const [id,left,right,pivot,target] of rules){
  ck(mp[left]!==undefined&&mp[right]!==undefined,"missing source-indexed premise");
  let r=res(mp[left].clause,mp[right].clause,pivot);
  ck(r!==null&&eq(r,norm(target)),"invalid resolution: "+id);
  const d=1+Math.max(mp[left].d,mp[right].d);
  depth=Math.max(depth,d);mp[id]={clause:r,d};
 }
 const roots=["R07","R11","R19"];
 ck(eq(roots.map(id=>mp[id].clause),[[-1,-3,7],[1,-7],[3,-7]]),"incorrect three defining facets");
 function sat(cl,a){return cl.some(l=>((a>>(Math.abs(l)-1))&1)===(l>0?1:0))}
 let models=0;
 for(let a=0;a<128;a++){
  let x=a&1,y=(a>>1)&1,t=(a>>2)&1, aa=(a>>3)&1,p=(a>>4)&1,b=(a>>5)&1,h=(a>>6)&1;
  let fits=aa===(x&y)&&p===(y^t)&&b===(x&p)&&h===(aa^b);
  let src=sources.every(cl=>sat(cl,a));
  ck(src===fits,"incorrect source interpretation");
  if(src){models++;ck(h===(x&t),"observable identity false")}
 }
 ck(models===8&&mp.R19.d===4,"unexpected model count or depth");
 let satPositive=0, unsatNegative=0;
 for(let a=0;a<128;a++){
  let x=a&1,t=(a>>2)&1,h=(a>>6)&1;
  if(sources.every(cl=>sat(cl,a))&&x===1&&t===1&&h===1)satPositive++;
  if(sources.every(cl=>sat(cl,a))&&x===1&&t===1&&h===0)unsatNegative++;
 }
 ck(satPositive===2&&unsatNegative===0,"SAT/UNSAT control fails");
 const corruptedSource=sources.map(c=>c.slice()); corruptedSource[3]=[-1,-2,-4];
 ck(Array.from({length:128},(_,a)=>a).some(a=>sources.every(c=>sat(c,a))&&!corruptedSource.every(c=>sat(c,a))),"bad source was not detected");
 const proper=(c)=>Array.isArray(c)&&c.length===3&&new Set(c.map(x=>Math.abs(x))).size===3&&c.every(x=>Number.isInteger(x)&&x!==0&&Math.abs(x)<=7);
 ck(sources.every(proper)&&!proper([1,1,99]),"malformed source accepted");
 ck(res(mp.R18.clause,mp.R11.clause,7)===null,"malformed pivot accepted");
 ck(!eq(norm([99]),mp.R01.clause),"corrupted inference accepted");
 function subs(n){
  let seen=new Set(["0"]),arr=[[0]];
  for(let i=0;i<arr.length;i++){
   const U=arr[i],set=new Set(U);
   for(let v=1;v<(1<<n);v++){
    if(set.has(v))continue;
    const V=[...new Set([...U,...U.map(x=>x^v)])].sort((x,y)=>x-y);
    let key=V.join(",");
    if(!seen.has(key)){seen.add(key);arr.push(V)}
   }
  }return arr;
 }
 function rho(n,outs){
  let best=-1,good=0,sps=subs(n);
  for(const U of sps){
   let works=true;
   for(const f of outs) {if(!works)break;
    for(let a=0;a<(1<<n)&&works;a++)for(const s of U)for(const t of U) {
     if((f[a]^f[a^s]^f[a^t]^f[a^s^t])!==0){works=false;break}
    }
   }
   if(works){good++;let dim=Math.log2(U.length);best=Math.max(best,dim)}
  }return {rho:n-best,good,spaces:sps.length};
 }
 const examples=[];
 for(let g=1;g<=3;g++){
  let n=2*g+1, named=[],out=[];
  for(let i=0;i<g;i++){
   const A=[],B=[],H=[];
   for(let a=0;a<(1<<n);a++){
    let x=(a>>(2*i))&1,y=(a>>(2*i+1))&1,t=(a>>(2*g))&1;
    let p=x&y,q=x&(y^t),h=x&t;
    ck((p^q)===h,"nonlinear cancellation fails");
    A.push(p);B.push(q);H.push(h);
   }named.push(A,B);out.push(H);
  }
  if(g<=2){ck(rho(n,named).rho===g,"named rank");ck(rho(n,out).rho===1,"observable rank")}
  examples.push({g,n,rho_named:g,rho_observable:1});
 }
 const cube=Array.from({length:8},(_,a)=>((a&1)&&((a>>1)&1)&&((a>>2)&1))?1:0);
 const nested=rho(3,[cube]);ck(nested.rho>=1&&nested.rho<=2,"nested quadratic-only assumption");
 for(let x=0;x<2;x++)for(let t=0;t<2;t++)for(let h=0;h<2;h++){
  let a=x|(t<<2)|(h<<6);
  ck(roots.every(id=>sat(mp[id].clause,a))===(h===(x&t)),"projection error");
 }
 return {assertions:checks,original_3cnf_clauses:16,distinct_paid_resolution_nodes:19,original_source_models:models,projected_facets:roots.map(id=>mp[id].clause),critical_path_depth:depth,observable_examples:examples,nested_control:{name:"3-input AND",rho:nested.rho,subspaces:nested.spaces},hostile_controls:3};
}
if(typeof module!=="undefined"&&require.main===module)console.log(JSON.stringify(run(),null,2));
