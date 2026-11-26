function audit(){
 const assert=(p,m)=>{if(!p)throw Error(m)};
 let seed=20261126, calls=0; const rand=n=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n};
 function dsu(n){let p=Array.from({length:n},(_,i)=>i);function find(x){while(p[x]!==x){p[x]=p[p[x]];x=p[x]}return x}return {find,join(a,b){a=find(a);b=find(b);if(a===b)return false;p[b]=a;return true}}}
 function blossom(g){
   const n=g.length,mt=Array(n).fill(-1);
   function search(root){
     let p=Array(n).fill(-1),b=Array.from({length:n},(_,i)=>i),used=Array(n).fill(false),q=[root];used[root]=true;
     function lca(a,c){let seen=Array(n).fill(false);while(true){a=b[a];seen[a]=true;if(mt[a]===-1)break;a=p[mt[a]]}while(true){c=b[c];if(seen[c])return c;c=p[mt[c]]}}
     function mark(v,x,child,fl){while(b[v]!==x){fl[b[v]]=fl[b[mt[v]]]=true;p[v]=child;child=mt[v];v=p[mt[v]]}}
     for(let h=0;h<q.length;h++){let v=q[h];for(let u of g[v]){
       if(b[v]===b[u]||mt[v]===u)continue;
       if(u===root||(mt[u]!==-1&&p[mt[u]]!==-1)){
         let x=lca(v,u),fl=Array(n).fill(false);mark(v,x,u,fl);mark(u,x,v,fl);
         for(let i=0;i<n;i++)if(fl[b[i]]){b[i]=x;if(!used[i]){used[i]=true;q.push(i)}}
       }else if(p[u]===-1){p[u]=v;if(mt[u]===-1){let z=u;while(z!==-1){let a=p[z],c=a===-1?-1:mt[a];mt[z]=a;if(a!==-1)mt[a]=z;z=c}return true}let z=mt[u];used[z]=true;q.push(z)}
     }}return false;
   }
   for(let i=0;i<n;i++)if(mt[i]===-1)search(i);return mt;
 }
 function occ(rows){let a=new Map;rows.forEach((r,i)=>r.forEach(v=>{if(!a.has(v))a.set(v,[]);a.get(v).push(i)}));return a}
 function valid(rows,w,pins=new Map){return rows.every(r=>r.reduce((s,v)=>s+w.get(v),0)===2)&&[...pins].every(([v,b])=>w.get(v)===b)}
 function local(rows,pins){
   calls++;let g=[],slots=[],ports=new Map,free=[],w=new Map;const node=()=>{g.push([]);return g.length-1},edge=(a,b)=>{g[a].push(b);g[b].push(a)};
   let total=0, o=occ(rows);
   for(let [v] of o)if(pins.has(v))w.set(v,pins.get(v));
   for(let r of rows){let t=2-r.reduce((s,v)=>s+(pins.has(v)?pins.get(v):0),0),l=r.filter(v=>!pins.has(v)).length;if(t<0||t>l)return null;slots.push(Array.from({length:t},node));total+=t}
   for(let [v,is] of o){if(pins.has(v))continue;assert(is.length<=2,"local degree");let a=node(),b=node();edge(a,b);for(let s of slots[is[0]])edge(a,s);if(is.length===2){for(let s of slots[is[1]])edge(b,s)}else free.push(b);ports.set(v,[a,b])}
   if(total%2)free.push(node());for(let i=0;i<free.length;i++)for(let j=0;j<i;j++)edge(free[i],free[j]);
   let mt=blossom(g);if(mt.includes(-1))return null;
   for(let [v,[a,b]] of ports)w.set(v,+(mt[a]!==b));assert(valid(rows,w),"matching lift");return w;
 }
 function chart(rows,pins){
   let o=occ(rows),d=dsu(rows.length);for(let [v,is] of o)if(!pins.has(v)&&is.length===2)d.join(...is);
   let by=new Map;rows.forEach((r,i)=>{let k=d.find(i);if(!by.has(k))by.set(k,[]);by.get(k).push(i)});let regions=[...by.values()],ri=Array(rows.length);regions.forEach((a,k)=>a.forEach(i=>ri[i]=k));
   let high=[...o].filter(([v,is])=>!pins.has(v)&&is.length>2),R=regions.length,adj=Array.from({length:R+high.length},()=>[]),bad=new Set, e=[];
   high.forEach(([v,is],j)=>{let m=new Map;for(let i of is)m.set(ri[i],(m.get(ri[i])||0)+1);if([...m.values()].some(x=>x>2))bad.add(j);for(let k of m.keys())e.push([k,R+j])});
   let f=dsu(adj.length),cut=new Set(bad);for(let [a,b] of e)if(!bad.has(b-R)&&!f.join(a,b))cut.add(b-R);
   for(let [a,b] of e)if(!cut.has(b-R)){adj[a].push(b);adj[b].push(a)}
   return {regions:regions.map(a=>a.map(i=>rows[i])),high:high.map(a=>a[0]),R,adj,cut:[...cut].map(j=>high[j][0]),bad:bad.size};
 }
 function solve(rows,pins=new Map,cap=12){
   let {regions,high,R,adj,cut,bad}=chart(rows,pins),attempts=0;if(cut.length>cap)return {w:null,unknown:true,h:cut.length,bad,regions:R,attempts};
   for(let bits=0;bits<2**cut.length;bits++){attempts++;let pp=new Map(pins);cut.forEach((v,i)=>pp.set(v,(bits>>i)&1));let seen=new Set,w=new Map(pp),ok=true;
     function put(v,b){assert(!w.has(v)||w.get(v)===b,"glue");w.set(v,b)}
     function visit(u,parent){
       assert(!seen.has(u),"quotient cycle");seen.add(u);
       let kids=adj[u].filter(v=>v!==parent).map(v=>[v,visit(v,u)]);
       if(u>=R){let dom=[0,1].filter(b=>kids.every(([v,M])=>M[b]!==null));return dom.map(b=>b) /* variable message is list of allowed bits */}
       let results=[];for(let b=0;b<(parent<0?1:2);b++){
         let p=new Map(pp),fail=false;for(let [v,D] of kids){if(!D.length){fail=true;break}if(D.length===1)p.set(high[v-R],D[0])}
         if(parent>=0)p.set(high[parent-R],b);
         let a=fail?null:local(regions[u],p);results.push(a===null?null:{a,kids});
       }return results;
     }
     // child region responses need retained messages at variable nodes for reconstruction
     const memo=new Map;
     function rec(u,parent){
       assert(!seen.has(u),"cycle");seen.add(u);let kids=adj[u].filter(v=>v!==parent).map(v=>[v,rec(v,u)]),out;
       if(u>=R)out={dom:[0,1].filter(b=>kids.every(([v,M])=>M.rows[b]!==null)),kids};
       else {let M=[];for(let b=0;b<(parent<0?1:2);b++){let p=new Map(pp),fail=false;for(let [v,D] of kids){if(!D.dom.length){fail=true;break}if(D.dom.length===1)p.set(high[v-R],D.dom[0])}if(parent>=0)p.set(high[parent-R],b);M.push(fail?null:local(regions[u],p))}out={rows:M,kids}}
       memo.set(u,out);return out;
     }
     function lift(u,b){let M=memo.get(u);if(u>=R){put(high[u-R],b);for(let [v] of M.kids)lift(v,b)}else{let a=M.rows[b];assert(a!==null,"unattainable");for(let [v,z] of a)put(v,z);for(let [v] of M.kids)lift(v,a.get(high[v-R]))}}
     for(let u=0;u<R;u++)if(!seen.has(u)){let m=rec(u,-1);if(m.rows[0]===null){ok=false;break}lift(u,0)}
     if(ok){assert(valid(rows,w,pins),"global lift");return {w,unknown:false,h:cut.length,bad,regions:R,attempts}}
   }return {w:null,unknown:false,h:cut.length,bad,regions:R,attempts}
 }
 function brute(rows,pins){let vars=[...occ(rows).keys()];assert(vars.length<=20,"brute cap");for(let k=0;k<2**vars.length;k++){let w=new Map(vars.map((v,i)=>[v,(k>>i)&1]));if(valid(rows,w,pins))return w}return null}
 // Certified local equality subtraction, then generalized occupancy propagation on quotient rows.
 function closure(rows,pins=new Map){
   let vs=[...occ(rows).keys()],idx=new Map(vs.map((v,i)=>[v,i])),d=dsu(vs.length),seen=new Map,joins=0,rounds=0;
   for(let r of rows)for(let j=0;j<4;j++){let key=r.filter((_,i)=>i!==j).sort((a,b)=>a-b).join(",");if(seen.has(key)){if(d.join(idx.get(r[j]),idx.get(seen.get(key))))joins++}else seen.set(key,r[j])}
   let a=rows.map(r=>r.map(v=>d.find(idx.get(v)))),p=new Map;
   for(let [v,b] of pins){let u=d.find(idx.get(v));if(p.has(u)&&p.get(u)!==b)return {no:true,joins,rounds};p.set(u,b)}
   let change=true;while(change){change=false;rounds++;for(let r of a){let u=[...new Set(r)],supports=u.map(()=>new Set),num=0;for(let k=0;k<2**u.length;k++){let w=new Map(u.map((v,i)=>[v,(k>>i)&1]));if(r.reduce((s,v)=>s+w.get(v),0)!==2||u.some(v=>p.has(v)&&p.get(v)!==w.get(v)))continue;num++;u.forEach((v,i)=>supports[i].add(w.get(v)))}if(!num)return {no:true,joins,rounds};u.forEach((v,i)=>{if(supports[i].size===1&&!p.has(v)){p.set(v,[...supports[i]][0]);change=true}})}}
   // Try a canonical lift (not a completeness assertion); fill free equality classes with zero,
   // then choose locally private triples in the equality gadgets separately through original rows.
   return {no:false,joins,rounds};
 }
 function eqGraph(n,edges,neg=false){let rows=[],next=n;for(let [u,v] of edges){let p=next++,q=next++,r=next++;rows.push([u,p,q,r],[v,p,q,r])}if(neg)rows.push([0,1,2,3]);return rows}
 function grid(k){let e=[];for(let i=0;i<k;i++)for(let j=0;j<k;j++){let v=i*k+j;if(i+1<k)e.push([v,v+k]);if(j+1<k)e.push([v,v+1])}return e}
 function allEqualWitness(rows,n){let w=new Map;for(let i=0;i<n;i++)w.set(i,0);for(let i=0;i<rows.length;i+=2){let [u,p,q,r]=rows[i];w.set(p,1);w.set(q,1);w.set(r,0)}assert(valid(rows,w),"grid equality witness");return w}
 let random=0,randomSat=0,randomNo=0,randomClosure=0,matchingControls=0,matchingSat=0;
 // degree<=2 residuals including pins; independent exhaustive source reference
 for(let t=0;t<180;t++){let rows=[],counts=Array(9).fill(0);for(let j=0;j<4;j++){let cand=counts.map((c,i)=>i).filter(i=>counts[i]<2);if(cand.length<4)break;let r=[];for(let k=0;k<4;k++){let i=rand(cand.length),v=cand.splice(i,1)[0];r.push(v);counts[v]++}rows.push(r)}let pins=new Map;for(let v of occ(rows).keys())if(rand(4)===0)pins.set(v,rand(2));let a=local(rows,pins),b=brute(rows,pins);assert(!!a===!!b,"local reference");matchingControls++;matchingSat+=+!!b}
 for(let t=0;t<220;t++){let rows=[];for(let j=0;j<1+rand(7);j++){let c=Array.from({length:8},(_,i)=>i),r=[];for(let k=0;k<4;k++)r.push(c.splice(rand(c.length),1)[0]);rows.push(r)}let pins=new Map;for(let v of occ(rows).keys())if(rand(5)===0)pins.set(v,rand(2));let cl=closure(rows,pins),a=solve(rows,pins),b=brute(rows,pins);assert(!a.unknown&&!!a.w===!!b,"tree reference");assert(!cl.no||!b,"closure false NO");randomClosure+=+cl.no;random++;randomSat+=+!!b;randomNo+=+!b}
 let trees=[],grids=[];
 for(let n of [16,32,64,128,256]){let e=Array.from({length:n-1},(_,i)=>[Math.floor(i/2),i+1]);let pair=[];for(let neg of [false,true]){let rows=eqGraph(n,e,neg),cl=closure(rows),start=calls,a=solve(rows);assert(!a.unknown&&!!a.w===!neg,"tree pair");assert(cl.no===neg,"tree equality closure");pair.push({rows:rows.length,vars:occ(rows).size,h:a.h,regions:a.regions,attempts:a.attempts,matchingCalls:calls-start,closure:cl})}trees.push({n,sat:pair[0],unsat:pair[1]})}
 for(let k of [4,8,16,24]){let e=grid(k),p=eqGraph(k*k,e,false),q=eqGraph(k*k,e,true),a=closure(p),b=closure(q),c=chart(p,new Map);assert(!a.no&&b.no,"grid closure");allEqualWitness(p,k*k);grids.push({k,rows:p.length,vars:occ(p).size,h:c.cut.length,bad:c.bad,joins:a.joins,unsatRows:q.length,negativeClosure:b.no})}
 // Four-port equality barrier: actual native star with each port appearing once.
 let star=eqGraph(5,[[0,1],[0,2],[0,3],[0,4]]),relation=[];
 for(let b=0;b<16;b++){let p=new Map(Array.from({length:4},(_,i)=>[i+1,(b>>i)&1]));if(brute(star,p))relation.push(b)}
 assert(relation.join(",")==="0,15","star relation");
 return {seed:20261126,random,randomSat,randomNo,randomClosure,matchingControls,matchingSat,matchingNo:matchingControls-matchingSat,calls,trees,grids,starRelation:relation};
}
console.log(JSON.stringify(audit(),null,2));
