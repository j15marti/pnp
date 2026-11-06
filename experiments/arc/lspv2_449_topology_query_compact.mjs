// LSPV-2/449 compact, independent family/query regression. Node >=18.
// This is a finite host-language test, NOT a native FLMV tape experiment.
const assert = (b,m) => {if(!b) throw new Error(m)};
function graph(name) {
  let n,edges=[];
  if(name==='k4') {n=4;for(let u=0;u<4;u++)for(let v=u+1;v<4;v++)edges.push([u,v]);}
  else if(name==='cube') {n=8;for(let u=0;u<8;u++)for(let k=0;k<3;k++){let v=u^(1<<k);if(u<v)edges.push([u,v]);}}
  else if(name==='petersen') {n=10;for(let i=0;i<5;i++){edges.push([i,(i+1)%5],[i,i+5],[i+5,5+(i+2)%5]);}}
  else throw Error(name);
  edges=edges.map(([u,v])=>[Math.min(u,v),Math.max(u,v)]).sort((a,b)=>a[0]-b[0]||a[1]-b[1]);
  const inc=Array.from({length:n},()=>[]);
  edges.forEach(([u,v],i)=>{inc[u].push(i);inc[v].push(i)});
  assert(inc.every(a=>a.length===3),'not cubic');
  return {n,edges,inc};
}
function comps(n,edges,removed) {
  const seen=new Set(),result=[];
  for(let v=0;v<n;v++)if(!seen.has(v)){
    let queue=[v];seen.add(v);
    for(let i=0;i<queue.length;i++)for(let j=0;j<edges.length;j++){
      if(removed.has(j))continue;
      let [a,b]=edges[j],u=queue[i],next=a===u?b:b===u?a:-1;
      if(next>=0&&!seen.has(next)){seen.add(next);queue.push(next);}
    }
    result.push(queue);
  }
  return result;
}
const sat=(c,parts)=>parts.every(part=>part.reduce((x,v)=>x^c[v],0)===0);
function original(inc,c) {
  const clauses=[];
  for(let v=0;v<inc.length;v++){
    const e=[...inc[v]].sort((a,b)=>a-b);
    for(let p=0;p<2;p++)for(let q=0;q<2;q++){
      const s=p^q^1^c[v],signs=[p,q,s];
      clauses.push(e.map((edge,i)=>signs[i]?-(edge+1):edge+1));
    }
  }
  return clauses;
}
let assertions=0, sources=0, queries=0, shortQueries=0;
const test=(b,msg)=>{assert(b,msg);assertions++;};
for(let name of ['k4','cube','petersen']){
  const {n,edges,inc}=graph(name);const signatures=new Set();
  for(let mask=0;mask<(1<<n);mask++){
    const charge=Array.from({length:n},(_,v)=>(mask>>v)&1);
    if(charge.reduce((a,b)=>a^b,0)===0)continue;
    sources++;
    const clauses=original(inc,charge);
    test(clauses.length===4*n,'clause count');
    test(clauses.every(a=>a.length===3&&new Set(a.map(Math.abs)).size===3),'proper source');
    test(!sat(charge,comps(n,edges,new Set())),'odd source');
    const row=[];
    for(let v=0;v<n;v++){
      let post=[...charge];post[0]^=1;
      const drop=new Set(inc[v]),parts=comps(n,edges,drop);
      const answer=Number(sat(post,parts));
      const expected=1^charge[v]^Number(v===0);
      test(parts.length===2&&parts.some(p=>p.length===1),'vertex deletion connectivity');
      test(answer===expected,'4-edit query');
      row.push(answer);queries++;
    }
    signatures.add(row.join(''));
    // All one-, two- and three-edit scripts are source-independent.
    // For fixed distinct edge deletions <=2, all surviving graphs remain connected.
    const edgeSets=[new Set()];
    for(let a=0;a<edges.length;a++)edgeSets.push(new Set([a]));
    for(let a=0;a<edges.length;a++)for(let b=a+1;b<edges.length;b++)edgeSets.push(new Set([a,b]));
    for(let drop of edgeSets){
      const parts=comps(n,edges,drop);
      test(parts.length===1,'3-edge-connectivity control');
      for(let flips=0;flips<=3-drop.size;flips++){
        // Choose any reference vertex: only flip-count parity affects SAT.
        const edited=[...charge];
        if(flips&1)edited[0]^=1;
        test(Number(sat(edited,parts))===(flips&1),'<=3 edit blindness');
        shortQueries++;
      }
    }
  }
  test(signatures.size===(1<<(n-1)),'disclosure injection');
}
console.log(JSON.stringify({status:'PASS',source_count:sources,four_edit_queries:queries,short_edit_query_controls:shortQueries,assertions},null,2));