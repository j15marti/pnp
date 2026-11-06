#!/usr/bin/env node
// LSPV-1/439. Deterministic all-source, paid-DEF-facet strict RES proof generator.
// No historical mixed GF(2) exporter or free semantic oracle.
function make(charge) {
const X=[1,2,3], W=[9,10,11], G=4;
const norm=a=>{let s=[...new Set(a)].sort((x,y)=>Math.abs(x)-Math.abs(y)||y-x);if(s.some(x=>s.includes(-x)))throw Error("tautology");return s};
const nodes=[], blocks=[], facets={};
const add=(kind,clause,source)=>{const z={id:nodes.length+1,kind,clause:norm(clause)};if(source)z.source=source;nodes.push(z);return z.id};
for(let mask=0;mask<8;mask++){let b=[(mask>>2)&1,(mask>>1)&1,mask&1];if((b[0]+b[1]+b[2])%2===charge)continue;let c=b.map((v,j)=>v?-(j+1):j+1), y=5+blocks.length;let a=add("SOURCE_SPLIT",[4,c[0],y],{block:blocks.length,face:0,wrong_bits:b}),d=add("SOURCE_SPLIT",[-y,c[1],c[2]],{block:blocks.length,face:1,wrong_bits:b});blocks.push({b,c,y,a,d})}
for(let j=0;j<3;j++){const x=j+1,w=j+9;facets[w]=[add("DEFINITION_FACET",[-w,-4],{owner_wire:w,facet:0}),add("DEFINITION_FACET",[-w,x],{owner_wire:w,facet:1}),add("DEFINITION_FACET",[w,4,-x],{owner_wire:w,facet:2})]}
const res=(a,b,p)=>{const A=nodes[a-1].clause,B=nodes[b-1].clause;if(!(A.includes(p)&&B.includes(-p)))throw Error("invalid oriented pivot");return add("RES",norm([...A.filter(x=>x!==p),...B.filter(x=>x!==-p)]),null) && (nodes[nodes.length-1].pivot=p,nodes[nodes.length-1].parents=[a,b],nodes.length)};
const implicates=[];
for(const q of blocks){let live=res(q.a,q.d,q.y);for(let j=0;j<3;j++){let x=j+1,w=j+9;if(q.c[j]>0)live=res(live,facets[w][2],x);else live=res(facets[w][1],live,x)}
const target=norm([4,...q.b.map((v,j)=>v?-(j+9):(j+9))]);
if(JSON.stringify(nodes[live-1].clause)!==JSON.stringify(target))throw Error("wrong B");
if(charge===0){let wi=9+q.b.findIndex(v=>v===1);live=res(live,facets[wi][0],4)}
implicates.push({wrong_bits:q.b,node_id:live,clause:nodes[live-1].clause})}
const covers=[];
for(let g=0;g<2;g++)for(let mask=0;mask<8;mask++){let b=[(mask>>2)&1,(mask>>1)&1,mask&1];if((b[0]+b[1]+b[2]+charge*g)%2===charge)continue;let id=(charge===0||g===0)?implicates.find(z=>JSON.stringify(z.wrong_bits)===JSON.stringify(b)).node_id:facets[9+b.findIndex(x=>x===1)][0];let clause=nodes[id-1].clause;let assignment={4:g,9:b[0],10:b[1],11:b[2]};if(clause.some(l=>assignment[Math.abs(l)]===(l>0?1:0)))throw Error("invalid blocker");covers.push({g,wbits:b,node_id:id})}
const expected=charge===0?20:16;if(nodes.filter(z=>z.kind==="RES").length!==expected||covers.length!==8)throw Error("wrong count");
let modelCount=0;
for(let mask=0;mask<2048;mask++){const bits=Array.from({length:12},(_,i)=>((mask>>(i-1))&1));const satisfied=c=>c.some(l=>bits[Math.abs(l)]===(l>0?1:0));if(nodes.slice(0,17).every(z=>satisfied(z.clause))){modelCount++;if(nodes.some(z=>!satisfied(z.clause)))throw Error("unsound inference")}}
return {charge,source_split:8,gate_facets:9,paid_RES:expected,local_extended_models:modelCount,cover_count:covers.length,implicates,covers,certificate:nodes}
}
const data={schema:'LSPV1-439-native-strict-RES-local-port-v1',results:[make(0),make(1)]};
if(typeof process!=='undefined')process.stdout.write(JSON.stringify(data,null,2)+'\n');
