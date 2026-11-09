// LSPV-2/530 independent V8 cost-sound CDCL decision-nogood replay.
// Distinct test-only solver calculus: original signed CNF, UP, global RUP, restart, deletion.
// No historical R_mix341 inference or native FLMV execution.
function assert(p,msg){if(!p)throw Error(msg||"assertion failed");}
function pop(x){let n=0;while(x){x&=x-1;n++}return n}
function edges(name){
 if(name==="K4"){let e=[];for(let a=0;a<4;a++)for(let b=a+1;b<4;b++)e.push([a,b]);return [4,e]}
 if(name==="PRISM")return [6,[[0,1],[1,2],[0,2],[3,4],[4,5],[3,5],[0,3],[1,4],[2,5]]];
 let e=[];for(let a=0;a<8;a++)for(let b=a+1;b<8;b++)if(pop(a^b)===1)e.push([a,b]);return [8,e];
}
function tseitin(name,mask){
 const [h,e]=edges(name),cs=[];
 for(let v=0;v<h;v++){
  const inc=e.map(([a,b],i)=>a===v||b===v?i+1:0).filter(Boolean);
  assert(inc.length===3,"not cubic");
  for(let bits=0;bits<8;bits++)if(pop(bits)%2!==((mask>>v)&1))
   cs.push(inc.map((x,i)=>((bits>>(2-i))&1)?-x:x));
 }
 return {n:e.length,cs};
}
function up(db,decisions){
 const a=new Map();
 for(const l of decisions){let x=Math.abs(l),b=l>0;
  if(a.has(x)&&a.get(x)!==b)return {conflict:true,a};
  a.set(x,b)
 }
 for(;;){
  let changed=false;
  for(const c of db){
   let un=0,u=0,sat=false;
   for(const l of c){let x=Math.abs(l),v=a.get(x);
    if(v===undefined){un++;u=l}else if(v===(l>0)){sat=true;break}
   }
   if(sat)continue;
   if(un===0)return {conflict:true,a};
   if(un===1){a.set(Math.abs(u),u>0);changed=true;break}
  }
  if(!changed)return {conflict:false,a}
 }
}
function rup(db,c){return up(db,c.map(x=>-x)).conflict}
function truth(F){
 if(F.n>16)throw Error("finite brute-force bound");
 for(let mask=0;mask<1<<F.n;mask++)
  if(F.cs.every(c=>c.some(l=>(((mask>>(Math.abs(l)-1))&1)===Number(l>0)))))return true;
 return false;
}
function solve(F,allowOneDelete){
 const db=F.cs.map(c=>[...c]),m=F.cs.length;
 let q=0,del=0,steps=0;
 for(let restart=0;restart<10000;restart++){
  const decisions=[];
  for(;;){
   if(++steps>100000)throw Error("nontermination");
   const r=up(db,decisions);
   if(r.conflict){
    const clause=decisions.map(x=>-x).sort((x,y)=>Math.abs(x)-Math.abs(y)||x-y);
    assert(rup(db,clause),"global-learn RUP failure");
    q++;db.push(clause);
    if(!clause.length)return {label:"UNSAT",q,del};
    if(allowOneDelete&&del===0&&q===3){
     const j=db.findIndex((c,i)=>i>=m&&c!==clause);
     if(j>=0){db.splice(j,1);del++}
    }
    break;
   }
   if(r.a.size===F.n){
    assert(F.cs.every(c=>c.some(l=>r.a.get(Math.abs(l))===(l>0))),"bad model");
    return {label:"SAT",q,del};
   }
   for(let v=1;v<=F.n;v++)if(!r.a.has(v)){decisions.push(-v);break}
  }
 }
 throw Error("restart cap");
}
function main(){
 let checks=0,cases=0,sat=0,unsat=0,conflicts=0,deletions=0;
 for(const g of ["K4","PRISM","CUBE"]){
  const [h]=edges(g);
  for(const mask of [0,1,3,(1<<h)-1]){
   const f=tseitin(g,mask),parity=pop(mask)%2;
   assert(Number(!truth(f))===parity,"source parity mismatch");checks++;
   assert(f.cs.length===4*h,"incorrect strict3 size");checks++;
   for(const doDelete of [false,true]){
    const x=solve(f,doDelete);
    assert((x.label==="UNSAT")===Boolean(parity),"wrong SAT label");checks++;
    if(parity){assert(x.q>0,"no counted root conflict");checks++;unsat++}
    else sat++;
    if(doDelete&&parity){assert(x.del===1,"deletion control");checks++}
    cases++;conflicts+=x.q;deletions+=x.del;
   }
  }
 }
 const invalid=[[[1,1]],[[1,-1]],[[0]],[[4]],[[1,2,3,1]]];
 // Explicit declared input validator rejects repeated signs, zero and oversized width.
 function valid(n,cs){return Number.isInteger(n)&&n>0&&Array.isArray(cs)&&cs.every(c=>
  c.length>=1&&c.length<=3&&c.every(l=>Number.isInteger(l)&&l!==0&&Math.abs(l)<=n)&&
  new Set(c.map(l=>Math.abs(l))).size===c.length)}
 for(const cs of invalid){assert(!valid(3,cs),"malformed source accepted");checks++}
 assert(!rup([[-1,2],[-2]],[1]),"RAT-only control mistaken as RUP");checks++;
 return {verified:"LSPV-2/530 V8",assertions:checks,cases,sat,unsat,conflicts,deletions,
  limitation:"No original-source SHA or full historical checker; finite semantic control only"};
}
return main();