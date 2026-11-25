function audit(){
const A=(x,m)=>{if(!x)throw Error(m)};let seed=0xce020025;
function rnd(n){seed^=seed<<13;seed^=seed>>>17;seed^=seed<<5;return (seed>>>0)%n}
function shuffle(x){for(let i=x.length-1;i>0;i--){let j=rnd(i+1);[x[i],x[j]]=[x[j],x[i]]}return x}
const range=n=>Array.from({length:n},(_,i)=>i);
function partition(v,E){let p=new Map(v.map(x=>[x,x]));function f(x){while(p.get(x)!==x)x=p.get(x);return x}for(let [a,b] of E)p.set(f(a),f(b));return new Map(v.map(x=>[x,f(x)]))}
function components(v,E){let p=partition(v,E),m=new Map();for(let x of v){let r=p.get(x);if(!m.has(r))m.set(r,[]);m.get(r).push(x)}return [...m.values()]}
function even(v,w,E){return components(v,E).every(a=>!a.reduce((s,x)=>s^w.get(x),0))}
const key=(a,b)=>a<b?`${a},${b}`:`${b},${a}`;
function graph(n,E,M,C){let d=Array(n).fill(0),md=d.slice(),id=new Map(),used=new Set();E.forEach(([a,b],i)=>{A(a!==b&&a>=0&&b>=0&&a<n&&b<n&&!id.has(key(a,b)),"simple");id.set(key(a,b),i);d[a]++;d[b]++;if(M.has(i)){md[a]++;md[b]++}});A(d.every(x=>x===3)&&md.every(x=>x===1),"cubic matching");C=C.map(c=>{A(c.length>=4&&c.length%2===0,"cycle size");return c.map((a,j)=>{A(!used.has(a),"vertex disjoint");used.add(a);let e=id.get(key(a,c[(j+1)%c.length]));A(e!==undefined&&M.has(e)===(j%2===0),"alternating");return e})});return {n,E,M:[...M],C}}
function flip(M,c){for(let e of c)M.has(e)?M.delete(e):M.add(e)}
function compEdges(g,M){return g.E.filter((_,i)=>!M.has(i))}
function good(g,M){return components(range(g.n),compEdges(g,M)).every(a=>a.length%2===0)}
function brute(g,guard={}){let trials=0;for(let z=0;z<2**g.C.length;z++){if(Object.entries(guard).some(([i,b])=>((z>>i)&1)!==b))continue;let m=new Set(g.M);g.C.forEach((c,i)=>{if((z>>i)&1)flip(m,c)});trials++;if(good(g,m))return [true,trials]}return [false,trials]}
function solve(g,guard={},cap=20){
 let M=new Set(g.M),Q=[],L=[],st={jobs:0,splits:0,scans:0,dominance:0,contractions:0,leafTrials:0,maxLeaf:0,merges:0};
 g.C.forEach((c,i)=>{if(Object.hasOwn(guard,i)){if(guard[i])flip(M,c)}else(c.length===4?Q:L).push({i,c})});
 let sq=new Set(Q.flatMap(x=>x.c)),lg=new Set(L.flatMap(x=>x.c)),p=partition(range(g.n),g.E.filter((_,i)=>!lg.has(i)&&(!M.has(i)||sq.has(i))));
 let v=[...new Set(p.values())],w=new Map(v.map(x=>[x,0]));for(let x of p.values())w.set(x,w.get(x)^1);
 let S=L.map(({i,c})=>({i,o:[1,0].map(b=>c.filter((_,j)=>j%2===b).map(e=>g.E[e].map(x=>p.get(x))))})),choice={...guard};
 function job(v,w,S){
 st.jobs++;
 while(true){let common=[],chosen=-1,bit=0;for(let j=0;j<S.length;j++){let s=S[j],q=s.o.map(e=>partition(v,e)),m=new Map();for(let x of v){let k=q[0].get(x)+","+q[1].get(x);if(m.has(k))common.push([x,m.get(k)]);else m.set(k,x)}let finer=(a,b)=>s.o[a].every(([x,y])=>q[b].get(x)===q[b].get(y));if(chosen<0&&(finer(0,1)||finer(1,0))){chosen=j;bit=finer(0,1)?1:0}}
 st.scans++;if(!common.length&&chosen<0)break;
 if(chosen>=0){let s=S[chosen];choice[s.i]=bit;common.push(...s.o[bit]);S=S.filter((_,j)=>j!==chosen);st.dominance++}
 let p=partition(v,common),nv=[...new Set(p.values())],nw=new Map(nv.map(x=>[x,0]));for(let x of v)nw.set(p.get(x),nw.get(p.get(x))^w.get(x));st.contractions+=v.length-nv.length;
 S=S.map(s=>({i:s.i,o:s.o.map(e=>e.map(([a,b])=>[p.get(a),p.get(b)]))}));v=nv;w=nw;
 }
 let supports=S.map(s=>[...new Set(s.o.flat().flat())]),potential=(drop)=>supports.flatMap(a=>{let b=a.filter(x=>x!==drop);return b.slice(1).map(x=>[b[0],x])});
 let cc=components(v,potential(-1));if(cc.some(a=>a.reduce((s,x)=>s^w.get(x),0)))return false;
 if(cc.length>1){let unk=false;for(let a of cc){let t=new Set(a),r=job(a,new Map(a.map(x=>[x,w.get(x)])),S.filter((_,i)=>t.has(supports[i][0])));if(r===false)return false;if(r===null)unk=true}return unk?null:true}
 if(!S.length)return true;
 for(let a of v){st.scans++;let vv=v.filter(x=>x!==a);if(vv.length<2)continue;let cc=components(vv,potential(a));if(cc.length<2)continue;st.splits++;let unk=false;for(let side of cc){let t=new Set(side),idx=range(S.length).filter(i=>supports[i].some(x=>t.has(x)));A(idx.every(i=>supports[i].every(x=>x===a||t.has(x))),"split support");let nw=new Map(side.map(x=>[x,w.get(x)]));nw.set(a,side.reduce((s,x)=>s^w.get(x),0));let r=job([a,...side],nw,idx.map(i=>S[i]));if(r===false)return false;if(r===null)unk=true}return unk?null:true}
 st.maxLeaf=Math.max(st.maxLeaf,S.length);if(S.length>cap)return null;
 for(let z=0;z<2**S.length;z++){st.leafTrials++;if(even(v,w,S.flatMap((s,j)=>s.o[(z>>j)&1]))){S.forEach((s,j)=>choice[s.i]=(z>>j)&1);return true}}return false
 }
 let yes=job(v,w,S);
 if(yes){for(let {i,c} of L){A(Object.hasOwn(choice,i),"choice lift");if(choice[i])flip(M,c)}
 while(true){let p=partition(range(g.n),compEdges(g,M)),hit=false;for(let {c} of Q){let e=c.filter(i=>!M.has(i));if(p.get(g.E[e[0]][0])!==p.get(g.E[e[1]][0])){flip(M,c);st.merges++;hit=true;break}}if(!hit)break}
 A(good(g,M),"even lift");let adj=range(g.n).map(()=>[]),col=g.E.map((_,i)=>M.has(i)?0:-1);g.E.forEach(([a,b],i)=>{if(!M.has(i)){adj[a].push([b,i]);adj[b].push([a,i])}});for(let a of range(g.n)){let x=a,b=1;while(true){let e=adj[x].find(([,i])=>col[i]===-1);if(!e)break;col[e[1]]=b;b=3-b;x=e[0]}}
 let c=range(g.n).map(()=>new Set());g.E.forEach(([a,b],i)=>{A(col[i]>=0,"color assigned");c[a].add(col[i]);c[b].add(col[i])});A(c.every(x=>x.size===3),"source coloring");return {yes,st,col}
 }return {yes,st}
}
function generated(k,chain,odd){let C=[],E=[],M=new Set(),n=0;function add(a,b,m=false){if(m)M.add(E.length);E.push([a,b])}function cy(l){let a=range(l).map(()=>n++);C.push(a);a.forEach((x,j)=>add(x,a[(j+1)%l],j%2===0));return a}
 let L=range(k).map(()=>cy(rnd(2)?8:6)),Q=chain?range(k-1).map(()=>cy(4)):[],ports=L.map(x=>shuffle(x.slice())),P=[];
 if(chain){for(let j=0;j<k-1;j++)for(let z=0;z<2;z++){P.push([ports[j].pop(),Q[j][z]],[ports[j+1].pop(),Q[j][z+2]])}for(let a of ports)while(a.length)P.push([a.pop(),a.pop()])}else{let a=shuffle(ports.flat());while(a.length)P.push([a.pop(),a.pop()])}
 let keys=new Set(E.map(([a,b])=>key(a,b))),sub=P.map(([a,b])=>keys.has(key(a,b))||(odd&&rnd(5)===0));if(sub.filter(Boolean).length%2){let i=sub.indexOf(false);if(i<0)return generated(k,chain,odd);sub[i]=true}let mid=[];P.forEach(([a,b],i)=>{if(sub[i]){let x=n++;mid.push(x);add(a,x);add(x,b)}else add(a,b)});shuffle(mid);while(mid.length)add(mid.pop(),mid.pop(),true);return graph(n,E,M,C)
}
function gp(n,k){let E=[];for(let i=0;i<n;i++)E.push([i,(i+1)%n],[i,n+i],[n+i,n+(i+k)%n]);return E}
function flower(k){let E=[];for(let i=0;i<k;i++){let a=4*i;E.push([a,a+1],[a,a+2],[a,a+3],[a+1,4*((i+1)%k)+1]);if(i<k-1)E.push([a+2,a+6],[a+3,a+7]);else E.push([a+2,3],[a+3,2])}return E}
function matchings(n,E){let adj=range(n).map(()=>[]);E.forEach(([a,b],i)=>{adj[a].push([b,i]);adj[b].push([a,i])});let used=Array(n).fill(false),out=[];function rec(m){let a=used.indexOf(false);if(a<0){out.push(m.slice());return}used[a]=true;for(let [b,i] of adj[a])if(!used[b]){used[b]=true;rec([...m,i]);used[b]=false}used[a]=false}rec([]);return out}
function diff(n,E,m1,m2){let a=new Set(m1),b=new Set(m2),adj=range(n).map(()=>[]);E.forEach(([x,y],i)=>{if(a.has(i)!==b.has(i)){adj[x].push([y,i]);adj[y].push([x,i])}});let seen=new Set(),C=[];for(let x=0;x<n;x++)if(adj[x].length&&!seen.has(x)){let c=[],v=x,prev=-1;do{seen.add(v);c.push(v);let e=prev<0?adj[v].find(([,i])=>a.has(i)):adj[v].find(([,i])=>i!==prev);[v,prev]=e}while(v!==x);C.push(c)}return C}

function planted(k){
 let C=[],E=[],M=new Set(),n=0;
 function add(a,b,m=false){if(m)M.add(E.length);E.push([a,b])}
 function cy(l){let a=range(l).map(()=>n++);C.push(a);a.forEach((x,j)=>add(x,a[(j+1)%l],j%2===0));return a}
 let L=range(k).map(()=>cy(8)),Q=range(k-1).map(()=>cy(4)),ports=L.map(x=>shuffle(x.slice())),P=[];
 for(let j=0;j<k-1;j++)for(let z=0;z<2;z++)P.push([ports[j].pop(),Q[j][z]],[ports[j+1].pop(),Q[j][z+2]]);
 let keys=new Set(E.map(([a,b])=>key(a,b)));
 for(let a of ports){let pairs;do{let t=shuffle(a.slice());pairs=[];while(t.length)pairs.push([t.pop(),t.pop()])}while(pairs.some(([x,y])=>keys.has(key(x,y))));P.push(...pairs)}
 let PM=new Set(M),offset=0,plant=[];for(let c of C){let b=rnd(2);plant.push(b);if(b)flip(PM,range(c.length).map(i=>offset+i));offset+=c.length}
 let part=partition(range(n),E.filter((_,i)=>!PM.has(i)).concat(P)),G=new Map();
 P.forEach(([a,b],i)=>{A(part.get(a)===part.get(b),"plant comp");let r=part.get(a);if(!G.has(r))G.set(r,[]);G.get(r).push(i)});
 let sub=P.map(()=>rnd(3)===0);for(let idx of G.values())if(idx.reduce((s,i)=>s^Number(sub[i]),0))sub[idx[0]]=!sub[idx[0]];
 let mids=[];P.forEach(([a,b],i)=>{if(sub[i]){let x=n++;mids.push(x);add(a,x);add(x,b)}else add(a,b)});shuffle(mids);
 A(mids.length%2===0,"plant parity");while(mids.length)add(mids.pop(),mids.pop(),true);
 let g=graph(n,E,M,C),pm=new Set(g.M);g.C.forEach((c,i)=>{if(plant[i])flip(pm,c)});A(good(g,pm),"planted reference");return {g,plant,subdivisions:sub.filter(Boolean).length};
}
let R={seed:"0xce020025",positive:[],guardClosure:null};
for(let k of [4,12,30,60,100]){
 let {g,plant,subdivisions}=planted(k),s=solve(g,{},1);
 A(s.yes===true,"large positive chart");
 let initialGood=good(g,new Set(g.M));
 let result={k,n:g.n,totalSwitches:g.C.length,subdivisions,initialGood,stats:s.st};
 if(k===4){A(brute(g)[0],"small planted brute")}
 if(k===12){
  // Paid guarded chart-local forcing: recheck all unfixed switches after every force.
  let guard={},probes=0,unknown=0,forces=0,passes=0;
  while(true){passes++;let hit=false;for(let i=0;i<g.C.length;i++)if(!Object.hasOwn(guard,i)){
    let a=solve(g,{...guard,[i]:0},4),b=solve(g,{...guard,[i]:1},4);probes+=2;
    A(!(a.yes===false&&b.yes===false),"contradict SAT guard");
    unknown+=Number(a.yes===null)+Number(b.yes===null);
    if(a.yes===false||b.yes===false){guard[i]=a.yes===false?1:0;forces++;hit=true;break}
  }if(!hit)break}
  let s2=solve(g,guard,4);A(s2.yes===true,"closure lift");
  R.guardClosure={n:g.n,probes,unknown,forces,passes,guard,final:s2.st};
 }
 R.positive.push(result)
}
return R
}
console.log(JSON.stringify(audit(),null,2));
