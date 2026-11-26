const fs=require('fs');
function audit(src) {
 const stats={A:0,B:0,C:0,assertions:0,probes:0,scans:0,kempe:0}, cap=50000;
 function ck(b,msg){stats.assertions++;if(!b)throw Error(msg);}
 const pairs=[[[0,1],[2,3]],[[0,2],[1,3]],[[0,3],[1,2]]], words=[[1,1,1,1],[1,1,2,2],[1,2,1,2],[1,2,2,1]];
 function type(w){return words.findIndex(z=>z.every((x,i)=>z.every((y,j)=>(x===y)===(w[i]===w[j]))));}
 function adj(n,E){let a=Array.from({length:n},()=>[]); E.forEach(([u,v],i)=>{a[u].push(i);if(v>=0)a[v].push(i)});return a;}
 function verify(n,E,w){return w&&w.length===E.length&&w.every(x=>x>=1&&x<=3)&&adj(n,E).every(a=>a.length===3&&new Set(a.map(i=>w[i])).size===3);}
 function color(n,E,pins={},lane="A"){
   const a=adj(n,E), w=E.map(()=>0), used=Array(n).fill(0); let nodes=0,aborted=false;
   if(E.some(([u,v])=>u===v))return {status:"NO",nodes};
   function put(i,c){const [u,v]=E[i],b=1<<c;if((used[u]&b)||(v>=0&&(used[v]&b)))return false;w[i]=c;used[u]|=b;if(v>=0)used[v]|=b;return true;}
   function pop(i,c){let [u,v]=E[i],b=1<<c;w[i]=0;used[u]^=b;if(v>=0)used[v]^=b;}
   for(const [i,c] of Object.entries(pins))if(!put(+i,c))return {status:"NO",nodes};
   function rec(){if(++nodes>cap){aborted=true;return false;}let best=-1,opts=null;
     for(let i=0;i<E.length;i++)if(!w[i]){let[u,v]=E[i],b=used[u]|(v<0?0:used[v]),o=[1,2,3].filter(c=>!(b&(1<<c)));if(!o.length)return false;if(!opts||o.length<opts.length){best=i;opts=o;if(o.length===1)break;}}
     if(best<0)return true;for(let c of opts){if(!put(best,c))throw Error("put");if(rec())return true;pop(best,c);if(aborted)return false;}return false;
   }
   const yes=rec();stats[lane]+=nodes;return {status:yes?"YES":aborted?"UNKNOWN":"NO",w:yes?w.slice():null,nodes};
 }
 function matching(n,E,lane="C"){
   const a=adj(n,E),cover=Array(n).fill(false), chosen=E.map(()=>false);let nodes=0,aborted=false,ans=null;
   if(E.some(([u,v])=>u===v||v<0))return{status:"NO",nodes};
   function terminal(){let w=chosen.map(x=>x?1:0);for(let i=0;i<E.length;i++)if(!w[i]){let start=E[i][0],v=start,e=i,c=2,len=0;do{if(w[e])return null;w[e]=c;len++;const [x,y]=E[e];v=x===v?y:x;c=5-c;let next=a[v].find(j=>j!==e&&!chosen[j]);e=next;}while(v!==start);if(len%2)return null;}return w;}
   function rec(){if(++nodes>cap){aborted=true;return false;}let v=-1,opts=null;for(let i=0;i<n;i++)if(!cover[i]){let o=a[i].filter(j=>{const[x,y]=E[j];return !cover[x===i?y:x]});if(!o.length)return false;if(!opts||o.length<opts.length){v=i;opts=o;}}
     if(v<0){ans=terminal();return !!ans;}
     cover[v]=true;for(let e of opts){let[x,y]=E[e],u=x===v?y:x;cover[u]=true;chosen[e]=true;if(rec())return true;cover[u]=false;chosen[e]=false;if(aborted)break;}cover[v]=false;return false;
   }
   const yes=rec();stats[lane]+=nodes; if(yes)ck(verify(n,E,ans),"matching lift");return{status:yes?"YES":aborted?"UNKNOWN":"NO",w:ans,nodes};
 }
 function pole(E,S,cutOrder=null){const V=[...S].sort((a,b)=>a-b),set=new Set(V),map=new Map(V.map((v,i)=>[v,i])),inside=[],boundary=[];E.forEach(([u,v],i)=>{if(set.has(u)&&set.has(v))inside.push(i);else if(set.has(u)!==set.has(v))boundary.push(i);});if(cutOrder)boundary=cutOrder.slice();let e=inside.map(i=>E[i].map(v=>map.get(v)));for(let [j,i] of boundary.entries()){let [u,v]=E[i];e.push([map.get(set.has(u)?u:v),-1-j]);}return {n:V.length,V,E:e,inside,boundary};}
 function actual(p,t,w){ck(verify(p.n,p.E,w),"pole witness");ck(type(w.slice(-4))===t,"type witness");return w;}
 function direct(p){let out={};for(let t=0;t<4;t++){let pins={};words[t].forEach((c,j)=>pins[p.E.length-4+j]=c);let r=color(p.n,p.E,pins,"A");ck(r.status!=="UNKNOWN","A cap");if(r.w)out[t]=actual(p,t,r.w);}return out;}
 function close(p,P,solver){const k=p.E.length-4, e=p.E.slice(0,k).map(x=>x.slice()),v=p.E.slice(k).map(x=>x[0]),map=[];let n=p.n;
    if(P.includes(0)){let t=P.find(x=>x!==0);for(let [i,j] of pairs[t-1]){map[i]=map[j]=e.length;e.push([v[i],v[j]]);}}
    else{let t=[1,2,3].find(x=>!P.includes(x));for(let [i,j] of pairs[t-1]){let u=n++;map[i]=e.length;e.push([v[i],u]);map[j]=e.length;e.push([v[j],u]);}e.push([n-2,n-1]);}
    stats.probes++;let r=solver(n,e);ck(r.status!=="UNKNOWN","closure cap");if(!r.w)return null;
    ck(verify(n,e,r.w),"cap coloring");let w=r.w.slice(0,k).concat(map.map(i=>r.w[i])),t=type(w.slice(-4));ck(P.includes(t),"cap incorrect type");actual(p,t,w);return{t,w};
 }
 function exchange(p,w){let k=p.E.length-4, x=w[k],y=w.slice(k).find(c=>c!==x)||([1,2,3].find(c=>c!==x));const a=adj(p.n,p.E),r=w.slice();let e=k,v=p.E[e][0];r[e]=y;let len=1;
   while(true){let j=a[v].find(i=>i!==e&&(w[i]===x||w[i]===y));ck(j!==undefined,"Kempe broken");r[j]=w[j]===x?y:x;len++;if(p.E[j][1]<0)break;let [u,z]=p.E[j];v=u===v?z:u;e=j;ck(len<=p.E.length,"Kempe loop");}
   const t=type(r.slice(-4));ck(t!==type(w.slice(-4)),"Kempe no change");actual(p,t,r);stats.kempe++;return {t,w:r};
 }
 function adaptive(p){let out={},q=0;const ask=P=>{q++;let r=close(p,P,(n,e)=>color(n,e,{},"B"));if(r)out[r.t]=r.w;return r;};
   let r=ask([0,1]);if(!r){r=ask([2,3]);if(r){let t=exchange(p,r.w);out[t.t]=t.w;}ck(q<=3,"queries");return{out,q};}
   let b=[0,1,2,3].filter(x=>x!==r.t).slice(0,2),s=ask(b);
   if(!s){let t=exchange(p,r.w);out[t.t]=t.w;return{out,q};}
   let c=[0,1,2,3].filter(x=>x!==r.t&&x!==s.t);ask(c);ck(q<=3,"queries");return{out,q};
 }
 function matchingAudit(p){let out={},rejected=[];for(let i=0;i<4;i++)for(let j=i+1;j<4;j++){let r=close(p,[i,j],(n,e)=>matching(n,e));if(r)out[r.t]=r.w;else rejected.push([i,j]);}return{out,rejected};}
 function checkPole(p){const a=direct(p),b=adaptive(p),c=matchingAudit(p),keys=Object.keys(a).map(Number),B=Object.keys(b.out).map(Number),C=Object.keys(c.out).map(Number);ck(keys.length===0||keys.length>=2,"singleton");ck(B.length===Math.min(3,keys.length),"adaptive coverage");ck(B.every(t=>keys.includes(t))&&C.every(t=>keys.includes(t)),"false type");for(let i=0;i<4;i++)for(let j=i+1;j<4;j++)ck(c.rejected.some(z=>z[0]===i&&z[1]===j)===(!keys.includes(i)&&!keys.includes(j)),"C negative");return {A:keys,B,queries:b.q,rows:b.out};}
 function scan8(n,E){const a=Array.from({length:n},()=>[]);E.forEach(([u,v])=>{a[u].push(v);a[v].push(u);});let sets=new Map();for(let i=0;i<n;i++)sets.set(String(i),[i]);
   for(let k=1;k<8;k++){let next=new Map();for(let S of sets.values()){for(let v of S)for(let u of a[v])if(!S.includes(u)){let T=[...S,u].sort((x,y)=>x-y);next.set(T.join(","),T);}}sets=next;}
   stats.scans+=sets.size;let out=[];for(let S of sets.values()){let p=pole(E,S);if(p.boundary.length===4)out.push(p);}return out;}
 function relabel(w,from,to){let map={};for(let i=0;i<4;i++){if(map[from[i]]!==undefined&&map[from[i]]!==to[i])throw Error("incompatible map");map[from[i]]=to[i];}let rem=[1,2,3].filter(x=>!Object.values(map).includes(x));for(let x of [1,2,3])if(!map[x])map[x]=rem.shift();return w.map(x=>map[x]);}
 const E=src.E,n=Math.max(...E.flat())+1;ck(n===160&&E.length===240&&src.W.filter(x=>x===0).length===1&&src.W[src.z]===0,"fingerprint dimensions");ck(adj(n,E).every(a=>a.reduce((x,i)=>x^src.W[i],0)===0),"flow");
 const rawA=color(n,E,{[src.z]:1},"A"),rawC=matching(n,E);let poles=scan8(n,E),rec=[];
 for(let p of poles){let r=checkPole(p);rec.push({V:p.V,boundary:p.boundary,...r});}
 // Integrated: only disjoint, no adjacent regions with verified exact two-wire relation.
 const selected=poles.map((p,i)=>({p,r:rec[i]})).filter(({r})=>r.B.length===2&&r.B.includes(0));
 let removed=new Set(selected.flatMap(({p})=>p.V));ck(removed.size===selected.reduce((s,{p})=>s+p.n,0),"overlap");let V=Array.from({length:n},(_,i)=>i).filter(v=>!removed.has(v)),map=new Map(V.map((v,i)=>[v,i])),red=[],orig=[],wire=[];
 E.forEach(([u,v],i)=>{if(map.has(u)&&map.has(v)){red.push([map.get(u),map.get(v)]);orig.push(i);}});
 for(let {p,r} of selected){let typ=r.B.find(x=>x!==0),ends=p.boundary.map(i=>E[i].find(v=>map.has(v)));ck(ends.every(v=>v!==undefined),"adjacent caps");let seam=[];for(let[i,j]of pairs[typ-1]){seam[i]=seam[j]=red.length;red.push([map.get(ends[i]),map.get(ends[j])]);}wire.push(seam);}
 let integrated=matching(V.length,red);ck(integrated.status==="YES","integrated");let lifted=E.map(()=>0);orig.forEach((id,i)=>lifted[id]=integrated.w[i]);selected.forEach(({p,r},i)=>{let word=wire[i].map(j=>integrated.w[j]),t=type(word),w=r.rows[t];ck(!!w,"missing stored type");let L=relabel(w,w.slice(-4),word);p.inside.concat(p.boundary).forEach((id,j)=>lifted[id]=L[j]);});let zc=lifted[src.z];lifted=lifted.map(c=>c===1?zc:c===zc?1:c);ck(verify(n,E,lifted)&&lifted[src.z]===1,"original lift");
 // Actual small poles: remove disjoint edge pair from Petersen/prism/cube; remove adjacent vertices.
 const cycle=(n,o)=>Array.from({length:n},(_,i)=>[o+i,o+(i+1)%n]);
 const pet=cycle(5,0).concat(Array.from({length:5},(_,i)=>[5+i,5+(i+2)%5]),Array.from({length:5},(_,i)=>[i,i+5]));
 const prism=k=>cycle(k,0).concat(cycle(k,k),Array.from({length:k},(_,i)=>[i,i+k]));
 function cutEdges(E,i,j){let v=[...E[i],...E[j]],n=Math.max(...E.flat())+1;if(new Set(v).size!==4)return null;let e=E.filter((_,t)=>t!==i&&t!==j).concat(v.map((x,k)=>[x,-1-k]));return{n,E:e};}
 let catalog=new Map(),all=0,queryHistogram={};
 for(let H of [pet,prism(4),prism(5),prism(6)]){
  let hn=Math.max(...H.flat())+1;for(let [u,v] of H){let p=pole(H,Array.from({length:hn},(_,i)=>i).filter(x=>x!==u&&x!==v));if(p.boundary.length!==4)continue;let a=checkPole(p);all++;queryHistogram[a.queries]=(queryHistogram[a.queries]||0)+1;let key=a.A.join("");if(!catalog.has(key))catalog.set(key,{p,a});}
  for(let i=0;i<H.length;i++)for(let j=i+1;j<H.length;j++){let p=cutEdges(H,i,j);if(!p)continue;let a=checkPole(p);all++;queryHistogram[a.queries]=(queryHistogram[a.queries]||0)+1;let key=a.A.join("");if(!catalog.has(key))catalog.set(key,{p,a});}
 }
 // Exact one-large-query gluing on catalog; rotate pole port order to get every relation.
 for(let {p} of [...catalog.values()])for(let perm of [[0,1,2,3],[0,2,1,3],[0,3,2,1]]){let k=p.E.length-4,p2={n:p.n,E:p.E.slice(0,k).concat(perm.map((j,i)=>[p.E[k+j][0],-1-i]))},a=checkPole(p2);let key=a.A.join("");if(!catalog.has(key))catalog.set(key,{p:p2,a});}
 function join(p,q){let k=p.E.length-4,l=q.E.length-4;return p.E.slice(0,k).concat(q.E.slice(0,l).map(([u,v])=>[u+p.n,v+p.n]),Array.from({length:4},(_,i)=>[p.E[k+i][0],q.E[l+i][0]+p.n]));}
 // For two-state support, use pair cap. For >=3, square cap (types 0,1,3); repair by one Kempe exchange.
 function large(p,B){if(B.length===2)return close(p,B,(n,e)=>color(n,e,{},"B"));let k=p.E.length-4,e=p.E.slice(0,k).map(x=>x.slice()),n=p.n;for(let i=0;i<4;i++)e.push([p.E[k+i][0],n+i]);for(let i=0;i<4;i++)e.push([n+i,n+(i+1)%4]);let r=color(n+4,e,{},"B");ck(r.status!=="UNKNOWN","large cap");if(!r.w)return null;let w=r.w.slice(0,k+4),t=type(w.slice(-4));actual(p,t,w);if(!B.includes(t))return exchange(p,w);return{t,w};}
 let joins={yes:0,no:0,repairs:0},examples=[];
 for(let {p,a} of catalog.values())for(let {p:q,a:b} of catalog.values()){
   const G=join(p,q),ref=matching(p.n+q.n,G);ck(ref.status!=="UNKNOWN","join ref");
   let before=stats.kempe,r=a.B.length?large(q,a.B):null;joins.repairs+=stats.kempe-before;
   ck(!!r===(ref.status==="YES"),"join mismatch");if(r){let w=a.rows[r.t],l=relabel(w,w.slice(-4),r.w.slice(-4)),full=l.slice(0,-4).concat(r.w.slice(0,-4),r.w.slice(-4));ck(verify(p.n+q.n,G,full),"join lift");joins.yes++;if(!examples.some(x=>x.status==="YES"))examples.push({status:"YES",E:G,w:full,A:a.A,B:b.A});}else{joins.no++;if(!examples.some(x=>x.status==="NO"))examples.push({status:"NO",E:G,A:a.A,B:b.A});}
 }
 let recurrence=0;for(let N=12;N<=256;N+=2)for(let s=6;s<=N/2;s+=2){let x=BigInt(N),y=BigInt(s);ck(3n*(y+2n)**8n+(x-y+4n)**8n<=x**8n-1n,"recurrence");recurrence++;}
 return {source:src,stats,rawA:{status:rawA.status,nodes:rawA.nodes},rawC:{status:rawC.status,nodes:rawC.nodes},poles:rec,selected:selected.length,integrated:{n:V.length,E:red,nodes:integrated.nodes,lifted,matching:lifted.map((c,i)=>c===1?i:-1).filter(i=>i>=0)},catalog:{tests:all,types:[...catalog.keys()],queryHistogram,joins,examples},recurrence};
}
const raw=JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));console.log(JSON.stringify(audit(raw.source||raw),null,2));
