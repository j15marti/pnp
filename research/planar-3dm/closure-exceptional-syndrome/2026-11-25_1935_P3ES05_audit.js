/* P3ES05 exact nested seam audit, node.js */
const audit=function audit(){
 const out={seed:20261125,randomJobs:0,randomTargets:0,source:[],nodes:0,splits:0,rank2:0,leafCalls:0,maxDepth:0,checks:0,closureJobs:[],note:"Exhaustive small cut search and supplied relay segmentation are audit-only; production SFM and TU LP not executed."};
 function ok(x,msg){out.checks++;if(!x)throw Error(msg)}
 let seed=out.seed;function rand(n){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n}
 const bit=i=>1n<<BigInt(i);
 const pc=x=>{let n=0;while(x){x&=x-1n;n++}return n};
 const xor=(v)=>v.reduce((a,b)=>a^b,0n);
 function add(B,v,t=0n){for(const [p,w] of B){if(v&p){v^=w[0];t^=w[1]}}if(!v)return t;const p=bit(v.toString(2).length-1);B.set(p,[v,t]);return null}
 function basis(v){const B=new Map();for(const x of v)add(B,x);return [...B.values()].map(x=>x[0])}
 function space(B){let s=[0n];for(const v of B)s=s.concat(s.map(x=>x^v));return s}
 function seam(L,R,B){const E=new Map(),W=[];for(const x of L)add(E,x.v,x.v);for(const v of R.map(x=>x.v).concat(B)){const t=add(E,v);if(t!==null&&t)W.push(t)}return basis(W)}
 function exact(A){let D=new Map([[0n,{w:0,h:0n}]]);for(const x of A){for(const [s,y] of [...D]){const u=s^x.v,w=y.w+x.w;if(!D.has(u)||w<D.get(u).w)D.set(u,{w,h:y.h^x.h})}}return D}
 function choose(A,B,mode){if(A.length<=4)return null;if(mode==="relay"){
   const g=[...new Set(A.filter(x=>x.g>=0).map(x=>x.g))].sort((a,b)=>a-b);
   if(!g.length)return null;
   let subset;
   if(A.some(x=>x.g===-2))subset=g;
   else if(g.length>=2)subset=g.slice(0,Math.floor(g.length/2));
   else return null;
   const S=new Set(subset),L=A.filter(x=>S.has(x.g)),R=A.filter(x=>!S.has(x.g)),W=seam(L,R,B);
   ok(L.length>=4&&R.length>0&&W.length<=2,"relay seam");
   return [L,R,W];
 } if(A.length>11)return null;
 for(let mask=1;mask<(1<<A.length)-1;mask++){if(pc(BigInt(mask))<4)continue;const L=A.filter((_,i)=>mask&(1<<i)),R=A.filter((_,i)=>!(mask&(1<<i))),W=seam(L,R,B);if(W.length<=2)return [L,R,W]}return null}
 function solve(A,B,mode,depth=0,stats={nodes:0,splits:0,rank2:0,maxDepth:0}){
   out.nodes++;stats.nodes++;out.maxDepth=Math.max(out.maxDepth,depth);stats.maxDepth=Math.max(stats.maxDepth,depth);
   const cut=choose(A,B,mode);
   if(!cut){out.leafCalls++;ok(A.length<=20,"audit leaf cap");const D=exact(A);return new Map(space(B).map(q=>[q,D.get(q)||null]));}
   const [L,R,W]=cut;out.splits++;stats.splits++;if(W.length===2){out.rank2++;stats.rank2++}
   const table=solve(L,W,mode,depth+1,stats), V=[];
   for(const q of space(W))if(q){const y=table.get(q);ok(y!==null,"seam state attainable");V.push({v:q,w:y.w,h:y.h,g:-1})}
   ok(L.length<A.length&&R.length+V.length<A.length,"strict size decrease");
   return solve(R.concat(V),B,mode,depth+1,stats)
 }
 function verify(A,q,y){if(!y)return;const chosen=A.filter(x=>x.h&y.h);ok(xor(chosen.map(x=>x.v))===q,"lift syndrome");ok(chosen.reduce((s,x)=>s+x.w,0)===y.w,"lift cost")}
 for(let z=0;z<400;z++){
   const m=5+rand(7),d=3+rand(5),A=Array.from({length:m},(_,i)=>({v:BigInt(rand(1<<d)),w:rand(8),h:bit(i),g:-2})),B=basis(Array.from({length:1+rand(2)},()=>BigInt(rand(1<<d))));
   const D=exact(A),stats={nodes:0,splits:0,rank2:0,maxDepth:0},T=solve(A,B,"small",0,stats);ok(stats.nodes<=4*m,"node cap");
   for(const q of space(B)){const y=T.get(q);ok((y?.w??null)===(D.get(q)?.w??null),"random optimum");verify(A,q,y);out.randomTargets++}out.randomJobs++
 }
 const U="013 021 110 113 221 222 231 300 302 330",V=U+" 002",Q="001 010 011 100 101 110";
 function parse(s){return s.split(" ").map(t=>[...t].map(Number))}
 const ru=[[12,13],[15,14],[18,16,17],[20,19,21],[19,20],[14,12,15],[13,17,16],[21,18],[19,14,21],[16,18,13],[17,20],[15,12],[0,11,5],[0,6,9],[8,5,1],[5,11,1],[6,2,9],[2,6,10],[9,2,7],[3,4,8],[10,4,3],[8,7,3]];
 const rv=[[12,22,13],[15,14],[18,16,17],[20,19,21],[19,20,22],[14,12,15],[13,17,16],[21,18],[19,14,21],[16,18,13],[17,22,20],[15,12],[0,11,5],[0,6,9],[8,5,1],[5,11,1],[6,2,9],[2,6,10],[9,2,7],[3,4,8],[10,4,3],[8,7,3],[4,10,0]];
 const rq=[[6,7,8],[11,9,10],[10,9,6],[7,11,8],[9,11,7],[8,10,6],[0,5,2],[0,4,3],[3,5,0],[2,1,4],[5,1,2],[4,1,3]];
 function rotation(T,n,R){const G=Array.from({length:3*n+T.length},()=>[]);T.forEach((t,i)=>t.forEach((v,c)=>{G[c*n+v].push(3*n+i);G[3*n+i].push(c*n+v)}));ok(G.every((a,i)=>a.slice().sort((x,y)=>x-y).join()===R[i].slice().sort((x,y)=>x-y).join()),"rotation adjacency");const seen=new Set();let F=0;for(let u=0;u<R.length;u++)for(const v of R[u]){let a=u,b=v;if(seen.has(a+":"+b))continue;F++;do{seen.add(a+":"+b);const row=R[b],c=row[(row.indexOf(a)+1)%row.length];a=b;b=c}while(!seen.has(a+":"+b))}ok(seen.size===6*T.length&&R.length-3*T.length+F===2,"connected planar certificate")}
 rotation(parse(U),4,ru);rotation(parse(V),4,rv);rotation(parse(Q),2,rq);
 function build(s,L){let T=parse(s),n=4,G=T.map(()=>-2),v=T[0][0];for(let j=0;j<L;j++){const rows=parse(Q).map(t=>t.map(x=>x+n));T[0][0]=j===0?n:T[0][0];if(j>0)T[T.length-6][0]=n;rows[0][0]=v;T.push(...rows);G.push(...rows.map(()=>j));n+=2}const A=T.map((t,i)=>({v:xor(t.map((x,c)=>bit(c*n+x))),w:1,h:bit(i),g:G[i]}));ok(new Set(T.map(t=>t.join(","))).size===T.length,"distinct triples");for(let c=0;c<3;c++)for(let v=0;v<n;v++){const d=T.filter(t=>t[c]===v).length;ok(d>=2&&d<=3,"degree promise")}return {T,n,A,t:bit(3*n)-1n}}
 function matching(T,n,p,a,b){const adj=Array.from({length:n},()=>[]);T.forEach((t,i)=>{if(p[i]!==0)adj[t[a]].push(t[b])});const owner=Array(n).fill(-1);function aug(u,vis){for(const v of adj[u])if(!vis[v]){vis[v]=true;if(owner[v]<0||aug(owner[v],vis)){owner[v]=u;return true}}return false}for(let i=0;i<n;i++)if(!aug(i,Array(n).fill(false)))return false;return true}
 function base(S,p){const {T,n,A,t}=S;p=p.slice();let changed=true;while(changed){changed=false;for(let c=0;c<3;c++)for(let v=0;v<n;v++){const I=T.map((x,i)=>x[c]===v?i:-1).filter(i=>i>=0),P=I.filter(i=>p[i]===1),O=I.filter(i=>p[i]!==0);if(P.length>1||!O.length)return null;if(P.length===1){for(const i of O)if(i!==P[0]){p[i]=0;changed=true}}else if(O.length===1&&p[O[0]]<0){p[O[0]]=1;changed=true}}}
  if(![[0,1],[0,2],[1,2]].every(([a,b])=>matching(T,n,p,a,b)))return null;
  const E=new Map();let target=t;A.forEach((x,i)=>{if(p[i]===1)target^=x.v;else if(p[i]<0)add(E,x.v)});if(add(E,target)!==0n)return null;return p}
 function close(S){let p=Array(S.T.length).fill(-1),rounds=0;while(true){p=base(S,p);if(!p)return {label:"NO",rounds};let ch=false;for(let i=0;i<p.length;i++)if(p[i]<0){const a=p.slice(),b=p.slice();a[i]=0;b[i]=1;const x=base(S,a),y=base(S,b);if(!x&&!y)return {label:"NO",rounds};if(!x||!y){p=x||y;rounds++;ch=true;break}}if(!ch)break}return {label:p.every(x=>x>=0)?"YES":"LIVE",rounds,p}}
 for(const [s,expected] of [[U,6],[V,4]])for(const L of [0,1,2,4,8,16,32,64]){
  const S=build(s,L),stats={nodes:0,splits:0,rank2:0,maxDepth:0};const y=solve(S.A,[S.t],"relay",0,stats).get(S.t);ok(y&&y.w===expected+2*L,"relay minimum");verify(S.A,S.t,y);ok(stats.nodes<=4*S.A.length,"relay node bound");
  if(expected===4){const chosen=S.T.filter((_,i)=>y.h&bit(i));ok(chosen.length===S.n&&[0,1,2].every(c=>new Set(chosen.map(t=>t[c])).size===S.n),"source cover")}
  out.source.push({case:expected===4?"SAT":"UNSAT",relays:L,m:S.A.length,n:S.n,min:y.w,...stats});
  if(L<=4){const C=close(S);ok(C.label==="LIVE"||C.label===(expected===4?"YES":"NO"),"closure sound");if(C.label==="LIVE"){const residual=S.A.filter((_,i)=>C.p[i]<0),fixed=S.A.filter((_,i)=>C.p[i]===1),target=S.t^xor(fixed.map(x=>x.v));const a=solve(residual,basis([target]),"small").get(target);ok(a&&a.w+fixed.length===expected+2*L||expected!==4&&(!a||a.w+fixed.length>S.n),"guarded source decision")}out.closureJobs.push({case:expected===4?"SAT":"UNSAT",L,label:C.label,rounds:C.rounds})}
 }
 return out;
};
console.log(JSON.stringify(audit(),null,2));
