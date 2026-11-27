const fs=require('node:fs');
function run(fs,anchor,cap=3200000,verify=null){
 const vs=[...new Set(fs.flatMap(f=>f.vs))].sort((a,b)=>a-b),n=vs.length,idx=new Map(vs.map((x,i)=>[x,i])),bit=i=>1n<<BigInt(i),rhs=bit(n),low=rhs-1n;let ops=0,probes=0,learn=[],passes=0;
 const count=()=>{if(++ops>cap)throw Error("CAP")};const pc=w=>{let b=0;while(w){w&=w-1;b^=1}return b};
 const F=fs.map(f=>{let ids=f.vs.map(v=>idx.get(v));let masks=Array.from({length:2**ids.length},(_,m)=>ids.reduce((s,v,i)=>s|((m>>i&1)?bit(v):0n),0n));return{masks,rows:f.ok}});
 function close(extra){
  let B=new Map(),change=true;
  const reduce=r=>{for(let [i,v] of B)if(r&bit(i)){count();r^=v}return r};
  // maintain fully reduced basis, so arbitrary Map order is safe
  function add(r){r=reduce(r);if(!(r&low))return r===rhs?-1:0;let i=0;while(!(r&bit(i)))i++;for(let [j,v] of B)if(v&bit(i)){count();B.set(j,v^r)}B.set(i,r);return 1}
  for(let r of extra)if(add(r)<0)return{no:true,B};
  while(change){change=false;
   for(let f of F){let known=[];for(let m=1;m<f.masks.length;m++){count();let v=reduce(f.masks[m]);if(!(v&low))known.push([m,Number(v===rhs)])}
    let rows=[];for(let w of f.rows){count();if(known.every(([m,b])=>pc(w&m)===b))rows.push(w)}if(!rows.length)return{no:true,B};
    // reduce every constant local character on attained restricted rows
    for(let m=1;m<f.masks.length;m++){let b=pc(rows[0]&m),ok=true;for(let w of rows){count();if(pc(w&m)!==b){ok=false;break}}if(ok){let z=add(f.masks[m]|(b?rhs:0n));if(z<0)return{no:true,B};if(z)change=true}}
   }
  }
  return{no:false,B,reduce}
 }
 const a=bit(idx.get(anchor)),eq=(ids,b)=>ids.reduce((m,id)=>m|bit(idx.get(id)),b?rhs:0n);let root=[a],status="UNKNOWN";
 try{while(true){passes++;const z=close(root);if(z.no){status="UNSAT";break}
   if(verify){if(learn.length===verify.length)break;const [ids,b]=verify[learn.length];const r=eq(ids,b);probes++;if(!close([...root,r^rhs]).no)throw Error("bad certificate");learn.push([ids,b]);root.push(r);continue}
   let change=false;
   outer:for(let k=1;k<=2;k++)for(let i=0;i<n;i++)for(let j=k===1?i:i+1;j<(k===1?i+1:n);j++){let m=bit(i)|(k===1?0n:bit(j));if(!(z.reduce(m)&low))continue;for(let b=0;b<2;b++){let r=m|(b?rhs:0n);probes++;if(close([...root,r]).no){let ids=k===1?[vs[i]]:[vs[i],vs[j]];learn.push([ids,1-b]);root.push(r^rhs);change=true;break outer}}}
   if(!change)break;
  }}catch(e){if(String(e).includes("CAP"))status="UNKNOWN_CAP";else throw e}
 return{status,ops,probes,passes,learn,anchor,vs}
}
const [compiler,corpus,registry,helper]=process.argv.slice(2);const c=fs.readFileSync(compiler,'utf8'),h=fs.readFileSync(helper,'utf8');const compile=Function(c.slice(c.indexOf('function compile'),c.indexOf('function auditLocal'))+';return compile;')();const {sha,normalize,eliminate,gauge}=Function(h.slice(0,h.indexOf('function cnfSolve'))+';return {sha,normalize,eliminate,gauge};')();const B=JSON.parse(fs.readFileSync(corpus)),R=JSON.parse(fs.readFileSync(registry));for(const name of ['JOINT-24','RANDOM-3CNF-40']){let x=B.instances.find(x=>x.id===name),r=R.instances.find(x=>x.alias==='EB-'+name),g=compile(x),b=JSON.stringify(g.network)+'\n';if(sha(b)!==r.sha256||b.length*8!==r.N_bits||sha(x.dimacs)!==r.source_cnf.sha256||sha(JSON.stringify(g.source_map)+'\n')!==r.source_map_sha256)throw Error('identity');let e=eliminate(normalize(g.network).fs,true),a=gauge(e.fs);if(!e.fs.every(f=>f.ok.every(w=>f.ok.includes(w^(2**f.vs.length-1)))))throw Error('gauge');let d=run(e.fs,a),v=run(e.fs,a,3200000,d.learn);console.log(JSON.stringify({name,discovery:d,replay:v}));}
