// Dependency-free Node.js; run node 2026-11-25_M22_02_audit.js
const U=[[-193,-196,-198],[194,196,197],[1,2,197],[-2,-3,-194],[-2,-4,-194],[-3,-5,-6],[-4,-5,-6],[5,7,8],[6,7,8],[-7,-18,-19],[-7,-20,-21],[-8,-18,-19],[-8,-20,-21],[3,9,10],[3,11,12],[4,13,14],[4,15,16],[9,12,15],[10,13,17],[11,16,17],[-9,-13,-16],[-9,-14,-17],[-10,-11,-14],[-10,-12,-16],[-11,-13,-15],[-12,-15,-17],[2,24,32],[18,23,25],[18,28,29],[19,23,25],[19,28,29],[20,22,26],[20,30,31],[21,22,31],[21,26,27],[24,27,30],[-1,-22,-23],[-1,-24,-25],[-22,-25,-32],[-23,-24,-26],[-26,-28,-30],[-27,-28,-31],[-27,-29,-31],[-29,-30,-32],[33,34,196],[-34,-35,-195],[-34,-36,-198],[-35,-37,-38],[-36,-37,-38],[37,39,40],[38,39,40],[-39,-50,-51],[-39,-52,-53],[-40,-50,-51],[-40,-52,-53],[35,41,42],[35,43,44],[36,45,46],[36,47,48],[41,44,47],[42,45,49],[43,48,49],[-41,-45,-48],[-41,-46,-49],[-42,-43,-46],[-42,-44,-48],[-43,-45,-47],[-44,-47,-49],[34,56,64],[50,55,57],[50,60,61],[51,55,57],[51,60,61],[52,54,58],[52,62,63],[53,54,63],[53,58,59],[56,59,62],[-33,-54,-55],[-33,-56,-57],[-54,-57,-64],[-55,-56,-58],[-58,-60,-62],[-59,-60,-63],[-59,-61,-63],[-61,-62,-64],[65,66,193],[-66,-67,-195],[-66,-68,-197],[-67,-69,-70],[-68,-69,-70],[69,71,72],[70,71,72],[-71,-82,-83],[-71,-84,-85],[-72,-82,-83],[-72,-84,-85],[67,73,74],[67,75,76],[68,77,78],[68,79,80],[73,76,79],[74,77,81],[75,80,81],[-73,-77,-80],[-73,-78,-81],[-74,-75,-78],[-74,-76,-80],[-75,-77,-79],[-76,-79,-81],[66,88,96],[82,87,89],[82,92,93],[83,87,89],[83,92,93],[84,86,90],[84,94,95],[85,86,95],[85,90,91],[88,91,94],[-65,-86,-87],[-65,-88,-89],[-86,-89,-96],[-87,-88,-90],[-90,-92,-94],[-91,-92,-95],[-91,-93,-95],[-93,-94,-96],[-97,-98,-197],[98,99,195],[98,100,195],[99,101,102],[100,101,102],[-101,-103,-104],[-102,-103,-104],[103,114,115],[103,116,117],[104,114,115],[104,116,117],[-99,-105,-106],[-99,-107,-108],[-100,-109,-110],[-100,-111,-112],[-105,-108,-111],[-106,-109,-113],[-107,-112,-113],[105,109,112],[105,110,113],[106,107,110],[106,108,112],[107,109,111],[108,111,113],[-98,-120,-128],[-114,-119,-121],[-114,-124,-125],[-115,-119,-121],[-115,-124,-125],[-116,-118,-122],[-116,-126,-127],[-117,-118,-127],[-117,-122,-123],[-120,-123,-126],[97,118,119],[97,120,121],[118,121,128],[119,120,122],[122,124,126],[123,124,127],[123,125,127],[125,126,128],[-129,-130,-196],[130,131,193],[130,132,194],[131,133,134],[132,133,134],[-133,-135,-136],[-134,-135,-136],[135,146,147],[135,148,149],[136,146,147],[136,148,149],[-131,-137,-138],[-131,-139,-140],[-132,-141,-142],[-132,-143,-144],[-137,-140,-143],[-138,-141,-145],[-139,-144,-145],[137,141,144],[137,142,145],[138,139,142],[138,140,144],[139,141,143],[140,143,145],[-130,-152,-160],[-146,-151,-153],[-146,-156,-157],[-147,-151,-153],[-147,-156,-157],[-148,-150,-154],[-148,-158,-159],[-149,-150,-159],[-149,-154,-155],[-152,-155,-158],[129,150,151],[129,152,153],[150,153,160],[151,152,154],[154,156,158],[155,156,159],[155,157,159],[157,158,160],[-161,-162,-193],[162,163,198],[162,164,198],[163,165,166],[164,165,166],[-165,-167,-168],[-166,-167,-168],[167,178,179],[167,180,181],[168,178,179],[168,180,181],[-163,-169,-170],[-163,-171,-172],[-164,-173,-174],[-164,-175,-176],[-169,-172,-175],[-170,-173,-177],[-171,-176,-177],[169,173,176],[169,174,177],[170,171,174],[170,172,176],[171,173,175],[172,175,177],[-162,-184,-192],[-178,-183,-185],[-178,-188,-189],[-179,-183,-185],[-179,-188,-189],[-180,-182,-186],[-180,-190,-191],[-181,-182,-191],[-181,-186,-187],[-184,-187,-190],[161,182,183],[161,184,185],[182,185,192],[183,184,186],[186,188,190],[187,188,191],[187,189,191],[189,190,192],[1,33,65],[-97,-129,-161],[5,37,69],[-101,-133,-165],[6,38,70],[-102,-134,-166],[14,46,78],[-110,-142,-174],[32,64,96],[-128,-160,-192]];
const W="001110010011110001010001110100111110011011000101000101001010100001011010101011000100000111001010110101001110001001101000110001100010100101101110010101011001001100000110111001001101001101101001010101";
function audit(U,W){
 const assert=(b,m)=>{if(!b)throw Error(m)};
 const X=[[2,6,11],[3,8,9],[3,7,9],[4,5,10],[1,5,10],[1,2,7],[4,8,12],[6,11,12],[-1,-10,-12],[-2,-6,-11],[-6,-7,-9],[-4,-5,-10],[-1,-3,-4],[-8,-11,-12],[-5,-7,-9],[-2,-3,-8]];
 const Y=[[1,2,3],[1,4,5],[2,4,6],[3,5,6],[-1,-2,-4],[-1,-3,-6],[-2,-3,-5],[-4,-5,-6]];
 const V=U.map(c=>c.slice());[V[2][2],V[44][2]]=[V[44][2],V[2][2]];
 const lit=(x,l)=>x[Math.abs(l)-1]===Number(l>0),sat=(F,x)=>F.every(c=>c.some(l=>lit(x,l)));
 function compile(F,n){
  const inc=Array.from({length:n},()=>[]),keys=new Set();
  assert(F.length*3===4*n,"m");
  F.forEach((c,i)=>{assert(c.length===3&&new Set(c.map(Math.abs)).size===3&&c.every(l=>l&&Math.abs(l)<=n&&Math.sign(l)===Math.sign(c[0])),"grammar");const k=c.slice().sort((a,b)=>a-b).join();assert(!keys.has(k),"duplicate");keys.add(k);for(const l of c)inc[Math.abs(l)-1].push(i)});
  const P=[];inc.forEach((cs,v)=>{assert(cs.length===4,"occ");for(const s of [0,1]){const e=cs.filter(c=>Number(F[c][0]>0)===s);assert(e.length===2,"sign");P.push({v,s,e})}});
  return {inc,P};
 }
 function up(F){let p=F.map(c=>c.slice());while(true){if(p.some(c=>!c.length))return null;const u=p.find(c=>c.length===1);if(!u)return p;p=p.filter(c=>!c.includes(u[0])).map(c=>c.filter(l=>l!==-u[0]))}}
 function closure(F,guards=[]){let p=up(F.concat(guards.map(l=>[l]))),probes=0,forces=0;while(p&&p.length){let change=false;for(const v of new Set(p.flat().map(Math.abs))){for(const l of [v,-v]){probes++;if(up(p.concat([[l]]))===null){p=up(p.concat([[-l]]));forces++;change=true;break}}if(change)break}if(!change)break}return {probes,forces,conflict:p===null}}
 function normalize(F,n,C,x){
  assert(sat(F,x),"input witness");const r=F.map(c=>Math.abs(c.find(l=>lit(x,l)))-1);let steps=0,scans=0;
  while(true){
   const counts=Array(n).fill(0);r.forEach(v=>counts[v]++);const root=counts.indexOf(0);if(root<0)break;
   const seen=new Set([root]),queue=[root],parent=new Map();let end=null;
   for(let j=0;j<queue.length&&!end;j++){const v=queue[j];for(const c of C.inc[v]){scans++;const w=r[c];if(counts[w]===2){end=[v,c];break}if(!seen.has(w)){seen.add(w);queue.push(w);parent.set(w,[v,c])}}}
   assert(end,"augmentation missing");let [v,c]=end;
   while(true){r[c]=v;if(v===root)break;[v,c]=parent.get(v)}
   steps++;
   assert(steps<=n,"progress");
   const rs=Array.from({length:n},()=>[]);r.forEach((v,i)=>rs[v].push(i));
   assert(rs.every(cs=>cs.length<=2&&(cs.length!==2||Math.sign(F[cs[0]][0])===Math.sign(F[cs[1]][0]))),"representative invariants");
  }
  const D=C.P.filter(p=>p.e.every(i=>r[i]===p.v));assert(D.length===n/3,"exact double count");return {D,steps,scans}
 }
 function track(F,n,C,D){
  const usedV=new Set(),usedC=new Set();for(const p of D){assert(!usedV.has(p.v)&&p.e.every(c=>!usedC.has(c)),"packing");usedV.add(p.v);p.e.forEach(c=>usedC.add(c))}
  const rest=F.map((_,i)=>i).filter(i=>!usedC.has(i)),match=Array(n).fill(-1);let scans=0;
  function dfs(c,seen){for(const l of F[c]){const v=Math.abs(l)-1;scans++;if(usedV.has(v)||seen.has(v))continue;seen.add(v);if(match[v]<0||dfs(match[v],seen)){match[v]=c;return true}}return false}
  for(const c of rest){if(!dfs(c,new Set())){
   const S=new Set([c]),Q=[c],B=new Set();for(let j=0;j<Q.length;j++)for(const l of F[Q[j]]){const v=Math.abs(l)-1;if(usedV.has(v)||B.has(v))continue;B.add(v);assert(match[v]>=0,"augment path");if(!S.has(match[v])){S.add(match[v]);Q.push(match[v])}}
   assert(B.size<S.size,"Hall");const gamma=new Set([...S].flatMap(i=>F[i].map(l=>Math.abs(l)-1)));
   const lhs=D.reduce((a,p)=>a+p.e.filter(c=>S.has(c)).length-Number(gamma.has(p.v)),0);
   assert(lhs<S.size-gamma.size,"cut");return {ok:false,S:[...S],B:[...B],lhs,rhs:S.size-gamma.size,scans}
  }}
  const x=Array(n).fill(-1);for(const p of D)x[p.v]=p.s;match.forEach((c,v)=>{if(c>=0)x[v]=Number(F[c][0]>0)});
  assert(x.every(v=>v>=0)&&sat(F,x),"lift");return {ok:true,x,scans}
 }
 function direct(F,n,D){const U=new Set(D.map(p=>p.v)),C=new Set(D.flatMap(p=>p.e)),R=F.map((_,i)=>i).filter(i=>!C.has(i));function rec(i){if(i===R.length)return true;for(const l of F[R[i]]){const v=Math.abs(l)-1;if(U.has(v))continue;U.add(v);if(rec(i+1))return true;U.delete(v)}return false}return rec(0)}
 function greedy(C,n){const D=[],v=new Set(),c=new Set();for(const p of C.P){if(v.has(p.v)||p.e.some(i=>c.has(i)))continue;D.push(p);v.add(p.v);p.e.forEach(i=>c.add(i));if(D.length===n/3)break}assert(D.length===n/3,"greedy bound");return D}
 function small(F,n){const C=compile(F,n),models=[];let normalized=0,augments=0,normalScans=0,tracks=0,yes=0,no=0,scans=0,guardSATfailure=0,example=null,guardProbes=0,guardForces=0;const root=closure(F);
  for(let i=0;i<2**n;i++){const x=Array.from({length:n},(_,j)=>(i>>j)&1);if(!sat(F,x))continue;models.push(x);const a=normalize(F,n,C,x);assert(track(F,n,C,a.D).ok,"normalization track");normalized++;augments+=a.steps;normalScans+=a.scans}
  const D=[],vs=new Set(),cs=new Set();
  function rec(start){if(D.length===n/3){const r=track(F,n,C,D);assert(r.ok===direct(F,n,D),"independent cover mismatch");tracks++;scans+=r.scans;if(r.ok)yes++;else{no++;const witness=models.find(x=>D.every(p=>x[p.v]===p.s));if(witness){guardSATfailure++;if(!example)example={D:D.slice(),hall:r,guardWitness:witness}}}const cl=closure(F,D.map(p=>(p.s?1:-1)*(p.v+1)));guardProbes+=cl.probes;guardForces+=cl.forces;assert(!cl.conflict||!r.ok,"closure rejects feasible track");return}
   for(let j=start;j<C.P.length;j++){const p=C.P[j];if(vs.has(p.v)||p.e.some(i=>cs.has(i)))continue;D.push(p);vs.add(p.v);p.e.forEach(i=>cs.add(i));rec(j+1);D.pop();vs.delete(p.v);p.e.forEach(i=>cs.delete(i))}
  }rec(0);return {models:models.length,normalized,augments,normalScans,tracks,yes,no,scans,guardSATfailure,example,root,guardProbes,guardForces,greedy:track(F,n,C,greedy(C,n))}
 }
 const CU=compile(U,198),CV=compile(V,198);const x=Array.from(W,Number);assert(sat(V,x),"V known witness");const z=normalize(V,198,CV,x);const vr=track(V,198,CV,z.D);assert(vr.ok,"V lift");
 let nodes=0;function dpll(F){nodes++;const R=up(F);if(!R)return false;if(!R.length)return true;const c=R.reduce((a,b)=>a.length<=b.length?a:b);return dpll(R.concat([[c[0]]]))||dpll(R.concat([[-c[0]]]))}
 const modules=Array.from({length:6},(_,i)=>U.slice(2,254).filter(c=>c.some(l=>Math.abs(l)>=1+32*i&&Math.abs(l)<=32+32*i)));modules.forEach((M,i)=>assert(M.length===42&&M.every(c=>c.every(l=>Math.abs(l)>=193||(Math.abs(l)>=1+32*i&&Math.abs(l)<=32+32*i))),"privacy"));
 let directNo=0,moduleNo=0,calls=0;for(let b=0;b<64;b++){const value=l=>Number(!!(b&(1<<(Math.abs(l)-193))))===Number(l>0);if(U.slice(0,2).some(c=>!c.some(value))){directNo++;continue}let found=false;for(const M of modules){calls++;const R=M.filter(c=>!c.some(l=>Math.abs(l)>=193&&value(l))).map(c=>c.filter(l=>Math.abs(l)<193));if(!dpll(R)){found=true;break}}assert(found,"U not refuted");moduleNo++}
 const ug=track(U,198,CU,greedy(CU,198));assert(!ug.ok,"U candidate");
 return {Y6:small(Y,6),X12:small(X,12),U198:{root:closure(U),greedy:ug,directNo,moduleNo,calls,nodes},V198:{root:closure(V),normalizationSteps:z.steps,normalizationScans:z.scans,trackScans:vr.scans,witness:vr.x,guardClosure:closure(V,z.D.map(p=>(p.s?1:-1)*(p.v+1)))},fractional:{uniformNumerator:1,denominator:6}};
}
console.log(JSON.stringify(audit(U,W),null,2));
