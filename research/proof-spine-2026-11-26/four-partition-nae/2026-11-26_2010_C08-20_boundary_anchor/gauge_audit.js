function gaugeAudit(){
 let seed=7202019, tests=0,admitted=0,declined=0,checks=0,terms=0,types={TRUE:0,FALSE:0,NAE:0},multipleSinks=0,unmatchedAnchor=0;
 const rng=n=>Array.from({length:n},(_,i)=>i);function rnd(n){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n}
 function ck(v,m){checks++;if(!v)throw Error(m)}
 function matching(rows){let m=new Map();function aug(i,s){for(let [v] of rows[i])if(!s.has(v)){s.add(v);if(!m.has(v)||aug(m.get(v),s)){m.set(v,i);return true}}return false}for(let i=0;i<rows.length;i++)if(!aug(i,new Set()))return null;return m}
 function reference(rows,vs){ // Solve matching parity equations, enumerate terms only for small audit.
  let edges=[], er=rows.map(r=>[...new Set(r.map(x=>x[0]))].map(v=>{edges.push(v);return [v,edges.length-1]}));
  let equations=[],base=null;
  function rec(i,used,perm,mask){if(i===er.length){terms++;let p=0;for(let j=0;j<perm.length;j++)for(let k=j+1;k<perm.length;k++)p^=Number(perm[j]>perm[k]);if(base===null)base=[mask,p];else equations.push([mask^base[0],p^base[1]]);return}
    for(let [v,e] of er[i])if(!used.has(v)){used.add(v);rec(i+1,used,[...perm,vs.indexOf(v)],mask^(1<<e));used.delete(v)}}
  rec(0,new Set(),[],0);ck(base!==null,"missing term");
  let piv=new Map();for(let [mask,rhs] of equations){while(mask){let p=31-Math.clz32(mask);if(!piv.has(p)){piv.set(p,[mask,rhs]);break}let q=piv.get(p);mask^=q[0];rhs^=q[1]}if(!mask&&rhs)return null}
  let sol=0;for(let p=0;p<edges.length;p++)if(piv.has(p)){let [mask,rhs]=piv.get(p);for(let j=0;j<p;j++)if((mask>>j)&1)rhs^=(sol>>j)&1;sol|=rhs<<p}
  return er.map(r=>new Map(r.map(([v,e])=>[v,(sol>>e)&1])))
 }
 function summarize(rows,I,B){
   let a=I,vs=rng(I+1), cr=rows.map(r=>r.map(([v,s])=>v<I?[v,s,-1]:[a,s,v-I]));
   let M=matching(cr);if(!M)return null;
   if(!M.has(a))unmatchedAnchor++;
   let reach=vs.map(v=>new Set([v]));for(let [v,i] of M)for(let [w] of cr[i])reach[v].add(w);
   for(let v of vs)for(let w of vs)if(reach[w].has(v))for(let u of reach[v])reach[w].add(u);
   let seen=new Set(),sinks=[];
   for(let v of vs)if(!seen.has(v)){let s=vs.filter(w=>reach[v].has(w)&&reach[w].has(v));s.forEach(w=>seen.add(w));if(s.every(w=>reach[w].size===s.length))sinks.push(s)}
   if(sinks.length>1)multipleSinks++;
   let summary={type:"TRUE"};
   for(let S of sinks){
     if(S.length===1&&!M.has(S[0]))continue;
     let R=S.map(v=>cr[M.get(v)]), ref=reference(R,S);
     if(ref===null)continue;
     let pot=new Map(), stack=[], bad=false;
     // Row IDs encoded as strings; variable IDs distinct namespace.
     let graph=new Map();for(let i=0;i<R.length;i++)graph.set("r"+i,[]);for(let v of S)if(v!==a)graph.set("v"+v,[]);
     for(let i=0;i<R.length;i++)for(let [v,s] of R[i])if(v!==a){let k="r"+i,j="v"+v,c=s^ref[i].get(v);graph.get(k).push([j,c]);graph.get(j).push([k,c])}
     let start=graph.keys().next().value;pot.set(start,0);stack.push(start);
     for(let k=0;k<stack.length;k++)for(let [j,c] of graph.get(stack[k])){let p=pot.get(stack[k])^c;if(pot.has(j)){if(pot.get(j)!==p)bad=true}else{pot.set(j,p);stack.push(j)}}
     ck(pot.size===graph.size,"gauge graph disconnected");if(bad)continue;
     if(!S.includes(a))return {type:"FALSE"};
     let literals=[];for(let i=0;i<R.length;i++)for(let [v,s,b] of R[i])if(v===a)literals.push([b,s^ref[i].get(v)^pot.get("r"+i)]);
     ck(literals.length>0,"no anchor occurrence");summary={type:"NAE",literals};
   }
   return summary
 }
 function evalSum(s,w){if(s.type==="TRUE")return true;if(s.type==="FALSE")return false;let x=((w>>s.literals[0][0])&1)^s.literals[0][1];return s.literals.some(([v,c])=>(((w>>v)&1)^c)!==x)}
 // Random controls for exact interface identity, not a SAT research lane.
 for(let t=0;t<1200;t++){
  tests++;let I=1+rnd(4),B=1+rnd(4),m=1+rnd(I+2),rows=[];
  for(let j=0;j<m;j++){let k=1+rnd(4);rows.push(rng(k).map(()=>[rnd(I+B),rnd(2)]))}
  let s=summarize(rows,I,B);if(s===null){declined++;continue}admitted++;types[s.type]++;
  for(let w=0;w<(1<<B);w++){
   let ok=false;for(let z=0;z<(1<<I);z++){let bit=v=>v<I?(z>>v)&1:(w>>(v-I))&1;
    if(rows.every(r=>r.some(([v,c])=>(bit(v)^c)!==(bit(r[0][0])^r[0][1])))){ok=true;break}}
   ck(ok===evalSum(s,w),"symbolic gauge interface mismatch "+JSON.stringify({rows,I,B,w,s}));
  }
 }
 return {seed:7202019,tests,admitted,declined,checks,terms,types,multipleSinks,unmatchedAnchor,scope:"small random interface falsifiers; actual RST construction not implemented; linear system uses enumerated matching terms only at tiny size"};
}
console.log(JSON.stringify(gaugeAudit(),null,2));
