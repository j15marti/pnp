function bw16(){
 const stats={checks:0,ports:0,wires:0,pathSteps:0,closureScans:0,spanInsertions:0,products:0,proofLines:0,modelsChecked:0};function ok(x){stats.checks++;if(!x)throw Error("assertion "+stats.checks)}
 const F=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]],P=[];for(let k=0;k<3;k++)for(let b=0;b<3;b++)P.push([0,1,2].map(i=>3*i+(k*i+b)%3));for(let i=0;i<3;i++)P.push([0,1,2].map(j=>3*i+j));
 const parity=a=>{let p=0;while(a){p^=1;a&=a-1}return p};
 function physical(n,clauses,signs){
  const V=[],W=[],labels=[],groups=Array.from({length:n+clauses.length},()=>[]),rep=[],owners=[];
  function vertex(type,ls){let id=V.length;V.push({type,ps:ls.map((l,j)=>{labels.push(l);return 4*id+j}),next:0});return id}
  const take=v=>4*v+V[v].next++;
  function wire(p,q,s){W.push([p,q,s]);ok((labels[p]^labels[q])===s)}
  for(let i=0;i<clauses.length;i++){const c=clauses[i],ls=c.map((v,j)=>(1<<(v+1))^((signs[i]>>j)&1));ls.push(ls[0]^ls[1]^ls[2]);let copy=[];for(let d=0;d<2;d++){let v=vertex("B",ls);copy.push(v);for(let j=0;j<4;j++){let p=take(v),g=j<3?c[j]:n+i,s=j<3?(signs[i]>>j)&1:0;groups[g].push([p,s]);if(j<3&&rep[g]===undefined)rep[g]=[p,s]}}owners.push(copy)}
  for(let g=0;g<groups.length;g++){let a=groups[g];if(!a.length)continue;let common=labels[a[0][0]]^a[0][1];if(a.length===2){wire(a[0][0],a[1][0],a[0][1]^a[1][1]);continue}
   let path=Array.from({length:a.length/2-1},()=>vertex("E",Array(4).fill(common)));
   for(let j=1;j<path.length;j++)wire(take(path[j-1]),take(path[j]),0);
   let free=[];for(let v of path)while(V[v].next<4)free.push(take(v));ok(free.length===a.length);a.forEach(([p,s],j)=>wire(p,free[j],s))
  }
  const old=W.splice(0);for(let [p,q,s] of old){let z=Array.from({length:5},()=>vertex("E",Array(4).fill(labels[q])));for(let a=0;a<5;a++)for(let b=a+1;b<5;b++)if(a!==0||b!==1)wire(take(z[a]),take(z[b]),0);wire(p,take(z[0]),s);wire(take(z[1]),q,0)}
  const used=new Set(),pairs=new Set(),adj=Array.from({length:labels.length},()=>[]);
  function link(p,q,s){adj[p].push([q,s]);adj[q].push([p,s])}
  for(let [p,q,s] of W){ok(!used.has(p)&&!used.has(q));used.add(p);used.add(q);let a=p>>2,b=q>>2,k=[Math.min(a,b),Math.max(a,b)].join(":");ok(a!==b&&!pairs.has(k));pairs.add(k);link(p,q,s)}
  ok(used.size===labels.length);for(let v of V){ok(v.next===4);if(v.type==="E"){for(let j=1;j<4;j++){ok(labels[v.ps[0]]===labels[v.ps[j]]);link(v.ps[0],v.ps[j],0)}}else ok(v.ps.reduce((a,p)=>a^labels[p],0)===0)}
  for(let i=0;i<clauses.length;i++)for(let v of owners[i])for(let j=0;j<3;j++){let p=4*v+j,[r,t]=rep[clauses[i][j]],want=t^((signs[i]>>j)&1),seen=new Map([[p,0]]),queue=[p];for(let h=0;h<queue.length&&!seen.has(r);h++)for(let [q,s] of adj[queue[h]])if(!seen.has(q)){seen.set(q,seen.get(queue[h])^s);queue.push(q);stats.pathSteps++}ok(seen.has(r)&&seen.get(r)===want)}
  stats.ports+=labels.length;stats.wires+=W.length;
  return {V,W,labels,rep,owners};
 }
 function engine(n,clauses,signs,guard,maxD,rep){
  const M=1<<n, masks=Array.from({length:M},(_,i)=>i).sort((a,b)=>pop(a)-pop(b)||a-b),idx=[];function pop(a){let k=0;while(a){a&=a-1;k++}return k}
  masks.forEach((m,i)=>idx[m]=i);const bit=m=>1n<<BigInt(idx[m]),one=bit(0),varp=j=>bit(1<<j);
  function terms(p){let t=[];while(p){let b=p&-p;p^=b;t.push(b.toString(2).length-1)}return t}
  const top=p=>p.toString(2).length-1,deg=p=>p?pop(masks[top(p)]):-1;
  const mul=(p,j)=>terms(p).reduce((a,i)=>a^bit(masks[i]|(1<<j)),0n);
  function prod(p,q){let z=0n;for(let i of terms(p))for(let j of terms(q))z^=bit(masks[i]|masks[j]);return z}
  const literal=(j,s)=>varp(j)^(s?one:0n);
  const axioms=clauses.map(([a,b,c],i)=>prod(one^literal(a,signs[i]&1)^literal(b,(signs[i]>>1)&1),one^literal(a,signs[i]&1)^literal(c,(signs[i]>>2)&1)));
  if(guard!==null)axioms.push(varp(0)^(guard?one:0n));
  // Paid local closure: explicit small-chart feasibility/hull, no general semantic oracle.
  let chart=Array.from({length:M},(_,x)=>x).filter(x=>guard===null||(x&1)===guard);
  function value(p,x){return terms(p).reduce((a,i)=>a^+((x&masks[i])===masks[i]),0)}
  let changed=true;while(changed&&chart.length){changed=false;for(let a of axioms){stats.closureScans++;let good=chart.filter(x=>!value(a,x));if(!good.length){chart=[];break}let base=good[0],span=new Set([0]);for(let x of good){let d=x^base;if(!span.has(d))for(let z of [...span])span.add(z^d)}let next=chart.filter(x=>span.has(x^base));if(next.length<chart.length){chart=next;changed=true;break}}}
  let models=Array.from({length:M},(_,x)=>x).filter(x=>axioms.every(p=>!value(p,x)));stats.modelsChecked+=M;ok(models.every(x=>chart.includes(x)));
  let lines=[],basis=new Map(),rev=[];
  function line(p,op,a,b){ok(deg(p)<=maxD);lines.push({p,op,a,b});return lines.length-1}
  function xor(a,b){return line(lines[a].p^lines[b].p,"xor",a,b)}
  function insert(k){let p=lines[k].p;while(p){let t=top(p);if(!basis.has(t)){basis.set(t,k);stats.spanInsertions++;return true}k=xor(k,basis.get(t));p=lines[k].p}return false}
  axioms.forEach((p,i)=>{if(deg(p)<=maxD)insert(line(p,"axiom",i,0))});
  let grow=true;
  while(grow&&!basis.has(0)){grow=false;for(let j=0;j<n&&!basis.has(0);j++){
   const old=[...basis.values()],hi=new Map();
   for(let i=0;i<old.length&&!basis.has(0);i++){let p=mul(lines[old[i]].p,j),comb=1n<<BigInt(i);stats.products++;
    while(p&&deg(p)>maxD){let t=top(p);if(!hi.has(t)){hi.set(t,[p,comb]);p=null;break}let h=hi.get(t);p^=h[0];comb^=h[1]}
    if(!p)continue; // zero or stored high pivot
    let residual=p;while(residual&&basis.has(top(residual)))residual^=lines[basis.get(top(residual))].p;if(!residual)continue;
    let k=-1;for(let t=0;t<old.length;t++)if((comb>>BigInt(t))&1n)k=k<0?old[t]:xor(k,old[t]);ok(k>=0&&mul(lines[k].p,j)===p);if(insert(line(p,"mul",k,j)))grow=true;
   }
  }}
  const rejected=basis.has(0);ok(!rejected||models.length===0);
  // Independently replay all trace lines, then affine representative substitution.
  const repForms=Array.from({length:n},(_,j)=>literal(j,rep[j][1]));
  function subst(p){let z=0n;for(let i of terms(p)){let a=one,m=masks[i];for(let j=0;j<n;j++)if((m>>j)&1)a=prod(a,repForms[j]);z^=a}return z}
  const lifted=[];for(let i=0;i<lines.length;i++){let l=lines[i],p=l.p;
   if(l.op==="axiom")ok(p===axioms[l.a]);else if(l.op==="xor")ok(p===(lines[l.a].p^lines[l.b].p));else ok(p===mul(lines[l.a].p,l.b));
   let q=subst(p);ok(deg(q)<=maxD);if(l.op==="xor")ok(q===(lifted[l.a]^lifted[l.b]));if(l.op==="mul"){let z=prod(lifted[l.a],repForms[l.b]);ok(z===q);ok(deg(mul(lifted[l.a],l.b))<=maxD)}lifted.push(q)
  }
  if(rejected)ok(lifted[basis.get(0)]===one);
  stats.proofLines+=lines.length;return {models:models.length,closureWords:chart.length,rejected,traceLines:lines.length,rank:basis.size};
 }
 function run(n,cs,ss,guards,name,degreeTests){let G=physical(n,cs,ss);
  // Check the affine lift on every source word, including nonmodels. Evaluate actual B4 predicates,
  // wires and equality components. Thus all local physical axioms pull back exactly.
  for(let x=0;x<(1<<n);x++){let bits=G.labels.map(l=>parity(l&((x<<1)|1)));for(let i=0;i<cs.length;i++){let a=cs[i].map((v,j)=>((x>>v)&1)^((ss[i]>>j)&1));let bad=+(a[0]===a[1]&&a[0]===a[2]);for(let v of G.owners[i]){let p=bits.slice(4*v,4*v+4);ok(+(p.reduce((s,z)=>s+z,0)!==2)===bad);ok(((1^p[0]^p[1])&(1^p[0]^p[2]))===bad)}}}
  const out=[];for(let g of guards)for(let d of degreeTests)out.push({name,guard:g,degree:d,...engine(n,cs,ss,g,d,G.rep)});return out;
 }
 const results=[...run(7,F,F.map(()=>0),[null,0,1],"Fano",[2,3]),...run(9,P,P.map(()=>0),[null,0,1],"affine-plane",[2,3])];
 for(let i=0;i<F.length;i++)for(let j=0;j<3;j++){let ss=F.map(()=>0);ss[i]=1<<j;results.push(...run(7,F,ss,[null],"Fano sign "+i+"/"+j,[3]))}
 for(let r of results){if(r.name==="Fano"||r.name==="affine-plane"){ok(r.models===0);ok(r.rejected===(r.degree===3))}else ok(r.models===10&&!r.rejected)}
 // one-budget controls in original source only (not the direct signed NAE compiler).
 const budgets=[];for(let i=0;i<F.length;i++)for(let b=0;b<2;b++){let count=0;for(let x=0;x<128;x++)if(F.every((c,j)=>{let a=c.map(v=>(x>>v)&1);return !(a.every(v=>v===a[0])&&(j!==i||a[0]===b))}))count++;ok(count===5);budgets.push(count)}
 return {stats,results,budgetCounts:budgets,limitations:"Finite local hull enumeration; source trace plus representative algebra replay and actual signed path verification, not materialized full native proof or full native saturation. Budget neighbors source-only. No generic repair, formal kernel or measured CM."}
}
console.log(JSON.stringify(bw16(), null, 2));
