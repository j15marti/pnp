'use strict';
// LSPV-4/507 standalone finite verifier. Hosted V8, NOT native FLMV.
const graphs=(()=>{
const k4=[],k33=[],cube=[];
for(let i=0;i<4;i++)for(let j=i+1;j<4;j++)k4.push([i,j]);
for(let i=0;i<3;i++)for(let j=3;j<6;j++)k33.push([i,j]);
for(let i=0;i<8;i++)for(let d of [1,2,4])if(i<(i^d))cube.push([i,i^d]);
const lines=[[0,1,3],[1,2,4],[2,3,5],[3,4,6],[4,5,0],[5,6,1],[6,0,2]];
const heawood=lines.flatMap((s,i)=>s.map(v=>[v,7+i]));
return [['K4',4,k4],['K3,3',6,k33],['Q3',8,cube],['Heawood',14,heawood]];
})();
function encode(h,edges,charge){
const m=edges.length,w=Math.ceil(Math.log2(m+1)),inc=Array.from({length:h},()=>[]);
edges.forEach(([a,b],i)=>{inc[a].push(i+1);inc[b].push(i+1)});
const str=['10100101',h.toString(2).padStart(12,'0'),m.toString(2).padStart(12,'0')];
let groups=[],pos=32;
for(let v=0;v<h;v++){
let grp=[];inc[v].sort((a,b)=>a-b);if(inc[v].length!==3)throw Error('degree');
for(let z=0;z<8;z++){
const bits=[(z>>2)&1,(z>>1)&1,z&1];
if((bits[0]^bits[1]^bits[2])===((charge>>v)&1))continue;
for(let j=0;j<3;j++){
str.push(inc[v][j].toString(2).padStart(w,'0'),String(bits[j]));
if(j===2)grp.push(pos+w);
pos+=w+1;
}}
groups.push(grp);
}
return {s:str.join(''),groups};
}
const cases=[];
for(const [name,h,edges] of graphs){
const q=2**h,inputs=[],keys=new Set();let quartet=null;
for(let b=0;b<q;b++){
const {s,groups}=encode(h,edges,b);
if(quartet===null)quartet=groups;
const key=groups.map(g=>s[g[0]]).join('');
if(keys.has(key))throw Error('trace collision');keys.add(key);inputs.push(s);
if((b.toString(2).replace(/0/g,'').length%2)===0&&key.length!==h)throw Error('key');
}
const checks=h<=8?Array.from({length:q},(_,i)=>i):[0,1,3,19,674,4660,q-1];
for(const b of checks)for(let v=0;v<h;v++){
const a=inputs[b],c=inputs[b^(1<<v)];let changes=[];
for(let k=0;k<a.length;k++)if(a[k]!==c[k])changes.push(k);
if(changes.join(',')!==quartet[v].join(','))throw Error('quartet mismatch');
}
cases.push({graph:name,H:h,N:inputs[0].length,sources:q,required_query_groups:h,
trace_cache_hits_across_distinct_charges:0,cache_leaves:q,full_trie_nodes:2*q-1,
aggregate_fresh_input_probes_floor:q*h});
}
const raw={label:'LSPV4_507_PARITY_TRACE_COVER_REPLAY',status:'PASS',cases,
native_FLMV:false,historical_Rmix341:false};
process.stdout.write(JSON.stringify(raw,null,2)+'\n');
