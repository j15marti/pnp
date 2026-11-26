// node audit.js; reused helper functions from AGE16 blob ad61ccb096f7d574deea0e4bf2441021765d5ea8
function audit(){
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

 function rows(T){let R=new Map;for(let [i,...t]of T)t.forEach((v,c)=>{let k=c+":"+v;if(!R.has(k))R.set(k,[]);R.get(k).push(i)});return R}
 function valid(T,S,G=[]){let s=new Set(S);return s.size===S.length&&S.every(i=>T.some(t=>t[0]===i))&&[...rows(T).values()].every(r=>r.filter(i=>s.has(i)).length===1)&&G.every(([i,b])=>Number(s.has(i))===b)}
 function closure(T,G=[]){let R=rows(T),P=new Map,changed=true;function pin(i,b){if(P.has(i))return P.get(i)===b;P.set(i,b);changed=true;return true}for(let[i,b]of G)if(!pin(i,b))return null;
  while(changed){changed=false;for(let r of R.values()){let one=r.filter(i=>P.get(i)===1),u=r.filter(i=>!P.has(i));if(one.length>1||(!one.length&&!u.length))return null;if(one.length){for(let i of u)if(!pin(i,0))return null}else if(u.length===1&&!pin(u[0],1))return null}}return P}

 function count(T,G=[]){
  let R=rows(T),P=closure(T,G);if(P===null)return 0n;
  let K=[...R.keys()],index=new Map(K.map((x,i)=>[x,i])),M=new Map(T.map(([i,...t])=>[i,t.reduce((a,v,c)=>a|(1n<<BigInt(index.get(c+":"+v))),0n)])),live=K.map(k=>R.get(k).filter(i=>!P.has(i)));
  let mask=(1n<<BigInt(K.length))-1n;for(let [i,b]of P)if(b)mask^=M.get(i);
  let memo=new Map;function f(m){if(!m)return 1n;if(memo.has(m))return memo.get(m);let best=null;for(let j=0;j<K.length;j++)if(m>>BigInt(j)&1n){let q=live[j].filter(i=>(m&M.get(i))===M.get(i));if(best===null||q.length<best.length)best=q;if(!q.length)break}let n=0n;for(let i of best)n+=f(m^M.get(i));memo.set(m,n);return n}return f(mask)
 }
 function liftCore(C,edges,alt=0){let w=range(C.n).map(()=>0);for(let i of edges){let[a,p,b,q]=C.E[i];w[a]|=1<<p;w[b]|=1<<(q+2)}let tbl={0:alt?[3,4]:[2,5],5:[0,7],9:[0,7],6:[1,6],10:[1,6]};return w.flatMap((x,i)=>{check(tbl[x],"cycle table");return tbl[x].map(j=>8*i+j)})}
 function cycle(C,i){let[a,p,b]=C.E[i],Q=[b],prev=new Map([[b,-1]]);for(let j=0;j<Q.length&&!prev.has(a);j++)C.E.forEach((e,k)=>{if(e[0]===Q[j]&&!prev.has(e[2])){prev.set(e[2],k);Q.push(e[2])}});check(prev.has(a),"Eulerian");let L=[i];for(let v=a;v!==b;){let k=prev.get(v);L.push(k);v=C.E[k][0]}return L}

function make(l){
 let C=core(l),T=C.T.map(t=>t.slice()),X=2*C.n,Y=X,Z=X,par=range(C.n),find=i=>{while(i!==par[i])i=par[i];return i},keep=new Set;
 C.E.forEach(([a,p,b],i)=>{let u=find(a),v=find(b);if(u!==v){par[u]=v;keep.add(i)}});
 check(keep.size===C.n-1,"tree");let patches=[];
 C.E.forEach(([a,p,b],i)=>{if(keep.has(i))return;let orig=8*a+p,old=T[orig][1],ent=X++,x2=X++,x3=X++,off=T.length;T[orig][1]=ent;
 let xs=[old,ent,x2,x3],yz=[[0,0],[0,1],[1,1],[1,0]];for(let j=0;j<4;j++)T.push([off+j,xs[j],Y+yz[j][0],Z+yz[j][1]]);
 T.push([off+4,x2,Y+2,Z+2],[off+5,x3,Y+2,Z+2]);Y+=3;Z+=3;patches.push({orig,off});});
 check(X===Y&&Y===Z,"balance");return {C,T,patches};
}
function acquire(T,G=[]){
 let P=closure(T,G);if(P===null)return {no:true};let R=rows(T),by=new Map(T.map(t=>[t[0],t])),seen=new Set,blocks=[],of=new Map;
 for(let [i]of T)if(!seen.has(i)){let q=[i];seen.add(i);for(let j=0;j<q.length;j++)for(let c of [2,3])for(let a of R.get((c-1)+":"+by.get(q[j])[c]))if(!seen.has(a)){seen.add(a);q.push(a)}let opts=[];
 if(q.length===2&&q.every(j=>by.get(j)[2]===by.get(q[0])[2]&&by.get(j)[3]===by.get(q[0])[3]))opts=q.map(j=>[j]);
 if(q.length===4&&[2,3].every(c=>new Set(q.map(j=>by.get(j)[c])).size===2)){for(let a=0;a<4;a++)for(let b=a+1;b<4;b++)if([2,3].every(c=>by.get(q[a])[c]!==by.get(q[b])[c]))opts.push([q[a],q[b]])}
 let type=q.length===2&&opts.length===2?"leaf":q.length===4&&opts.length===2&&new Set(opts.flat()).size===4?"phase":"core";let j=blocks.length;blocks.push({q,opts,type});q.forEach(i=>of.set(i,j));}
 let removed=new Set,replace=new Map,lifts=[],guards=[],phaseCount=0,leafSeen=new Set;
 for(let B of blocks.filter(b=>b.type==="phase")){
 phaseCount++;let link=[];for(let i of B.q){let r=R.get("0:"+by.get(i)[1]);if(r.length===2){let a=r.find(j=>j!==i),L=blocks[of.get(a)];if(L.type==="leaf")link.push({i,a,L})}}
 if(link.length!==2||link[0].L!==link[1].L||leafSeen.has(link[0].L))return {open:true};let L=link[0].L;leafSeen.add(L);if(new Set(link.map(x=>x.a)).size!==2)return {open:true};
 let outer=B.q.filter(i=>!link.some(t=>t.i===i)),entrance=outer.filter(i=>{let r=R.get("0:"+by.get(i)[1]);return r.length===2&&r.some(j=>j!==i&&blocks[of.get(j)].type==="core")});if(entrance.length!==1)return {open:true};let a=entrance[0],b=outer.find(i=>i!==a),xa=by.get(a)[1],xb=by.get(b)[1],orig=R.get("0:"+xa).find(j=>j!==a);
 if(xa===xb||replace.has(orig)||!R.get("0:"+xb).some(j=>blocks[of.get(j)].type==="core"))return {open:true};let F=[[],[]];
 for(let s of B.opts)for(let t of L.opts){let set=new Set([...s,...t]);if(!link.every(z=>Number(set.has(z.i))+Number(set.has(z.a))===1))continue;if(set.has(a)===set.has(b))return {open:true};if([...B.q,...L.q].every(i=>!P.has(i)||P.get(i)===Number(set.has(i))))F[Number(set.has(b))].push([...set]);}
 if(!F[0].length&&!F[1].length)return {no:true};if(F.some(f=>f.length>1))return {open:true};if(!F[0].length)guards.push([orig,1]);if(!F[1].length)guards.push([orig,0]);for(let i of [...B.q,...L.q])removed.add(i);replace.set(orig,xb);lifts.push({orig,F});
 }
 if(leafSeen.size!==blocks.filter(b=>b.type==="leaf").length||!phaseCount)return {open:true};
 let C=T.filter(t=>!removed.has(t[0])).map(t=>replace.has(t[0])?[t[0],replace.get(t[0]),t[2],t[3]]:t.slice());guards.push(...[...P].filter(([i])=>!removed.has(i)));let Q=closure(C,guards);if(Q===null)return {no:true};
 if(new Set(C.map(t=>key(t.slice(1)))).size!==C.length||![2,3].every(c=>new Set(C.map(t=>t[c])).size===new Set(C.map(t=>t[1])).size))return {open:true};
 // Verify original remaining core is connected even without using the restored incidence wires.
 let raw=T.filter(t=>!removed.has(t[0])),rc=rows(raw),bc=new Map(raw.map(t=>[t[0],t])),q=[raw[0][0]],s=new Set(q);for(let j=0;j<q.length;j++)for(let c=1;c<=3;c++)for(let i of rc.get((c-1)+":"+bc.get(q[j])[c]))if(!s.has(i)){s.add(i);q.push(i)}if(q.length!==C.length)return {open:true};
 return {C,guards:[...Q],phaseCount,pins:P.size,tableCalls:2*phaseCount,lift:S=>{let set=new Set(S);return [...S,...lifts.flatMap(({orig,F})=>{let f=F[Number(set.has(orig))];check(f.length===1,"lift");return f[0]})]}};
}
let results=[];
for(let l of [2,3,4,6,8,12]){
 let {C,T,patches}=make(l),A=acquire(T.slice().reverse());check(A.C&&A.phaseCount===C.n+1&&A.pins===0,"acquire");let original=new Map(C.T.map(t=>[t[0],key(t)]));check(A.C.length===C.T.length&&A.C.every(t=>original.get(t[0])===key(t)),"core recovery");check(new Set(T.map(t=>key(t.slice(1)))).size===T.length,"distinct");let sizes=[1,2,3].map(c=>new Set(T.map(t=>t[c])).size);check(sizes.every(x=>x===sizes[0]),"balance");
 let covers=[liftCore(C,[],0),liftCore(C,[],1),...C.E.map((_,i)=>liftCore(C,cycle(C,i)))],yes=new Set,no=new Set;
 // Use indexed row validation with O(m) membership rather than repeated source scans.
 let RR=rows(T),ids=new Set(T.map(t=>t[0]));function ok(S,G=[]){let set=new Set(S);return set.size===S.length&&S.every(i=>ids.has(i))&&[...RR.values()].every(r=>r.filter(i=>set.has(i)).length===1)&&G.every(([i,b])=>Number(set.has(i))===b)}
 for(let V of covers){let S=A.lift(V);check(ok(S),"lift");let s=new Set(S);for(let [i]of T)(s.has(i)?yes:no).add(i)}
 check(yes.size===T.length&&no.size===T.length,"full unary support");let g=[[patches[0].off,0]],B=acquire(T,g);check(B.C,"positive");let V=covers.find(S=>B.guards.every(([i,b])=>Number(S.includes(i))===b));check(V,"witness");let S=B.lift(V);check(ok(S,g),"guard");let bad=patches[0].off+4,h=[...g,[bad,0]];check(S.includes(bad)&&acquire(T,h).no,"negative");check(rows(T.filter(t=>!h.some(([i])=>i===t[0]))).size===rows(T).size,"no isolated owner");let n=null,gc=null;if(l<=3){n=count(T);gc=count(T,g);check(n===count(A.C)&&gc===count(B.C,B.guards)&&gc>0n&&count(T,h)===0n,"counts")}
 results.push({l,triples:T.length,core:C.T.length,ownersPerPart:sizes[0],highPhases:A.phaseCount,leafMessages:A.tableCalls,remainingHighPhases:0,initialPins:A.pins,witnesses:covers.length,positivePins:B.pins,positiveDeletion:g[0][0],negativeDeletion:bad,count:n===null?null:String(n),guardedCount:gc===null?null:String(gc)});
}
let local=0;for(let k=0;k<729;k++){let g=range(6).map(i=>Math.floor(k/3**i)%3),f=[0,0],d=[0,0];for(let s of [[0,2],[1,3]])for(let t of [[4],[5]]){let q=new Set([...s,...t]);if(Number(q.has(2))+Number(q.has(4))!==1||Number(q.has(3))+Number(q.has(5))!==1)continue;if(g.every((v,i)=>v===0||Number(q.has(i))===v-1))f[Number(q.has(0))]++}for(let w=0;w<64;w++){let b=i=>(w>>i)&1;if(!g.every((v,i)=>!v||b(i)===v-1))continue;if(b(0)+b(1)===1&&b(1)+b(2)===1&&b(2)+b(3)===1&&b(3)+b(0)===1&&b(4)+b(5)===1&&b(2)+b(4)===1&&b(3)+b(5)===1)d[b(0)]++}check(key(f)===key(d),"local");local++}
return {results,localGuardTests:local};
}
console.log(JSON.stringify(audit(),null,2));
