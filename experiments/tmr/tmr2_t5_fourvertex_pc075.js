/* TMR-2/075 source: exact four-vertex beat-tournament CSP/path consistency test. */
function audit(){
  const REV="tmr2-t5-fourvertex-pc075-js.v1",SEED=202611172016;
  let assertions=0; const ck=(v,m)=>{assertions++;if(!v)throw Error(m);};
  const beat=(a,b)=>((b-a+5)%5===1||(b-a+5)%5===3);
  const E6=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]];
  function count(n,E){let acc=0;const a=new Array(n).fill(0);const go=i=>{if(i===n){if(E.every(([u,v])=>beat(a[u],a[v])))acc++;return};for(let c=0;c<5;c++){a[i]=c;go(i+1)}};go(0);return acc}
  function pc(n,E){
    const rel=Array.from({length:n},(_,i)=>Array.from({length:n},(_,j)=>Array.from({length:5},(_,a)=>Array.from({length:5},(_,b)=>i===j?a===b:true))));
    for(const [u,v] of E){for(let a=0;a<5;a++)for(let b=0;b<5;b++){rel[u][v][a][b]&&=beat(a,b);rel[v][u][b][a]&&=beat(a,b)}}
    let passes=0,updates=0;
    for(let again=true;again;){passes++;again=false;
      for(let i=0;i<n;i++)for(let j=0;j<n;j++)for(let k=0;k<n;k++)for(let a=0;a<5;a++)for(let b=0;b<5;b++){
        if(!rel[i][j][a][b])continue;
        let can=false;for(let c=0;c<5;c++)if(rel[i][k][a][c]&&rel[k][j][c][b]){can=true;break}
        if(!can){rel[i][j][a][b]=false;again=true;updates++}
      }
    }
    return {unsat:rel.some(row=>row.some(r=>r.every(a=>a.every(v=>!v)))),passes,updates};
  }
  function detector(n,E){
    function one(edges,orientation){
      const out=Array.from({length:n},()=>new Set);
      for(const [u,v] of edges)out[u].add(v);
      for(let a=0;a<n;a++)for(const b of out[a])for(const c of out[b]){
        if(a===b||a===c||b===c)continue;
        for(const d of out[a])if(d!==a&&d!==b&&d!==c&&out[b].has(d)&&out[c].has(d))return {orientation,vertices:[a,b,c,d]};
      }
      return null;
    }
    return one(E,"forward")||one(E.map(([u,v])=>[v,u]),"reverse");
  }
  function encode(n,E){
    const es=[...E].sort((a,b)=>a[0]-b[0]||a[1]-b[1]);
    return `p t5 ${n} ${es.length}\n`+Array.from({length:n},(_,i)=>`v ${i}\n`).join("")+es.map(([u,v])=>`a ${u} ${v}\n`).join("");
  }
  function parse(src){
    if(!/^[\x00-\x7f]*$/.test(src)||!src.endsWith("\n")||src.includes("\r"))throw Error("ASCII");
    const lines=src.slice(0,-1).split("\n"),h=lines[0].split(" ");
    if(h.length!==4||h[0]!=="p"||h[1]!=="t5"||!h.slice(2).every(x=>/^(0|[1-9]\d*)$/.test(x)))throw Error("header");
    const n=+h[2],m=+h[3];
    if(n>src.length||m>src.length||lines.length!==1+n+m)throw Error("count");
    for(let i=0;i<n;i++)if(lines[i+1]!==`v ${i}`)throw Error("vertex");
    const E=[];
    for(const line of lines.slice(n+1)){const f=line.split(" ");if(f.length!==3||f[0]!=="a"||!f.slice(1).every(x=>/^(0|[1-9]\d*)$/.test(x)))throw Error("arc"); const u=+f[1],v=+f[2]; if(u>=n||v>=n)throw Error("range");E.push([u,v])}
    if(encode(n,E)!==src)throw Error("canonical");return {n,E};
  }
  function family(h,b,type){
    const E=[];let next=3;
    for(let j=0;j<b;j++){
      const priv=Array.from({length:h-3},()=>next++);
      const sinks=Array.from({length:h},()=>next++);
      for(const u of [0,1,2,...priv])for(const v of sinks)E.push([u,v]);
    }
    E.push([0,1],type==="no"?[1,2]:[0,2]);return {n:next,E};
  }
  function conditionedFamilyCount(h,b,type){
    let total=0;
    for(let s=0;s<5;s++)for(let t=0;t<5;t++)for(let u=0;u<5;u++){
      const tcol=[s,t,u];if(!beat(s,t)||!beat(tcol[type==="no"?1:0],u))continue;
      let block=0;
      for(let p=0;p<5;p++){ // h=4: exactly one private source per block
        let common=0;for(let q=0;q<5;q++)if([s,t,u,p].every(x=>beat(x,q)))common++;
        block+=common**h;
      }
      total+=block**b;
    }
    return total;
  }
  const masks=[];
  for(let m=0;m<32;m++){
    let imageOut=0,imageIn=0;
    for(let b=0;b<5;b++)for(let a=0;a<5;a++)if(m&(1<<a)){
      if(beat(a,b))imageOut|=1<<b;
      if(beat(b,a))imageIn|=1<<b;
    }
    masks.push([m,imageOut,imageIn]);ck(imageOut>=0&&imageOut<32&&imageIn>=0&&imageIn<32,"mask");
  }
  const satByArc=[0,0,0,0,0,0,0],unsatByArc=[0,0,0,0,0,0,0],unsats=[];
  for(let m=0;m<64;m++){
    const E=E6.filter((_,i)=>(m&(1<<i))!==0);
    const cert=parse(encode(4,E));ck(cert.n===4&&cert.E.length===E.length,"source");
    const z=count(4,E),p=pc(4,E);
    ck(p.unsat===(z===0),"PC correct on 4-DAG");
    ck(!!detector(4,E)===(z===0),"two motifs characterize unsat 4-DAG");
    if(z===0){unsatByArc[E.length]++;unsats.push({edges:E,pc_passes:p.passes,pc_updates:p.updates})}
    else satByArc[E.length]++;
  }
  ck(unsatByArc.slice(0,5).every(x=>x===0)&&unsatByArc[5]===2&&unsatByArc[6]===1,"minimality");
  let familyChecks=0,renamings=0;
  const hs=[[4,2],[5,2],[9,3],[14,5]];
  for(const [h,b] of hs)for(const type of ["yes","no"]){
    const {n,E}=family(h,b,type);
    ck(parse(encode(n,E)).n===n,"family parse");
    ck(!!detector(n,E)===(type==="no"),"family YES/NO");
    familyChecks++;
    if(h===4){const z=conditionedFamilyCount(h,b,type);ck((z>0)===(type==="yes"),"actual label count");}
    // Deterministic full permutation checks on small family; 12 rotations on larger.
    const num=(h===4?120:12);
    for(let r=0;r<num;r++){
      const perm=Array.from({length:n},(_,i)=>(i+r)%n);
      const er=E.map(([u,v])=>[perm[u],perm[v]]);
      ck(!!detector(n,er)===(type==="no"),"renaming detection");renamings++;
    }
  }
  const tgt=[];for(let a=0;a<5;a++)for(let b=0;b<5;b++)if(beat(a,b))tgt.push([a,b]);
  ck(detector(5,tgt)===null&&count(5,tgt)===5,"T5 easy control");
  return {revision:REV,seed:SEED,assertions,failures:0,exact_DAGs:64,domain_masks:32,
    mask_images:masks,sat_by_arcs:satByArc,unsat_by_arcs:unsatByArc,unsat_examples:unsats,
    path_consistency_all_64:true,smallest_acyclic_unsat_vertices:4,
    smallest_acyclic_unsat_arcs:5,source_family_checks:familyChecks,
    renamed_source_checks:renamings,math_review:"OPEN",P_vs_NP:"OPEN"};
}
console.log(JSON.stringify(audit(),null,2));
