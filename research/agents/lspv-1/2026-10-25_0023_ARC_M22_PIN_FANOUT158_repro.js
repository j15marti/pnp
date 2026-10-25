"use strict";
/* ARC-M22-PIN-FANOUT158, deterministic standalone verifier.
   Run: node research/agents/lspv-1/2026-10-25_0023_ARC_M22_PIN_FANOUT158_repro.js
   The UNSAT label of U198 is imported, not computationally proved. */
const U=[[-193,-196,-198],[194,196,197],[1,2,197],[-2,-3,-194],[-2,-4,-194],[-3,-5,-6],[-4,-5,-6],[5,7,8],[6,7,8],[-7,-18,-19],[-7,-20,-21],[-8,-18,-19],[-8,-20,-21],[3,9,10],[3,11,12],[4,13,14],[4,15,16],[9,12,15],[10,13,17],[11,16,17],[-9,-13,-16],[-9,-14,-17],[-10,-11,-14],[-10,-12,-16],[-11,-13,-15],[-12,-15,-17],[2,24,32],[18,23,25],[18,28,29],[19,23,25],[19,28,29],[20,22,26],[20,30,31],[21,22,31],[21,26,27],[24,27,30],[-1,-22,-23],[-1,-24,-25],[-22,-25,-32],[-23,-24,-26],[-26,-28,-30],[-27,-28,-31],[-27,-29,-31],[-29,-30,-32],[33,34,196],[-34,-35,-195],[-34,-36,-198],[-35,-37,-38],[-36,-37,-38],[37,39,40],[38,39,40],[-39,-50,-51],[-39,-52,-53],[-40,-50,-51],[-40,-52,-53],[35,41,42],[35,43,44],[36,45,46],[36,47,48],[41,44,47],[42,45,49],[43,48,49],[-41,-45,-48],[-41,-46,-49],[-42,-43,-46],[-42,-44,-48],[-43,-45,-47],[-44,-47,-49],[34,56,64],[50,55,57],[50,60,61],[51,55,57],[51,60,61],[52,54,58],[52,62,63],[53,54,63],[53,58,59],[56,59,62],[-33,-54,-55],[-33,-56,-57],[-54,-57,-64],[-55,-56,-58],[-58,-60,-62],[-59,-60,-63],[-59,-61,-63],[-61,-62,-64],[65,66,193],[-66,-67,-195],[-66,-68,-197],[-67,-69,-70],[-68,-69,-70],[69,71,72],[70,71,72],[-71,-82,-83],[-71,-84,-85],[-72,-82,-83],[-72,-84,-85],[67,73,74],[67,75,76],[68,77,78],[68,79,80],[73,76,79],[74,77,81],[75,80,81],[-73,-77,-80],[-73,-78,-81],[-74,-75,-78],[-74,-76,-80],[-75,-77,-79],[-76,-79,-81],[66,88,96],[82,87,89],[82,92,93],[83,87,89],[83,92,93],[84,86,90],[84,94,95],[85,86,95],[85,90,91],[88,91,94],[-65,-86,-87],[-65,-88,-89],[-86,-89,-96],[-87,-88,-90],[-90,-92,-94],[-91,-92,-95],[-91,-93,-95],[-93,-94,-96],[-97,-98,-197],[98,99,195],[98,100,195],[99,101,102],[100,101,102],[-101,-103,-104],[-102,-103,-104],[103,114,115],[103,116,117],[104,114,115],[104,116,117],[-99,-105,-106],[-99,-107,-108],[-100,-109,-110],[-100,-111,-112],[-105,-108,-111],[-106,-109,-113],[-107,-112,-113],[105,109,112],[105,110,113],[106,107,110],[106,108,112],[107,109,111],[108,111,113],[-98,-120,-128],[-114,-119,-121],[-114,-124,-125],[-115,-119,-121],[-115,-124,-125],[-116,-118,-122],[-116,-126,-127],[-117,-118,-127],[-117,-122,-123],[-120,-123,-126],[97,118,119],[97,120,121],[118,121,128],[119,120,122],[122,124,126],[123,124,127],[123,125,127],[125,126,128],[-129,-130,-196],[130,131,193],[130,132,194],[131,133,134],[132,133,134],[-133,-135,-136],[-134,-135,-136],[135,146,147],[135,148,149],[136,146,147],[136,148,149],[-131,-137,-138],[-131,-139,-140],[-132,-141,-142],[-132,-143,-144],[-137,-140,-143],[-138,-141,-145],[-139,-144,-145],[137,141,144],[137,142,145],[138,139,142],[138,140,144],[139,141,143],[140,143,145],[-130,-152,-160],[-146,-151,-153],[-146,-156,-157],[-147,-151,-153],[-147,-156,-157],[-148,-150,-154],[-148,-158,-159],[-149,-150,-159],[-149,-154,-155],[-152,-155,-158],[129,150,151],[129,152,153],[150,153,160],[151,152,154],[154,156,158],[155,156,159],[155,157,159],[157,158,160],[-161,-162,-193],[162,163,198],[162,164,198],[163,165,166],[164,165,166],[-165,-167,-168],[-166,-167,-168],[167,178,179],[167,180,181],[168,178,179],[168,180,181],[-163,-169,-170],[-163,-171,-172],[-164,-173,-174],[-164,-175,-176],[-169,-172,-175],[-170,-173,-177],[-171,-176,-177],[169,173,176],[169,174,177],[170,171,174],[170,172,176],[171,173,175],[172,175,177],[-162,-184,-192],[-178,-183,-185],[-178,-188,-189],[-179,-183,-185],[-179,-188,-189],[-180,-182,-186],[-180,-190,-191],[-181,-182,-191],[-181,-186,-187],[-184,-187,-190],[161,182,183],[161,184,185],[182,185,192],[183,184,186],[186,188,190],[187,188,191],[187,189,191],[189,190,192],[1,33,65],[-97,-129,-161],[5,37,69],[-101,-133,-165],[6,38,70],[-102,-134,-166],[14,46,78],[-110,-142,-174],[32,64,96],[-128,-160,-192]];
function Y(p=false){const P=[[1,2,3],[1,4,5],[2,4,6],[3,5,6]],M=p?P:[[1,2,4],[1,3,6],[2,3,5],[4,5,6]];return [...P,...M.map(c=>c.map(x=>-x))]}
function multiply(F,n){const k=Math.max(...F.flat().map(Math.abs));return Array.from({length:n},(_,j)=>F.map(c=>c.map(x=>Math.sign(x)*(Math.abs(x)+j*k)))).flat()}
function grammar(F,isM22){const k=Math.max(0,...F.flat().map(Math.abs)),pos=Array(k+1).fill(0),neg=pos.slice(),seen=new Set();for(const c of F){if(isM22&&(c.length!==3||new Set(c.map(Math.abs)).size!==3||!(c.every(x=>x>0)||c.every(x=>x<0))))throw Error("pure M22");let key=c.slice().sort((a,b)=>a-b).join(",");if(seen.has(key))throw Error("duplicate");seen.add(key);for(const x of c)(x>0?pos:neg)[Math.abs(x)]++}const delta=Math.max(0,...pos.map((x,i)=>x+neg[i]));if(isM22){if(3*F.length!==4*k)throw Error("global quota");for(let v=1;v<=k;v++)if(pos[v]!==2||neg[v]!==2)throw Error("signed quota")};return{k,m:F.length,delta}}
function pin(F,a){return F.map(c=>c.some(x=>a[Math.abs(x)]!==undefined&&a[Math.abs(x)]===(x>0))?null:c.filter(x=>a[Math.abs(x)]===undefined)).filter(c=>c!==null)}
function satSmall(F){const k=Math.max(0,...F.flat().map(Math.abs));if(k>16)return null;for(let mask=0;mask<2**k;mask++)if(F.every(c=>c.some(x=>!!(mask&(1<<(Math.abs(x)-1)))===(x>0))))return true;return false}
function bits(F){const k=new Set(F.flat().map(Math.abs)).size,h=Math.max(1,Math.ceil(Math.log2(Math.max(k,F.length)+1)));return 3*h+1+F.reduce((z,c)=>z+2+c.length*(h+1),0)}
function intact(F,p){const s=new Set(p);return F.filter(c=>c.every(x=>!s.has(Math.abs(x)))).length}
function runAudit(){
let assertions=0,rows=[];
const cases=[
["Y-SAT",Y(),true,true],["Y-paired-SAT",Y(true),true,true],
["Yx2-SAT",multiply(Y(),2),true,null],["Yx8-SAT",multiply(Y(),8),true,null],
["Yx16-SAT",multiply(Y(),16),true,null],["Yx64-SAT",multiply(Y(),64),true,null],
["Yx128-SAT",multiply(Y(),128),true,null],["U198-UNSAT-imported",U,true,null],
["U198-plus-Y-UNSAT-imported",U.concat(Y().map(c=>c.map(x=>Math.sign(x)*(Math.abs(x)+198)))),true,null],
["ordinary-UNSAT8",Array.from({length:8},(_,i)=>[1,2,3].map((v,j)=>i&(1<<j)?-v:v)),false,false],
["Horn-UNSAT",[[-1,2],[-2,3],[1],[-3]],false,false],
["affine-SAT",[[1,2],[-1,-2]],false,true]];
for(const [name,F,isM22,label]of cases){
 const z=grammar(F,isM22),N=bits(F);
 if(label!==null){if(satSmall(F)!==label)throw Error("incorrect label "+name);assertions++}
 for(const b of [0,1,2,3,Math.min(z.k,5),Math.min(z.k,Math.ceil(Math.log2(N)))]){
  const p=Array.from({length:Math.min(z.k,b)},(_,i)=>i+1);
  if(intact(F,p)<z.m-z.delta*p.length)throw Error("incidence floor "+name);assertions++}
 let child=[],grand=[],minIntact=Infinity;
 if(z.k>=2)for(const x of [false,true]){const C=pin(F,{1:x});child.push(bits(C));
  for(const y of [false,true]){const D=pin(C,{2:y}),E=pin(F,{1:x,2:y});
   if(JSON.stringify(D)!==JSON.stringify(E))throw Error("two-level semantics "+name);
   grand.push(bits(D));const untouched=intact(F,[1,2]);if(D.length<untouched||untouched<z.m-2*z.delta)throw Error("untouched floor two level "+name);
   minIntact=Math.min(minIntact,untouched);assertions+=2}
  assertions++}
 if(z.k<=6&&z.k>=2){let joined=false;for(let a=0;a<4;a++)joined ||= satSmall(pin(pin(F,{1:!!(a&1)}),{2:!!(a&2)}));if(joined!==satSmall(F))throw Error("SAT/UNSAT join mismatch");assertions++}
 rows.push({name,...z,M22:isM22,source_bits:N,label_verified:label===null?"not brute-forced":label,two_level_child_bits:child,two_level_grandchild_bits:grand,two_pin_untouched:minIntact,required_floor:z.m-2*z.delta});
}
return{run:"ARC-M22-PIN-FANOUT158",status:"PROVED/EXACT in a restricted raw-pin-and-copy model; COMPUTATIONAL finite audit",archive_U_blob:"8e8511fc574650625fedbf30469ef9e714d2a6c3",method:"12 deterministic sources, two real restriction levels, small SAT/UNSAT exhaustive controls",seed:null,assertions,failures:0,cases:rows,limitations:["U198 UNSAT imported from Doecker, not exhaustively proved here","No propagation, caching, learned clauses, symbolic decision or early exit","No physical FLMV bit-work/peak-space measurement","Neither ARC-EDGE-90 nor P versus NP proved"]};
}
if(typeof module!=="undefined"&&typeof require!=="undefined"&&require.main===module)console.log(JSON.stringify(runAudit(),null,2));
