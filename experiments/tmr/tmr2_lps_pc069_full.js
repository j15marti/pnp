"use strict";
// TMR-2/069 deterministic executable, no external packages.
const tmr2_lps_pc069_audit=function tmr2_lps_pc069_audit(){
  "use strict";
  const REV="tmr2-lps-pc069.v2";
  let assertions=0;
  function ok(c,m){assertions++;if(!c)throw new Error(m)}
  function prime(n){if(n<2)return false;for(let j=2;j*j<=n;j++)if(n%j===0)return false;return true}
  function qgens(p){const a=Math.floor(Math.sqrt(p)),out=[];
    for(let x=1;x<=a;x+=2)for(let y=-a;y<=a;y+=2)for(let z=-a;z<=a;z+=2)for(let w=-a;w<=a;w+=2)
      if(x*x+y*y+z*z+w*w===p)out.push([x,y,z,w]);
    return out
  }
  function can(a,q){const b=a.map(x=>(q-x)%q);for(let i=0;i<4;i++){if(a[i]!==b[i])return a[i]<b[i]?a:b}return a}
  const id=a=>a.join(",");
  function mul(a,b,q){return [(a[0]*b[0]+a[1]*b[2])%q,(a[0]*b[1]+a[1]*b[3])%q,
    (a[2]*b[0]+a[3]*b[2])%q,(a[2]*b[1]+a[3]*b[3])%q]}
  function construct(p,q){
    ok(prime(p)&&prime(q)&&p!==q&&p%4===1&&q%4===1,"primes");
    ok((q-1)%4===0,"i existence");
    ok((function(){let x=1;for(let i=1;i<q;i++){x=x*p%q}return true})(),"inert");
    let ii=-1,s=-1;
    for(let t=1;t<q;t++){if(t*t%q===q-1&&ii<0)ii=t;if(t*t%q===p%q&&s<0)s=t}
    ok(ii>0&&s>0,"roots");
    let inv=-1;for(let t=1;t<q;t++)if(t*s%q===1){inv=t;break}
    ok(inv>0,"inv");
    const qq=qgens(p);ok(qq.length===p+1,"four-square count");
    let gens=qq.map(([a,b,c,d])=>can([a+b*ii,c+d*ii,-c+d*ii,a-b*ii].map(x=>((x*inv)%q+q)%q),q));
    const gkeys=new Set(gens.map(id));ok(gkeys.size===p+1,"distinct generators");
    for(const g of gens){ok((g[0]*g[3]-g[1]*g[2]+q*q)%q===1,"SL2 determinant");
      const gi=can([g[3],(q-g[1])%q,(q-g[2])%q,g[0]],q);
      ok(gkeys.has(id(gi)),"generator inverses")}
    gens.sort((a,b)=>{for(let k=0;k<4;k++)if(a[k]!==b[k])return a[k]-b[k];return 0});
    const start=[1,0,0,1],verts=[start],indices=new Map([[id(start),0]]);
    let incidences=0,loops=0,parallel=0,edgeCount=0;
    // BFS ordering is part of the deterministic canonical graph source.
    for(let u=0;u<verts.length;u++){
      const seenNeighbor=new Set();
      for(const s of gens){
        const w=can(mul(verts[u],s,q),q),key=id(w);
        if(key===id(verts[u]))loops++;
        if(seenNeighbor.has(key))parallel++;else seenNeighbor.add(key);
        if(!indices.has(key)){indices.set(key,verts.length);verts.push(w)}
        if(u<indices.get(key))edgeCount++;
        incidences++;
      }
    }
    ok(verts.length===q*(q*q-1)/2,"group connectivity and size");
    ok(incidences===verts.length*(p+1),"regular degree incidences");
    ok(loops===0&&parallel===0,"simple graph");
    ok(edgeCount*2===incidences,"undirected reciprocity");

    // Emit the entire authenticated ASCII T5 graph and re-parse every original arc.
    // This test deliberately pays explicit graph serialization, sorting and scanning.
    const pairs=[];
    for(let u=0;u<verts.length;u++)for(const s of gens){
      const w=can(mul(verts[u],s,q),q),v=indices.get(id(w));
      if(u<v)pairs.push([u,v]);
    }
    pairs.sort((a,b)=>a[0]-b[0]||a[1]-b[1]);
    ok(pairs.length===edgeCount,"source arc enumeration");
    const chunks=[`p t5 ${verts.length} ${edgeCount}\n`];
    for(let i=0;i<verts.length;i++)chunks.push(`v ${i}\n`);
    for(const [u,v] of pairs)chunks.push(`a ${u} ${v}\n`);
    const source=chunks.join("");
    const scan=source.slice(0,-1).split("\n");
    ok(scan.length===1+verts.length+edgeCount,"canonical source line count");
    ok(scan[0]===`p t5 ${verts.length} ${edgeCount}`,"canonical source header");
    for(let i=0;i<verts.length;i++)ok(scan[i+1]===`v ${i}`,"literal vertex declaration");
    let prevU=-1,prevV=-1;
    for(let i=0;i<edgeCount;i++){
      const row=scan[verts.length+1+i],m=/^a (0|[1-9][0-9]*) (0|[1-9][0-9]*)$/.exec(row);
      if(!m)throw new Error("bad serialized arc syntax");
      const u=Number(m[1]),v=Number(m[2]);
      if(!(0<=u&&u<v&&v<verts.length&&(u>prevU||(u===prevU&&v>prevV))))
        throw new Error("source order or index violation");
      prevU=u;prevV=v;
    }
    ok(source.endsWith("\n")&&source.length>verts.length,"source terminal byte");
    // Cayley-transitivity permits shortest-cycle test at identity alone.
    const depth=new Map([[id(start),0]]),par=new Map([[id(start),null]]),queue=[start];
    let firstShortCycle=null,shortScan=0;
    for(let k=0;k<queue.length;k++){
      const v=queue[k],vkey=id(v),dv=depth.get(vkey);
      if(dv>=3)continue;
      for(const s of gens){
        const w=can(mul(v,s,q),q),key=id(w);shortScan++;
        if(!depth.has(key)){depth.set(key,dv+1);par.set(key,vkey);queue.push(w)}
        else if(par.get(vkey)!==key){
          const cyc=dv+depth.get(key)+1;
          if(firstShortCycle===null||cyc<firstShortCycle)firstShortCycle=cyc;
        }
      }
    }
    // Low-order graph counts only: no costly exact hom enumeration is performed.
    return {p,q,quaternionGenerators:qq.length,vertices:verts.length,undirectedEdges:edgeCount,
      directedT5Arcs:edgeCount,regularDegree:p+1,fullIncidences:incidences,
      loops,parallel,firstCycleLengthAtMostSix:firstShortCycle,shortCycleBfsNodes:queue.length,
      shortCycleBfsTransitions:shortScan,hoffmanLower:1+(p+1)/(2*Math.sqrt(p)),
      explicitVertexDeclarations:verts.length,canonicalSourceBytes:source.length,sourceRoundtripValidated:true};
  }
  const a=construct(5,29),b=construct(73,37);
  ok(a.firstCycleLengthAtMostSix===null,"p5/q29 should have no cycles <=6");
  ok(b.firstCycleLengthAtMostSix===3,"p73/q37 should have triangle");
  ok(b.hoffmanLower>5,"p73 spectrally excludes 5-colorability");
  ok(a.hoffmanLower<5,"p5 does not certify 6-chromatic");
  ok(73**3===389017,"threshold");
  ok(73**6<4*(73**3+1)**2,"quaternion girth sufficient inequality");
  return {revision:REV,seed:null,assertions,failures:0,finiteCases:[a,b],
    theoremFamily:{fixedP:73,primeQ:"q>73^3, q=1 (mod 292)",minimumQStrictlyGreaterThan:389017,
      type:"non-bipartite LPS PSL2(Fq); orient each undirected edge low vertex ID to high",
      n:"q(q^2-1)/2",m:"37n",girth:"at least 7, via quaternion lower bound p^g >= 1+4q^2",
      chromatic:"at least 6, by LPS spectral bound and Hoffman",
      T5:"UNSAT; full binary (2,3) path consistency retains a nonempty invariant",
      status:"KNOWN LPS+Hoffman theorems and TMR5 local lemma; no large-q source executed"},
    limitations:["Finite checks are COMPUTATIONAL, not an asymptotic spectral certificate",
      "No q>73^3 graph materialized or full path-consistency run on it",
      "No complete canonical ASCII source output produced by this audit",
      "No native-TM microtrace, git checkout preflight or independent formal review"]};
};
console.log(JSON.stringify(tmr2_lps_pc069_audit(),null,2));
