// Run with Node.js, no packages. Fixtures are pinned in source. BigInt exact.
const U=[[-193,-196,-198],[194,196,197],[1,2,197],[-2,-3,-194],[-2,-4,-194],[-3,-5,-6],[-4,-5,-6],[5,7,8],[6,7,8],[-7,-18,-19],[-7,-20,-21],[-8,-18,-19],[-8,-20,-21],[3,9,10],[3,11,12],[4,13,14],[4,15,16],[9,12,15],[10,13,17],[11,16,17],[-9,-13,-16],[-9,-14,-17],[-10,-11,-14],[-10,-12,-16],[-11,-13,-15],[-12,-15,-17],[2,24,32],[18,23,25],[18,28,29],[19,23,25],[19,28,29],[20,22,26],[20,30,31],[21,22,31],[21,26,27],[24,27,30],[-1,-22,-23],[-1,-24,-25],[-22,-25,-32],[-23,-24,-26],[-26,-28,-30],[-27,-28,-31],[-27,-29,-31],[-29,-30,-32],[33,34,196],[-34,-35,-195],[-34,-36,-198],[-35,-37,-38],[-36,-37,-38],[37,39,40],[38,39,40],[-39,-50,-51],[-39,-52,-53],[-40,-50,-51],[-40,-52,-53],[35,41,42],[35,43,44],[36,45,46],[36,47,48],[41,44,47],[42,45,49],[43,48,49],[-41,-45,-48],[-41,-46,-49],[-42,-43,-46],[-42,-44,-48],[-43,-45,-47],[-44,-47,-49],[34,56,64],[50,55,57],[50,60,61],[51,55,57],[51,60,61],[52,54,58],[52,62,63],[53,54,63],[53,58,59],[56,59,62],[-33,-54,-55],[-33,-56,-57],[-54,-57,-64],[-55,-56,-58],[-58,-60,-62],[-59,-60,-63],[-59,-61,-63],[-61,-62,-64],[65,66,193],[-66,-67,-195],[-66,-68,-197],[-67,-69,-70],[-68,-69,-70],[69,71,72],[70,71,72],[-71,-82,-83],[-71,-84,-85],[-72,-82,-83],[-72,-84,-85],[67,73,74],[67,75,76],[68,77,78],[68,79,80],[73,76,79],[74,77,81],[75,80,81],[-73,-77,-80],[-73,-78,-81],[-74,-75,-78],[-74,-76,-80],[-75,-77,-79],[-76,-79,-81],[66,88,96],[82,87,89],[82,92,93],[83,87,89],[83,92,93],[84,86,90],[84,94,95],[85,86,95],[85,90,91],[88,91,94],[-65,-86,-87],[-65,-88,-89],[-86,-89,-96],[-87,-88,-90],[-90,-92,-94],[-91,-92,-95],[-91,-93,-95],[-93,-94,-96],[-97,-98,-197],[98,99,195],[98,100,195],[99,101,102],[100,101,102],[-101,-103,-104],[-102,-103,-104],[103,114,115],[103,116,117],[104,114,115],[104,116,117],[-99,-105,-106],[-99,-107,-108],[-100,-109,-110],[-100,-111,-112],[-105,-108,-111],[-106,-109,-113],[-107,-112,-113],[105,109,112],[105,110,113],[106,107,110],[106,108,112],[107,109,111],[108,111,113],[-98,-120,-128],[-114,-119,-121],[-114,-124,-125],[-115,-119,-121],[-115,-124,-125],[-116,-118,-122],[-116,-126,-127],[-117,-118,-127],[-117,-122,-123],[-120,-123,-126],[97,118,119],[97,120,121],[118,121,128],[119,120,122],[122,124,126],[123,124,127],[123,125,127],[125,126,128],[-129,-130,-196],[130,131,193],[130,132,194],[131,133,134],[132,133,134],[-133,-135,-136],[-134,-135,-136],[135,146,147],[135,148,149],[136,146,147],[136,148,149],[-131,-137,-138],[-131,-139,-140],[-132,-141,-142],[-132,-143,-144],[-137,-140,-143],[-138,-141,-145],[-139,-144,-145],[137,141,144],[137,142,145],[138,139,142],[138,140,144],[139,141,143],[140,143,145],[-130,-152,-160],[-146,-151,-153],[-146,-156,-157],[-147,-151,-153],[-147,-156,-157],[-148,-150,-154],[-148,-158,-159],[-149,-150,-159],[-149,-154,-155],[-152,-155,-158],[129,150,151],[129,152,153],[150,153,160],[151,152,154],[154,156,158],[155,156,159],[155,157,159],[157,158,160],[-161,-162,-193],[162,163,198],[162,164,198],[163,165,166],[164,165,166],[-165,-167,-168],[-166,-167,-168],[167,178,179],[167,180,181],[168,178,179],[168,180,181],[-163,-169,-170],[-163,-171,-172],[-164,-173,-174],[-164,-175,-176],[-169,-172,-175],[-170,-173,-177],[-171,-176,-177],[169,173,176],[169,174,177],[170,171,174],[170,172,176],[171,173,175],[172,175,177],[-162,-184,-192],[-178,-183,-185],[-178,-188,-189],[-179,-183,-185],[-179,-188,-189],[-180,-182,-186],[-180,-190,-191],[-181,-182,-191],[-181,-186,-187],[-184,-187,-190],[161,182,183],[161,184,185],[182,185,192],[183,184,186],[186,188,190],[187,188,191],[187,189,191],[189,190,192],[1,33,65],[-97,-129,-161],[5,37,69],[-101,-133,-165],[6,38,70],[-102,-134,-166],[14,46,78],[-110,-142,-174],[32,64,96],[-128,-160,-192]];
const W="001110010011110001010001110100111110011011000101000101001010100001011010101011000100000111001010110101001110001001101000110001100010100101101110010101011001001100000110111001001101001101101001010101";
function audit(U,W){
 const assert=(b,m)=>{if(!b)throw Error(m)};
 const bit=i=>1n<<BigInt(i);
 const top=x=>x.toString(2).length-1;
 const parity=x=>{let v=0;while(x){x&=x-1n;v^=1}return v};
 const mask=c=>c.reduce((a,v)=>a^bit(Math.abs(v)-1),0n);
 const lit=(x,l)=>Number(!!(x&bit(Math.abs(l)-1)))^Number(l<0);
 const sat=(F,x)=>F.every(c=>c.some(l=>lit(x,l)));
 const sig=(F,x)=>F.reduce((s,c,i)=>s|(BigInt(1^c.reduce((a,l)=>a^lit(x,l),0))<<BigInt(i)),0n);
 const weight=x=>{let w=0;while(x){x&=x-1n;w++}return w};
 function validate(F,n){const cnt=Array.from({length:n},()=>[0,0]),keys=new Set();assert(F.length*3===4*n,"count");for(const c of F){assert(c.length===3&&new Set(c.map(Math.abs)).size===3&&c.every(l=>Math.sign(l)===Math.sign(c[0])&&Math.abs(l)<=n&&l!==0),"grammar");let k=c.slice().sort((a,b)=>a-b).join();assert(!keys.has(k),"duplicate");keys.add(k);for(const l of c)cnt[Math.abs(l)-1][Number(l>0)]++}assert(cnt.every(c=>c[0]===2&&c[1]===2),"occurrences")}
 function affine(rows,n){let piv=new Map();for(let [a,b] of rows){while(a&&piv.has(top(a))){const q=piv.get(top(a));a^=q[0];b^=q[1]}if(!a){if(b)return null}else piv.set(top(a),[a,b])}const ex=[];let d=0;for(let i=0;i<n;i++){if(!piv.has(i)){ex.push([bit(d++),0]);continue}let [a,b]=piv.get(i);a^=bit(i);let f=0n;while(a){let j=top(a);a^=bit(j);f^=ex[j][0];b^=ex[j][1]}ex.push([f,b])}return {ex,d}}
 const evalf=(f,z)=>parity(f[0]&z)^f[1];
 function track(F,n,s,cap=20){
  const a=affine(F.map((c,i)=>[mask(c),1^Number(!!(s&bit(i)))^Number(c[0]<0)]),n);
  if(!a)return {status:"UNSAT",why:"inconsistent parity"};
  const cs=[];
  for(let i=0;i<F.length;i++)if(s&bit(i)){
   let l=F[i].map(v=>[a.ex[Math.abs(v)-1][0],a.ex[Math.abs(v)-1][1]^Number(v<0)]);
   if(l.some(f=>!f[0]&&f[1]))continue;
   l=l.filter(f=>f[0]);if(!l.length)return {status:"UNSAT",why:"forced false"};
   if(l.some(f=>l.some(g=>f[0]===g[0]&&f[1]!==g[1])))continue;
   cs.push(l)
  }
  const piv=new Map(),base=[];
  function reduce(v){let c=0n;while(v&&piv.has(top(v))){let [w,q]=piv.get(top(v));v^=w;c^=q}return [v,c]}
  for(const cl of cs)for(const [v] of cl){const [r,c]=reduce(v);if(r){piv.set(top(r),[r,c^bit(base.length)]);base.push(v)}}
  const parent=base.map((_,i)=>i);
  function find(x){while(parent[x]!==x){parent[x]=parent[parent[x]];x=parent[x]}return x}
  function union(x,y){parent[find(x)]=find(y)}
  const coords=cs.map(cl=>cl.map(([v,b])=>{const [r,c]=reduce(v);assert(!r,"span");return [c,b]}));
  const scope=cl=>{let m=cl.reduce((v,f)=>v|f[0],0n),xs=[];while(m){let j=top(m);m^=bit(j);xs.push(j)}return xs};
  for(const cl of coords){const xs=scope(cl);for(const j of xs)union(xs[0],j)}
  const blocks=new Map();for(let j=0;j<base.length;j++){const r=find(j);if(!blocks.has(r))blocks.set(r,{ids:[],clauses:[]});blocks.get(r).ids.push(j)}
  for(const cl of coords)blocks.get(find(scope(cl)[0])).clauses.push(cl);
  let y=0n,tries=0;const ranks=[...blocks.values()].map(b=>b.ids.length).sort((a,b)=>b-a);
  for(const b of blocks.values()){
   if(b.ids.length>cap)return {status:"UNKNOWN",ranks};
   let ok=false;
   for(let t=0;t<2**b.ids.length;t++){let z=0n;for(let j=0;j<b.ids.length;j++)if(t&(1<<j))z|=bit(b.ids[j]);tries++;if(b.clauses.every(cl=>cl.some(f=>evalf(f,z)))){y|=z;ok=true;break}}
   if(!ok)return {status:"UNSAT",why:"exhausted block",ranks,tries}
  }
  const lift=affine(base.map((v,j)=>[v,Number(!!(y&bit(j)))]),a.d);assert(lift,"basis lift");let z=0n;for(let i=0;i<a.d;i++)if(lift.ex[i][1])z|=bit(i);
  let x=0n;for(let i=0;i<n;i++)if(evalf(a.ex[i],z))x|=bit(i);
  assert(sat(F,x)&&sig(F,x)===s,"lift invalid");return {status:"SAT",ranks,tries,x:x.toString()}
 }
 function up(cs){while(true){if(cs.some(c=>!c.length))return null;const u=cs.find(c=>c.length===1);if(!u)return cs;cs=cs.filter(c=>!c.includes(u[0])).map(c=>c.filter(x=>x!==-u[0]))}}
 function paidClosure(cs){let calls=0,forced=0;let p=up(cs);while(p&&p.length){let step=false;for(const v of new Set(p.flat().map(Math.abs))){for(const l of [v,-v]){calls++;if(up([...p,[l]])===null){p=up([...p,[-l]]);forced++;step=true;break}}if(step)break}if(!step)break}return {conflict:p===null,calls,forced}}
 const P=[[1,5,10],[2,7,8],[2,6,8],[3,4,9],[0,4,9],[0,1,6],[3,7,11],[5,10,11]].map(c=>c.map(v=>v+1));
 const Q=[[0,9,11],[1,5,10],[5,6,8],[3,4,9],[0,2,3],[7,10,11],[4,6,8],[1,2,7]].map(c=>c.map(v=>-v-1));
 const X=P.concat(Q),Y=[[1,2,3],[1,4,5],[2,4,6],[3,5,6],[-1,-2,-4],[-1,-3,-6],[-2,-3,-5],[-4,-5,-6]];
 const V=U.map(c=>c.slice());[V[2][2],V[44][2]]=[V[44][2],V[2][2]];
 for(const [F,n] of [[X,12],[Y,6],[U,198],[V,198]])validate(F,n);
 function small(F,n){let all=new Map(),models=0,min=Infinity,minSat=Infinity,mins=0,minSatCount=0,example=null;
  for(let i=0;i<2**n;i++){let x=BigInt(i),s=sig(F,x),w=weight(s),ok=sat(F,x);if(w<min){min=w;mins=0}if(w===min)mins++;if(ok){models++;if(w<minSat){minSat=w;minSatCount=0;example=i}if(w===minSat)minSatCount++}all.set(s,(all.get(s)||false)||ok)}
  let yes=0,no=0,rankMax=0;for(const [s,ok] of all){let r=track(F,n,s);assert(r.status===(ok?"SAT":"UNSAT"),"fiber disagreement");if(ok)yes++;else no++;rankMax=Math.max(rankMax,...(r.ranks||[0]))}
  let impossible=0;for(let i=0;i<2**Math.min(F.length,10);i++){let s=BigInt(i);if(!all.has(s)){assert(track(F,n,s).status==="UNSAT","impossible parity");impossible++}}
  return {n,models,minParityExceptions:min,minimizerAssignments:mins,minSATExceptions:minSat,minSATAssignments:minSatCount,minSATWitness:example,realizableFibers:all.size,satFibers:yes,unsatFibers:no,inconsistentChecks:impossible,largestEnumeratedBlockRank:rankMax,closure:paidClosure(F)}
 }
 let nodes=0;function dpll(cs){nodes++;cs=up(cs);if(cs===null)return false;if(!cs.length)return true;const c=cs.reduce((a,b)=>a.length<=b.length?a:b);return dpll([...cs,[c[0]]])||dpll([...cs,[-c[0]]])}
 const modules=Array.from({length:6},(_,i)=>U.slice(2,254).filter(c=>c.some(x=>Math.abs(x)>=1+32*i&&Math.abs(x)<=32+32*i)));
 for(let i=0;i<6;i++){assert(modules[i].length===42,"module count");assert(modules[i].every(c=>c.every(x=>Math.abs(x)>=193||(Math.abs(x)>=1+32*i&&Math.abs(x)<=32+32*i))),"module privacy")}
 let direct=0,covered=0,calls=0;
 for(let b=0;b<64;b++){const value=l=>Number(!!(b&(1<<(Math.abs(l)-193))))^Number(l<0);if(U.slice(0,2).some(c=>!c.some(value))){direct++;continue}let found=false;for(const M of modules){calls++;const R=M.filter(c=>!c.some(l=>Math.abs(l)>=193&&value(l))).map(c=>c.filter(l=>Math.abs(l)<193));if(!dpll(R)){found=true;break}}assert(found,"U198 unrefuted");covered++}
 const v=Array.from(W).reduce((x,w,i)=>x|(w==="1"?bit(i):0n),0n);assert(sat(V,v),"V witness");const vs=track(V,198,sig(V,v));assert(vs.status==="SAT","V parity lift");
 const result={Y6:small(Y,6),X12:small(X,12),U198:{direct,covered,calls,nodes,allOdd:track(U,198,0n),closure:paidClosure(U)},V198:{verifiedWitness:true,track:vs,allOdd:track(V,198,0n),closure:paidClosure(V)},counterexample:{positive:P,negative:Q}};
 assert(result.X12.minParityExceptions===2&&result.X12.minSATExceptions===4,"gap");return result
}
console.log(JSON.stringify(audit(U,W),null,2));
