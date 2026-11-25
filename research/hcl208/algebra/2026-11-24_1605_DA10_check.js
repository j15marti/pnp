function runDA10(){
 const result={seed:"0xda1005",fixed:{sat:0,unsat:0,checks:0,lifts:0,acPins:0,acScans:0},source:{sat:0,unsat:0,models:[],nodes:0,closureScans:0,pins:0,lifts:0},scales:[],tupleChecks:0,assertions:0};
 let seed=0xda1005;const rnd=n=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n}; const check=(p,msg)=>{result.assertions++;if(!p)throw Error(msg)};
 const pairs=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]];
 const tuples=Array.from({length:256},(_,i)=>Array.from({length:4},(_,j)=>(i>>(2*j))&3));
 function graph(t,twist=false,chain=false){
  const g=Array.from({length:4*t},()=>rnd(4)),edges=[],children=Array.from({length:t},()=>[]),used=new Set(),parentPos=Array(t).fill(-1);
  for(let b=0;b<t;b++)for(const [u,v] of pairs)edges.push({u:4*b+u,v:4*b+v,s:g[4*b+u]^g[4*b+v]^((twist&&b===0&&u===0&&v===1)?1:0)});
  for(let b=1;b<t;b++){let p=chain?b-1:rnd(b);let free=[0,1,2,3].filter(j=>!used.has(4*p+j));if(!free.length){p=b-1;free=[0,1,2,3].filter(j=>!used.has(4*p+j));}const u=4*p+free[rnd(free.length)],v=4*b;used.add(u);used.add(v);parentPos[b]=0;const s=g[u]^g[v];children[p].push({b,u,v,s});edges.push({u,v,s});}
  const ports=[];for(let v=0;v<4*t;v++)if(!used.has(v))ports.push({v,s:rnd(4)});
  return {t,g,edges,children,ports,parentPos};
 }
 function raw(G,w){return G.ports.map((p,i)=>w[i]^p.s^G.g[p.v])}
 function projection(G,word){
  const adj=Array.from({length:4*G.t},()=>[]);for(const e of G.edges){adj[e.u].push([e.v,e.s]);adj[e.v].push([e.u,e.s]);}
  const q=Array(4*G.t).fill(-1),stack=[0];q[0]=0;let balanced=true;while(stack.length){let u=stack.pop();for(const [v,s] of adj[u]){if(q[v]<0){q[v]=q[u]^s;stack.push(v);}else if(q[v]!== (q[u]^s))balanced=false;}}
  const vals=G.ports.map((p,i)=>word[i]^p.s^q[p.v]);return !balanced||vals.some(x=>x!==vals[0]);
 }
 function closure(G,word){
  const d=Array(4*G.t).fill(15);for(let i=0;i<word.length;i++){const p=G.ports[i];d[p.v]&=~(1<<(word[i]^p.s));}
  let changed=true;while(changed){changed=false;for(const e of G.edges){result.fixed.acScans++;for(const [u,v] of [[e.u,e.v],[e.v,e.u]]){if(!d[u]||!d[v])return false;if((d[u]&(d[u]-1))===0){let a=31-Math.clz32(d[u]),n=d[v]&~(1<<(a^e.s));if(n!==d[v]){d[v]=n;changed=true;result.fixed.acPins++;break;}}}if(changed)break;}}return d.every(Boolean);
 }
 function dp(G,word){
  const forbid=Array(4*G.t).fill(-1);G.ports.forEach((p,i)=>forbid[p.v]=word[i]^p.s);
  const edges=Array.from({length:G.t},()=>[]);for(const e of G.edges)if((e.u>>2)===(e.v>>2))edges[e.u>>2].push(e);
  const tab=Array.from({length:G.t},()=>Array(4).fill(null));
  for(let b=G.t-1;b>=0;b--)for(const a of tuples){result.tupleChecks++;const key=a[0];if(tab[b][key])continue;if(a.some((x,j)=>x===forbid[4*b+j]))continue;if(edges[b].some(e=>(a[e.u%4]^a[e.v%4])===e.s))continue;const choices=[];let ok=true;for(const c of G.children[b]){let j=tab[c.b].findIndex((v,i)=>v&&(i^a[c.u%4])!==c.s);if(j<0){ok=false;break;}choices.push([c.b,j]);}if(ok)tab[b][key]={a,choices};}
  const root=tab[0].findIndex(Boolean);if(root<0)return null;const out=Array(4*G.t),todo=[[0,root]];while(todo.length){const [b,j]=todo.pop(),v=tab[b][j];v.a.forEach((x,k)=>out[4*b+k]=x);todo.push(...v.choices);}return out;
 }
 function valid(G,word,x){return G.edges.every(e=>(x[e.u]^x[e.v])!==e.s)&&G.ports.every((p,i)=>(x[p.v]^word[i])!==p.s)}
 function test(G,word){const cl=closure(G,word),p=projection(G,word),x=dp(G,word);check(p===!!x,"projection vs independent block DP");check(cl||!x,"sound AC");result.fixed.checks++;if(x){check(valid(G,word,x),"lift");result.fixed.sat++;result.fixed.lifts++;}else result.fixed.unsat++;return !!x;}
 for(const tw of [false,true]){let G=graph(1,tw);for(const w of tuples)test(G,raw(G,w));}
 for(let i=0;i<120;i++){let G=graph(2+i%5,i%3===0);let w=Array(G.ports.length).fill(i%4);test(G,raw(G,w));w[i%w.length]^=1;test(G,raw(G,w));let random=w.map(()=>((rnd(256)>>4)&3));test(G,raw(G,random));}
 for(const t of [1,2,4,8,16,32,64,128,256]){const G=graph(t,false,true),H=graph(t,true,true);let w=Array(G.ports.length).fill(0);const bad=test(G,raw(G,w));w[0]=1;const good=test(G,raw(G,w));const twist=test(H,raw(H,Array(H.ports.length).fill(0)));result.scales.push({cliques:t,privateVertices:4*t,ports:G.ports.length,rank:2*(G.ports.length-1),bad,good,twist});}
 // Each ordinary clause is compiled to one independently gauged K4 with four ports.
 // Port 0 is fixed to 0 and three others are the three literal truth values.
 const fano=[];for(let a=1;a<=7;a++)for(let b=a+1;b<=7;b++){let c=a^b;if(c>b)fano.push([a,b,c]);}
 const clausesF=fano.flatMap(c=>[c,c.map(x=>-x)]);check(clausesF.length===14,"Fano");
 const cube=Array.from({length:8},(_,i)=>[1,2,3].map((v,j)=>(i>>j&1)?v:-v));
 function satClause(c,w){return c.some(l=>!!(w>>(Math.abs(l)-1)&1)===(l>0))}
 function solve(n,cs){
  const gs=cs.map(()=>graph(1));function visit(a){result.source.nodes++;
   // Exact unit closure on projected affine rejection events; restart after every pin.
   let change=true;while(change){change=false;for(const c of cs){result.source.closureScans++;let open=[],ok=false;for(const l of c){const v=a[Math.abs(l)-1];if(v<0)open.push(l);else if((v===1)===(l>0)){ok=true;break;}}if(ok)continue;if(!open.length)return null;if(open.length===1){const l=open[0];a[Math.abs(l)-1]=l>0?1:0;result.source.pins++;change=true;break;}}}
   const j=a.indexOf(-1);if(j<0)return a;for(let b=0;b<2;b++){const v=a.slice();v[j]=b;const x=visit(v);if(x)return x;}return null;
  }
  const x=visit(Array(n).fill(-1));let models=0;for(let w=0;w<(1<<n);w++)if(cs.every(c=>satClause(c,w)))models++;
  check(!!x===(models>0),"source count ref");if(x){result.source.sat++;for(let i=0;i<cs.length;i++){const G=gs[i],w=raw(G,[0,...cs[i].map(l=>+( (x[Math.abs(l)-1]===1)===(l>0)))]);const y=dp(G,w);check(!!y&&valid(G,w,y),"source K4 lift");}result.source.lifts++;}else result.source.unsat++;return models;
 }
 for(let mask=0;mask<256;mask++)solve(3,cube.filter((_,i)=>mask>>i&1));
 result.source.models.push(solve(7,clausesF));for(let i=0;i<14;i++)result.source.models.push(solve(7,clausesF.filter((_,j)=>i!==j)));check(result.source.models[0]===0&&result.source.models.slice(1).every(x=>x===5),"Fano counts");
 return result;
}
console.log(JSON.stringify(runDA10(),null,2));
