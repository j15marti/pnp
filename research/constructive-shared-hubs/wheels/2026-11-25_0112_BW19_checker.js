/* Node.js: node checker.js chart0.json chart1.json chart2.json chart3.json chart4.json MS24.json BH18.json */
function experiment(data){
  const assert=(x,msg)=>{if(!x)throw Error(msg)};
  const bit=i=>1n<<BigInt(i), idx=x=>x.toString(2).length-1;
  function setup(j){let N=j.rowMap.length, O=j.ownerIDs.length;let groups=Array.from({length:O},()=>[]);j.rowMap.forEach(([o],r)=>groups[o].push(r));return {j,N,O,groups,A:j.pairHex.map(s=>BigInt("0x"+s)),D:groups.map(g=>g.reduce((m,r)=>j.live[r]?m|bit(r):m,0n))}}
  function apply(s,d){for(const [r,h] of d.delta??[])s.A[r]&=~BigInt("0x"+h);for(const r of d.removedRows??[])s.D[s.j.rowMap[r][0]]&=~bit(r);}
  function symmetric(s){for(let r=0;r<s.N;r++)for(let t=r+1;t<s.N;t++)if(s.j.rowMap[r][0]!==s.j.rowMap[t][0])assert(Boolean(s.A[r]&bit(t))===Boolean(s.A[t]&bit(r)),"asymmetric pair")}
  function ac(s,D,c){let change=true;while(change){c.ac++;change=false;for(let o=0;o<s.O;o++){for(const r of s.groups[o])if(D[o]&bit(r)){for(let p=0;p<s.O;p++)if(p!==o){c.support++;if(!(s.A[r]&D[p])){D[o]&=~bit(r);change=true;break}}}if(!D[o])return false;}}return true}
  function hull(s,D,c){
    c.hulls++;
    let rows=s.groups.map((g,o)=>g.filter(r=>Boolean(D[o]&bit(r)))),pos=new Int32Array(s.N),off=[],nv=0;
    for(let i=0;i<s.O;i++){off[i]=nv;nv+=rows[i].length-1;rows[i].forEach((r,j)=>pos[r]=j)}
    const G=Array.from({length:2*nv},()=>[]),H=G.map(()=>[]);
    function edge(a,b){G[a].push(b);H[b].push(a);c.edges++}
    function imp(a,b){edge(a,b);edge(b^1,a^1)}
    const lit=(i,t,v)=>2*(off[i]+t-1)+v; // threshold index t>=1
    function bounds(a,j,lo,hi){if(lo>0)imp(a,lit(j,lo,1));if(hi<rows[j].length-1)imp(a,lit(j,hi+1,0))}
    for(let i=0;i<s.O;i++)for(let t=2;t<rows[i].length;t++)imp(lit(i,t,1),lit(i,t-1,1));
    for(let i=0;i<s.O;i++)for(let j=0;j<s.O;j++)if(i!==j&&rows[i].length>1&&rows[j].length>1){
      const r=rows[i],lo=[],hi=[];for(const x of r){c.range++;const z=s.A[x]&D[j];assert(z!==0n,"AC not closed");lo.push(pos[idx(z&-z)]);hi.push(pos[idx(z)])}
      let mn=lo[0],mx=hi[0];
      for(let t=1;t<r.length;t++){bounds(lit(i,t,0),j,mn,mx);mn=Math.min(mn,lo[t]);mx=Math.max(mx,hi[t])}
      mn=lo[r.length-1];mx=hi[r.length-1];
      for(let t=r.length-1;t>=1;t--){bounds(lit(i,t,1),j,mn,mx);mn=Math.min(mn,lo[t-1]);mx=Math.max(mx,hi[t-1])}
    }
    let seen=new Uint8Array(2*nv),ord=[];
    for(let a=0;a<2*nv;a++)if(!seen[a]){seen[a]=1;let st=[[a,0]];while(st.length){let f=st[st.length-1];if(f[1]<G[f[0]].length){let b=G[f[0]][f[1]++];if(!seen[b]){seen[b]=1;st.push([b,0])}}else{ord.push(f[0]);st.pop()}}}
    let comp=new Int32Array(2*nv).fill(-1),k=0;for(let ii=ord.length-1;ii>=0;ii--){let a=ord[ii];if(comp[a]>=0)continue;comp[a]=k;let st=[a];while(st.length){let z=st.pop();for(let b of H[z])if(comp[b]<0){comp[b]=k;st.push(b)}}k++}
    for(let v=0;v<nv;v++)if(comp[2*v]===comp[2*v+1])return {status:"UNSAT",contradiction:v};
    const truth=a=>comp[a]>comp[a^1];for(let a=0;a<G.length;a++)if(truth(a))for(let b of G[a])assert(truth(b),"invalid SCC model");
    let pick=rows.map((r,i)=>{let n=0;for(let t=1;t<r.length;t++)if(truth(lit(i,t,1)))n++;return r[n]});
    for(let i=0;i<s.O;i++)for(let j=i+1;j<s.O;j++)if(!(s.A[pick[i]]&bit(pick[j])))return {status:"OPEN"};
    return {status:"SAT",pick};
  }
  function run(s,cap){const c={ac:0,support:0,hulls:0,edges:0,range:0,probes:0},D=s.D.slice(),removed=[];let root;
    function closed(D){return ac(s,D,c)?hull(s,D,c):{status:"UNSAT",ac:true}}
    root=closed(D);const initial=root.status;let tried=new Set();while(root.status==="OPEN"&&c.probes<cap){
      let os=s.groups.map((g,o)=>({o,rs:g.filter(r=>Boolean(D[o]&bit(r)))})).filter(a=>a.rs.length>1).sort((a,b)=>a.rs.length-b.rs.length||a.o-b.o);
      let r;for(const a of os){r=a.rs.find(x=>!tried.has(x));if(r!==undefined)break}if(r===undefined)break;
      tried.add(r);c.probes++;let E=D.slice();E[s.j.rowMap[r][0]]=bit(r);let q=closed(E);
      if(q.status==="SAT"){root=q;break}
      if(q.status==="UNSAT"){D[s.j.rowMap[r][0]]&=~bit(r);removed.push({r,certificate:q});root=closed(D);tried.clear()}
    }
    return {id:s.j.id,guard:s.j.guard,initial,status:root.status,pick:root.pick,removed,c,live:D.reduce((n,m,o)=>n+s.groups[o].filter(r=>Boolean(m&bit(r))).length,0)}
  }
  function make(id,domains,allowed,guard=[]){let rowMap=domains.flatMap((d,i)=>d.map(r=>[i,r])),A=rowMap.map(([i,a],r)=>rowMap.reduce((m,[j,b],t)=>i!==j&&allowed(i,a,j,b)?m|bit(t):m,0n));return {id,guard,ownerIDs:domains.map((_,i)=>i),rowMap,live:rowMap.map(()=>true),pairHex:A.map(x=>x.toString(16))}}
  function wheel(n,drop=false){let d=Array.from({length:n+1},()=>["0","1","2"]);let edge=(i,j)=>{if(i>j)[i,j]=[j,i];return (i===0&&!(drop&&j===1))||(i>0&&(j-i===1||(i===1&&j===n)))};return make("wheel-"+n+(drop?"-drop":""),d,(i,a,j,b)=>!edge(i,j)||a!==b)}
  const fano=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]];
  function fanoChart(flip=false){let domains=fano.map((e,i)=>Array.from({length:8},(_,x)=>x.toString(2).padStart(3,"0")).filter(w=>{let a=w.split("").map(Number);if(flip&&i===0)a[0]^=1;return !(a[0]===a[1]&&a[1]===a[2])}));return make(flip?"Fano-sign":"Fano",domains,(i,a,j,b)=>fano[i].every((v,k)=>!fano[j].includes(v)||a[k]===b[fano[j].indexOf(v)]))}
  function count(s){let n=0;function rec(p){if(p.length===s.O){n++;return}for(const r of s.groups[p.length])if(p.every(t=>s.A[t]&bit(r)))rec([...p,r])}rec([]);return n}
  // AC/PC check directly for unguarded wheel roots: all pair-compatible rows extend to every third owner.
  function pc(s){for(let r=0;r<s.N;r++)for(let t=r+1;t<s.N;t++)if(s.A[r]&bit(t))for(let o=0;o<s.O;o++)if(o!==s.j.rowMap[r][0]&&o!==s.j.rowMap[t][0]&&!(s.A[r]&s.A[t]&s.D[o]))return false;return true}
  let controls=[];for(let j of [wheel(3),wheel(5),wheel(7),wheel(5,true),wheel(6),fanoChart(),fanoChart(true)]){let s=setup(j);symmetric(s);let models=count(s),r=run(s,24);assert(r.status==="OPEN"||(r.status==="SAT")===(models>0),"control discrepancy");controls.push({models,pc:pc(s),...r})}
  let jobs=[];for(let i=0;i<5;i++)for(let mode of [false,true]){let s=setup(data[i]);symmetric(s);let importAC={ac:0,support:0};if(mode){apply(s,data[5].jobs[i].combined);symmetric(s);assert(ac(s,s.D,importAC),"MS24 closed UNSAT");const b=data[6].jobs.find(j=>j.ref===data[5].refs[i]&&j.mode===true);assert(b,"BH18 guard missing");assert(JSON.stringify(b.guard)===JSON.stringify(s.j.guard),"BH guard mismatch");apply(s,b);symmetric(s);assert(ac(s,s.D,importAC),"BH18 closed UNSAT");}
    jobs.push({mode,importAC,...run(s,9)});
  }
  return {controls,jobs,notes:"Imported peer pair deletions accepted on exact guard provenance, no independent replay; no BH18 ternary consumer. Row index order is fixed. AC and order hull only; SAT pick verified against current pair masks, not upstream source lifts. Probe cap 9."}
}
const fs=require('node:fs'); const data=process.argv.slice(2).map(p=>JSON.parse(fs.readFileSync(p,'utf8'))); console.log(JSON.stringify(experiment(data),null,2));
