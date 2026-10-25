// Exact executable independent JavaScript audit; Node.js 18+.
// U_198 signed literal source from Döcker Appendix C, Git blob f9dda41a810ad8e02bd553f2711a26a4050861f9.
// Base UNSAT imported, no complete 2^198 exhaustive check.
const U=[[-193,-196,-198],[194,196,197],[1,2,197],[-2,-3,-194],[-2,-4,-194],[-3,-5,-6],[-4,-5,-6],[5,7,8],[6,7,8],[-7,-18,-19],[-7,-20,-21],[-8,-18,-19],[-8,-20,-21],[3,9,10],[3,11,12],[4,13,14],[4,15,16],[9,12,15],[10,13,17],[11,16,17],[-9,-13,-16],[-9,-14,-17],[-10,-11,-14],[-10,-12,-16],[-11,-13,-15],[-12,-15,-17],[2,24,32],[18,23,25],[18,28,29],[19,23,25],[19,28,29],[20,22,26],[20,30,31],[21,22,31],[21,26,27],[24,27,30],[-1,-22,-23],[-1,-24,-25],[-22,-25,-32],[-23,-24,-26],[-26,-28,-30],[-27,-28,-31],[-27,-29,-31],[-29,-30,-32],[33,34,196],[-34,-35,-195],[-34,-36,-198],[-35,-37,-38],[-36,-37,-38],[37,39,40],[38,39,40],[-39,-50,-51],[-39,-52,-53],[-40,-50,-51],[-40,-52,-53],[35,41,42],[35,43,44],[36,45,46],[36,47,48],[41,44,47],[42,45,49],[43,48,49],[-41,-45,-48],[-41,-46,-49],[-42,-43,-46],[-42,-44,-48],[-43,-45,-47],[-44,-47,-49],[34,56,64],[50,55,57],[50,60,61],[51,55,57],[51,60,61],[52,54,58],[52,62,63],[53,54,63],[53,58,59],[56,59,62],[-33,-54,-55],[-33,-56,-57],[-54,-57,-64],[-55,-56,-58],[-58,-60,-62],[-59,-60,-63],[-59,-61,-63],[-61,-62,-64],[65,66,193],[-66,-67,-195],[-66,-68,-197],[-67,-69,-70],[-68,-69,-70],[69,71,72],[70,71,72],[-71,-82,-83],[-71,-84,-85],[-72,-82,-83],[-72,-84,-85],[67,73,74],[67,75,76],[68,77,78],[68,79,80],[73,76,79],[74,77,81],[75,80,81],[-73,-77,-80],[-73,-78,-81],[-74,-75,-78],[-74,-76,-80],[-75,-77,-79],[-76,-79,-81],[66,88,96],[82,87,89],[82,92,93],[83,87,89],[83,92,93],[84,86,90],[84,94,95],[85,86,95],[85,90,91],[88,91,94],[-65,-86,-87],[-65,-88,-89],[-86,-89,-96],[-87,-88,-90],[-90,-92,-94],[-91,-92,-95],[-91,-93,-95],[-93,-94,-96],[-97,-98,-197],[98,99,195],[98,100,195],[99,101,102],[100,101,102],[-101,-103,-104],[-102,-103,-104],[103,114,115],[103,116,117],[104,114,115],[104,116,117],[-99,-105,-106],[-99,-107,-108],[-100,-109,-110],[-100,-111,-112],[-105,-108,-111],[-106,-109,-113],[-107,-112,-113],[105,109,112],[105,110,113],[106,107,110],[106,108,112],[107,109,111],[108,111,113],[-98,-120,-128],[-114,-119,-121],[-114,-124,-125],[-115,-119,-121],[-115,-124,-125],[-116,-118,-122],[-116,-126,-127],[-117,-118,-127],[-117,-122,-123],[-120,-123,-126],[97,118,119],[97,120,121],[118,121,128],[119,120,122],[122,124,126],[123,124,127],[123,125,127],[125,126,128],[-129,-130,-196],[130,131,193],[130,132,194],[131,133,134],[132,133,134],[-133,-135,-136],[-134,-135,-136],[135,146,147],[135,148,149],[136,146,147],[136,148,149],[-131,-137,-138],[-131,-139,-140],[-132,-141,-142],[-132,-143,-144],[-137,-140,-143],[-138,-141,-145],[-139,-144,-145],[137,141,144],[137,142,145],[138,139,142],[138,140,144],[139,141,143],[140,143,145],[-130,-152,-160],[-146,-151,-153],[-146,-156,-157],[-147,-151,-153],[-147,-156,-157],[-148,-150,-154],[-148,-158,-159],[-149,-150,-159],[-149,-154,-155],[-152,-155,-158],[129,150,151],[129,152,153],[150,153,160],[151,152,154],[154,156,158],[155,156,159],[155,157,159],[157,158,160],[-161,-162,-193],[162,163,198],[162,164,198],[163,165,166],[164,165,166],[-165,-167,-168],[-166,-167,-168],[167,178,179],[167,180,181],[168,178,179],[168,180,181],[-163,-169,-170],[-163,-171,-172],[-164,-173,-174],[-164,-175,-176],[-169,-172,-175],[-170,-173,-177],[-171,-176,-177],[169,173,176],[169,174,177],[170,171,174],[170,172,176],[171,173,175],[172,175,177],[-162,-184,-192],[-178,-183,-185],[-178,-188,-189],[-179,-183,-185],[-179,-188,-189],[-180,-182,-186],[-180,-190,-191],[-181,-182,-191],[-181,-186,-187],[-184,-187,-190],[161,182,183],[161,184,185],[182,185,192],[183,184,186],[186,188,190],[187,188,191],[187,189,191],[189,190,192],[1,33,65],[-97,-129,-161],[5,37,69],[-101,-133,-165],[6,38,70],[-102,-134,-166],[14,46,78],[-110,-142,-174],[32,64,96],[-128,-160,-192]];
function runAudit(U){
let asserts=0;
const check=(x,why)=>{asserts++;if(!x)throw Error(why)};
const support=c=>c.map(Math.abs).sort((a,b)=>a-b).join(",");
const checkM22=F=>{
let P=new Map(),Q=new Map(),ps=new Set(),ns=new Set(),seen=new Set();
for(const c of F){
check(c.length===3&&new Set(c.map(Math.abs)).size===3,"proper");
check(c.every(z=>z>0)||c.every(z=>z<0),"pure polarity");
const key=c.slice().sort((a,b)=>a-b).join(",");check(!seen.has(key),"duplicate");seen.add(key);
for(const z of c){const M=z>0?P:Q, k=Math.abs(z);M.set(k,(M.get(k)||0)+1)}
(z=>z>0?ps:ns)(c[0]).add(support(c));
}
check(P.size===Q.size,"signed name sizes"); for(const [v,n]of P){check(n===2&&Q.get(v)===2,"signed quotas")}
check(3*F.length===4*P.size,"regular identity");
let q=0;for(const s of ps){if(!ns.has(s))q++}
return {k:P.size,m:F.length,defect:q,fullyPaired:q===0};
};
const connected=F=>{
const vertices=new Set(),adj=new Map();
for(const c of F){const vs=c.map(Math.abs);for(const v of vs){vertices.add(v);if(!adj.has(v))adj.set(v,new Set());for(const w of vs){if(v!==w)adj.get(v).add(w)}}}
const start=vertices.values().next().value;if(start==null)return false;
const got=new Set([start]),q=[start];for(let i=0;i<q.length;i++){for(const v of adj.get(q[i]))if(!got.has(v)){got.add(v);q.push(v)}}return got.size===vertices.size
};
const ucycle=p=>{
let F=[];for(let i=0;i<p;i++){let off=198*i;for(let j=0;j<U.length;j++){
let c=U[j].map(z=>(z>0?1:-1)*(Math.abs(z)+off));
if(j===1)c[0]=194+198*((i+1)%p);F.push(c);
}}return F
};
const zcycle=h=>{let F=[];for(let i=0;i<h;i++){const [a,b,c,d,e,f]=[1,2,3,4,5,6].map(z=>z+6*i),next=1+6*((i+1)%h);F.push([next,b,c],[a,d,e],[b,d,f],[c,e,f],[-a,-b,-d],[-a,-c,-f],[-b,-c,-e],[-d,-e,-f])}return F};
const sat=(F,a)=>F.every(c=>c.some(z=>(a[Math.abs(z)-1]===1)===(z>0)));
const bits=k=>Math.ceil(Math.log2(k+1));
const densebits=(k,m)=>3*bits(k)+2+3*m*(bits(k)+1);
const witness="010110111001100010001111000101011110010101001111010001001011010000110010000100001001010111010000111010101010001101001010010010110001100011111001010101011011001110000100000001110110111000101100100001";
const w=witness.split("").map(Number);
const base=checkM22(U);
check(base.k===198&&base.m===264&&base.defect===132&&!base.fullyPaired,"U grammar/defect");
check(connected(U),"U connected");
check(U[1].join(",")==="194,196,197","selected original positive clause");
check(w.length===198,"198bit witness");
check(sat(U.filter((_,j)=>j!==1),w),"source-deletion witness true");
check(w[193]===0&&w[195]===0&&w[196]===0,"source-clause witness false");
const uMinusPort=U.map((c,j)=>j===1?[196,197]:c);
check(connected(uMinusPort),"local copy stays connected with outgoing occurrence absent");
let cases=[];
for(const p of [2,3,4,8,16,32]){
const F=ucycle(p),a=checkM22(F),Z=zcycle(33*p),b=checkM22(Z);
check(connected(F)&&connected(Z),"two-label connected");
check(!a.fullyPaired&&!b.fullyPaired&&a.defect===132*p&&b.defect===132*p,"nonpaired defect");
check(a.k===198*p&&a.m===264*p&&a.k===b.k&&a.m===b.m,"matched size");
let wz=[];for(let j=0;j<33*p;j++)wz.push(1,1,1,0,0,0);
check(sat(Z,wz),"source-readable SAT witness");
const x0=194,x1=194+198,x2=194+198*(2%p);
const L1=F.slice(264).concat([[-x0],[x1]]);
const L2=F.slice(528).concat([[-x0],[x1],[-x1],[x2]]);
check(L1.length===264*(p-1)+2&&L2.length===264*(p-2)+4,"two-level sizes");
check(L2.some(c=>c.length===1&&c[0]===x1)&&L2.some(c=>c.length===1&&c[0]===-x1),"second level explicit contradiction");
cases.push({p,k:a.k,m:a.m,defect:a.defect,source_bits:densebits(a.k,a.m),level1_clauses:L1.length,level2_before_unit_simplification:L2.length,after_unit_simplification_clauses:1,sat_matched_public_witness:true,unsat_proof:"published U plus port-permutation lemma"});
}
const Y=zcycle(1),yc=checkM22(Y);check(yc.k===6&&!yc.fullyPaired,"Y eligible");
let models=0;for(let mask=0;mask<64;mask++){const a=Array.from({length:6},(_,i)=>(mask>>i)&1);if(sat(Y,a))models++}check(models===20,"Y models");
const H=Y.slice(0,4).concat(Y.slice(0,4).map(c=>c.map(z=>-z)));
check(checkM22(H).fullyPaired,"H paired control");
let malformed=Y.map(c=>c.slice());malformed[0][1]=-malformed[0][1];
let rejected=false;try{checkM22(malformed)}catch(e){rejected=true}check(rejected,"malformed mixed rejected");
return {run:"M22-CYCLIC-UNSAT-PORT109",source_sha:"f9dda41a810ad8e02bd553f2711a26a4050861f9",status:"PROVED/EXACT restricted, COMPUTATIONAL audit; U UNSAT IMPORT",fixture:{k:198,m:264,selected_clause:[194,196,197],source_deleted_clause_SAT_witness:witness},cases,Y_models:models,assertion_checks:asserts,failures:0,logical_scope:"two-level existential exact interface from imported U UNSAT and locally checked deletion witness",limitations:["No all-input ARC contraction","No direct post-acquisition lower bound","Ordinary unit-CNF descendants leave C_star","No actual FLMV machine bit-time/space trace","U original UNSAT imported from publication/archived proof"]}
}
console.log(JSON.stringify(runAudit(U),null,2));
