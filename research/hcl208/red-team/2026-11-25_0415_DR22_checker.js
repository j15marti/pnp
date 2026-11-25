// Run with node; deterministic.
function dr22(){
  let checks=0; const ok=(x)=>{checks++;if(!x)throw Error("failed assertion "+checks)};
  const pop=x=>{let p=0;while(x){p^=x&1;x>>>=1}return p};
  const nae=(a,b,c)=>a!==b||b!==c;
  // Local truth-table compiler: forbidden patterns have parity opposite the charge.
  for(let b=0;b<2;b++)for(let x=0;x<8;x++){
    let feasible=true;
    for(let f=0;f<8;f++)if(pop(f)!==b){
      let a=(x^f)&1,d=((x^f)>>1)&1,c=((x^f)>>2)&1;
      let t=Number(!a&&!d);
      let possible=[0,1].some(z=>nae(a,d,z)&&nae(z^1,c,0));
      ok(possible===Boolean(a||d||c));
      if(pop(x)===b)ok(nae(a,d,t)&&nae(t^1,c,0));
      feasible=feasible&&possible;
    }
    ok(feasible===(pop(x)===b));
  }
  // Every distinct-variable signed NAE owner has full local affine hull.
  for(let f=0;f<8;f++)for(let a=1;a<8;a++){
    let vals=new Set();for(let x=0;x<8;x++)if(x!==f&&x!==(f^7))vals.add(pop(a&x));
    ok(vals.size===2);
  }
  function graph(m){
    let vs=[],ids=new Map(),edges=[],stars=[];
    for(let i=0;i<m;i++)for(let j=0;j<m;j++)if(i!==j){ids.set(i*m+j,vs.length);vs.push([i,j]);stars.push([])}
    function add(u,v){let e=edges.length;edges.push([u,v]);stars[u].push(e);stars[v].push(e)}
    for(let i=0;i<m;i++){
      let cyc=vs.map((v,k)=>[v,k]).filter(([v])=>v[0]===i).map(([,k])=>k);
      for(let k=0;k<cyc.length;k++)add(cyc[k],cyc[(k+1)%cyc.length]);
    }
    for(let i=0;i<m;i++)for(let j=i+1;j<m;j++)add(ids.get(i*m+j),ids.get(j*m+i));
    let E=edges.length,V=vs.length,charge=Array(V).fill(0);charge[0]=1;
    let descriptors=[{kind:"g",scope:-1}],owners=[];
    for(let e=0;e<E;e++)descriptors.push({kind:"x",e,scope:edges[e][0]});
    for(let v=0;v<V;v++){
      ok(stars[v].length===3);
      let [a,b,c]=stars[v].map(e=>e+1);
      for(let f=0;f<8;f++)if(pop(f)!==charge[v]){
        let t=descriptors.length;descriptors.push({kind:"t",f,scope:v});
        owners.push([[a,f&1],[b,(f>>1)&1],[t,0]]);
        owners.push([[t,1],[c,(f>>2)&1],[0,0]]);
      }
    }
    return {m,V,E,vs,edges,stars,charge,descriptors,owners};
  }
  function pair(g,i,j){
    let a=g.descriptors[i],b=g.descriptors[j],sc=[...new Set([a.scope,b.scope].filter(v=>v>=0))];
    let es=[...new Set(sc.flatMap(v=>g.stars[v]))];
    let local=new Map(es.map((e,k)=>[e,k]));
    let value=(d,w)=>{if(d.kind==="g")return 0;if(d.kind==="x")return(w>>local.get(d.e))&1;let z=g.stars[d.scope].map(e=>(w>>local.get(e))&1);return Number(!(z[0]^(d.f&1))&&!(z[1]^((d.f>>1)&1)))};
    let counts=[0,0];
    for(let w=0;w<(1<<es.length);w++){
      if(sc.some(v=>g.stars[v].reduce((p,e)=>p^((w>>local.get(e))&1),0)!==g.charge[v]))continue;
      counts[value(a,w)^value(b,w)]++;
    }
    ok(counts[0]>0&&counts[1]>0);return counts;
  }
  function controls(m,all){
    let g=graph(m),P=g.descriptors.length;
    let nPairs=0,minMinority=1,seed=20261125;
    let trial=(i,j)=>{if(i===j)return;let c=pair(g,i,j);minMinority=Math.min(minMinority,Math.min(...c)/(c[0]+c[1]));nPairs++};
    if(all)for(let i=0;i<P;i++)for(let j=0;j<i;j++)trial(i,j);
    else for(let k=0;k<2048;k++){seed=(Math.imul(seed,1664525)+1013904223)>>>0;let i=seed%P;seed=(Math.imul(seed,1664525)+1013904223)>>>0;trial(i,seed%P)}
    // Authenticated all-zero source word: exactly one original vertex fails.
    let x=Array(P).fill(0);for(let i=1;i<P;i++){let d=g.descriptors[i];if(d.kind==="t")x[i]=Number(!(d.f&1)&&!((d.f>>1)&1))}
    let bad=[];for(let i=0;i<g.owners.length;i++){let l=g.owners[i].map(([v,s])=>x[v]^s);if(!nae(...l))bad.push(i)}
    ok(bad.length===1);let badId=bad[0],flip=g.owners[badId].map(p=>p.slice());flip[1][1]^=1;ok(nae(...flip.map(([v,s])=>x[v]^s)));
    // Decode actual signed owner list using authenticated gauge id 0 and degree-2 private ids.
    let occ=Array.from({length:P},()=>[]);g.owners.forEach((o,k)=>o.forEach(([v])=>occ[v].push(k)));
    let groups=new Map(),used=new Set();
    for(let t=1;t<P;t++)if(occ[t].length===2){
      let [i,j]=occ[t];if(g.owners[i].some(([v])=>v===0))[i,j]=[j,i];
      let a=g.owners[i],b=g.owners[j];ok(a[2][0]===t&&a[2][1]===0&&b[0][0]===t&&b[0][1]===1&&b[2][0]===0&&b[2][1]===0);
      let key=[a[0][0],a[1][0],b[1][0]].join(",");let f=a[0][1]+2*a[1][1]+4*b[1][1];
      if(!groups.has(key))groups.set(key,[]);groups.get(key).push(f);used.add(i);used.add(j);
    }
    ok(used.size===g.owners.length&&groups.size===g.V);
    let total=0;let count=new Map();
    for(let [k,fs] of groups){ok(fs.length===4&&new Set(fs).size===4&&fs.every(f=>pop(f)===pop(fs[0])));total^=1^pop(fs[0]);for(let e of k.split(","))count.set(e,(count.get(e)||0)+1)}
    ok(total===1&&count.size===g.E&&[...count.values()].every(n=>n===2));
    return {m,vertices:g.V,edges:g.E,targetVariables:P,owners:g.owners.length,pairChecks:nPairs,minMinority,oddChargeContradiction:true,oneOwnerDeletedSAT:true,oneLiteralFlippedSAT:true,badOwnerIndex:badId,decodedXorRows:groups.size,localOwnerAffineClosure:"no deductions by truth table",fullMomentMatrixBuilt:false,guard:[],sourceMap:"owner indices and variable IDs generated by graph(m); identity NAE source map"};
  }
  let results=[controls(5,true),controls(40,false)];return {checks,results,limits:"No full SDP, full portfolio, upstream S27 replay or formal kernel check. Local marginals and exact XOR decode checked; moment positivity is symbolic."};
}
console.log(JSON.stringify(dr22(),null,2));
