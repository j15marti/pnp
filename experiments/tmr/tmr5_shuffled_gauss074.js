const result=(function audit(){
"use strict";
let checks=0, accepted=0, rejected=0, replayed=0, randomCases=0, invalidRejected=0;
const ok=(v,s)=>{checks++;if(!v)throw Error("CHECK "+s);};
let rng=716231;
const rand=()=>{rng^=rng<<13;rng^=rng>>>17;rng^=rng<<5;return rng>>>0;};
const parity=x=>{let p=0;while(x){p^=x&1;x>>=1;}return p;};
function shuffle(a){a=a.map(x=>x.slice());for(let i=a.length-1;i>0;i--){let j=rand()%(i+1);[a[i],a[j]]=[a[j],a[i]];}return a;}
function block(ids,b){return Array.from({length:8},(_,x)=>x).filter(x=>parity(x)===(1-b)).map(x=>ids.map((id,k)=>((x>>(2-k))&1)?-id:id));}
function rowsOf(cs){
 const groups=new Map();
 cs.forEach((c,i)=>{
  if(c.length!==3||c.some(x=>!Number.isSafeInteger(x)||x===0))throw Error("invalid input");
  const ids=c.map(Math.abs).sort((a,b)=>a-b);
  if(new Set(ids).size!==3)throw Error("nonproper");
  const pat=ids.reduce((p,id)=>(p<<1)|(c.includes(-id)?1:0),0),key=ids.join(",");
  if(!groups.has(key))groups.set(key,{ids,seen:new Map()});
  if(!groups.get(key).seen.has(pat))groups.get(key).seen.set(pat,i);
 });
 const rows=[];
 for(const g of groups.values())for(let charge=0;charge<2;charge++){
  const patterns=Array.from({length:8},(_,p)=>p).filter(p=>parity(p)===(1-charge));
  if(patterns.every(p=>g.seen.has(p)))rows.push({ids:g.ids,charge,source:patterns.map(p=>g.seen.get(p))});
 }
 return rows;
}
function gauss(rows){
 const ids=[...new Set(rows.flatMap(r=>r.ids))].sort((a,b)=>a-b);
 const col=new Map(ids.map((v,i)=>[v,i])),basis=new Map();
 for(let j=0;j<rows.length;j++){
  let mask=rows[j].ids.reduce((m,v)=>m^(1n<<BigInt(col.get(v))),0n),rhs=rows[j].charge,used=1n<<BigInt(j);
  for(let i=ids.length-1;i>=0;i--){
   if(((mask>>BigInt(i))&1n)===0n)continue;
   if(basis.has(i)){let b=basis.get(i);mask^=b.mask;rhs^=b.rhs;used^=b.used;}
   else{basis.set(i,{mask,rhs,used});break;}
  }
  if(mask===0n&&rhs===1){let out=[];for(let t=0;t<rows.length;t++)if((used>>BigInt(t))&1n)out.push(t);return out;}
 }
 return null;
}
function replay(cs,rows,indices){
 if(!indices?.length)return false;
 let seen=new Set(),occ=new Map(),rhs=0;
 for(const j of indices){
  if(j<0||j>=rows.length||seen.has(j))return false;seen.add(j);
  const row=rows[j],pats=new Set();
  for(const src of row.source){
   const clause=cs[src];if(!clause)return false;
   const ids=clause.map(Math.abs).sort((a,b)=>a-b);
   if(ids.join()!==row.ids.join())return false;
   const pat=ids.reduce((p,id)=>(p<<1)|(clause.includes(-id)?1:0),0);
   if(parity(pat)!==(1-row.charge))return false;
   pats.add(pat);
  }
  if(pats.size!==4)return false;
  rhs^=row.charge;row.ids.forEach(v=>occ.set(v,(occ.get(v)||0)^1));
 }
 return rhs===1&&[...occ.values()].every(v=>v===0);
}
function decide(cs){
 const rows=rowsOf(cs),selected=gauss(rows);
 if(selected){ok(replay(cs,rows,selected),"certificate replay");accepted++;replayed++;}else rejected++;
 return {rows,selected};
}
function sat(cs,n){
 for(let a=0;a<2**n;a++)if(cs.every(c=>c.some(l=>((a>>(Math.abs(l)-1))&1)===(l>0?1:0))))return a;
 return null;
}
function k4(charges){
 const edge=[];for(let a=0;a<4;a++)for(let b=a+1;b<4;b++)edge.push([a,b]);
 const inc=Array.from({length:4},()=>[]);
 edge.forEach(([a,b],i)=>{inc[a].push(i+1);inc[b].push(i+1);});
 return inc.flatMap((ids,i)=>block(ids,charges[i]));
}
const odd=k4([0,0,0,1]),even=k4([0,0,0,0]);
ok(sat(odd,6)===null&&sat(even,6)!==null,"K4 opposite truth");
let base=decide(odd);ok(base.rows.length===4&&base.selected.length===4,"K4 exact four-row core");
ok(decide(even).selected===null,"even K4 SAT control");
for(let omit=0;omit<odd.length;omit++){
 const removed=odd.filter((_,i)=>i!==omit);
 ok(decide(removed).selected===null&&sat(removed,6)!==null,"incomplete K4 core control");
}
let exhausted=0;
for(let mask=0;mask<256;mask++){
 const clauses=[];for(let p=0;p<8;p++)if(mask&(1<<p))clauses.push([1,2,3].map((v,i)=>((p>>(2-i))&1)?-v:v));
 const truth=sat(clauses,3),proof=decide(clauses);
 ok(!proof.selected||truth===null,"complete 3var CNF sound");
 if(truth===null)ok(proof.selected!==null,"full8 contradictory triple");
 exhausted++;
}
for(let iter=0;iter<400;iter++){
 const cs=[];for(let a=1;a<=4;a++)for(let b=a+1;b<=4;b++)for(let c=b+1;c<=4;c++)for(let p=0;p<8;p++)if((rand()&3)!==0)cs.push([a,b,c].map((v,j)=>((p>>(2-j))&1)?-v:v));
 const truth=sat(cs,4),proof=decide(shuffle(cs));
 ok(!proof.selected||truth===null,"4var randomized sound");randomCases++;
}
const shuffledSamples=[];
for(let iter=0;iter<25;iter++){
 const flipped=new Set([1,2,3,4,5,6].filter(v=>(rand()&1)===1));
 let transformed=odd.map(row=>row.map(l=>(l>0?1:-1)*(flipped.has(Math.abs(l))?-1:1)*(Math.abs(l)*7+11)));
 let cs=shuffle(transformed.concat(block([500,501,502],0),[[600,601,602],[600,-601,602],[-600,601,602]],transformed.slice(0,4),[[1000,1001,-1002]]));
 const proof=decide(cs);
 ok(proof.selected!==null&&replay(cs,proof.rows,proof.selected),"permutation signs duplicate arbitrary clauses");
 ok(proof.selected.length===4,"distractor not necessary");
 shuffledSamples.push({clauseCount:cs.length,affineRows:proof.rows.length,certificateRows:proof.selected.length,sourceIndices:proof.selected.flatMap(j=>proof.rows[j].source)});
}
for(let z=0;z<25;z++)ok(decide(shuffle(even.concat([[7,8,9]]))).selected===null,"SAT parity with unrelated clause");
for(const bad of [[[1,1,2]],[[-1,1,2]],[[1,2,0]]]){try{decide(bad)}catch(_e){invalidRejected++;}}
ok(invalidRejected===3,"syntax rejects");
const badCert=base.selected.slice(1);ok(!replay(odd,base.rows,badCert),"incomplete certificate rejected");
return {status:"COMPUTATIONAL",seed:716231,deterministic:true,checks,exhausted,randomCases,accepted,rejected,replayed,invalidRejected,badCertificateRejected:true,failures:0,K4:{clauses:odd.length,rows:base.rows.length,certificate:base.selected.length},samples:shuffledSamples.slice(0,3),scope:"Proper three-distinct-variable CNF; inconsistent authenticated subset of complete parity blocks; not universal SAT nor a TM trace"};
})();
console.log(JSON.stringify(result,null,2));
