/* LSPV-4/455, standalone deterministic finite-source check, no dependencies.
 * Execute: node -e "console.log(require('./lspv4_455_gray_orfold_public.js'))"
 * This source is also directly eval-able as an expression. */
(()=>{
 let tests=0;
 const ok=(b,m)=>{if(!b)throw Error(m);tests++};
 const SAT=(clauses)=>{
  const vs=[...new Set(clauses.flat().map(x=>Math.abs(x)))].sort((a,b)=>a-b);
  for(let mask=0;mask<2**vs.length;mask++){
   const a=new Map(vs.map((v,i)=>[v,(mask>>i)&1]));
   if(clauses.every(C=>C.some(l=>a.get(Math.abs(l))===+(l>0))))return true;
  }return false;
 };
 const pin=(z,u,v,positive)=>{let a=positive?z:-z;
  return [[a,u,v],[a,u,-v],[a,-u,v],[a,-u,-v]]};
 const BL=(n,vs)=>vs.map((v,j)=>(n>>j&1)?-v:v);
 // Strict proper-three original two-block PATH3 sources, with shared z=1.
 // Types: full SAT, conflicting boundary pins, and signed K4 controls.
 let cases=[];
 for(let kind=0;kind<4;kind++){
  for(let polarity=0;polarity<2;polarity++){
   let f1=[...pin(1,2,3,true)],f2=[...pin(1,4,5,kind!==1)];
   if(kind===2)f2.push(...pin(1,4,5,false));
   if(kind===3)f1=[...pin(1,2,3,false)];
   if(polarity){f1=f1.map(c=>c.map(v=>-v));f2=f2.map(c=>c.map(v=>-v))}
   cases.push([f1,f2]);
  }
 }
 let pairs=0,folded=0,flip=0;
 for(const [f1,f2] of cases){
  ok(f1.concat(f2).every(c=>c.length===3&&new Set(c.map(Math.abs)).size===3),"original strict");
  let m0=SAT(f1.concat([[1]])),m1=SAT(f1.concat([[-1]]));
  let forbidden=[];if(!m0)forbidden.push(BL(0,[1]));if(!m1)forbidden.push(BL(1,[1]));
  let mutable=[...f2.map(c=>c.slice()),...forbidden.map(c=>c.slice()),[-1]];
  let fixed=mutable.length-1;
  let saw=[];
  for(let b=0;b<2;b++){
   mutable[fixed][0]=b?1:-1;
   let res=SAT(mutable);folded++;
   let pair=false;
   if(m0){pair ||= SAT(f2.concat([[1*-1],[b?1:-1]]));pairs++}
   if(m1){pair ||= SAT(f2.concat([[1],[b?1:-1]]));pairs++}
   ok(res===pair,"OR projection");
   ok(JSON.stringify(mutable.slice(0,f2.length))===JSON.stringify(f2),"source immutability");
   saw.push(res);
   if(b)flip++;
  }
  ok((saw[0]||saw[1])===SAT(f1.concat(f2)),"whole parent");
 }
 for(let a=0;a<4;a++)for(let b=0;b<4;b++){
  let forced=[[b&1?1:-1],[b&2?2:-2]];
  ok(SAT([BL(a,[1,2]),...forced])===(a!==b),"blocker sign");
 }
 ok(!SAT([[]]),"empty clause");
 return {cases:cases.length,checks:tests,foldedCalls:folded,pairCalls:pairs,graySignEdits:flip,status:"PASS",scope:"finite original proper-3CNF plus general-CNF child"};
})()