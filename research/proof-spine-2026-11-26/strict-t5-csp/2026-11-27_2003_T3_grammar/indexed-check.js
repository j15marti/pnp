function check(s){
 const C=Function(s.compiler.slice(s.compiler.indexOf("function compile("),s.compiler.indexOf("function auditLocal("))+";return compile")(),H=Function(s.hybrid.split('if(typeof require==="function"')[0]+";return {sha,norm}")(),B=JSON.parse(s.corpus),R=JSON.parse(s.registry),eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b),assert=(a,b)=>{if(!a)throw Error(b)};
 function fast(initial){
  let factors=new Map(initial.map(f=>[f.id,f])),inc=new Map(),version=new Map(),heap=[],dict=new Map(),tr=[],next=Math.max(...initial.map(f=>f.id))+1,counts={incidenceUpdates:0,eligibility:0,heapComparisons:0,heapPushes:0,heapPops:0,stale:0,maxHeap:0,wordTests:0,hits:0,keyChars:0};
  function less(a,b){counts.heapComparisons++;return a[0]<b[0]||a[0]===b[0]&&a[1]<b[1]}
  function push(x){counts.heapPushes++;let i=heap.length;heap.push(x);while(i){let p=(i-1)>>1;if(!less(heap[i],heap[p]))break;[heap[i],heap[p]]=[heap[p],heap[i]];i=p}counts.maxHeap=Math.max(counts.maxHeap,heap.length)}
  function pop(){counts.heapPops++;let x=heap[0],y=heap.pop();if(heap.length){heap[0]=y;for(let i=0;;){let j=i*2+1;if(j>=heap.length)break;if(j+1<heap.length&&less(heap[j+1],heap[j]))j++;if(!less(heap[j],heap[i]))break;[heap[i],heap[j]]=[heap[j],heap[i]];i=j}}return x}
  function insert(f){for(let v of f.vs){counts.incidenceUpdates++;if(!inc.has(v))inc.set(v,new Set());inc.get(v).add(f.id)}}
  function erase(f){factors.delete(f.id);for(let v of f.vs){counts.incidenceUpdates++;inc.get(v).delete(f.id)}}
  function bucket(v){return [...(inc.get(v)??[])].map(i=>factors.get(i))}
  function update(v){counts.eligibility++;let ver=(version.get(v)??0)+1;version.set(v,ver);let b=bucket(v);if(b.length&&b.length<=2&&new Set(b.flatMap(f=>f.vs)).size<=7)push([b.length,v,ver])}
  for(let f of initial)insert(f);for(let v of inc.keys())update(v);
  while(heap.length){let [n,v,ver]=pop();if(version.get(v)!==ver){counts.stale++;continue}let b=bucket(v);assert(b.length===n,"heap eligibility");let V=[...new Set(b.flatMap(f=>f.vs))].filter(x=>x!==v).sort((a,b)=>a-b),U=[v,...V],key=JSON.stringify([U.length,b.map(f=>[f.vs.map(x=>U.indexOf(x)),f.ok]).sort((a,b)=>JSON.stringify(a).localeCompare(JSON.stringify(b)))]);counts.keyChars+=key.length;let ok;
   if(dict.has(key)){counts.hits++;ok=dict.get(key)}else{ok=[];for(let y=0;y<2**V.length;y++){let yes=false;for(let p=0;p<2;p++){counts.wordTests++;let a=new Map(V.map((x,i)=>[x,y>>i&1]));a.set(v,p);if(b.every(f=>f.ok.includes(f.vs.reduce((w,x,i)=>w+(a.get(x)<<i),0))))yes=true}if(yes)ok.push(y)}dict.set(key,ok)}
   let out=next++;tr.push({pivot:v,in:b.map(f=>f.id),out,vs:V,ok});for(let f of b)erase(f);if(ok.length!==2**V.length){let f={id:out,vs:V,ok};factors.set(out,f);insert(f)}if(!ok.length)break;
   // Only these incident buckets changed; lazy versions invalidate all stale candidates.
   for(let x of U)update(x);
  }return {trace:tr,counts,fs:[...factors.values()],entries:dict.size}
 }
 function canon(c){let d=[...new Set(c)].sort((a,b)=>a-b);return d.some(l=>d.includes(-l))?null:d}
 function unique(F){let m=new Map();for(let c of F){let d=canon(c);if(d)m.set(d.join(","),d)}return [...m.values()]}
 function tableToCnf(fs){let F=[],checks=0;for(let f of fs){let n=f.vs.length,bad=Array.from({length:2**n},(_,i)=>i).filter(w=>!f.ok.includes(w));if(!bad.length)continue;let fixed=f.vs.map((v,i)=>[v,i,bad[0]>>i&1]).filter(([v,i,b])=>bad.every(w=>(w>>i&1)===b)),Q=bad.length===2**(n-fixed.length)?[fixed.map(([v,i,b])=>b?-v:v)]:bad.map(w=>f.vs.map((v,i)=>w>>i&1?-v:v));for(let w=0;w<2**n;w++){checks++;assert(Q.every(c=>c.some(l=>((w>>f.vs.indexOf(Math.abs(l)))&1)===Number(l>0)))===f.ok.includes(w),"cnf truth")}F.push(...Q)}return {F:unique(F),checks}}
 function propagation(F,guard){let p=new Map(guard.map(l=>[Math.abs(l),Number(l>0)])),reads=0;while(true){let cng=false;for(let c of F){let open=[],sat=false;for(let l of c){reads++;let v=Math.abs(l);if(!p.has(v))open.push(l);else if(p.get(v)===Number(l>0)){sat=true;break}}if(sat)continue;if(!open.length)return {conflict:true,reads,p};if(open.length===1){p.set(Math.abs(open[0]),Number(open[0]>0));cng=true}}if(!cng)return {conflict:false,reads,p}}}
 let out=[];
 for(let [k,id] of [["joint","JOINT-24"],["random","RANDOM-3CNF-40"]]){
  let cert=JSON.parse(s[k]),I=B.instances.find(x=>x.id===id),e=R.instances.find(x=>x.alias==="EB-"+id),G=C(I),raw=JSON.stringify(G.network)+"\n";assert(H.sha(raw)===e.sha256&&raw.length*8===e.N_bits&&H.sha(I.dimacs)===e.source_cnf.sha256&&I.dimacs.length*8===e.source_cnf.N_bits,"authentication");let S=H.norm(G.network);assert(cert.instance_id===e.instance_id&&cert.original_N_bits===e.N_bits&&cert.gauge===S.gauge&&cert.guard_id==="EMPTY"&&cert.residual_id==="ROOT","metadata");
  let t0=Date.now(),A=fast(S.factors),elapsed=Date.now()-t0;assert(eq(A.trace,cert.projection),"indexed trace");
  // Independent full occurrence scan and exact truth-table replay, with no dictionary.
  let fs=S.factors.slice(),words=0,scans=0,seen=new Set(fs.map(f=>f.id));
  for(let t of cert.projection){let b=fs.filter(f=>{scans++;return f.vs.includes(t.pivot)});let V=[...new Set(b.flatMap(f=>f.vs))].filter(x=>x!==t.pivot).sort((a,b)=>a-b);assert(b.length&&eq(b.map(f=>f.id),t.in)&&eq(V,t.vs)&&!seen.has(t.out),"scope");seen.add(t.out);let ok=[];for(let y=0;y<2**V.length;y++){let pass=false;for(let p=0;p<2;p++){words++;let val=x=>x===t.pivot?p:(y>>V.indexOf(x))&1;if(b.every(f=>f.ok.includes(f.vs.reduce((w,x,i)=>w+(val(x)<<i),0))))pass=true}if(pass)ok.push(y)}assert(eq(ok,t.ok),"projection");fs=fs.filter(f=>!b.includes(f));if(ok.length!==2**V.length)fs.push({id:t.out,vs:V,ok})}
  let {F,checks}=tableToCnf(fs),selectors=[...new Set(cert.guards.flatMap(g=>g.guard.map(Math.abs)))],cover=0,intersections=0;for(let mask=1;mask<1<<cert.guards.length;mask++){let M=new Map(),good=true,odd=0;for(let i=0;i<cert.guards.length;i++)if(mask>>i&1){odd^=1;for(let l of cert.guards[i].guard){let v=Math.abs(l),b=Number(l>0);if(M.has(v)&&M.get(v)!==b)good=false;M.set(v,b)}}if(good)cover+=(odd?1:-1)*2**(selectors.length-M.size);intersections++}assert(cover===2**selectors.length,"coverage");
  let reads=0,nodes=0;
  for(let g of cert.guards){function visit(t,guard){nodes++;let u=propagation(F,guard);reads+=u.reads;if(u.conflict){assert(t===0,"bad terminal");return}assert(Array.isArray(t)&&t.length===3&&!u.p.has(t[0]),"bad branch");for(let b of [0,1])visit(t[1+b],guard.concat(b?t[0]:-t[0]))}visit(g.tree,g.guard)}
  out.push({id,verified:true,certificateSha:H.sha(s[k]),indexed:A.counts,indexedMs:elapsed,entries:A.entries,independentReplay:{words,scans,cnfChecks:checks,guardIntersections:intersections,cover,selectors:selectors.length,nodes,literalReads:reads}})
 }return out;
}
if(typeof require==='function'){const fs=require('fs'),keys=['compiler','corpus','registry','hybrid','joint','random'];console.log(JSON.stringify(check(Object.fromEntries(keys.map((k,i)=>[k,fs.readFileSync(process.argv[i+2],'utf8')]))),null,2));}
