/* LSPV-2/431 independent successor checkpoint direct-sum experiment.
Run: node lspv2_431_shared_checkpoint_directsum.mjs
The finite tests are not a lower bound against unrestricted SAT machines. */
const produce = function produce(){
const records=[];let checks=0;
function runCase(q,k,mode){
 const M=4*k+8, tables=Array.from({length:q},()=>new Map()), trace=[];
 function frontier(i){let x=0,d=0;while(d<k&&tables[i].has(x)){x=tables[i].get(x);d++;}return {x,d};}
 function fresh(table,parity=null){const used=new Set([0,...table.keys(),...table.values()]);for(let v=1;v<M;v++)if(!used.has(v)&&(parity===null||v%2===parity))return v;throw Error("no unused state");}
 function ask(i,v){const t=tables[i];if(!t.has(v)){const f=frontier(i);t.set(v,fresh(t,f.x===v&&f.d===k-1?1:null));}const ans=t.get(v);trace.push([i,v,ans]);return ans;}
 for(let z=0;z<q*k-1;z++){
  let i=0,v=0;
  if(mode==="round"){i=z%q;v=frontier(i).x;}
  else if(mode==="front"){i=Math.min(q-1,Math.floor(z/k));v=frontier(i).x;}
  else if(mode==="stray"){i=z%q;v=(7*z+3)%M;}
  else if(mode==="repeat"){i=0;v=0;}
  else {i=(17*z+Math.floor(z/3))%q;v=z%3===0?frontier(i).x:(13*z+5)%M;}
  ask(i,v);
 }
 const counts=Array(q).fill(0);for(const [i] of trace)counts[i]++;
 const victim=counts.findIndex(z=>z<k);if(victim<0)throw Error("missing unresolved arm");
 function complete(m,bit){
  const t=new Map(m);let x=0;
  for(let z=0;z<k;z++){if(!t.has(x))t.set(x,fresh(t,z===k-1?bit:null));x=t.get(x);}
  if(x%2!==bit)throw Error("parity obstruction");
  for(let v=0;v<M;v++)if(!t.has(v))t.set(v,0);
  return Array.from({length:M},(_,j)=>t.get(j));
 }
 const sat=tables.map(t=>complete(t,1)),unsat=tables.map((t,i)=>complete(t,i===victim?0:1));
 function answer(tt){return tt.every(f=>{let x=0;for(let j=0;j<k;j++)x=f[x];return (x&1)===1;});}
 if(!answer(sat)||answer(unsat))throw Error("incorrect labels");
 for(const [i,v,a] of trace)if(sat[i][v]!==a||unsat[i][v]!==a)throw Error("incompatible query transcript");
 checks+=2*trace.length+2*q;
 return {q,k,M,mode,queries:trace.length,victim,counts,trace,sat,unsat};
}
for(const q of [2,3,4,5])for(const k of [1,2,3,5])for(const mode of ["round","front","stray","repeat","hybrid"])records.push(runCase(q,k,mode));
function graph(name){
 if(name==="K4"){let e=[];for(let a=0;a<4;a++)for(let b=a+1;b<4;b++)e.push([a,b]);return [4,e];}
 let e=[];for(let a=0;a<8;a++)for(let j of [1,2,4]){let b=a^j;if(a<b)e.push([a,b]);}return [8,e];
}
function tseitin(name,odd){
 const [H,edges]=graph(name),clauses=[];
 for(let v=0;v<H;v++){
  let inc=edges.map(([a,b],i)=>a===v||b===v?i:-1).filter(i=>i>=0);
  if(inc.length!==3)throw Error("not cubic");
  for(let a=0;a<8;a++){let parity= ((a&1)?1:0)^((a&2)?1:0)^((a&4)?1:0);if(parity===(odd&&v===0?1:0))continue;
   clauses.push(inc.map((j,h)=>((a>>h)&1)?-(j+1):j+1));
  }
 }
 function sat(skip=-1){for(let mask=0;mask<(1<<edges.length);mask++){let good=true;for(let j=0;j<clauses.length;j++){if(j===skip)continue;let c=clauses[j];if(!c.some(z=>((mask>>(Math.abs(z)-1))&1)===(z>0?1:0))){good=false;break;}}if(good)return true;}return false;}
 const isSat=sat(),deletionWitnesses=odd?clauses.filter((_,j)=>sat(j)).length:null;
 if(isSat===odd||clauses.length!==4*H||odd&&deletionWitnesses!==4*H)throw Error("Tseitin control");
 checks+=clauses.length+(odd?clauses.length:0);
 return {name,vertices:H,edge_vars:edges.length,clauses:clauses.length,charge:odd?"odd":"even",sat:isSat,deletionWitnesses};
}
const controls=[tseitin("K4",false),tseitin("K4",true),tseitin("cube",false),tseitin("cube",true)];
const aliases=[2,3,5].map(q=>{const k=5,M=4*k+8;const f=Array(M).fill(0);for(let i=0;i<k-1;i++)f[i]=i+1;f[k-1]=M-1;let x=0;for(let i=0;i<k;i++)x=f[x];if(x%2!==1)throw Error("alias");return {q,k,M,endpoint_bit:x&1,independent_oracle_cost:q*k,verified_alias_oracle_cost:k,alias_indices:Array(q).fill(0)};});
const qsum=records.reduce((a,z)=>a+z.queries,0);
return {schema:"LSPV2-431/shared-checkpoint-AND/1",timestamp:"2026-11-05 18:28 PST",model:"independent opaque indexed successor tables, NOT SAT solver runtime",records,controls,aliases,producer_checks:checks,summary:{cases:records.length,queries:qsum,controls:controls.length,all_pair_labels:"SAT and UNSAT completions from same <qk query transcript",M_rule:"4k+8",explicit_input_bits:"q*M*ceil(log2 M)",statuses:"PROVED/RESTRICTED model theorem, COMPUTATIONAL finite fixtures, OPEN arbitrary-A FLMV"}};
};
const result=produce();
if (typeof process!== 'undefined') console.log(JSON.stringify(result));
