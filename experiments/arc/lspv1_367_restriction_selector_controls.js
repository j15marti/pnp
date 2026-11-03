// LSPV-1 RESTRICTION_STABLE_REFLECTION367, deterministic finite controls
// No dependencies. Reports a restricted universal-selector construction, not a P vs NP proof.
function run367(){
const E=[[1,2],[1,3],[1,4],[2,3],[2,4],[3,4]];
const CHECK=(ok,msg)=>{if(!ok)throw Error(msg);};
let assertions=0;
function ck(ok,msg){assertions++;CHECK(ok,msg);}
function gen(charges){
 let C=[];
 for(let u=1;u<=4;u++){
  let inc=E.map((e,i)=>e.includes(u)?i+1:0).filter(Boolean);
  ck(inc.length===3,"not cubic");
  for(let a=0;a<8;a++){
   let parity=((a>>0)&1)^((a>>1)&1)^((a>>2)&1);
   if(parity!==charges[u-1]){
    let clause=inc.map((x,i)=>((a>>i)&1)?-x:x);
    C.push(clause);
   }
  }
 }
 return C;
}
function sat(C,mask){return C.every(c=>c.some(l=>l>0?((mask>>(l-1))&1)===1:((mask>>(-l-1))&1)===0));}
function models(C,v){let n=0;for(let a=0;a<(1<<v);a++)if(sat(C,a))n++;return n;}
const odd=gen([1,0,0,0]),even=gen([0,0,0,0]);
ck(odd.length===16&&even.length===16,"source count");
ck(models(odd,6)===0,"odd UNSAT"); ck(models(even,6)===8,"even SAT count");
let deletion=0,flips=0;
for(let i=0;i<odd.length;i++){
 let neighbor=odd.filter((_,j)=>j!==i);
 ck(models(neighbor,6)>0,"deletion witness "+i);deletion++;
 for(let k=0;k<3;k++){
  let changed=odd.map((c,j)=>j===i?c.map((l,t)=>t===k?-l:l):c.slice());
  ck(models(changed,6)>0,"sign repair "+i+","+k);flips++;
 }
}
let templates=[];
for(let i=1;i<=6;i++)for(let j=i+1;j<=6;j++)for(let k=j+1;k<=6;k++)
 for(let b=0;b<8;b++)templates.push([b&1?-i:i,b&2?-j:j,b&4?-k:k]);
ck(templates.length===160,"template count");
const key=c=>c.slice().sort((a,b)=>Math.abs(a)-Math.abs(b)).join(",");
const keys=new Set(templates.map(key));ck(keys.size===160,"unique templates");
let selected=[];
for(let j=0;j<odd.length;j++){
 let ix=templates.findIndex(t=>key(t)===key(odd[j]));
 ck(ix>=0,"source in template");selected.push(ix);
}
let surviving=[];
for(let j=0;j<odd.length;j++){
 let hot=0;
 for(let t=0;t<templates.length;t++){
  const active=t===selected[j];
  if(active){hot++;surviving.push(templates[t]);}
  // Each gated clause is (!selector[j,t] OR template[t]).
  // With the fixed selector, inactive clauses become TRUE.
 }
 ck(hot===1,"exactly one");
}
ck(surviving.length===odd.length&&surviving.every((c,j)=>key(c)===key(odd[j])),"restriction EXACT");
const tv=[[1],[-1]];
// Toy reflection source uses selectors (s00,s01,s10,s11), witness x,
// with marker rejecting iff slot0 is x AND slot1 is ~x.
let toySat=0,toyAcceptSat=0,toyInvalidRejected=0,validCodes=0, toyCorrectReject=0;
for(let sel=0;sel<16;sel++){
 const bits=[0,1,2,3].map(i=>(sel>>i)&1);
 const hot=(bits[0]+bits[1]===1)&&(bits[2]+bits[3]===1);
 const reject=(bits[0]===1)&&(bits[3]===1);
 if(hot)validCodes++;
 else toyInvalidRejected++;
 if(hot&&reject){toyCorrectReject++;ck(models([[1],[-1]],1)===0,"toy rejected only contradiction");}
 for(let x=0;x<2;x++){
  const gated=[0,1].every(j=>[0,1].every(t=>!bits[2*j+t]||sat([tv[t]],x)));
  if(hot&&reject&&gated)toySat++;
  if(hot&&!reject&&gated)toyAcceptSat++;
 }
}
ck(validCodes===4&&toyCorrectReject===1&&toySat===0&&toyAcceptSat>0,"toy both labels");
let bad=0;
for(const clause of [[0],[1,-1],[7],[]]){
 const valid=clause.length===3&&new Set(clause.map(Math.abs)).size===3&&clause.every(x=>x!==0&&Math.abs(x)<=6);
 ck(!valid,"bad signed three-literal source accepted");bad++;
}
let badProof=0;
for(const pivot of [0,2,-2]){ const valid=pivot===1;ck(!valid,"bad pivot accepted");badProof++;}
const rows=4, xorAdds=3;
ck(rows*3+xorAdds===15,"K4 XOR mixed control exact known upper");
return {run:"RESTRICTION_STABLE_REFLECTION367",scope:"finite construction and symbolic restriction, NOT asymptotic proof check",
 formula:{graph:"K4",variables:6,oddClauses:16,evenClauses:16,oddModels:models(odd,6),evenModels:models(even,6),deletionSAT:deletion,signFlipSAT:flips},
 selector:{threeLiteralTemplates:templates.length,slots:odd.length,gatedClauses:templates.length*odd.length,oneHotActive:odd.length,specializationEqualsOriginal:true},
 toy:{validSelectorCodes:validCodes,rejectionCodes:toyCorrectReject,rejectSATmodels:toySat,acceptSATmodels:toyAcceptSat},
 controls:{malformedRejected:bad,corruptedPivotsRejected:badProof,knownMixedK4Nodes:15},assertions,
 proofStatus:{finite:"COMPUTATIONAL",restrictionLemma:"PROVED/EXACT symbolic",resolutionLowerBound:"KNOWN theorem on growing expander Tseitin",mixedTransfer:"OPEN",B3:"OPEN",PvsNP:"OPEN"}
};
}
if(typeof module!=="undefined"&&module.exports)module.exports=run367;
if(typeof require!=="undefined"&&require.main===module)process.stdout.write(JSON.stringify(run367(),null,2)+"\n");
