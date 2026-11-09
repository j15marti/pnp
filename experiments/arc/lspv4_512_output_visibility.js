// Independent JavaScript finite control for LSPV-4/512 output-channel firewall.
// Strict3 K4 Tseitin source. Does not implement native FLMV instruction semantics.
const crypto=require('node:crypto');
const assert=require('node:assert/strict');
const edges=[];
for(let a=0;a<4;a++)for(let b=a+1;b<4;b++)edges.push([a,b]);
const clauses=[];
for(let vertex=0;vertex<4;vertex++){
 const ports=edges.map(([a,b],idx)=>a===vertex||b===vertex?idx+1:null).filter(x=>x!==null);
 assert.equal(ports.length,3);
 for(let mask=0;mask<8;mask++){
  const sign=[(mask>>2)&1,(mask>>1)&1,mask&1];
  const p=sign[0]^sign[1]^sign[2];
  if(p!==Number(vertex===0))clauses.push(ports.map((id,i)=>[id,sign[i]]));
 }
}
function enc(C){return '11010101'+C.flatMap(row=>row.map(([v,s])=>v.toString(2).padStart(3,'0')+s)).join('')+'01';}
const U=enc(clauses), C2=clauses.map(row=>row.map(l=>[...l]));C2[0][0][1]^=1;const S=enc(C2);
const diff=[...U].flatMap((x,i)=>x!==S[i]?[i]:[]);
assert.equal(diff.length,1);assert.equal(diff[0],11);assert.equal(U.length,202);
function assignments(C){let total=0;for(let a=0;a<64;a++){
 if(C.every(row=>row.some(([v,neg])=>Boolean((a>>(v-1))&1)!==Boolean(neg))))total++;
 }return total;}
const nU=assignments(clauses),nS=assignments(C2);
assert.equal(nU,0);assert.equal(nS,2);
function syntacticParser(bits){
 if(bits.length!==202||bits.slice(0,8)!=='11010101'||bits.slice(-2)!=='01')return null;
 const out=[];
 for(let i=0;i<16;i++){
  const row=[];for(let j=0;j<3;j++){
   const k=8+12*i+4*j;
   const id=parseInt(bits.slice(k,k+3),2);
   if(id<1||id>6)return null;
   row.push([id,Number(bits[k+3])]);
  }
  if(new Set(row.map(x=>x[0])).size!==3)return null;
  out.push(row);
 }
 return out;
}
assert.deepEqual(syntacticParser(U),clauses);
assert.deepEqual(syntacticParser(S),C2);
const corrupt=[U.slice(1),U+'0','0'+U.slice(1),U.slice(0,-2)+'00',U.slice(0,8)+'000'+U.slice(11)];
corrupt.forEach(x=>assert.equal(syntacticParser(x),null));
const pivot=diff[0], trace=['HEADER_CHECK','FULL_LENGTH_CHECK','MATCH_ALL_NONPIVOT','READ_AND_WRITE_LABEL','HALT'];
const records=[U,S].map((bits,d)=>({descriptor:d,pivot_sign:Number(bits[pivot]),internal_trace:[...trace],write_only_output:d}));
assert.deepEqual(records[0].internal_trace,records[1].internal_trace);
assert.notEqual(records[0].write_only_output,records[1].write_only_output);
const hash=s=>crypto.createHash('sha256').update(s).digest('hex');
const result={status:'COMPUTATIONAL strict3 source control',graph:'K4',n_vertices:4,n_edges:6,n_clauses:clauses.length,encoded_bits:U.length,difference_indices_0based:diff,source_sha256_unsat:hash(U),source_sha256_sat:hash(S),sat_witnesses_after_flip:nS,unsat_witnesses_original:nU,rank_internal_only:0,rank_output_aware:1,compatible_internal_only:2,compatible_output_aware:1,malformed_rejection_controls:corrupt.length,records,scope:'finite witness only; output tape not part of defined internal configuration, general fallback is conditional on any correct full SAT decider'};
console.log(JSON.stringify(result,null,2));
