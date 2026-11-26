// Run with Node.js: node audit.js
const audit = function audit(){
 const check=(x,m)=>{if(!x)throw Error(m)},range=n=>Array.from({length:n},(_,i)=>i),key=a=>a.join(",");
 function core(l){
  let n=l*l,E=[],T=[],id=(x,y)=>x+l*y;
  for(let a=0;a<n;a++)for(let p=0;p<8;p++)T.push([8*a+p,2*a+(p>>2),2*a+((p>>1)&1),2*a+(p&1)]);
  for(let x=0;x<l;x++)for(let y=0;y<l;y++){
   if(x+1<l)E.push([id(x,y),0,id(x+1,y),0]);
   if(y+1<l)E.push([id(x,y),1,id(x,y+1),1]);
  }
  let O=[],I=[];
  for(let x=0;x<l;x++)O.push([id(x,l-1),1]);
  for(let y=l-1;y>=0;y--)O.push([id(l-1,y),0]);
  for(let x=l-1;x>=0;x--)I.push([id(x,0),1]);
  for(let y=0;y<l;y++)I.push([id(0,y),0]);
  I.reverse();O.forEach((o,i)=>E.push([...o,...I[i]]));
  E.forEach(([a,p,b])=>T[8*a+p][1]=2*b);
  return {T,E,n}
 }
 function make(l,k){
  let C=core(l),T=C.T.map(a=>a.slice()),off=T.length,base=2*C.n,n=k*k,id=(x,y)=>x+k*y,ports=range(n).map(()=>[-1,-1,-1,-1]),X=base;
  function put(a,p,b,q){check(ports[a][p]<0&&ports[b][q]<0,"port reuse");ports[a][p]=ports[b][q]=X++}
  for(let y=0;y<k;y++)for(let x=0;x<k;x++){
   if(x+1<k)put(id(x,y),0,id(x+1,y),2);
   if(y+1<k)put(id(x,y),1,id(x,y+1),3);
  }
  let ring=[];for(let x=0;x<k;x++)ring.push([id(x,0),3]);for(let y=0;y<k;y++)ring.push([id(k-1,y),0]);for(let x=k-1;x>=0;x--)ring.push([id(x,k-1),1]);for(let y=k-1;y>=0;y--)ring.push([id(0,y),2]);
  ring=ring.slice(1,-1);let val=([a,p])=>((a%k+Math.floor(a/k))&1)^(p&1);
  while(ring.length){let i=ring.findIndex((p,j)=>j+1<ring.length&&val(p)!==val(ring[j+1]));check(i>=0,"boundary balance");let [a,b]=ring.splice(i,2);put(...a,...b)}
  ports[0][2]=T[0][1];ports[0][3]=X;T[0][1]=X++;
  check(X===base+2*n,"X balance");
  let yz=[[0,0],[0,1],[1,1],[1,0]];
  for(let a=0;a<n;a++)for(let p=0;p<4;p++)T.push([off+4*a+p,ports[a][p],base+2*a+yz[p][0],base+2*a+yz[p][1]]);
  check(new Set(T.map(t=>key(t.slice(1)))).size===T.length,"distinct triples");
  check([1,2,3].every(c=>new Set(T.map(t=>t[c])).size===base+2*n),"equal parts");
  return {C,T,off}
 }
 function rows(T){let R=new Map;for(let [i,...t]of T)t.forEach((v,c)=>{let k=c+":"+v;if(!R.has(k))R.set(k,[]);R.get(k).push(i)});return R}
 function valid(T,S,G=[]){let s=new Set(S);return s.size===S.length&&S.every(i=>T.some(t=>t[0]===i))&&[...rows(T).values()].every(r=>r.filter(i=>s.has(i)).length===1)&&G.every(([i,b])=>Number(s.has(i))===b)}
 function closure(T,G=[]){let R=rows(T),P=new Map,changed=true;function pin(i,b){if(P.has(i))return P.get(i)===b;P.set(i,b);changed=true;return true}for(let[i,b]of G)if(!pin(i,b))return null;
  while(changed){changed=false;for(let r of R.values()){let one=r.filter(i=>P.get(i)===1),u=r.filter(i=>!P.has(i));if(one.length>1||(!one.length&&!u.length))return null;if(one.length){for(let i of u)if(!pin(i,0))return null}else if(u.length===1&&!pin(u[0],1))return null}}return P}
 function acquire(T,G=[]){
  let P=closure(T,G);if(P===null)return {no:true};let R=rows(T),by=new Map(T.map(t=>[t[0],t])),seen=new Set,blocks=[],of=new Map;
  for(let [i]of T)if(!seen.has(i)){let q=[i];seen.add(i);for(let j=0;j<q.length;j++)for(let c of [2,3])for(let x of R.get((c-1)+":"+by.get(q[j])[c]))if(!seen.has(x)){seen.add(x);q.push(x)}
   if(q.length!==4||[2,3].some(c=>new Set(q.map(i=>by.get(i)[c])).size!==2))continue;let opts=[];
   for(let a=0;a<4;a++)for(let b=a+1;b<4;b++)if([2,3].every(c=>by.get(q[a])[c]!==by.get(q[b])[c]))opts.push(new Set([q[a],q[b]]));
   if(opts.length!==2||new Set([...opts[0],...opts[1]]).size!==4)continue;
   q.forEach(i=>of.set(i,blocks.length));blocks.push({q,opts});
  }
  if(!blocks.length)return {open:true};
  let adj=blocks.map(()=>[]),internal=new Set;
  for(let[k,r]of R)if(k.startsWith("0:")&&r.length===2&&r.every(i=>of.has(i))){let[a,b]=r,g=of.get(a),h=of.get(b);adj[g].push([h,a,b]);adj[h].push([g,b,a]);internal.add(k)}
  // Executed adapter admits a single connected phase component and a single exact-one entrance.
  let queue=[0],p=new Map([[0,0]]);
  for(let j=0;j<queue.length;j++){let g=queue[j];for(let[h,a,b]of adj[g]){let target=!blocks[g].opts[p.get(g)].has(a),v=Number(blocks[h].opts[1].has(b)===target);if(p.has(h)){if(p.get(h)!==v)return {no:true}}else{p.set(h,v);queue.push(h)}}}
  if(queue.length!==blocks.length)return {open:true};
  let Q=blocks.flatMap(g=>g.q),outer=Q.filter(i=>!internal.has("0:"+by.get(i)[1]));
  if(outer.length!==2)return {open:true};
  let a=outer.find(i=>{let r=R.get("0:"+by.get(i)[1]);return r.length===2&&r.some(j=>!of.has(j))});
  if(a===undefined)return {open:true};
  let b=outer.find(i=>i!==a),xa=by.get(a)[1],xb=by.get(b)[1],other=R.get("0:"+xa).find(i=>i!==a);
  if(xa===xb||of.has(other))return {open:true};
  let L=[null,null];for(let flip of [0,1]){let S=queue.flatMap(g=>[...blocks[g].opts[p.get(g)^flip]]),s=new Set(S);if(s.has(a)===s.has(b))return {open:true};if(Q.every(i=>!P.has(i)||P.get(i)===Number(s.has(i))))L[Number(s.has(b))]=S}
  if(!L[0]&&!L[1])return {no:true};
  let C=T.filter(t=>!of.has(t[0])).map(t=>t[0]===other?[t[0],xb,t[2],t[3]]:t.slice());
  if(new Set(C.map(t=>key(t.slice(1)))).size!==C.length||![2,3].every(c=>new Set(C.map(t=>t[c])).size===new Set(C.map(t=>t[1])).size))return {open:true};
  let guard=[...P].filter(([i])=>!of.has(i));if(!L[0])guard.push([other,1]);if(!L[1])guard.push([other,0]);
  return {C,guard,blocks:blocks.length,pins:P.size,lift:S=>{let t=L[Number(S.includes(other))];check(t!==null,"lift guard");return [...S,...t]}}
 }
 function count(T,G=[]){
  let R=rows(T),P=closure(T,G);if(P===null)return 0n;
  let K=[...R.keys()],index=new Map(K.map((x,i)=>[x,i])),M=new Map(T.map(([i,...t])=>[i,t.reduce((a,v,c)=>a|(1n<<BigInt(index.get(c+":"+v))),0n)])),live=K.map(k=>R.get(k).filter(i=>!P.has(i)));
  let mask=(1n<<BigInt(K.length))-1n;for(let [i,b]of P)if(b)mask^=M.get(i);
  let memo=new Map;function f(m){if(!m)return 1n;if(memo.has(m))return memo.get(m);let best=null;for(let j=0;j<K.length;j++)if(m>>BigInt(j)&1n){let q=live[j].filter(i=>(m&M.get(i))===M.get(i));if(best===null||q.length<best.length)best=q;if(!q.length)break}let n=0n;for(let i of best)n+=f(m^M.get(i));memo.set(m,n);return n}return f(mask)
 }
 function liftCore(C,edges,alt=0){let w=range(C.n).map(()=>0);for(let i of edges){let[a,p,b,q]=C.E[i];w[a]|=1<<p;w[b]|=1<<(q+2)}let tbl={0:alt?[3,4]:[2,5],5:[0,7],9:[0,7],6:[1,6],10:[1,6]};return w.flatMap((x,i)=>{check(tbl[x],"cycle table");return tbl[x].map(j=>8*i+j)})}
 function cycle(C,i){let[a,p,b]=C.E[i],Q=[b],prev=new Map([[b,-1]]);for(let j=0;j<Q.length&&!prev.has(a);j++)C.E.forEach((e,k)=>{if(e[0]===Q[j]&&!prev.has(e[2])){prev.set(e[2],k);Q.push(e[2])}});check(prev.has(a),"Eulerian");let L=[i];for(let v=a;v!==b;){let k=prev.get(v);L.push(k);v=C.E[k][0]}return L}
 // Independent local MGI control: all exact square boundary words in cyclic E,N,W,S order.
 let yz=[[0,0],[0,1],[1,1],[1,0]],F=range(16).map(w=>{let s=range(4).filter(i=>w>>i&1);return Number(s.length===2&&[0,1].every(c=>new Set(s.map(i=>yz[i][c])).size===2))});
 check(F[5]*F[10]===1&&F[0]*F[15]+F[3]*F[12]+F[9]*F[6]===0,"crossing obstruction");
 let results=[];
 for(let [l,k]of [[2,2],[2,4],[3,4],[4,8],[6,12],[8,16]]){
  let {C,T,off}=make(l,k),A=acquire(T.slice().reverse());check(A.C&&A.blocks===k*k&&A.pins===0,"acquire");let original=new Map(C.T.map(t=>[t[0],key(t)]));check(A.C.length===C.T.length&&A.C.every(t=>original.get(t[0])===key(t)),"core recovery");
  let covers=[liftCore(C,[],0),liftCore(C,[],1),...C.E.map((_,i)=>liftCore(C,cycle(C,i)))],yes=new Set,no=new Set;
  for(let V of covers){let S=A.lift(V);check(valid(T,S),"native lift");let s=new Set(S);for(let [i]of T)(s.has(i)?yes:no).add(i)}
  check(yes.size===T.length&&no.size===T.length,"full unary support");
  let g=[[off,0]],B=acquire(T,g);check(B.C,"positive");let V=covers.find(S=>B.guard.every(([i,b])=>Number(S.includes(i))===b));check(V,"positive core witness");let S=B.lift(V);check(valid(T,S,g),"guard lift");let bad=S.find(i=>i>=off+4*(k*k-1)),h=[...g,[bad,0]];
  check(bad!==undefined&&acquire(T,h).no,"negative");let deletion=T.filter(t=>!h.some(([i])=>i===t[0]));check(rows(deletion).size===rows(T).size,"no isolated owner");
  let n=null,gc=null;if(l<=3){n=count(A.C);gc=count(B.C,B.guard);check(n===count(T)&&gc===count(T,g)&&gc>0n&&count(T,h)===0n,"exact reference")}
  results.push({l,k,triples:T.length,core_triples:A.C.length,phase_defects:k*k,phase_components:1,initial_pins:A.pins,positive_pins:B.pins,full_support_witnesses:covers.length,positive_deletions:[off],negative_deletions:[off,bad],exact_count:n===null?null:String(n),positive_count:gc===null?null:String(gc)});
 }
 return {local_signature:F,results};
};
console.log(JSON.stringify(audit(),null,2));
