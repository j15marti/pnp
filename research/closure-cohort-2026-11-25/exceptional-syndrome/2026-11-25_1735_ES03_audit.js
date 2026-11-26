function audit(){
 const states=[0,3,5,6],ALL=105;let assertions=0,calls=0,forced=0;const ok=(x,msg)=>{assertions++;if(!x)throw Error(msg)};
 function match(g){
  calls++;let n=g.length,m=Array(n).fill(-1),p,base,used,blossom;
  function lca(a,b){let seen=Array(n).fill(false);while(true){a=base[a];seen[a]=true;if(m[a]<0)break;a=p[m[a]]}while(true){b=base[b];if(seen[b])return b;b=p[m[b]]}}
  function mark(v,b,c){while(base[v]!=b){blossom[base[v]]=blossom[base[m[v]]]=true;p[v]=c;c=m[v];v=p[m[v]]}}
  function path(r){p=Array(n).fill(-1);base=Array.from({length:n},(_,i)=>i);used=Array(n).fill(false);used[r]=true;let q=[r];for(let h=0;h<q.length;h++){let v=q[h];for(let u of g[v]){if(base[v]==base[u]||m[v]==u)continue;if(u==r||(m[u]>=0&&p[m[u]]>=0)){let b=lca(v,u);blossom=Array(n).fill(false);mark(v,b,u);mark(u,b,v);for(let i=0;i<n;i++)if(blossom[base[i]]){base[i]=b;if(!used[i]){used[i]=true;q.push(i)}}}else if(p[u]<0){p[u]=v;if(m[u]<0)return u;u=m[u];used[u]=true;q.push(u)}}}return -1}
  for(let i=0;i<n;i++)if(m[i]<0){let v=path(i);while(v>=0){let u=p[v],w=m[u];m[v]=u;m[u]=v;v=w}}
  return m.every((v,i)=>v>=0&&m[v]==i&&g[i].includes(v))?m:null
 }
 function gadget(g,P,mask){const node=()=>{g.push([]);return g.length-1},edge=(a,b)=>{g[a].push(b);g[b].push(a)};if(mask===null){let Q=P.slice();if(Q.length%2)Q.push(node());for(let i=0;i<Q.length;i++)for(let j=0;j<i;j++)edge(Q[i],Q[j]);return true}
  if(!mask)return false;ok(P.length===3,"ternary degree");
  if(mask===1){for(let p of P)edge(p,node());return true}
  let c=node(),first=-1;for(let i=0;i<3;i++)if(mask&(1<<(7^(1<<i)))){edge(c,P[i]);if(first<0)first=i}
  if(mask&1){let a=[0,1,2].filter(i=>i!==first);edge(P[a[0]],P[a[1]])}return true
 }
 function cut(n,E,C,root=n-1){let skip=new Set(C),S=new Set([root]),q=[root];for(let u of q)for(let i=0;i<E.length;i++){if(skip.has(i))continue;let [a,b]=E[i],v=a==u?b:b==u?a:-1;if(v>=0&&!S.has(v)){S.add(v);q.push(v)}}let T=Array.from({length:n},(_,i)=>i).filter(i=>!S.has(i));ok(T.length>0,"cut nontrivial");let A=new Set(T),ids=E.map(([u,v],i)=>A.has(u)!==A.has(v)?i:-1).filter(i=>i>=0);ok(ids.join()==C.join(),"cut ids");return T}
 const boundary=(E,S)=>{let A=new Set(S);return E.map(([a,b],i)=>A.has(a)!==A.has(b)?i:-1).filter(i=>i>=0)}
 const pat=(w,c)=>c.reduce((a,j,i)=>a|(w[j]<<i),0);
 function closure(owners,pins){let change=true;owners=owners.map(o=>({C:o.C,mask:o.mask}));pins=new Map(pins);while(change){change=false;for(let o of owners){for(let s of states)if(o.mask>>s&1)for(let j=0;j<3;j++)if(pins.has(o.C[j])&&pins.get(o.C[j])!==(s>>j&1)){o.mask&=~(1<<s);change=true;break}if(!o.mask)return null;for(let j=0;j<3;j++){let vals=states.filter(s=>o.mask>>s&1).map(s=>s>>j&1);if(vals.every(x=>x===vals[0])&&!pins.has(o.C[j])){pins.set(o.C[j],vals[0]);forced++;change=true}}}}return {owners,pins}}
 function solve(n,E,owners,pins=new Map()){
  let merged=new Map;for(let o of owners){let k=o.C.join();merged.set(k,{C:o.C,mask:(merged.get(k)?.mask??ALL)&o.mask})}
  let cl=closure([...merged.values()],pins);if(!cl)return null;({owners,pins}=cl);
  let nodes=owners.map(o=>({...o,S:cut(n,E,o.C),children:[],tab:new Map}));nodes.sort((a,b)=>a.S.length-b.S.length);let root={S:Array.from({length:n},(_,i)=>i),C:[],mask:1,children:[],tab:new Map};nodes.push(root);let sets=nodes.map(o=>new Set(o.S));
  for(let i=0;i<nodes.length-1;i++){let p=-1;for(let j=i+1;j<nodes.length;j++){let a=nodes[i].S,hit=a.filter(x=>sets[j].has(x)).length;ok(hit===0||hit===a.length,"laminar");if(hit===a.length&&p<0)p=j}ok(p>=0,"parent");nodes[p].children.push(i)}
  for(let ni=0;ni<nodes.length;ni++){
   let o=nodes[ni],map=Array(n).fill(-1),next=0,rel=new Map;
   for(let ci of o.children){let id=next++;for(let v of nodes[ci].S)map[v]=id;rel.set(id,{C:nodes[ci].C,mask:[...nodes[ci].tab.keys()].reduce((a,s)=>a|(1<<s),0)})}
   for(let v of o.S)if(map[v]<0)map[v]=next++;
   let out=next++;let incid=Array.from({length:next},()=>[]),Q=[];
   for(let e=0;e<E.length;e++){let [u,v]=E[e],a=map[u]<0?out:map[u],b=map[v]<0?out:map[v];if(a===b)continue;incid[a].push(e);incid[b].push(e);Q.push([e,a,b])}
   for(let s of (o===root?[0]:states.filter(x=>o.mask>>x&1))){
    let g=[],port=new Map,fail=false;
    for(let v=0;v<next;v++){let ids=incid[v],P=ids.map(e=>{let p=g.length;g.push([]);port.set(v+","+e,p);return p});let r=rel.get(v),mask=r?r.mask:(v===out&&o!==root?1<<s:null);if(r)ok(ids.join()===r.C.join(),"child ids");if(v===out&&o!==root)ok(ids.join()===o.C.join(),"parent ids");if(!gadget(g,P,mask)){fail=true;break}}
    if(fail)continue;let banned=new Set,links=[];
    for(let [e,a,b] of Q){let u=port.get(a+","+e),v=port.get(b+","+e),p=pins.get(e);links.push([e,u,v]);if(p===1){banned.add(u);banned.add(v)}else if(p!==0){g[u].push(v);g[v].push(u)}}
    let ren=Array(g.length).fill(-1),back=[];for(let i=0;i<g.length;i++)if(!banned.has(i)){ren[i]=back.length;back.push(i)}
    let m=match(back.map(i=>g[i].filter(j=>ren[j]>=0).map(j=>ren[j])));if(!m)continue;
    let w=new Map;for(let [e,u,v] of links)w.set(e,pins.get(e)===1?1:(m[ren[u]]===ren[v]?1:0));o.tab.set(s,w)
   }
  }
  if(!root.tab.has(0))return null;let w=Array(E.length).fill(-1),stack=[[nodes.length-1,0]];
  while(stack.length){let [i,s]=stack.pop(),o=nodes[i],a=o.tab.get(s);ok(!!a,"backpointer");for(let [e,v] of a){ok(w[e]<0||w[e]===v,"shared edge");w[e]=v}for(let j of o.children){let c=nodes[j].C,k=c.reduce((z,e,h)=>z|(a.get(e)<<h),0);stack.push([j,k])}}
  ok(w.every(x=>x===0||x===1),"all edges covered");ok(valid(n,E,owners,w,pins),"lift");return w
 }
 function valid(n,E,O,w,pins=new Map){let p=Array(n).fill(0);for(let i=0;i<E.length;i++)if(w[i]){p[E[i][0]]^=1;p[E[i][1]]^=1}return p.every(x=>!x)&&O.every(o=>o.mask>>pat(w,o.C)&1)&&[...pins].every(([e,v])=>w[e]===v)}
 function words(n,E){let a=[];for(let x=0;x<2**E.length;x++){let w=E.map((_,i)=>x>>i&1);if(valid(n,E,[],w))a.push(w)}return a}
 function k33(){let E=[];for(let i=0;i<3;i++)for(let j=3;j<6;j++)E.push([i,j]);return {n:6,E,S:Array.from({length:6},(_,i)=>[i])}}
 function expand(G,v){let {n,E,S}=G;let es=E.map((e,i)=>e.includes(v)?i:-1).filter(i=>i>=0);ok(es.length===3,"cubic");for(let j=1;j<3;j++){let i=es[j];E[i]=E[i].map(a=>a===v?n+j-1:a)}E.push([v,n],[n,n+1],[n+1,v]);for(let s of S)if(s.includes(v))s.push(n,n+1);S.push([v],[n],[n+1]);G.n+=2;return G}
 function owners(G,F){return F.map((f,i)=>({C:boundary(G.E,G.S[i]),mask:ALL^(1<<f)}))}
 function ranks(G,O){let W=words(G.n,G.E),rows=G.E.map((_,i)=>W.reduce((a,w,j)=>a|(BigInt(w[i])<<BigInt(j)),0n));function rank(v){let B=new Map;for(let x of v)while(x){let k=x.toString(2).length;if(B.has(k))x^=B.get(k);else{B.set(k,x);break}}return B.size}let min=99;for(let s=1;s<(1<<O.length);s++){let a=new Set;O.forEach((o,i)=>{if(s>>i&1)o.C.forEach(e=>a.add(e))});let k=s.toString(2).split("1").length-1,d=rank([...a].map(e=>rows[e]))-k;if(s===(1<<O.length)-1)ok(d===-1,"full deficit");else{ok(d>=0,"strict");min=Math.min(min,d)}}return min}
 let G=k33(),W=words(G.n,G.E),K={yes:0,no:0},firstNo=null,neighbor=null;for(let f=0;f<1024;f++){let F=Array.from({length:5},(_,i)=>states[f>>2*i&3]),O=owners(G,F),ref=W.some(w=>valid(G.n,G.E,O,w)),got=solve(G.n,G.E,O);ok(!!got===ref,"K33");if(ref)K.yes++;else{K.no++;if(!firstNo)firstNo=F}}
 ranks(G,owners(G,firstNo));for(let i=0;i<5&&!neighbor;i++)for(let t of states)if(t!==firstNo[i]){let F=firstNo.slice();F[i]=t;if(W.some(w=>valid(G.n,G.E,owners(G,F),w))){neighbor=F;break}}
 let seed=0x335e503;function rand(n){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return Math.floor(seed/2**32*n)}
 let random={yes:0,no:0};for(let j=0;j<160;j++){let G=k33();if(j%2)expand(G,0);if(j%4===3)expand(G,0);let W=words(G.n,G.E),O=G.S.map(s=>({C:boundary(G.E,s),mask:states.reduce((a,t)=>rand(2)?a|(1<<t):a,0)})),pins=new Map;if(j%3===0)pins.set(rand(G.E.length),rand(2));let ref=W.some(w=>valid(G.n,G.E,O,w,pins)),got=solve(G.n,G.E,O,pins);ok(ref===!!got,"random");if(ref)random.yes++;else random.no++}
 let large=[];for(let k of [1,4,16,64]){let G=k33();for(let i=0;i<k;i++)expand(G,0);let make=F=>owners(G,F.concat([0],Array(3*k).fill(0))).filter((_,i)=>i!==5);let a=solve(G.n,G.E,make(firstNo)),b=solve(G.n,G.E,make(neighbor));ok(!a&&!!b,"scale");large.push({expansions:k,vertices:G.n,edges:G.E.length,owners:make(neighbor).length})}
 // Prior atom and K5 signed controls, independent enumeration.
 let A=[[15,32,47],[13,17,28],[14,36,42],[11,53,62],[10,39,45]],sum=new Set([0]);for(let a of A)sum=new Set([...sum].flatMap(x=>a.map(y=>x^y)));ok(sum.size===63&&!sum.has(29),"atom");
 let pairs=[[[0,1],[2,3]],[[0,2],[1,4]],[[0,3],[2,4]],[[0,4],[1,3]],[[1,2],[3,4]]];function k5(f){return Array.from({length:32},(_,x)=>x).some(x=>pairs.every((P,i)=>P.some(([a,b],j)=>((x>>a^x>>b)&1)===(1^((f>>(2*i+j))&1)))))}ok(!k5(0),"K5");for(let i=0;i<10;i++)ok(k5(1<<i),"K5 flip");
 // All 16 ternary masks via isolated gadget deletion.
 for(let mask0=0;mask0<16;mask0++){let mask=states.reduce((a,s,j)=>a|((mask0>>j&1)<<s),0);for(let s of states){let g=[[],[],[]],good=gadget(g,[0,1,2],mask),m=null;if(good){let back=Array.from({length:g.length},(_,i)=>i).filter(i=>i>=3||!(s>>i&1)),r=new Map(back.map((v,i)=>[v,i]));m=match(back.map(v=>g[v].filter(u=>r.has(u)).map(u=>r.get(u))))}ok(!!m===!!(mask>>s&1),"gadget mask")}}
 return {assertions,matchingCalls:calls,forcedPinDeductions:forced,K33:K,strictSubsetChecks:30,firstNo,neighbor,random,large,atomMissing:29,K5No:true,K5SatFlips:10,gadgetChecks:64}
}
console.log(JSON.stringify(audit(),null,2));
