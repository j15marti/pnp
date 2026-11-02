#!/usr/bin/env node
/* No-producer-import independent referee. node verify333_public.js */
'use strict';
const assert=require('assert');
const F9p=['156','238','135','469','247','789'],F9n=['468','167','234','358','129','579'];
const B9p=['123','456','789','147','258','369'],B9n=['159','267','348','168','249','357'];
let checks=0;const check=(a,msg)=>{checks++;assert(a,msg)};
const source=(p,n)=>p.map(c=>[...c].map(Number)).concat(n.map(c=>[...c].map(x=>-Number(x))));
const f9=source(F9p,F9n),b9=source(B9p,B9n);
function sat(clauses,a){return clauses.every(c=>c.some(l=>((a>>>(Math.abs(l)-1))&1)===Number(l>0)))}
function valid(n,cl){
 if(!Number.isInteger(n)||n%3||!Array.isArray(cl)||3*cl.length!==4*n)return false;
 let count=Array(2*n+1).fill(0),seen=new Set();
 for(const c of cl){
  if(!Array.isArray(c)||c.length!==3||c.some(x=>!Number.isInteger(x)||x===0||Math.abs(x)>n))return false;
  if(new Set(c.map(Math.abs)).size!==3||!(c.every(x=>x>0)||c.every(x=>x<0)))return false;
  const key=c.slice().sort((x,y)=>x-y).join(',');
  if(seen.has(key))return false;seen.add(key);
  for(const l of c)count[n+l]++;
 }
 for(let x=1;x<=n;x++)if(count[n+x]!==2||count[n-x]!==2)return false;
 return true;
}
function audit(n,cl,I){
 let rem=[];for(let x=1;x<=n;x++)if(!I.includes(x))rem.push(x);
 for(const c of cl)check(c.filter(l=>I.includes(Math.abs(l))).length<=1,'selected pivots share source clause');
 let H=cl.filter(c=>c.every(l=>!I.includes(Math.abs(l)))),groups=[];
 for(const x of I)groups.push([cl.filter(c=>c.includes(x)).map(c=>c.filter(l=>l!==x)),
                              cl.filter(c=>c.includes(-x)).map(c=>c.filter(l=>l!==-x))]);
 let hist={},rows=1<<rem.length;
 for(let z=0;z<rows;z++){
  let a=0;for(let j=0;j<rem.length;j++)if((z>>>j)&1)a|=1<<(rem[j]-1);
  let w=sat(H,a)?1:0;
  for(const [P,N] of groups)w*=Number(sat(P,a))+Number(sat(N,a));
  let actual=0;for(let b=0;b<(1<<I.length);b++){
   let mask=a;for(let j=0;j<I.length;j++)if((b>>>j)&1)mask|=1<<(I[j]-1);
   actual+=Number(sat(cl,mask));
  }
  check(actual===w,'weighted extension mismatch');
  hist[w]=(hist[w]||0)+1;
 }
 return {source_models:Object.entries(hist).reduce((s,[k,v])=>s+Number(k)*v,0),
 projected_models:Object.entries(hist).reduce((s,[k,v])=>s+(Number(k)>0?v:0),0),weights:hist};
}
check(valid(9,f9)&&valid(9,b9),'canonical sources');
const F=audit(9,f9,[1,4]),B=audit(9,b9,[1]);
check(F.source_models===70&&F.projected_models===48,'F9 totals');
check(B.source_models===18&&B.projected_models===17,'B9 totals');
check(B.weights['0']===239&&B.weights['1']===16&&B.weights['2']===1,'B9 weight');
for(let x=1;x<=9;x++)check(audit(9,b9,[x]).projected_models===17,'B9 symmetry');
const two=b9.concat(b9.map(c=>c.map(l=>Math.sign(l)*(Math.abs(l)+9))));
check(valid(18,two),'two-block canonical');
const B2=audit(18,two,[1,10]);check(B2.source_models===324&&B2.projected_models===289,'B9 product');
function pinCount(cs,n,pins,x,value){
 let count=0;for(let a=0;a<(1<<n);a++){
  if(((a>>>(x-1))&1)!==value)continue;
  if(Object.entries(pins).some(([v,b])=>((a>>>(Number(v)-1))&1)!==b))continue;
  count+=Number(sat(cs,a));
 }return count;
}
check(pinCount(b9,9,{2:0,3:0},1,0)===0&&pinCount(b9,9,{2:0,3:0},1,1)===4,'B9 opposite labels');
check(pinCount(f9,9,{3:0,5:1,6:0,7:0,8:0},1,0)===2&&
      pinCount(f9,9,{3:0,5:1,6:0,7:0,8:0},1,1)===0,'F9 opposite labels');
let pairs=0;for(let i=0;i<12;i++)for(let j=i+1;j<12;j++)for(const t of [0,1])for(const u of [0,1]){
 const a=f9[i],b=f9[j],same=a.some(x=>b.includes(x)),opp=a.some(x=>b.includes(-x));
 let req=new Map(),feasible=true;
 for(const [c,target] of [[a,t],[b,u]])for(const l of c){
  let bit=Number(l>0)===target?1:0;
  if(req.has(Math.abs(l))&&req.get(Math.abs(l))!==bit)feasible=false;
  req.set(Math.abs(l),bit);
 }
 check(feasible===(t===u?!opp:!same),'S/U mode');pairs++;
}
const bad=[f9.concat([f9[0]]),f9.slice(0,-1),[[1,1,6],...f9.slice(1)],
 [[1,-5,6],...f9.slice(1)],[[1,5,10],...f9.slice(1)],
 [[0,5,6],...f9.slice(1)],[[true,5,6],...f9.slice(1)],
 [[1,5,6,7],...f9.slice(1)],'malformed string'];
for(const x of bad)check(!valid(9,x),'malformed accepted');
process.stdout.write(JSON.stringify({independent_checks:checks,F9:F,B9:B,B9_squared:B2,
 B9_same_original:[0,4],F9_same_original:[2,0],source_SU_modes:pairs,
 malformed_rejected:bad.length,P_vs_NP_open:true},null,2)+'\n');
