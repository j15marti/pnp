function audit() {
  const counts={assertions:0,rankCalls:0,xorOps:0,closureScans:0,words:0,factorChecks:0,constructiveChecks:0,peakBasis:0};
  function ok(x,m){counts.assertions++;if(!x)throw Error(m);}
  function rank(rows){counts.rankCalls++;const basis=new Map();for(let x of rows){while(x){const p=x.toString(2).length-1;if(basis.has(p)){x^=basis.get(p);counts.xorOps++;}else{basis.set(p,x);counts.peakBasis=Math.max(counts.peakBasis,basis.size);break;}}}return basis.size;}
  const bit=i=>1n<<BigInt(i);
  function build(b,bad=false,deleted=false){let n=b+1,blocks=[],edges=[];for(let i=0;i<b;i++){const A=[n++,n++],B=[i,i+1],C=[n++,n++];blocks.push({A,B,C});let j=0;for(const a of A)for(const q of B)for(const c of C){let s=bad&&i===b-1?[0,0,0,0,0,1,2,3][j]:0;if(!(deleted&&i===b-1&&j===1))edges.push({a,q,c,s,i,j});j++;}}return {n,blocks,edges};}
  function rows(e){return [bit(e.a)^bit(e.q),bit(e.a)^bit(e.c)];}
  function sat(F,w){for(const e of F.edges){counts.factorChecks++;const a=Number((w>>BigInt(e.a))&1n),q=Number((w>>BigInt(e.q))&1n)^(e.s&1),c=Number((w>>BigInt(e.c))&1n)^(e.s>>1);if(a===q&&a===c)return false;}return true;}
  function guard(F,k,p){return F.blocks.slice(0,k).map((b,i)=>[b.A[0],Number((p>>BigInt(i))&1n)]);}
  function consistent(w,g){return g.every(([i,v])=>Number((w>>BigInt(i))&1n)===v);}
  function closure(F,g){const r=g.map(([i])=>bit(i));for(const e of F.edges){counts.closureScans++;ok(rank(r.concat(rows(e)))-r.length===2,"unexpected rank-one closure");}}
  function all(F,g){let first=null,vs=[],models=0;for(let w=0n;w<(1n<<BigInt(F.n));w++){if(!consistent(w,g))continue;counts.words++;if(sat(F,w)){models++;if(first===null)first=w;else vs.push(w^first);}}return {models,hull:rank(vs)};}
  function word(F,g,type,target){const p=new Map(g), v=Array(F.n).fill(0);
    if(type==="B"){for(const b of F.blocks){const a=p.get(b.A[0])??0;b.A.forEach(i=>v[i]=a);b.C.forEach(i=>v[i]=1-a);}}
    else {let t=F.blocks[target], a=p.get(t?.A[0])??0;let bb=type==="C"?1-a:type==="dist"?1-a:0;
      for(const b of F.blocks){b.B.forEach(i=>v[i]=bb);b.C.forEach(i=>v[i]=1-bb);b.A.forEach(i=>v[i]=p.get(i)??0);}
      if(type==="C"||type==="dist"){t.A.forEach(i=>v[i]=a);if(type==="dist")t.C.forEach(i=>v[i]=bb);}
    }
    return v.reduce((w,x,i)=>w|(x?bit(i):0n),0n);
  }
  function checkWitness(F,w,g){counts.constructiveChecks++;ok(consistent(w,g)&&sat(F,w),"invalid constructive word");}
  const single=build(1),subsetHistogram={};
  for(let mask=0;mask<256;mask++){const es=single.edges.filter((_,i)=>(mask>>i)&1),d=es.length-rank(es.flatMap(rows));subsetHistogram[d]=(subsetHistogram[d]??0)+1;ok(mask===255?d===3:d<3,"core strict maximum");}
  const small=[];
  for(let b=1;b<=3;b++){
    const F=build(b),U=build(b,true),V=build(b,true,true);let fibers=0,pairs=0,satNeighbors=0,unsatFibers=0,totalModels=0;let minHull=F.n;
    for(let k=0;k<=b;k++){
      for(let p=0n;p<(1n<<BigInt(k));p++){
        const g=guard(F,k,p);closure(F,g);closure(U,g);closure(V,g);const a=all(F,g),u=all(U,g),v=all(V,g);
        ok(a.models>0&&a.hull===F.n-k,"full hull");ok(u.models===0,"bad block not UNSAT");ok(v.models>0,"deletion neighbor not SAT");
        fibers++;unsatFibers++;satNeighbors++;totalModels+=a.models;minHull=Math.min(minHull,a.hull);
        for(let q=p+1n;q<(1n<<BigInt(k));q++){let i=0;while(((p^q)&bit(i))===0n)i++;let w=word(F,g,"dist",i);checkWitness(F,w,g);const g2=guard(F,k,q);for(const [j,x] of g2)w=x?w|bit(j):w&~bit(j);ok(!sat(F,w),"distinct residual");pairs++;}
      }
    }
    // Test every single coordinate, both RHS, independent of prescribed A-prefix.
    for(let i=0;i<F.n;i++)for(let a=0;a<2;a++){let g=[[i,a]];closure(F,g);const x=all(F,g);ok(x.models>0&&x.hull===F.n-1,"single-coordinate hull");}
    small.push({b,n:F.n,m:F.edges.length,fibers,unsatFibers,satNeighbors,pairs,totalModels,minHull,singleCoordinateQueries:2*F.n});
  }
  const scaling=[];
  for(const b of [4,8,16,32,64]){
    const F=build(b),k=b,g=guard(F,k,((1n<<BigInt(b))-1n)/3n);closure(F,g);
    const gr=g.map(([i])=>bit(i));const r=rank(gr.concat(F.edges.flatMap(rows)))-k;
    ok(r===F.n-k,"global quotient rank");
    const pinned=new Set(g.map(x=>x[0]));let flips=0;
    for(let i=0;i<F.n;i++)if(!pinned.has(i)){
      let t=F.blocks.findIndex(x=>x.C.includes(i)),type=t>=0?"C":F.blocks.some(x=>x.B.includes(i))?"B":"A";
      let w=word(F,g,type,t);checkWitness(F,w,g);checkWitness(F,w^bit(i),g);flips++;
    }
    for(let i=0;i<b;i++){let w=word(F,g,"dist",i);checkWitness(F,w,g);ok(!sat(F,w^bit(g[i][0])),"single opposite guard distinguished");}
    scaling.push({b,n:F.n,m:F.edges.length,k,r,deficiency:F.edges.length-r,distinctFibersAnalytic:(1n<<BigInt(b)).toString(),explicitFlipPairs:flips,explicitDistinguishers:b});
  }
  // Common Fano controls: original and each ordinary-clause deletion.
  const triples=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]];
  const fano=[];
  for(let del=-1;del<14;del++){let m=0;for(let w=0;w<128;w++){counts.words++;let legal=true;for(let j=0;j<14;j++)if(j!==del){counts.factorChecks++;const t=triples[j>>1];if(t.every(i=>((w>>i)&1)===(j&1))){legal=false;break;}}if(legal)m++;}ok(m===(del<0?0:5),"Fano");fano.push(m);}
  return {subsetHistogram,small,scaling,fano,counts};
}
console.log(JSON.stringify(audit(),null,2));
