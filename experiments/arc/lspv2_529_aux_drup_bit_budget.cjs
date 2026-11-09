// LSPV-2/529: pure-JavaScript finite DRUP budget and RAT control verifier.
// This implements a distinct DRUP checker, NOT native DRAT-trim, R_mix341 or FLMV.
"use strict";
const ck=(ok,label)=>{if(!ok)throw Error(label)};
function k4(q){
 const E=[];for(let a=0;a<4;a++)for(let b=a+1;b<4;b++)E.push([a,b]);
 const F=[];
 for(let v=0;v<4;v++){
  const inc=E.map((e,i)=>e.includes(v)?i+1:0).filter(Boolean);
  for(let z=0;z<8;z++){
   const b=[z>>2&1,z>>1&1,z&1];
   if((b[0]^b[1]^b[2])!==q[v])F.push(inc.map((x,i)=>b[i]?-x:x));
  }
 }return F;
}
function up(db,C){
 const a=new Map();
 for(const x of C){
  const id=Math.abs(x),val=x<0;
  if(a.has(id)&&a.get(id)!==val)return true;
  a.set(id,val);
 }
 for(;;){
  let changed=false;
  for(const c of db){
   let sat=false,free=[];
   for(const x of c){
    if(!a.has(Math.abs(x)))free.push(x);
    else if(a.get(Math.abs(x))===(x>0)){sat=true;break}
   }
   if(sat)continue;
   if(!free.length)return true;
   if(free.length===1){
    const x=free[0],id=Math.abs(x),val=x>0;
    if(a.has(id)){if(a.get(id)!==val)return true}
    else{a.set(id,val);changed=true}
   }
  }
  if(!changed)return false;
 }
}
function resolve(a,b,p){
 ck(a.includes(p)&&b.includes(-p),"pivot");
 const c=[...new Set([...a.filter(x=>x!==p),...b.filter(x=>x!==-p)])];
 if(c.some(x=>c.includes(-x)))return null;
 return c.sort((x,y)=>Math.abs(x)-Math.abs(y)||x-y);
}
function dp(F){
 let cur=F.map(c=>[...c].sort((x,y)=>Math.abs(x)-Math.abs(y)||x-y));
 const seen=new Set(cur.map(c=>c.join(","))),ops=[];
 for(let p=1;p<=6;p++){
  const pos=cur.filter(c=>c.includes(p)),neg=cur.filter(c=>c.includes(-p));
  const next=cur.filter(c=>!c.includes(p)&&!c.includes(-p));
  for(const a of pos)for(const b of neg){
   const c=resolve(a,b,p);if(c===null)continue;
   if(!seen.has(c.join(","))){ops.push(["+",c]);seen.add(c.join(","))}
   next.push(c);if(!c.length)return ops;
  }
  cur=[...new Map(next.map(c=>[c.join(","),c])).values()];
 }throw Error("expected UNSAT");
}
function replay(F,ops){
 const db=F.map(c=>[...c]);let adds=0,dels=0;
 for(const [action,c] of ops){
  ck(new Set(c).size===c.length&&!c.includes(0)&&!c.some(x=>c.includes(-x)),"clause grammar");
  if(action==="+"){ck(up(db,c),"RUP invalid");db.push(c);adds++}
  else if(action==="-"){
   const i=db.findIndex(d=>JSON.stringify(d)===JSON.stringify(c));
   ck(i>=0,"bad deletion");db.splice(i,1);dels++;
  }else throw Error("bad action");
 }
 ck(ops.length>0&&ops.at(-1)[0]==="+"&&ops.at(-1)[1].length===0,"no terminal empty");
 return {adds,dels};
}
function main(){
 let checks=0,sat=0,unsat=0,auxCases=0,rejected=0;
 for(let mask=0;mask<16;mask++){
  const q=[0,1,2,3].map(i=>mask>>i&1),F=k4(q);
  ck(F.length===16&&F.every(c=>c.length===3),"source grammar");checks++;
  const actual=[...Array(64).keys()].some(a=>F.every(c=>c.some(x=>(((a>>(Math.abs(x)-1))&1)===1)===(x>0))));
  ck(actual===(q.reduce((a,b)=>a+b,0)%2===0),"SAT parity");checks++;
  const options=[];
  for(const a of F)for(const b of F)for(const x of a)if(b.includes(-x)){
   const c=resolve(a,b,x);if(c!==null)options.push(c);
  }
  const fresh=[...options[0],1000003];
  ck(up(F,fresh),"fresh consequence");checks++;
  if(actual){
   sat++;ck(!up(F,[]),"SAT cannot RUP empty");checks++;
   let blocked=false;
   try{replay(F,[["+",fresh],["-",fresh],["+",[]]])}catch(e){blocked=true}
   ck(blocked,"SAT corrupted proof accepted");checks++;rejected++;
  }else{
   unsat++;const proof=dp(F);
   ck(proof.length===31,"DP records");checks++;
   ck(replay(F,proof).adds===31,"source RUP replay");checks++;
   const combined=[["+",fresh],["-",fresh],...proof];
   const result=replay(F,combined);
   ck(result.adds===32&&result.dels===1,"aux deletion");checks++;
   const log=combined.map(([a,c])=>(a==="-"?"d ":"")+(c.length?c.join(" ")+" ":"")+"0\n").join("");
   const B=log.length; // ASCII bytes; no comments or non-ASCII names.
   ck(B*(6+B)>=32*7,"bit-budget necessary condition");checks++;auxCases++;
  }
 }
 ck(sat===8&&unsat===8&&auxCases===8,"case totals");checks++;
 const before=[[-1,2],[-2]],after=[[-2]];
 ck(!up(before,[1])&&!up(after,[1]),"non-RUP RAT control");checks++;
 const rat=(db)=>db.filter(c=>c.includes(-1)).every(c=>up(db,c.filter(x=>x!==-1)));
 ck(!rat(before)&&rat(after),"RAT not monotone under retained clauses");checks++;
 return {checks,sat,unsat,auxCases,rejected,model:"finite declared DRUP+RAT guards, not historical R_mix341"};
}
const RESULT_529=main();
if(typeof process!=="undefined"&&process.stdout)process.stdout.write(JSON.stringify(RESULT_529,null,2)+"\n");
