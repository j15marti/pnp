// LSPV-1/537. Declared strict signed 3-CNF collision control.
// Finite controls only. NOT a historical R_mix341 native checker.
"use strict";
function assert(b,msg){if(!b)throw Error(msg||"assertion failed")}
function combinations(a,k){if(k===0)return [[]];if(a.length<k)return [];
 const out=[];for(let i=0;i<=a.length-k;i++)for(const sub of combinations(a.slice(i+1),k-1))out.push([a[i],...sub]);return out}
function graph(name){
 let e=[],h;
 if(name==="K4"){h=4;for(let i=0;i<h;i++)for(let j=i+1;j<h;j++)e.push([i,j])}
 if(name==="prism"){h=6;e=[[0,1],[1,2],[0,2],[3,4],[4,5],[3,5],[0,3],[1,4],[2,5]]}
 if(name==="cube"){h=8;for(let i=0;i<8;i++)for(let j=i+1;j<8;j++)if(popcount(i^j)===1)e.push([i,j])}
 if(name==="Petersen"){h=10;for(let i=0;i<5;i++){e.push([i,(i+1)%5],[i,i+5],[i+5,((i+2)%5)+5])}}
 return {h,e:e.sort((a,b)=>Number(0 in b?false:false)||((a.includes(0)?0:1)-(b.includes(0)?0:1)))};
}
function popcount(x){let s=0;while(x){s+=x&1;x>>=1}return s}
function norm(cl){return [...new Set(cl)].sort((a,b)=>Math.abs(a)-Math.abs(b)||b-a)}
function key(cl){return cl.join(",")}
function signed(ids,bits){return norm(ids.map((id,i)=>bits[i]?-id:id))}
function allbits(){let out=[];for(let a=0;a<2;a++)for(let b=0;b<2;b++)for(let c=0;c<2;c++)out.push([a,b,c]);return out}
function tseitin({h,e},odd){
 const out=[];for(let v=0;v<h;v++){const ids=e.flatMap(([a,b],i)=>a===v||b===v?[i+1]:[]);
 assert(ids.length===3,"not cubic");
 for(const bits of allbits())if((bits[0]+bits[1]+bits[2])%2!==Number(odd&&v===0))out.push(signed(ids,bits))
 }assert(out.length===4*h && new Set(out.map(key)).size===out.length);return out}
function easy(n,m){const out=allbits().map(bits=>signed([1,2,3],bits));
 for(let v=4;v<=n;v++)out.push(norm([1,2,v]));
 let used=new Set(out.map(key));assert(used.size===out.length);
 for(const ids of combinations(Array.from({length:n},(_,i)=>i+1),3)){
 for(const bits of allbits()){
  if(out.length===m)break;const cl=signed(ids,bits);if(!used.has(key(cl))){out.push(cl);used.add(key(cl))}
 }if(out.length===m)break
 }
 assert(out.length===m && used.size===m,"easy padding");
 return out}
function models(clauses,n){let count=0;for(let a=0;a<2**n;a++){
 if(clauses.every(cl=>cl.some(l=>Boolean(a&(2**(Math.abs(l)-1)))===(l>0))))count++;
 }return count}
function gamma(x){let b=x.toString(2);return "0".repeat(b.length-1)+b}
function encode(clauses,n,m){let w=Math.ceil(Math.log2(n+1)),s=gamma(n)+gamma(m);
 for(const cl of clauses){assert(cl.length===3);s+="0";for(const x of cl)s+=(x<0?"1":"0")+Math.abs(x).toString(2).padStart(w,"0")}return s}
function resolve(left,right,pivot){
 assert(left.includes(pivot)&&right.includes(-pivot),"pivot not present");
 const c=norm([...left.filter(x=>x!==pivot),...right.filter(x=>x!==-pivot)]);
 assert(!c.some(x=>c.includes(-x)),"tautological resolvent");return c
}
function certificate(source){let lines=[],steps=[],bs=allbits(),sourceSet=new Set(source.map(key));
 for(const bits of bs){let c=signed([1,2,3],bits);assert(sourceSet.has(key(c)),"missing source axiom");lines.push(c)}
 for(let a=0;a<2;a++)for(let b=0;b<2;b++){
  let i=a*4+b*2,j=i+1,c=resolve(lines[i],lines[j],3);
  assert(c.length===2);steps.push({i,j,pivot:3,c});lines.push(c)
 }
 for(let a=0;a<2;a++){
  let i=8+a*2,j=i+1,c=resolve(lines[i],lines[j],2);
  assert(c.length===1);steps.push({i,j,pivot:2,c});lines.push(c)
 }
 let c=resolve(lines[12],lines[13],1);assert(c.length===0);
 steps.push({i:12,j:13,pivot:1,c});lines.push(c);
 // Independent verifier reconstructs every derived record.
 for(let k=0;k<steps.length;k++){let t=steps[k],got=resolve(lines[t.i],lines[t.j],t.pivot);
  assert(key(got)===key(t.c),"bad inference")}
 return {inferences:steps.length,records:lines.length}
}
function run(){let t0=Date.now(),tests=[],assertions=0;
 for(const name of ["K4","prism","cube","Petersen"]){
  const g=graph(name),n=g.e.length,m=4*g.h,F=tseitin(g,true),S=tseitin(g,false),E=easy(n,m);
  assert(n===3*g.h/2 && E.length===F.length && F.length===m);assertions++;
  assert(models(F,n)===0);assertions++;
  assert(models(E,n)===0);assertions++;
  let even=models(S,n);assert(even===2**(n-g.h+1));assertions++;
  assert(encode(F,n,m).length===encode(E,n,m).length);assertions++;
  let p=certificate(E);assert(p.inferences===7 && p.records===15);assertions++;
  let misses=E.slice(0,8).filter(cl=>!new Set(F.map(key)).has(key(cl))).length;
  assert(misses===4);assertions++;
  let rejected=false;try{certificate(F)}catch(e){rejected=/missing source/.test(e.message)}
  assert(rejected);assertions++;
  let corrupted=false;try{resolve([1,2],[3,-2],1)}catch(e){corrupted=true}
  assert(corrupted);assertions++;
  tests.push({graph:name,vertices:g.h,variables:n,clauses:m,encoded_bits:encode(F,n,m).length,
   even_models:even,odd_models:0,control_models:0,resolution_inferences:p.inferences,
   original_source_clauses_missing_from_short_proof:misses});
 }
 return {status:"COMPUTATIONAL; symbolic pair-collision theorem in report",
  source_model:"strict signed 3CNF, explicit uniform-width binary literal identifiers",
  tests,assertions,wall_ms:Date.now()-t0,seed:"none",enumeration:"exhaustive",
  note:"Native historical R_mix341 and actual W_R minima not checked"};
}
if(typeof module!=="undefined"&&require.main===module)console.log(JSON.stringify(run(),null,2));
