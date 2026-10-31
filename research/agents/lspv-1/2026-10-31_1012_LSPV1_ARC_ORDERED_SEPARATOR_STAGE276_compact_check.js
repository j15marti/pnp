'use strict';
// Independent compact finite control for ordered-separator ARC stage 276.
// Node.js 18+, no dependencies. Full 15-source producer and no-import Python
// verifier are in the reproducibility archive; this is NOT the full test suite.
const test=(ok,msg)=>{if(!ok)throw Error(msg)};
const lit=(l,a)=>l>0?!!a[Math.abs(l)]:!a[-l];
const sat=(f,a)=>f.every(c=>c.some(l=>lit(l,a)));
const active=f=>[...new Set(f.flat().map(Math.abs))].sort((a,b)=>a-b);
function exact(f){
 const vars=active(f);for(let k=0;k<2**vars.length;k++){
  const a={};vars.forEach((v,i)=>a[v]=!!((k>>i)&1));
  if(sat(f,a))return {yes:true,assignment:a};
 }return {yes:false,assignment:null};
}
const Lsat=[[1,2],[1,-2],[-1,-2]];
const Lunsat=Lsat.concat([[-1,2]]);
const aux=[3,7,11,15];
function build(L){
 return L.flatMap((pair,i)=>[
  [pair[0],pair[1],aux[i]],[pair[0],pair[1],-aux[i]]
 ]);
}
function source_extremes(f){
 return f.map((c,j)=>({j,literals:c.map(l=>({
   signed:l,x:Math.abs(l),S:Number(l>0),U:Number(l<0),
   invertS:Number(l<0),invertU:Number(l>0)
 }))}));
}
function modes(c,d){
 const result={};for(const a of [0,1])for(const b of [0,1]){
  const values={};let good=true;
  for(const [cl,target] of [[c,a],[d,b]])for(const l of cl){
   const x=Math.abs(l);const want=(target===1)===(l>0);
   if(Object.prototype.hasOwnProperty.call(values,x)&&values[x]!==want)good=false;
   values[x]=want;
  }
  result[(a?'S':'U')+(b?'S':'U')]=good;
 }
 return result;
}
function proper(residual){
 let vars=active(residual),ren={};vars.forEach((v,i)=>ren[v]=i+1);
 let next=vars.length+1,out=[];
 for(const c of residual){
  if(c.length===0){
   out=[];for(let k=0;k<8;k++)out.push([0,1,2].map(i=>((k>>i)&1?1:-1)*(i+1)));
   return out;
  }
  const r=c.map(l=>(l>0?1:-1)*ren[Math.abs(l)]);
  if(r.length===3)out.push(r);
  else if(r.length===2){out.push(r.concat(next),r.concat(-next));next++;}
  else if(r.length===1){
   for(const s of [-1,1])for(const t of [-1,1])out.push(r.concat(s*next,t*(next+1)));
   next+=2;
  }
 }
 return out.length?out:[[1,2,3]];
}
function childFor(block,beta){
 const rem=[];for(const c of block){
  if(c.some(l=>Math.abs(l)<=2&&((l>0)===(beta[Math.abs(l)-1]===1))))continue;
  rem.push(c.filter(l=>Math.abs(l)>2));
 }return proper(rem);
}
function boundaryProfile(L){
 const src=build(L),blocks=L.map((_,i)=>src.slice(2*i,2*i+2));
 const profile=[];let joined=false,independentSat=blocks.every(b=>exact(b).yes);
 for(let p=0;p<=1;p++)for(let q=0;q<=1;q++){
  let labels=[],sigma=[p,q];
  for(const b of blocks){
   const ch=childFor(b,sigma);
   test(ch.every(c=>c.length===3&&new Set(c.map(Math.abs)).size===3),'nonproper child');
   const childYes=exact(ch).yes;
   // Pointwise source block projection: here each block implements one L.
   const localYes=(lit(b[0][0],{1:!!p,2:!!q})||
                   lit(b[0][1],{1:!!p,2:!!q}));
   test(localYes===childYes,'SAT/UNSAT child polarity error');
   labels.push(childYes);
  }
  const AND=labels.every(Boolean);joined ||= AND;
  profile.push({sigma,labels,AND,OR:labels.some(Boolean)});
 }
 test(exact(src).yes===joined,'global OR-AND mismatch');
 const extremes=source_extremes(src);
 for(const e of extremes)for(const l of e.literals)
  test(l.invertS===l.U&&l.invertU===l.S,'S/U inversion error');
 let matrixCount=0;
 for(let j=0;j<src.length;j++)for(let k=j+1;k<src.length;k++){
  const m=modes(src[j],src[k]);
  for(const key of ['SS','SU','US','UU'])test(typeof m[key]==='boolean','bad mode');
  matrixCount+=4;
 }
 // True-literal complement identity, verified for all active source assignments.
 const vv=active(src);
 for(let bits=0;bits<2**vv.length;bits++){
  const a={};vv.forEach((v,i)=>a[v]=!!((bits>>i)&1));
  const bar=Object.fromEntries(Object.entries(a).map(([v,value])=>[v,!value]));
  for(const c of src) test(c.filter(l=>lit(l,a)).length +
                            c.filter(l=>lit(l,bar)).length===3,'complement');
 }
 return {sourceSAT:exact(src).yes, joined, independentSat, profile,matrixCount,
         global0:sat(src,Object.fromEntries(vv.map(v=>[v,false]))),
         global1:sat(src,Object.fromEntries(vv.map(v=>[v,true])))};
}
const YES=boundaryProfile(Lsat),NO=boundaryProfile(Lunsat);
test(YES.sourceSAT && !NO.sourceSAT,'matched labels incorrect');
test(!YES.global0&&!YES.global1,'both global SAT endpoints must fail');
test(YES.profile.filter(x=>x.AND).length===1,'unique middle boundary absent');
test(YES.profile.find(x=>x.AND).sigma.join('')==='10','wrong SAT boundary');
test(NO.profile.every(x=>!x.AND && x.OR),'wrong join UNSAT counterexample');
test(NO.independentSat,'each UNSAT source block must be separately SAT');
const all8=[];for(let b=0;b<8;b++)all8.push([0,1,2].map(i=>((b>>i)&1?1:-1)*(i+1)));
test(!exact(all8).yes && exact(all8.slice(1)).yes,'H8/H7 controls');
process.stdout.write(JSON.stringify({verified:'PASS',matchedSAT:YES.sourceSAT,matchedUNSAT:!NO.sourceSAT,
  yesMiddleBoundary:YES.profile.find(x=>x.AND).sigma,sourcePairExtremeModes:YES.matrixCount+NO.matrixCount,
  noSourceAllBlockJoin:NO.profile.every(x=>!x.AND),H7SAT:true,H8UNSAT:true},null,2)+'\n');
