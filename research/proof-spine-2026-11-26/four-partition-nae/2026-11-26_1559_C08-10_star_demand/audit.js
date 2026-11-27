function audit(){
let checks=0;const ok=(p,m)=>{checks++;if(!p)throw Error(m)};
const bits=(w,n)=>Array.from({length:n},(_,i)=>(w>>i)&1);
const allowed=(x,d)=>{let z=0,o=0;for(let i=0;i<d;i++){z|=x[2*i]===0&&x[2*i+1]===0;o|=x[2*i]===1&&x[2*i+1]===1;}return !(z&&o)};
const original=(x,d)=>[0,1].some(t=>Array.from({length:d},(_,i)=>!(t===x[2*i]&&t===x[2*i+1])).every(Boolean));
const pairwise=(x,d)=>{for(let i=0;i<d;i++)for(let j=i+1;j<d;j++){const l=[x[2*i],x[2*i+1],1-x[2*j],1-x[2*j+1]];if(l.every(v=>v===l[0]))return false;}return true};
const local=[];
for(let d=1;d<=4;d++){
 const n=2*d, all=Array.from({length:1<<n},(_,w)=>bits(w,n)), good=all.filter(x=>original(x,d));
 let support=0,repairMin=n+1,repairSets=0,minForbidden=0;
 for(const x of all){const a=original(x,d);support+=+a;ok(a===pairwise(x,d)&&a===allowed(x,d),"local projection");}
 for(let r=0;r<(1<<n);r++){
   const outside=((1<<n)-1)^r, projection=new Set(good.map(x=>x.reduce((s,b,i)=>s|(b<<i),0)&outside));
   const free=projection.size===2**(n-bits(r,n).reduce((a,b)=>a+b,0));
   let touched=0;for(let i=0;i<d;i++)if(r&(3<<(2*i)))touched++;
   ok(free===(touched>=d-1),"repair demand");
   if(free){repairSets++;repairMin=Math.min(repairMin,bits(r,n).reduce((a,b)=>a+b,0));}
 }
 for(let t=0;t<3**n;t++){
  let a=t;const p=Array.from({length:n},()=>{let v=a%3;a=Math.floor(a/3);return v;});
  const compatible=q=>good.some(x=>q.every((b,i)=>b===2||b===x[i]));
  if(compatible(p))continue;
  let minimal=true;for(let i=0;i<n;i++)if(p[i]!==2){let q=p.slice();q[i]=2;if(!compatible(q)){minimal=false;break;}}
  if(minimal){minForbidden++;ok(p.filter(v=>v!==2).length===4,"prime width");}
 }
 ok(support===2*3**d-2**d,"support size");ok(repairMin===d-1,"minimum repairs");ok(minForbidden===d*(d-1),"prime count");
 local.push({d,support,repairMin,repairSets,minForbidden});
}
let seed=20261126;const rand=()=>{seed^=seed<<13;seed^=seed>>>17;seed^=seed<<5;return seed>>>0};
const shuf=a=>{a=a.slice();for(let i=a.length-1;i>0;i--){let j=rand()%(i+1);[a[i],a[j]]=[a[j],a[i]];}return a;};
const affineLines=()=>{let out=[];for(let i=0;i<3;i++){out.push({p:0,v:[3*i,3*i+1,3*i+2]});out.push({p:1,v:[i,3+i,6+i]});for(let s=1;s<=2;s++)out.push({p:s+1,v:[i,3+(i+s)%3,6+(i+2*s)%3]});}return out;};
const AG=()=>({n:9,clauses:affineLines(),type:"AG9",expect:false});
const cyclic=p=>({n:3*p,type:"cyclic"+p,expect:true,clauses:Array.from({length:4},(_,s)=>Array.from({length:p},(_,i)=>({p:s,v:[i,p+(i+s)%p,2*p+(i+2*s)%p]}))).flat(),w:Array.from({length:3*p},(_,i)=>+(i>=2*p))});
function ring(k,yes){let clauses=[];for(let i=0;i<k;i++)for(const c of affineLines())if(!(c.p===0&&c.v[0]===0)&&!(c.p===1&&c.v[0]===0))clauses.push({p:c.p,v:c.v.map(v=>9*i+v)});
for(let p=0;p<2;p++){let rows=Array.from({length:k},(_,i)=>({p,v:[9*i,9*i+(p===0?1:3),9*((i+1)%k)+(p===0?2:6)]}));if(yes)[rows[0].v[1],rows[1].v[1]]=[rows[1].v[1],rows[0].v[1]];clauses.push(...rows);}
return {n:9*k,clauses,type:`ring${k}-${yes?"YES":"NO"}`,expect:yes};}
function relabel(f){const p=shuf(Array.from({length:f.n},(_,i)=>i));let g={...f,clauses:shuf(f.clauses.map(c=>({p:c.p,v:c.v.map(v=>p[v])}))).map((c,id)=>({...c,id}))};if(f.w){g.w=[];f.w.forEach((v,i)=>g.w[p[i]]=v);}return g;}
function auth(f){let pairs=new Set(),ct=Array.from({length:4},()=>Array(f.n).fill(0));for(const c of f.clauses){ok(new Set(c.v).size===3,"arity");for(let v of c.v)ct[c.p][v]++;for(let i=0;i<3;i++)for(let j=i+1;j<3;j++){let key=[c.v[i],c.v[j]].sort((a,b)=>a-b).join(",");ok(!pairs.has(key),"linearity");pairs.add(key);}}ok(ct.every(a=>a.every(x=>x===1)),"four partitions");}
const sat=(clauses,x)=>clauses.every(c=>{let w=c.v.map((v,i)=>x[v]^(c.sign?.[i]??0));return !w.every(a=>a===w[0]);});
function independent(f,order){let blocked=new Set(),I=[];const neighbors=Array.from({length:f.n},()=>new Set());for(let c of f.clauses)for(let v of c.v)for(let w of c.v)neighbors[v].add(w);for(let v of order)if(!blocked.has(v)){I.push(v);for(let w of neighbors[v])blocked.add(w);}ok(I.length>=Math.ceil(f.n/9),"greedy bound");return I;}
function project(f,I){let set=new Set(I),stars=new Map(I.map(v=>[v,[]])),factors=[];for(const c of f.clauses){let v=c.v.find(v=>set.has(v));if(v===undefined)factors.push({...c,sign:[0,0,0],demand:1});else{ok(c.v.filter(w=>set.has(w)).length===1,"independent");stars.get(v).push({id:c.id,pair:c.v.filter(w=>w!==v)});}}
 const compact=factors.slice(),expanded=factors.slice();for(const [v,rows] of stars){ok(rows.length===4&&new Set(rows.flatMap(r=>r.pair)).size===8,"star");compact.push({v:rows.flatMap(r=>r.pair),demand:3,center:v,source:rows.map(r=>r.id)});for(let i=0;i<4;i++)for(let j=i+1;j<4;j++)expanded.push({v:[...rows[i].pair,...rows[j].pair],sign:[0,0,1,1],source:[rows[i].id,rows[j].id],demand:1});}
 let keys=new Set;for(const c of expanded){let a=c.v.map((v,i)=>`${v}:${c.sign[i]}`).sort().join("|"),b=c.v.map((v,i)=>`${v}:${1-c.sign[i]}`).sort().join("|");let key=a<b?a:b;ok(!keys.has(key),"no duplicate relation");keys.add(key);}
 let rem=Array.from({length:f.n},(_,i)=>i).filter(v=>!set.has(v));
 ok(expanded.length===f.clauses.length+2*I.length,"expanded count");ok(compact.reduce((s,c)=>s+c.demand,0)===f.clauses.length-I.length,"tariff");
 return {stars,expanded,compact,rem};
}
function hall(factors,n,rem){let slots=factors.flatMap(c=>Array.from({length:c.demand},()=>c.v)),match=Array(n).fill(-1),rmatch=Array(slots.length).fill(-1);function aug(i,seen){for(let v of slots[i])if(!seen.has(v)){seen.add(v);if(match[v]<0||aug(match[v],seen)){match[v]=i;rmatch[i]=v;return true;}}return false;}let size=0;for(let i=0;i<slots.length;i++)if(aug(i,new Set()))size++;
 let U=new Set(),V=new Set(),q=[];for(let i=0;i<slots.length;i++)if(rmatch[i]<0){U.add(i);q.push(i);}
 for(let k=0;k<q.length;k++)for(let v of slots[q[k]])if(!V.has(v)){V.add(v);if(match[v]>=0&&!U.has(match[v])){U.add(match[v]);q.push(match[v]);}}
 ok(size===rem.length,"saturate variables");ok(U.size===slots.length,"whole core");
 return {size,core:U.size,deficit:slots.length-size};
}
function lift(p,x){let y=x.slice();for(let [v,rows] of p.stars){let s=[0,1].find(t=>rows.every(r=>!(x[r.pair[0]]===t&&x[r.pair[1]]===t)));if(s===undefined)return null;y[v]=s;}return y;}
function geometry(f){for(let a=0;a<4;a++)for(let b=a+1;b<4;b++){let parent=Array.from({length:f.n},(_,i)=>i);let root=i=>{while(parent[i]!==i)i=parent[i];return i;};for(let c of f.clauses)if(c.p===a||c.p===b)for(let v of c.v)parent[root(v)]=root(c.v[0]);let groups=new Map;for(let v=0;v<f.n;v++){let r=root(v);if(!groups.has(r))groups.set(r,[]);groups.get(r).push(v);}if([...groups.values()].some(g=>g.length!==9))continue;
 let id=Array(f.n),base=Array(f.n),bad=false,num=0;for(let g of groups.values()){const pos=new Map(g.map((v,i)=>[v,i])),cs=f.clauses.filter(c=>c.v.every(v=>pos.has(v)));let words=[];for(let w=0;w<512;w++)if(cs.every(c=>{let a=c.v.map(v=>(w>>pos.get(v))&1);return !a.every(v=>v===a[0]);}))words.push(w);if(words.length!==2||(words[0]^words[1])!==511){bad=true;break;}for(let i=0;i<9;i++){id[g[i]]=num;base[g[i]]=(words[0]>>i)&1;}num++;}if(bad)continue;
 let adj=Array.from({length:num},()=>[]),contr=false;
 for(let c of f.clauses){let a=c.v.map(v=>[id[v],base[v]]);if(a.some(([u,s],i)=>a.some(([v,t],j)=>i!==j&&u===v&&s!==t)))continue;let d=[...new Map(a).entries()];if(d.length===1){contr=true;break;}if(d.length===2){let [[u,s],[v,t]]=d,w=1^s^t;adj[u].push([v,w]);adj[v].push([u,w]);}}
 if(contr)return {decision:false,phases:num};let val=Array(num).fill(-1),components=0;for(let u=0;u<num;u++)if(val[u]<0){components++;val[u]=0;let q=[u];for(let i=0;i<q.length;i++)for(let [v,w] of adj[q[i]]){let t=val[q[i]]^w;if(val[v]<0){val[v]=t;q.push(v);}else if(val[v]!==t)return {decision:false,phases:num};}}
 if(components===1){let x=id.map((u,v)=>val[u]^base[v]);if(sat(f.clauses,x))return {decision:true,phases:num,x};return {decision:false,phases:num};}
 }return {decision:null};}
const cases=[AG(),cyclic(5),cyclic(7),cyclic(17),cyclic(61),cyclic(257),...([3,5,9,17,33,65].flatMap(k=>[ring(k,true),ring(k,false)]))];
let data=[],fullWords=0;for(let input of cases){let f=relabel(input);auth(f);let immutable=JSON.stringify(f),I=independent(f,shuf(Array.from({length:f.n},(_,i)=>i))),p=project(f,I);ok(JSON.stringify(f)===immutable,"same source A");
 let h0=hall(f.clauses.map(c=>({...c,demand:1})),f.n,Array.from({length:f.n},(_,i)=>i)),h1=hall(p.expanded,f.n,p.rem),h2=hall(p.compact,f.n,p.rem);ok(h1.deficit===h0.deficit+3*I.length&&h2.deficit===h0.deficit,"deficit ledger");ok(JSON.stringify(f)===immutable,"same source B");
 let projectionTest=null;
 if(f.n<=15){const possible=new Set();for(let w=0;w<2**f.n;w++){let x=bits(w,f.n);fullWords++;if(sat(f.clauses,x))possible.add(p.rem.map(v=>x[v]).join(""));}let found=false;for(let w=0;w<2**p.rem.length;w++){let x=Array(f.n).fill(0);p.rem.forEach((v,i)=>x[v]=(w>>i)&1);let s=sat(p.expanded,x),l=lift(p,x);ok(s===possible.has(p.rem.map(v=>x[v]).join("")),"global projection");if(s&&l){ok(sat(f.clauses,l),"global lift");found=true;}else if(s)throw Error("lost lift");}ok(found===f.expect,"exhaustive label");projectionTest=found;}
 let g=geometry(f);if(g.decision!==null){ok(g.decision===f.expect,"geometry label");if(g.x){ok(sat(p.expanded,g.x),"geometry import");let y=lift(p,g.x);ok(y&&sat(f.clauses,y),"integrated lift");}}else if(f.w){ok(sat(f.clauses,f.w)&&sat(p.expanded,f.w),"explicit SAT control");ok(sat(f.clauses,lift(p,f.w)),"control lift");}
 ok(JSON.stringify(f)===immutable,"same source C/D");let fingerprint=2166136261;for(let i=0;i<immutable.length;i++)fingerprint=Math.imul(fingerprint^immutable.charCodeAt(i),16777619)>>>0;
 data.push({type:f.type,n:f.n,centers:I.length,originalCore:h0.core,expandedCore:h1.core,compactDemandCore:h2.core,deficit:h0.deficit,expandedDeficit:h1.deficit,compactDeficit:h2.deficit,geometry:g.decision,phases:g.phases??null,exhaustive:projectionTest,fingerprint:fingerprint.toString(16)});
}
return {seed:20261126,checks,fullWords,local,data,execution:"interleaved JS; no external solver"};
}
console.log(JSON.stringify(audit(),null,2));
