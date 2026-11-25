function BW10(){
  const R={seed:20261124,assertions:0,tupleChecks:0,edgeChecks:0,gaussCalls:0,closureQueries:0,closurePins:0,fixed:{SAT:0,UNSAT:0},fibers:{SAT:0,UNSAT:0},source:{SAT:0,UNSAT:0},scales:[]};
  let seed=R.seed;const rand=n=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return (seed>>>8)%n;};
  const chk=(x,m)=>{R.assertions++;if(!x)throw Error(m)};
  const C=x=>[BigInt(x&1),BigInt((x>>1)&1)], V=i=>[1n<<BigInt(i+1),1n<<BigInt(i+2)];
  const xor=(a,b)=>[a[0]^b[0],a[1]^b[1]], sum=a=>a.reduce(xor,C(0)), bit=(r,z)=>{let x=r&((z<<1n)|1n),b=0;while(x){b^=1;x&=x-1n}return b}, val=(a,z)=>bit(a[0],z)+2*bit(a[1],z);
  const eq=(a,b)=>xor(a,b); const eqc=(a,b)=>eq(a,C(b));
  function compile(blocks){
    let messages=[], events=[];
    const neq=(a,b)=>{for(const row of eq(a,b))events.push([row^1n])};
    for(let j=0;j<blocks.length;j++){
      const b=blocks[j];let p=-1,q=-1;const a=b.ports.map((ps,i)=>ps.map((x,k)=>{if(x===null){p=i;q=k;return null}return x.child===undefined?x.word:xor(messages[x.child],x.sign)}));
      const incoming=a.flat().filter(x=>x!==null);
      let c=null;
      if(b.kind==="single"){
        if(p>=0)c=sum(incoming);
        for(let i=0;i<incoming.length;i++)for(let k=i+1;k<incoming.length;k++)events.push(eq(incoming[i],incoming[k]));
      }else if(b.kind==="clique"){
        const gauge=[C(0),...Array.from({length:3},(_,i)=>b.edges.find(e=>e[0]===0&&e[1]===i+1)[2])];
        for(const [u,v,s] of b.edges)neq(xor(gauge[u],gauge[v]),s);
        let ref=a.findIndex((x,i)=>i!==p), t=xor(a[ref][0],gauge[ref]);
        if(p>=0)c=xor(t,gauge[p]);
        for(let i=0;i<4;i++)if(i!==p)neq(xor(a[i][0],gauge[i]),t);
      }else{
        const ref=p>=0?(p+1)%a.length:0,d=xor(a[ref][0],a[ref][1]);
        if(p>=0){c=xor(a[p][1-q],d);a[p][q]=c}
        events.push(eqc(d,0));
        for(const ps of a)neq(xor(ps[0],ps[1]),d);
        for(const [u,v,s] of b.edges){
          const k=sum([a[u][0],a[v][0],s]);
          for(let e=1;e<4;e++)for(let f=1;f<4;f++)if(e!==f)events.push([...eqc(d,e),...eqc(k,f)]);
        }
        neq(sum(b.edges.map(e=>e[2])),a.length%2?C(0):d);
      }
      messages.push(c);
    }
    return events;
  }
  function solve(rows,n){
    R.gaussCalls++;const basis=new Map();
    for(let r of rows){while(r>1n){let k=r.toString(2).length-1;if(basis.has(k))r^=basis.get(k);else{basis.set(k,r);break}}if(r===1n)return null;}
    let z=0n;for(const k of [...basis.keys()].sort((a,b)=>a-b))if(bit(basis.get(k),z))z|=1n<<BigInt(k-1);return z;
  }
  const active=(events,z)=>events.some(e=>e.every(r=>!bit(r,z)));
  function fiber(events,guard,n){
    let q=guard.slice();const probe=(extra=[])=>{R.closureQueries++;for(const e of events){const z=solve([...q,...extra,...e],n);if(z!==null)return z}return null};
    if(probe()===null)return null;
    let changed=true;const pinned=new Set();
    while(changed){changed=false;for(let i=0;i<n;i++)if(!pinned.has(i)){
      const r=1n<<BigInt(i+1);let a=probe([r]),b=probe([r^1n]);
      if(a===null||b===null){q.push(a===null?r^1n:r);pinned.add(i);R.closurePins++;changed=true;break;}
    }}
    return probe();
  }
  function reference(blocks,z){
    let tables=[];
    for(let j=0;j<blocks.length;j++){
      const b=blocks[j], n=b.ports.length;let par=-1;const ports=b.ports.map((ps,i)=>ps.map(x=>{if(x===null){par=i;return null}return x.child===undefined?{v:val(x.word,z)}:{child:x.child,s:val(x.sign,z)}}));
      let tab=Array(4).fill(null),root=null;
      for(let w=0;w<4**n;w++){
        R.tupleChecks++;let a=Array.from({length:n},(_,i)=>(w>>(2*i))&3);
        if(b.edges.some(([u,v,s])=>{R.edgeChecks++;return (a[u]^a[v])===val(s,z)}))continue;
        let children=[],ok=true;
        for(let i=0;i<n&&ok;i++)for(const x of ports[i])if(x!==null){
          if(x.child===undefined){if(a[i]===x.v){ok=false;break}}
          else{let h=tables[x.child].findIndex((v,k)=>v!==null&&(a[i]^k)!==x.s);if(h<0){ok=false;break}children.push([x.child,h]);}
        }
        if(ok){const rec={a,children};if(par>=0)tab[a[par]]=rec;else root=rec;}
      }
      if(par>=0)tables.push(tab);else{
        if(root===null)return null;
        let all=Array(blocks.length);function lift(j,rec){all[j]=rec.a;for(const [i,k] of rec.children)lift(i,tables[i][k]);}lift(j,root);return all;
      }
    }
    throw Error("missing root");
  }
  function verify(blocks,z,w){
    if(!w)return false;
    const par=blocks.map(b=>b.ports.findIndex(ps=>ps.includes(null)));
    return blocks.every((b,j)=>b.edges.every(([u,v,s])=>(w[j][u]^w[j][v])!==val(s,z))&&b.ports.every((ps,i)=>ps.every(x=>x===null||(x.child===undefined?w[j][i]!==val(x.word,z):(w[j][i]^w[x.child][par[x.child]])!==val(x.sign,z)))));
  }
  const ext=word=>({word}), bridge=(child,s)=>({child,sign:C(s)});
  function chain(types,ds){
    const bs=[];for(let j=0;j<types.length;j++){
      const k=types[j],last=j===types.length-1,has=j>0;
      if(k==="single"){let ps=[ext(C(1)),ext(C(2)),ext(C(3))];if(has)ps[0]=bridge(j-1,1);ps.push(last?ext(C(0)):null);bs.push({kind:k,ports:[ps],edges:[]});}
      else if(k==="clique"){let ps=Array.from({length:4},()=>[ext(C(0))]);if(!last)ps[0][0]=null;if(has)ps[1][0]=bridge(j-1,0);let e=[];for(let u=0;u<4;u++)for(let v=u+1;v<4;v++)e.push([u,v,C(0)]);bs.push({kind:k,ports:ps,edges:e});}
      else{let n=k==="even"?4:3,d=ds[j],ps=Array.from({length:n},()=>[ext(C(0)),ext(d)]);if(!last)ps[0][0]=null;if(has)ps[1][0]=bridge(j-1,0);let e=Array.from({length:n},(_,i)=>[i,(i+1)%n,n%2===0&&i===n-1?d:C(0)]);bs.push({kind:"cycle",ports:ps,edges:e});}
    }return bs;
  }
  function checkFixed(bs,z,events=compile(bs)){const w=reference(bs,z),ok=active(events,z);chk(ok===(w!==null),"fixed projection");if(w)chk(verify(bs,z,w),"lift");R.fixed[ok?"SAT":"UNSAT"]++;return ok}
  for(let t=0;t<160;t++){
    const k=1+rand(5),types=Array.from({length:k},()=>["single","clique","odd","even"][rand(4)]),ds=types.map(()=>C(1+rand(3))),bs=chain(types,ds);
    chk(!checkFixed(bs,0n),"balanced chain"); 
    const j=rand(k),b=bs[j],p=b.ports.flat().filter(x=>x&&x.child===undefined);p[rand(p.length)].word=C(rand(4));
    checkFixed(bs,0n);
    for(const b of bs){for(const ps of b.ports)for(const x of ps)if(x){if(x.child===undefined)x.word=C(rand(4));else x.sign=C(rand(4));}for(const e of b.edges)e[2]=C(rand(4));}
    checkFixed(bs,0n);
  }
  for(let t=0;t<60;t++){
    const bs=chain(["odd","clique","even","single"],[V(0),C(1),V(2),C(1)]); 
    // apply an affine gauge to each private vertex and change every incident sign/port consistently.
    const gs=bs.map(b=>b.ports.map(()=>rand(2)?C(rand(4)):V(2*rand(2))));
    const par=bs.map(b=>b.ports.findIndex(ps=>ps.includes(null)));
    bs.forEach((b,j)=>{for(const e of b.edges)e[2]=sum([e[2],gs[j][e[0]],gs[j][e[1]]]);b.ports.forEach((ps,i)=>ps.forEach(x=>{if(x){if(x.child===undefined)x.word=xor(x.word,gs[j][i]);else x.sign=sum([x.sign,gs[j][i],gs[x.child][par[x.child]]]);}}))});
    const events=compile(bs);
    for(let z=0n;z<16n;z++)checkFixed(bs,z,events);
    const guard=Array.from({length:1+rand(4)},()=>BigInt(rand(32)));
    const ref=Array.from({length:16},(_,i)=>BigInt(i)).find(z=>guard.every(r=>!bit(r,z))&&reference(bs,z)!==null);
    const w=fiber(events,guard,4);chk((w!==null)===(ref!==undefined),"fiber decision");if(w!==null){chk(guard.every(r=>!bit(r,w))&&verify(bs,w,reference(bs,w)),"fiber lift");}R.fibers[w===null?"UNSAT":"SAT"]++;
  }
  for(const k of [1,2,4,8,16,32,64,128]){
    let bs=chain(Array(k).fill("odd"),Array.from({length:k},(_,i)=>V(2*i))),events=compile(bs),z=0n;for(let i=0;i<k;i++)z|=1n<<BigInt(2*i);
    chk(!checkFixed(bs,z,events),"scale bad");chk(checkFixed(bs,z^1n,events),"scale escape");
    // One fixed outside word with last color free: exact Gaussian local support.
    const guard=Array.from({length:2*k-2},(_,i)=>(1n<<BigInt(i+1))^BigInt(i%2===0?1:0));let w=null;for(const e of events){w=solve([...guard,...e],2*k);if(w!==null)break;}chk(w!==null&&verify(bs,w,reference(bs,w)),"scale fiber");
    R.scales.push({blocks:k,variables:2*k,rawEscapeEvents:events.length,rejectWords:(3n**BigInt(k)).toString(),coverLowerBound:((3n**BigInt(k)+2n**BigInt(k)-1n)/(2n**BigInt(k))).toString()});
  }
  // Source controls: one odd rim per ordinary clause (BW07), no physical shared-degree claim.
  function clausesBlock(cl){const a=[C(0),...cl.map(([i,s])=>[0n,(1n<<BigInt(i+1))^BigInt(s)]),C(0)];return {kind:"cycle",ports:a.map(x=>[ext(x),ext(xor(x,C(1)))]),edges:a.map((_,i)=>[i,(i+1)%5,C(0)])}}
  const cube=Array.from({length:8},(_,m)=>[0,1,2].map(i=>[i,(m>>i)&1]));
  const fano=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]].flatMap(a=>[0,1].map(s=>a.map(i=>[i,s])));
  function source(cs,n){
    const es=cs.map(c=>compile([clausesBlock(c)]));let count=0,ref=0;
    for(let z=0n;z<(1n<<BigInt(n));z++){
      const a=cs.every(c=>c.some(([i,s])=>Number((z>>BigInt(i))&1n)!==s)); // s is falsifying assignment
      // affine literal here equals bit XOR s, hence matches source
      const b=es.every(e=>active(e,z));chk(a===b,"source chart");if(a)ref++;if(b)count++;
    }
    chk(count===ref,"source count");R.source[count?"SAT":"UNSAT"]++;return count;
  }
  for(let m=0;m<256;m++)source(cube.filter((_,i)=>(m>>i)&1),3);
  chk(source(fano,7)===0,"Fano");for(let i=0;i<14;i++)chk(source(fano.filter((_,j)=>i!==j),7)===5,"Fano neighbor");
  return R;
}
console.log(JSON.stringify(BW10(),null,2));
