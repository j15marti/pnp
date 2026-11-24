function run(){
  let state=0x2010540;const rnd=n=>{state=(Math.imul(state,1664525)+1013904223)>>>0;return state%n;};
  const assert=(p,m)=>{if(!p)throw Error(m);};
  const sat=(cs,x)=>cs.every(c=>c.some(l=>x[Math.abs(l)-1]===(l>0?1:0)));
  // Compile each variable to two paths; path x selects occurrences false at x.
  function compile(n,cs){
    let budgets=cs.map(()=>2),blocks=[],vertices=0,edges=0;
    for(let v=1;v<=n;v++){
      let paths=[[],[]];for(let j=0;j<cs.length;j++)for(const l of cs[j])if(Math.abs(l)===v)paths[l>0?0:1].push(j);
      for(let b=0;b<2;b++)if(!paths[b].length){paths[b].push(budgets.length);budgets.push(1);}
      let E=[],a=vertices++,z=vertices++;
      for(const path of paths){let prev=a;for(let k=0;k<path.length;k++){let next=k===path.length-1?z:vertices++;E.push([prev,next,path[k]]);prev=next;}}
      edges+=E.length;blocks.push({E,a,z,paths});
    }return {budgets,blocks,vertices,edges};
  }
  function rows(B){let out=[];for(let m=0;m<2**B.E.length;m++){let odd=new Set(),cost={};for(let i=0;i<B.E.length;i++)if((m>>i)&1){let [u,v,o]=B.E[i];for(let t of [u,v])odd.has(t)?odd.delete(t):odd.add(t);cost[o]=(cost[o]||0)+1;}if(odd.size===2&&odd.has(B.a)&&odd.has(B.z))out.push(cost);}return out;}
  function costCheck(H,x){let c=H.budgets.map(()=>0);for(let i=0;i<x.length;i++)for(let o of H.blocks[i].paths[x[i]])c[o]++;return c.every((a,i)=>a<=H.budgets[i]);}
  function domains(H,rs){return H.blocks.map((B,i)=>[...new Set(B.E.map(e=>e[2]))].map(o=>({b:i,o,d:[...new Set(rs[i].map(r=>r[o]||0))]}))).flat();}
  function forestSolve(H,rs){
    let nb=rs.length,nn=nb+H.budgets.length,par=Array.from({length:nn},(_,i)=>i),adj=Array.from({length:nn},()=>[]),cuts=[];
    const root=a=>{while(par[a]!==a)a=par[a];return a;};
    for(let e of domains(H,rs).sort((a,b)=>b.d.length-a.d.length)){let u=e.b,v=nb+e.o,ru=root(u),rv=root(v);if(ru===rv)cuts.push(e);else{par[ru]=rv;adj[u].push(v);adj[v].push(u);}}
    let visits=0;
    function treeSolve(R,K){
      let seen=new Set();
      function owner(u,p){seen.add(u);let i=u-nb,s=0;for(let v of adj[u])if(v!==p)s+=block(v,u);return s<=K[i]?K[i]-s:-Infinity;}
      function block(u,p){seen.add(u);let ch=adj[u].filter(v=>v!==p).map(v=>[v-nb,owner(v,u)]),best=Infinity;for(let r of R[u])if(ch.every(([i,k])=>(r[i]||0)<=k))best=Math.min(best,p<0?0:(r[p-nb]||0));return best;}
      for(let u=0;u<nn;u++)if(!seen.has(u)){if(u<nb){if(!Number.isFinite(block(u,-1)))return false;}else if(owner(u,-1)<0)return false;}return true;
    }
    function dfs(k,R,K){if(k===cuts.length){visits++;return treeSolve(R,K);}let {b,o,d}=cuts[k];for(let z of d){if(K[o]<z)continue;let f=R[b].filter(r=>(r[o]||0)===z);if(!f.length)continue;let A=R.slice(),L=K.slice();A[b]=f;L[o]-=z;if(dfs(k+1,A,L))return true;}return false;}
    return {sat:dfs(0,rs,H.budgets),visits,cuts:cuts.length};
  }
  function tseitin(s){let E=[],id=(i,j)=>(i%s)*s+(j%s);for(let i=0;i<s;i++)for(let j=0;j<s;j++)for(let b of [id(i,j),id(i+1,j),id(i,j+1)])E.push([id(i,j),s*s+b]);let inc=Array.from({length:2*s*s},()=>[]);E.forEach(([u,v],i)=>{inc[u].push(i+1);inc[v].push(i+1);});let cs=[];for(let v=0;v<inc.length;v++)for(let m=0;m<8;m++){let p=((m&1)+((m>>1)&1)+((m>>2)&1))%2;if(p!==(v===0?1:0))cs.push(inc[v].map((e,k)=>(m>>k)&1?-e:e));}return {n:E.length,cs};}
  function localClosure(H,pin=-1,bit=0){
    const D=H.blocks.map((_,i)=>i===pin?[bit]:[0,1]);const incid=H.budgets.map(()=>[]);H.blocks.forEach((B,i)=>{for(let o of new Set(B.E.map(e=>e[2])))incid[o].push([i,B.paths.map(p=>p.filter(t=>t===o).length)]);});
    let change=true;while(change){change=false;for(let o=0;o<incid.length;o++){let ls=incid[o],min=ls.reduce((s,[i,c])=>s+Math.min(...D[i].map(b=>c[b])),0);if(min>H.budgets[o])return null;for(let [i,c] of ls){let own=Math.min(...D[i].map(b=>c[b])),f=D[i].filter(b=>min-own+c[b]<=H.budgets[o]);if(!f.length)return null;if(f.length<D[i].length){D[i]=f;change=true;}}}}return D;
  }
  let out={seed:"0x2010540",random:0,randomSat:0,randomUnsat:0,assignments:0,physicalBlocks:0,physicalMasks:0,forestCases:0,forestLeaves:0,scaling:[],smallTseitinAssignments:0,probes:0};
  for(let k=0;k<100;k++){let n=3+rnd(4),m=1+rnd(8),cs=[];for(let j=0;j<m;j++){let a=[];while(a.length<3){let v=1+(state>>>8)%n;rnd(1000);if(!a.some(l=>Math.abs(l)===v))a.push((state>>>16)&1?v:-v);}cs.push(a);}
    let H=compile(n,cs),any=false;for(let mask=0;mask<2**n;mask++){let x=Array.from({length:n},(_,i)=>(mask>>i)&1),f=sat(cs,x);assert(f===costCheck(H,x),"CNF vs physical paths");any||=f;out.assignments++;}
    let R=H.blocks.map(B=>{let r=rows(B);assert(r.length===2,"cycle rows");for(let p of B.paths){let c={};for(let o of p)c[o]=(c[o]||0)+1;assert(r.some(z=>JSON.stringify(Object.entries(z).sort())===JSON.stringify(Object.entries(c).sort())),"row cost");}out.physicalBlocks++;out.physicalMasks+=2**B.E.length;return r;});
    if(k<30&&m<=6){let f=forestSolve(H,R);assert(f.sat===any,"forest solver");out.forestCases++;out.forestLeaves+=f.visits;}
    out.random++;if(any)out.randomSat++;else out.randomUnsat++;
  }
  for(let s of [2,3,4,8,16,32]){let {n,cs}=tseitin(s),H=compile(n,cs),D=domains(H,H.blocks.map(B=>B.paths.map(p=>Object.fromEntries(p.map(o=>[o,1])))));let p=H.blocks.reduce((a,B)=>a+B.E.length-1,0),f=D.length-H.blocks.length-H.budgets.length+1;assert(H.edges===24*s*s&&p===21*s*s&&f===13*s*s+1&&D.every(e=>e.d.length===2),"scaling counts");assert(localClosure(H).every(d=>d.length===2),"initial closure");if(s<=4)for(let i=0;i<n;i++)for(let b=0;b<2;b++){let d=localClosure(H,i,b);assert(d&&d.every((a,j)=>a.length===(j===i?1:2)),"single probe");out.probes++;}
    assert(!costCheck(H,Array(n).fill(0)),"zero unsat");let H2={...H,budgets:H.budgets.slice()};H2.budgets[0]=3;assert(costCheck(H2,Array(n).fill(0)),"SAT budget neighbor");if(s===2){let yes=0,yes2=0;for(let m=0;m<2**n;m++){let x=Array.from({length:n},(_,i)=>(m>>i)&1);yes+=costCheck(H,x);yes2+=costCheck(H2,x);out.smallTseitinAssignments++;}assert(yes===0&&yes2===2**(s*s*3-2*s*s-1),"Tseitin counts");}
    out.scaling.push({s,n,owners:H.budgets.length,coefficientVertices:H.vertices,coefficientEdges:H.edges,p,log2C:f,ell:1,neighborWitness:"all zero"});
  }
  return out;
}
console.log(JSON.stringify(run(),null,2));
