function fusion(F,pins,width,sameOnly=false){
 const P=new Map(pins),events={restrict:0,incidence:0,candidate:0,eval:0,output:0},steps=[],owners=F.length;
 let A=F.map((f,i)=>{let vs=f.vs.filter(v=>!P.has(v)),cost=[];for(let w=0;w<2**vs.length;w++){let j=0;for(const [k,v] of f.vs.entries()){events.restrict++;j|=(P.has(v)?P.get(v):(w>>vs.indexOf(v))&1)<<k}cost.push(f.cost[j])}return {id:i,vs,cost}});
 const S=xs=>[...new Set(xs.flatMap(x=>x.vs))].sort((a,b)=>a-b);let id=A.length,peak=A.reduce((s,f)=>s+f.cost.length,0),max=0,split=0,cross=0;
 while(A.some(f=>f.vs.length)){
  const occ=new Map();for(const f of A)for(const v of f.vs){events.incidence++;if(!occ.has(v))occ.set(v,[]);occ.get(v).push(f)}
  const [v,fs]=[...occ].sort((a,b)=>S(a[1]).length-S(b[1]).length||a[0]-b[0])[0];
  let groups=[];for(const f of fs.slice().sort((a,b)=>b.vs.length-a.vs.length||a.id-b.id)){
   let opts=[];for(const g of groups){events.candidate++;let u=S([...g,f]);if(u.length<=width&&(!sameOnly||g[0].vs.join(",")===f.vs.join(",")))opts.push({g,w:u.length});}
   opts.sort((a,b)=>a.w-b.w);if(opts.length)opts[0].g.push(f);else groups.push([f]);
  }
  if(groups.length>1)split++;A=A.filter(f=>!fs.includes(f));
  for(const g of groups){let U=S(g),vs=U.filter(x=>x!==v),cost=[];max=Math.max(max,U.length);if(new Set(g.map(f=>f.vs.join(","))).size>1)cross++;for(let w=0;w<2**vs.length;w++){let best=Infinity;for(let b=0;b<2;b++){let sum=0;for(let f of g){let j=0;for(let [k,u] of f.vs.entries()){events.eval++;j|=(u===v?b:(w>>vs.indexOf(u))&1)<<k}events.eval++;sum+=f.cost[j]}best=Math.min(best,sum)}cost.push(best);events.output++}
   let out={id:id++,vs,cost};steps.push({v,parents:g.map(f=>f.id),out:out.id});A.push(out);
  }
  peak=Math.max(peak,A.reduce((s,f)=>s+f.cost.length,0));
  if(Object.values(events).reduce((s,v)=>s+v,0)>3000000)return {status:"UNKNOWN",events,peak,max,split,cross,steps:[]};
 }
 return {status:"BOUND",bound:A.reduce((s,f)=>s+f.cost[0],0),events,steps,peak,max,split,cross,owners};
}
function verify(F,pins,cert){if(cert.status!=="BOUND")return null;let P=new Map(pins),A=new Map(),reads=0,rows=0,bitreads=0;
 for(const [i,f] of F.entries()){let vs=f.vs.filter(v=>!P.has(v)),cost=Array(2**vs.length).fill(Infinity);for(let w=0;w<f.cost.length;w++){rows++;let a=new Map(f.vs.map((v,j)=>[v,(w>>j)&1]));if([...P].some(([v,b])=>a.has(v)&&a.get(v)!==b))continue;let z=vs.reduce((m,v,j)=>m|(a.get(v)<<j),0);cost[z]=f.cost[w]}if(cost.includes(Infinity))throw Error("restriction");A.set(i,{vs,cost,owners:[i]})}
 for(const s of cert.steps){let g=s.parents.map(i=>A.get(i));if(g.some(x=>!x)||new Set(s.parents).size!==s.parents.length||A.has(s.out)||g.some(f=>!f.vs.includes(s.v)))throw Error("bad group");let U=[...new Set(g.flatMap(f=>f.vs))].sort((a,b)=>a-b),vs=U.filter(x=>x!==s.v),cost=Array(2**vs.length).fill(Infinity);for(let w=0;w<2**U.length;w++){rows++;let a=new Map(U.map((v,j)=>[v,(w>>j)&1])),z=vs.reduce((m,v,j)=>m|(a.get(v)<<j),0),sum=0;for(let f of g){let idx=0;for(let [j,v] of f.vs.entries()){idx|=a.get(v)<<j;bitreads++}sum+=f.cost[idx];reads++}cost[z]=Math.min(cost[z],sum)}s.parents.forEach(i=>A.delete(i));A.set(s.out,{vs,cost,owners:g.flatMap(f=>f.owners)})}
 let owners=[...A.values()].flatMap(f=>f.owners).sort((a,b)=>a-b);if(owners.length!==F.length||owners.some((x,i)=>x!==i)||[...A.values()].some(f=>f.vs.length))throw Error("incomplete coverage");let b=[...A.values()].reduce((s,f)=>s+f.cost[0],0);if(b!==cert.bound)throw Error("bound");return {b,reads,rows,bitreads}
}
function feedback(C,n,residue){let a=Array(n).fill(1),steps=[],reads=0,changed=0;const score=()=>{let u=0,z=0,table=[];for(const c of C){let k=0,d=0;for(const l of c){reads++;let x=a[Math.abs(l)-1],s=l>0?x:x-1;k+=s*s;d+=s}let r=((d%3)+3)%3;u+=k===0;z+=k>0&&r===0;table.push([k,k%3,r])}return {u,z,table}};let q=score();for(let i=0;i<n*4;i++){let best=q.u,bz=Infinity,j=-1,plain=-1,bq;for(let v=0;v<n;v++){a[v]^=1;let p=score();a[v]^=1;if(p.u>=q.u)continue;if(p.u<best){best=p.u;plain=v;j=v;bz=p.z;bq=p}else if(p.u===best&&residue&&p.z<bz){j=v;bz=p.z;bq=p}}if(j<0)break;changed+=Number(j!==plain);a[j]^=1;q=bq;steps.push([j+1,q.u,q.z])}return {steps,changed,reads,end:q.u,table:q.table,assignment:a}}
module.exports={fusion,verify,feedback};
