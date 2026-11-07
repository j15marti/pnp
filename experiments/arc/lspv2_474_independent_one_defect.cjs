// LSPV-2/474: independent V8/Node check of the one-defect component-boundary theorem.
// Independent of the full source-authenticator and fallback in Python reproducibility archive.
"use strict";
function tseitin(edges,charge){
  const n=1+Math.max(...edges.flat()), f=[];
  for(let v=0;v<n;v++){
    const es=edges.map((p,i)=>p.includes(v)?i+1:0).filter(Boolean).sort((a,b)=>a-b);
    if(es.length!==3)throw Error("not cubic");
    for(let a=0;a<8;a++){
      const bits=[a&1,(a>>1)&1,(a>>2)&1];
      if((bits[0]^bits[1]^bits[2])!==charge[v])
        f.push(es.map((x,j)=>bits[j]?-x:x));
    }
  }return f;
}
function testClause(c,a){return c.some(l=>a[Math.abs(l)]===(l>0));}
function brute(f,n){
  for(let mask=0;mask<(1<<n);mask++){
    const a={};for(let i=1;i<=n;i++)a[i]=Boolean(mask&(1<<(i-1)));
    if(f.every(c=>testClause(c,a)))return true;
  }return false;
}
function oneDefect(edges,charge,f,v){
  const n=charge.length, adj=Array.from({length:n},()=>[]);
  edges.forEach(([x,y],i)=>{adj[x].push([y,i+1]);adj[y].push([x,i+1]);});
  const seen=new Set([v]),components=[];
  for(let seed=0;seed<n;seed++){
    if(seen.has(seed))continue;
    const q=[seed],comp=[];seen.add(seed);
    for(let k=0;k<q.length;k++){
      const u=q[k];comp.push(u);
      for(const [w] of adj[u])if(!seen.has(w)){seen.add(w);q.push(w);}
    }
    components.push(comp);
  }
  const incident=adj[v].map(x=>x[1]).sort((a,b)=>a-b);
  for(let mask=0;mask<8;mask++){
    const a={};incident.forEach((id,j)=>a[id]=Boolean(mask&(1<<j)));
    if(!f.slice(4*v,4*v+4).every(c=>testClause(c,a)))continue;
    let ok=true;
    for(const comp of components){
      let x=0,y=0;
      for(const u of comp){
        x^=charge[u];
        for(const [w,e] of adj[u])if(w===v)y^=Number(a[e]);
      }
      if(x!==y){ok=false;break;}
    }
    if(ok)return {sat:true,components:components.length};
  }
  return {sat:false,components:components.length};
}
function split(off){
  const e=[];for(let i=0;i<4;i++)for(let j=i+1;j<4;j++)
    if(!(i===0&&j===1))e.push([off+i,off+j]);
  e.push([off,off+4],[off+4,off+1]);return e;
}
const graph={
  K4:Array.from({length:4},(_,i)=>Array.from({length:3-i},(_,j)=>[i,i+j+1])).flat(),
  cube:Array.from({length:8},(_,i)=>Array.from({length:7-i},(_,j)=>[i,i+j+1])
    .filter(([a,b])=>(a^b).toString(2).replace(/0/g,"").length===1)).flat(),
  bridge:[...split(0),...split(5),[4,9]]
};
let count=0;const classes={};let cutFailures=0;
for(const [name,ed] of Object.entries(graph)){
  const n=1+Math.max(...ed.flat()),charge=Array(n).fill(0);charge[0]=1;
  const orig=tseitin(ed,charge),m=ed.length;
  if(brute(orig,m))throw Error("odd Tseitin classified SAT");
  let yes=0,no=0;
  for(const v of (name==="bridge"?[4]:[0]))
    for(let i=4*v;i<4*v+4;i++)for(let j=0;j<3;j++){
      const mutated=orig.map(c=>c.slice());mutated[i][j]=-mutated[i][j];
      const found=oneDefect(ed,charge,mutated,v).sat;
      const oracle=brute(mutated,m);
      if(found!==oracle)throw Error("mismatch "+name+" "+v+" "+i+" "+j);
      found?yes++:no++;count++;
    }
  classes[name]={sat:yes,unsat:no};if(name==="bridge")cutFailures=no;
}
if(cutFailures!==6)throw Error("cut-vertex 6/6 falsifier failed");
console.log(JSON.stringify({status:"PASS",checks:count,classes,model:"finite host brute-force; not native FLMV"}));
