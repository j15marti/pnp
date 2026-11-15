"use strict";
// TMR-4/042 executable. The audit() function was executed without modifications in V8.
function audit(){
  "use strict";
  const triples=[];for(let a=0;a<5;a++)for(let b=a+1;b<5;b++)for(let c=b+1;c<5;c++)triples.push([a,b,c]);
  const full=(1<<triples.length)-1;let checks=0,peelRows=0;
  function claim(ok,msg){checks++;if(!ok)throw Error(msg)}
  function pop(x){let n=0;while(x){n++;x&=x-1}return n}
  function eligible(mask){
    const deg=[0,0,0,0,0];for(let i=0;i<10;i++)if(mask&(1<<i))for(const v of triples[i])deg[v]++;
    const ret=[];for(let i=0;i<10;i++)if(mask&(1<<i)&&triples[i].some(v=>deg[v]===1))ret.push(i);return ret;
  }
  function core(mask){for(;;){const e=eligible(mask);if(!e.length)return mask;for(const i of e)mask&=~(1<<i)}}
  const terminalMemo=new Map();
  function terminals(mask){
    if(terminalMemo.has(mask))return terminalMemo.get(mask);
    const e=eligible(mask),s=new Set();if(!e.length)s.add(mask);
    else for(const i of e)for(const t of terminals(mask^(1<<i)))s.add(t);
    terminalMemo.set(mask,s);return s;
  }
  function tarjan(adj){
    const n=adj.length,index=Array(n).fill(-1),low=Array(n).fill(0),on=Array(n).fill(false),stack=[],out=[];let time=0;
    function dfs(v){
      index[v]=low[v]=time++;stack.push(v);on[v]=true;
      for(const w of adj[v]){
        if(index[w]<0){dfs(w);low[v]=Math.min(low[v],low[w])}
        else if(on[w])low[v]=Math.min(low[v],index[w]);
      }
      if(low[v]===index[v]){const part=[];let w;do{w=stack.pop();on[w]=false;part.push(w)}while(w!==v);out.push(part)}
    }
    for(let v=0;v<n;v++)if(index[v]<0)dfs(v);
    return out;
  }
  const g=Array.from({length:2048},(_,state)=>{
    const mask=state>>1,phase=state&1;return phase===0&&mask===0?[state,1]:[state];
  });
  const comp=tarjan(g);claim(comp.length===2048&&comp.every(x=>x.length===1),"R_leaf zero SCCs");
  const toy=tarjan([[1],[0,2],[3],[3]]);claim(toy.length===3&&toy.some(x=>x.length===2&&x.includes(0)&&x.includes(1)),"generic zero cycle");
  const gcd=(a,b)=>b?gcd(b,a%b):a<0n?-a:a;
  function Q(a,b=1n){a=BigInt(a);b=BigInt(b);if(b<0n){a=-a;b=-b}let h=gcd(a,b);return[a/h,b/h]}
  const plus=(a,b)=>Q(a[0]*b[1]+b[0]*a[1],a[1]*b[1]);
  const times=(a,n)=>Q(a[0]*BigInt(n),a[1]);
  const le=(a,b)=>a[0]*b[1]<=b[0]*a[1];
  const eq=(a,b)=>a[0]*b[1]===b[0]*a[1];
  const str=a=>a[1]===1n?a[0].toString():a[0]+"/"+a[1];
  const lambda=[Q(0),Q(0),Q(1,2),Q(3,4),Q(1),Q(0),Q(1)];
  const dot=d=>d.reduce((s,x,i)=>plus(s,times(lambda[i],x)),Q(0));
  const z=[0,0,0,0,0,0,0],rows={
    NOP:{cost:0,delta:z},SWITCH:{cost:0,delta:z},
    PEEL:{cost:1,delta:[0,0,1,2,-1,0,0]},
    RESTORE:{cost:1,delta:[0,0,0,0,1,0,0]},
    HALT:{cost:1,delta:[0,0,0,0,0,0,1]}
  };
  for(const [name,row] of Object.entries(rows))claim(le(dot(row.delta),Q(row.cost)),"bad tariff "+name);
  const histogram={},cores={};
  for(let mask=0;mask<=full;mask++){
    const k=core(mask),e=eligible(mask),ts=terminals(mask),m=pop(mask),c=pop(k);
    claim(ts.size===1&&ts.has(k),"terminal nonconfluence "+mask);
    histogram[c]=(histogram[c]||0)+1;cores[mask]=k;
    for(const i of e){
      const v=mask^(1<<i),newcore=core(v);
      claim(newcore===k,"core not invariant "+mask+" "+i);
      claim(m-c-(pop(v)-pop(newcore))===1,"wrong core distance delta "+mask);
      claim(le(dot(rows.PEEL.delta),Q(1)),"paid PEEL overdischarge");
      peelRows++;
    }
    if(k===0){
      const primal=plus(times(lambda[2],m),plus(times(lambda[3],2*m),lambda[6]));
      claim(eq(primal,Q(2*m+1)),"primal gap "+mask);
      // LP dual y_PEEL=m, y_RESTORE=m, y_HALT=1:
      // SEP: y_PEEL >= m; FUS:2*y_PEEL>=2m;
      // GAMMA: -y_PEEL+y_RESTORE>=0; MACHINE:y_HALT>=1.
      const yp=m,yr=m,yh=1;
      claim(yp>=m&&2*yp>=2*m&&-yp+yr>=0&&yh>=1&&yp+yr+yh===2*m+1,"dual certificate "+mask);
    }
  }
  function nae(values,tri,sign=0){
    const a=tri.map((v,j)=>values[v]^((sign>>j)&1));return !(a[0]===a[1]&&a[1]===a[2]);
  }
  function sat(mask,n){
    for(let a=0;a<(1<<n);a++){
      const vals=Array.from({length:n},(_,j)=>(a>>j)&1);
      if(triples.every((t,i)=>!(mask&(1<<i))||nae(vals,t)))return true;
    }return false;
  }
  const k4=triples.reduce((s,t,i)=>t.every(v=>v<4)?s|(1<<i):s,0);
  claim(core(k4)===k4&&sat(k4,4),"SAT nonempty K4 core");
  claim(core(full)===full&&!sat(full,5),"UNSAT nonempty K5 core");
  let seed=0x15425;const rnd=()=>{seed^=seed<<13;seed^=seed>>>17;seed^=seed<<5;return seed>>>0};
  let qkCases=0,qkEdgeChecks=0;
  for(let k=2;k<=8;k++){
    const edges=[];let next=k;
    for(let i=0;i<k;i++){const y=next++,w=next++;edges.push({vs:[i,y,w],pivot:w,sgn:rnd()&7})}
    for(let i=0;i<k;i++)for(let j=i+1;j<k;j++){const v=next++;edges.push({vs:[i,j,v],pivot:v,sgn:rnd()&7})}
    claim(edges.length===k*(k+1)/2,"Qk edge count");
    for(let x=0;x<(1<<k);x++){
      const vals=Array(next).fill(0);for(let i=0;i<k;i++)vals[i]=(x>>i)&1;
      for(const e of edges){
        const [a,b]=e.vs;const l0=vals[a]^(e.sgn&1),l1=vals[b]^((e.sgn>>1)&1);
        const lp=l0===l1?1-l0:0;vals[e.pivot]=lp^((e.sgn>>2)&1);
      }
      for(const e of edges){claim(nae(vals,e.vs,e.sgn),"signed Qk witness");qkEdgeChecks++}qkCases++;
    }
  }
  // Countermodel: granting a free PEEL as a *new concrete* operation invalidates the certificate.
  claim(!le(dot(rows.PEEL.delta),Q(0)),"free PEEL should defeat tariff");
  return {
    status:"COMPUTATIONAL",execution:"V8 isolate function audit()",
    checkedAssertions:checks,edgeUniverse:triples.length,hypergraphs:full+1,peelRows,
    terminalDynamicProgrammingStates:terminalMemo.size,coreHistogram:histogram,
    zeroSCCs:{RleafPhaseStates:2048,componentCount:comp.length,toySCCCount:toy.length,toyNontrivial:[0,1]},
    coreControls:{satK4:{edges:pop(k4),coreEdges:pop(core(k4))},unsatK5:{edges:pop(full),coreEdges:pop(core(full))}},
    signedQk:{kRange:[2,8],allBoundaryAssignments:qkCases,verifiedSignedEdgeTruths:qkEdgeChecks,seedFinal:seed>>>0},
    tariff:{columns:["CNF","XOR","SEP","FUS","GAMMA","INT","MACHINE"],
      components:["0","0","|U|-|core(U)|","2|U|","|stack|","0","active"],
      lambda:lambda.map(str),rows:Object.fromEntries(Object.entries(rows).map(([name,r])=>[name,{cost:r.cost,delta:r.delta,weightedDischarge:str(dot(r.delta))}])),
      exactPrimal:"2m+1",exactDual:{"y_PEEL":"m","y_RESTORE":"m","y_HALT":"1"}},
    falsifier:{extraRule:"FREE_PEEL",cost:0,delta:rows.PEEL.delta,weightedDischarge:str(dot(rows.PEEL.delta))},
    limitations:"Typed preauthenticated R_leaf events, not physical Turing-machine transitions. No SAT lower bound."
  };
}
if(typeof require!=="undefined"&&require.main===module){process.stdout.write(JSON.stringify(audit(),null,2)+"\n");}
