function runTwinAutarkyAudit(){
 const started=Date.now();let checks=0;
 const sat=(F,n)=>{for(let a=0;a<2**n;a++)if(F.every(C=>C.some(x=>Boolean(a&(1<<(Math.abs(x)-1)))===(x>0))))return true;return false;};
 function reduce(F,n){
  const groups=new Map();
  for(let v=1;v<=n;v++){
   const signature=F.map(C=>C.includes(v)?"p":C.includes(-v)?"n":"0").join("");
   if(!groups.has(signature))groups.set(signature,[]);groups.get(signature).push(v);
  }
  const assignment=new Map(),classes=[];
  for(const G of groups.values())if(G.length>=2){classes.push(G);G.forEach((v,i)=>assignment.set(v,i===1));}
  const core=F.filter(C=>!C.some(x=>assignment.has(Math.abs(x))));
  return{core,assignment,classes};
 }
 function verify(F,n,semantic=true){
  const r=reduce(F,n);
  for(const C of F)if(C.some(x=>r.assignment.has(Math.abs(x)))){
   if(!C.some(x=>r.assignment.has(Math.abs(x))&&r.assignment.get(Math.abs(x))===(x>0)))throw Error("not autarky");
   checks++;
  }
  if(semantic){if(sat(F,n)!==sat(r.core,n))throw Error("SAT mismatch");checks++;}
  return r;
 }
 const clauses=[];
 for(let mask=1;mask<27;mask++){let q=mask,C=[];for(let v=1;v<=3;v++){const d=q%3;q=Math.floor(q/3);if(d)C.push(d===1?v:-v);}clauses.push(C);}
 let formulas=0;
 for(let i=-1;i<26;i++){
  if(i===-1){verify([],3);formulas++;continue;}
  verify([clauses[i]],3);formulas++;
  for(let j=i+1;j<26;j++){verify([clauses[i],clauses[j]],3);formulas++;
   for(let k=j+1;k<26;k++){verify([clauses[i],clauses[j],clauses[k]],3);formulas++;}
  }
 }
 let seed=20261008;
 const rnd=()=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed/2**32;};
 for(let trial=0;trial<500;trial++){
  const F=[];
  for(let c=0;c<15;c++){
   const C=[];
   for(let v=1;v<=6;v++)if(rnd()<0.35){const sign=rnd()<0.5?-1:1;if(v===1)C.push(sign*1,sign*7);else if(v===2)C.push(sign*2,sign*8);else C.push(sign*v);}
   F.push(C);
  }
  verify(F,8);
  const renamed=F.map(C=>C.map(x=>Math.sign(x)*(9-Math.abs(x))));verify(renamed,8);
 }
 const G=Array.from({length:128},(_,i)=>i+1);
 const base=[];
 for(const sign of [-1,1])for(const t of [129,130,-129,-130])base.push([...G.map(v=>sign*v),t]);
 const outside=Array.from({length:600},(_,j)=>Array.from({length:100},(_,i)=>{
 const v=131+i;return i<10&&((j>>i)&1)?-v:v;}));
 const product=[...base,...outside],res=verify(product,230,false);
 if(res.core.length!==0)throw Error("previous control not removed");checks++;
 const hardcore=Array.from({length:8},(_,m)=>[1,2,3].map(v=>((m>>(v-1))&1)?230+v:-(230+v)));
 const blocked=verify([...product,...hardcore],233,false);
 if(JSON.stringify(blocked.core)!==JSON.stringify(hardcore))throw Error("core corrupted");checks++;
 const bitlength=(F,n)=>8*(`p cnf ${n} ${F.length}\n`+F.map(C=>C.join(" ")+" 0\n").join("")).length;
 // One-pass result need not be twin-free: exhaustive search supplies a witness.
 let witness={F:[[1,2,3],[3,4,5],[5]]};
 const first=verify(witness.F,5),second=verify(first.core,5);
 witness.first=first.core;witness.second=second.core;
 if(!(second.core.length<first.core.length))throw Error("cascade control");checks++;
 outer:for(let i=0;i<26;i++)for(let j=i+1;j<26;j++)for(let k=j+1;k<26;k++){
  const F=[clauses[i],clauses[j],clauses[k]],a=reduce(F,3),b=reduce(a.core,3);
  if(a.core.length>0&&b.core.length<a.core.length){witness={F,first:a.core,second:b.core};break outer;}
 }
 return{status:"COMPUTATIONAL",checks,exhaustive_formulas:formulas,seed:20261008,
  random_formulas:500,renaming_controls:500,
  previous_independent_component:{source_bits:bitlength(product,230),remaining_clauses:res.core.length,child_bits:bitlength(res.core,230),classes:res.classes.map(G=>G.length)},
  arbitrary_remainder:{remaining_clauses:blocked.core.length,exactly_preserved:true},
  second_pass_witness:witness,elapsed_ms:Date.now()-started,
  limitations:"Reference semantics model uses explicit incidence signatures; it does not measure streaming resource bounds or prove general coverage."};
}
console.log(JSON.stringify(runTwinAutarkyAudit(), null, 2));
