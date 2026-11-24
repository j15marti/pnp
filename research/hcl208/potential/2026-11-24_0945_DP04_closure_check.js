function runDP04(){
 const Q=[0,1,2,3],pairs=[];for(let i=0;i<4;i++)for(let j=i+1;j<4;j++)pairs.push([i,j]);
 let seed=240945;function rng(n){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return (seed>>>8)%n}
 const C={queries:0,closureScans:0,deleted:0,searchNodes:0,tupleChecks:0,summaryChecks:0,liftEdges:0,referenceNodes:0,regions:0,storedWitnesses:0};
 function ok(x,es){return es.every(([u,v,s])=>(x[u]^x[v])!==s)}
 function solveLocal(n,cs,probe,closeOnly=false){
  if(closeOnly) C.unconditionalClosures=(C.unconditionalClosures||0)+1;else C.queries++;let constraints=probe?cs.concat([probe]):cs;
  function search(dom){C.searchNodes++;
   while(true){C.closureScans++;let change=false;
    outer:for(const {vs,fn} of constraints){let sup=vs.map(()=>0),x=Array(n).fill(0);
     function rec(i){if(i===vs.length){C.tupleChecks++;if(fn(x))for(let j=0;j<vs.length;j++)sup[j]|=1<<x[vs[j]];return}let v=vs[i];for(let z of Q)if(dom[v]&(1<<z)){x[v]=z;rec(i+1)}}
     rec(0);for(let j=0;j<vs.length;j++){let v=vs[j],next=dom[v]&sup[j];if(!next)return null;if(next!==dom[v]){C.deleted++;dom[v]=next;change=true;break outer}}
    }if(!change)break;
   }
   if(closeOnly)return dom;
   let v=dom.findIndex(d=>d&(d-1));if(v<0)return dom.map(d=>Q.find(z=>d&(1<<z)));
   for(let z of Q)if(dom[v]&(1<<z)){let d=dom.slice();d[v]=1<<z;let x=search(d);if(x)return x}return null
  }
  return search(Array(n).fill(15))
 }
 function edgeConstraint(u,v,s){return {vs:[...new Set([u,v])],fn:x=>(x[u]^x[v])!==s}}
 function eqConstraint(u,v,s){return {vs:[...new Set([u,v])],fn:x=>(x[u]^x[v])===s}}
 // Tree input: nodes ordered parent before child. Cross edges [parent local, child local, label].
 function solveTree(nodes){
  const m=nodes.length,cache=Array(m),children=Array.from({length:m},()=>[]);
  for(let i=1;i<m;i++){if(nodes[i].p>=i||nodes[i].cross.length!==4)throw Error("bad source");children[nodes[i].p].push(i)}
  for(let i=m-1;i>=0;i--){C.regions++;let v=nodes[i],cs=v.es.map(e=>edgeConstraint(...e));
   if(!solveLocal(v.n,cs,null,true))return null;
   for(let j of children[i]){let e=nodes[j].cross,masks=cache[j].masks;
    if(!masks.some(Boolean))return null;
    cs.push({vs:[...new Set(e.map(z=>z[0]))],fn:x=>pairs.some(([a,b],k)=>{C.summaryChecks++;return masks[k]&(1<<(x[e[a][0]]^x[e[b][0]]^e[a][2]^e[b][2]))})})
    if(!solveLocal(v.n,cs,null,true))return null;
   }
   if(i===0){let w=solveLocal(v.n,cs,null);if(!w)return null;cache[i]={w};C.storedWitnesses++;continue}
   let masks=Array(6).fill(0),w=Array.from({length:6},()=>Array(4).fill(null));let e=v.cross;
   for(let k=0;k<6;k++){let[a,b]=pairs[k];for(let z of Q){let sol=solveLocal(v.n,cs,eqConstraint(e[a][1],e[b][1],z));if(sol){masks[k]|=1<<z;w[k][z]=sol;C.storedWitnesses++}}}
   cache[i]={masks,w};
  }
  let out=Array(m);function lift(i,w,shift){let x=w.map(z=>z^shift);out[i]=x;
   for(let j of children[i]){let e=nodes[j].cross,found=false;for(let k=0;k<6&&!found;k++){let[a,b]=pairs[k],z=x[e[a][0]]^x[e[b][0]]^e[a][2]^e[b][2];let y=cache[j].w[k][z];if(!y)continue;
    for(let t of Q)if(e.every(([u,v,s])=>(x[u]^y[v]^t)!==s)){lift(j,y,t);found=true;break}
   }if(!found)throw Error("lift")}
  }lift(0,cache[0].w,0);
  for(let i=0;i<m;i++){if(!ok(out[i],nodes[i].es))throw Error("local");for(let [u,v,s] of nodes[i].cross||[]){C.liftEdges++;if((out[nodes[i].p][u]^out[i][v])===s)throw Error("cross")}}
  return out
 }
 function flatten(nodes){let offsets=[],n=0,es=[];for(let v of nodes){offsets.push(n);n+=v.n}nodes.forEach((v,i)=>{for(let[u,w,s]of v.es)es.push([u+offsets[i],w+offsets[i],s]);for(let[u,w,s]of v.cross||[])es.push([u+offsets[v.p],w+offsets[i],s])});return{n,es}}
 function reference(n,es){let x=Array(n).fill(-1),inc=Array.from({length:n},()=>[]);for(let [u,v,s]of es){inc[u].push([v,s]);if(u!==v)inc[v].push([u,s])}
  function rec(i){C.referenceNodes++;if(i===n)return x.slice();for(let z of Q){x[i]=z;if(inc[i].every(([j,s])=>x[j]===-1||(z^x[j])!==s)){let r=rec(i+1);if(r)return r}}x[i]=-1;return null}
  return rec(0)}
 function test(nodes){let {n,es}=flatten(nodes),a=solveTree(nodes),b=reference(n,es);if(!!a!==!!b)throw Error("decision mismatch");if(a&&!ok(a.flat(),es))throw Error("bad lift");return !!a}
 let random={SAT:0,UNSAT:0};for(let t=0;t<180;t++){let m=2+rng(3),nodes=[];for(let i=0;i<m;i++){let es=[];for(let j=0;j<rng(5);j++)es.push([0,1,rng(4)]);let v={n:2,es};if(i){v.p=rng(i);v.cross=Array.from({length:4},()=>[rng(2),rng(2),rng(4)])}nodes.push(v)}if(t%6===0)nodes[m-1].es=Q.map(s=>[0,1,s]);random[test(nodes)?"SAT":"UNSAT"]++}
 function star(n,es){let nodes=[{n,es:[]}];for(let[u,v]of es)nodes.push({p:0,n:1,es:[],cross:[[u,0,1],[u,0,2],[u,0,3],[v,0,0]]});return nodes}
 let E=[];for(let i=0;i<5;i++)for(let j=i+1;j<5;j++)E.push([i,j]);
 let starCases=[test(star(5,E)),...E.map((_,k)=>test(star(5,E.filter((_,i)=>i!==k))))];if(starCases[0]||starCases.slice(1).some(x=>!x))throw Error("K5");
 let scale=[];for(let n of [8,16,32,64,128]){let nodes=[{n:2,es:[[0,1,0]]}];for(let i=1;i<n;i++)nodes.push({p:i-1,n:2,es:[[0,1,0]],cross:[[0,0,1],[0,0,2],[0,0,3],[1,0,0]]});
 let q=C.queries,w=C.storedWitnesses;let a=solveTree(nodes);if(!a)throw Error("chain");scale.push({regions:n,queries:C.queries-q,storedWitnesses:C.storedWitnesses-w});nodes[n-1].es=Q.map(s=>[0,1,s]);if(solveTree(nodes))throw Error("bad chain")}
 // Pair summary controls, normalized child and parent words.
 function words(k){let out=[];for(let j=0;j<4**(k-1);j++){let x=[0],v=j;for(let i=1;i<k;i++){x.push(v%4);v=Math.floor(v/4)}out.push(x)}return out}
 let W=words(4),profileChecks=0;for(let t=0;t<100;t++){let R=W.filter(()=>rng(4)===0);let masks=pairs.map(([a,b])=>R.reduce((m,x)=>m|1<<(x[a]^x[b]),0));let s=Q.map(()=>rng(4));for(let x of W){let a=R.some(y=>Q.some(z=>x.every((v,i)=>(v^y[i]^s[i]^z)!==0)));let b=pairs.some(([i,j],k)=>masks[k]&(1<<(x[i]^x[j]^s[i]^s[j])));if(a!==b)throw Error("profile");profileChecks++}}
 let W5=words(5),bad=W5.filter(x=>new Set(x).size===4),good=W5;function profile5(R){let out=[];for(let i=0;i<5;i++)for(let j=i+1;j<5;j++)out.push(R.reduce((m,x)=>m|1<<(x[i]^x[j]),0));return out}
 let counter={badWords:bad.length,goodWords:good.length,sameMasks:JSON.stringify(profile5(bad))===JSON.stringify(profile5(good)),badGlue:bad.some(x=>new Set(x).size<4),goodGlue:good.some(x=>new Set(x).size<4)};if(!counter.sameMasks||counter.badGlue||!counter.goodGlue)throw Error("5-cut");
 let fano=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]],owners=fano.flatMap(t=>[0,1].map(b=>[t,b]));
 function fcount(drop){let c=0;for(let a=0;a<128;a++)if(owners.every(([t,b],i)=>i===drop||t.some(v=>((a>>v)&1)===b)))c++;return c}
 let fanoCounts=[fcount(-1),...owners.map((_,i)=>fcount(i))];if(fanoCounts[0]||fanoCounts.slice(1).some(x=>x!==5))throw Error("fano");
 return {seed:240945,random,starCases,scale,profileChecks,counter,fanoCounts,counters:C,discrepancies:0}
}
console.log(JSON.stringify(runDP04(),null,2));
