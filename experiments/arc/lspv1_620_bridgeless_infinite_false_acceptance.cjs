"use strict";
/* LSPV-1/620. Source-satisfiable bridgeless all-essential 3-CNF family,
   with checker-accepted bogus /341 refutations. Not mathematical UNSAT.
   OS replay from repo root:
   node experiments/arc/lspv1_620_bridgeless_infinite_false_acceptance.cjs 6,7,8,9 results620.json
   Pinned checker Git blob fcb7d4ced8f922de14c0bda16263a8cc7853e8e0.
*/
function must(b,m){if(!b)throw Error(m);}
function gram(k){
 must(Number.isSafeInteger(k)&&k>=6,"k>=6 required");
 const V=2*k,E=3*k,r=Math.floor(k/2),t=0,s=k+r,old=[];
 for(let i=0;i<k;i++)old.push([i,(i+1)%k]);
 for(let i=0;i<k;i++)old.push([k+i,k+(i+1)%k]);
 for(let i=0;i<k;i++)old.push([i,k+i]);
 const reserved=new Map([[0,0],[k-1,1],[2*k,10],[k+r,2],[k+r-1,3],[2*k+r,12]]);
 const edges=Array(E).fill(null),used=new Set(reserved.keys());
 for(const [i,j] of reserved)edges[j]=old[i];
 const rest=old.filter((_,i)=>!used.has(i));let n=0;
 for(let j=0;j<E;j++)if(edges[j]===null)edges[j]=rest[n++];
 const inc=Array.from({length:V},()=>[]);
 edges.forEach(([a,b],e)=>{inc[a].push(e);inc[b].push(e)});
 must(inc.every(a=>a.length===3),"cubic");
 must(inc[t].slice().sort((a,b)=>a-b).join(",")==="0,1,10","t support");
 must(inc[s].slice().sort((a,b)=>a-b).join(",")==="2,3,12","s support");
 return {k,V,E,t,s,edges,inc};
}
function solve(eqs,E){
 const a=eqs.map(([m,b])=>[m,Number(b)]),piv=[];let j=0;
 for(let col=0;col<E;col++){
  let z=j;while(z<a.length&&!((a[z][0]>>BigInt(col))&1n))z++;
  if(z===a.length)continue;
  [a[z],a[j]]=[a[j],a[z]];
  for(let i=0;i<a.length;i++)if(i!==j&&((a[i][0]>>BigInt(col))&1n)){
   a[i][0]^=a[j][0];a[i][1]^=a[j][1];
  }
  piv.push(col);j++;
 }
 for(let i=j;i<a.length;i++)if(a[i][0]===0n&&a[i][1])return {ok:false,rank:j};
 let mask=0n;for(let i=0;i<j;i++)if(a[i][1])mask|=1n<<BigInt(piv[i]);
 return {ok:true,rank:j,bits:Array.from({length:E},(_,e)=>Number((mask>>BigInt(e))&1n)).join("")};
}
function sat(c,x){return c.some(l=>l>0?x[Math.abs(l)-1]===1:x[Math.abs(l)-1]===0)}
function build(k){
 const G=gram(k),{V,E,t,s,inc}=G,q=Array(V).fill(0);
 q[1]=1;
 const charges=q.slice();charges[t]="0";charges[s]="0";
 const rows=inc.map((aa,v)=>aa.reduce((m,e)=>m|((v===t&&e===10)||(v===s&&e===12)?0n:(1n<<BigInt(e))),0n));
 const base=solve(rows.map((m,v)=>[m,q[v]]),E);
 must(base.ok&&base.rank===V,"base rank");
 const clauses=[],factors=new Map(),proof=[],deleted=[];
 for(let v=0;v<V;v++){
  const ids=[],vv=inc[v];
  for(let z=0;z<8;z++){
   const a=[z&1,(z>>1)&1,(z>>2)&1];
   let val=0;for(let j=0;j<3;j++)if((rows[v]>>BigInt(vv[j]))&1n)val^=a[j];
   if(val===q[v])continue;
   const c={id:"s"+v+"_"+z,vertex:v,literals:vv.map((e,j)=>a[j]?-(e+1):e+1)};
   ids.push(c.id);clauses.push(c);
   let tab=0;
   for(let m=0;m<8;m++){
    const x=Array(E).fill(0);vv.forEach((e,j)=>x[e]=(m>>j)&1);
    if(sat(c.literals,x))tab|=1<<m;
   }
   factors.set(c.id,{kind:"factor",support:vv.slice(),table:tab});
   const equations=rows.map((mask,u)=>[mask,q[u]^(u===v?1:0)]);
   vv.forEach((e,j)=>equations.push([1n<<BigInt(e),a[j]]));
   const one=solve(equations,E);
   must(one.ok&&one.rank===V+2,"deletion witness at v="+v+" z="+z);
   deleted.push({sourceId:c.id,assignment:one.bits});
  }
  must(ids.length===4,"four clauses v"+v);
  let last=ids[0];
  for(let j=1;j<=3;j++){
   const parents=[last,ids[j]],A=factors.get(last),B=factors.get(ids[j]),sup=[...new Set([...A.support,...B.support])];
   const support=j===3&&v===t?"102":j===3&&v===s?"123":sup;
   let table=0;
   for(let m=0;m<(1<<sup.length);m++){
    const bits=Array(E).fill(0);
    for(let z=0;z<support.length;z++)bits[support[z]]=(m>>z)&1;
    function value(f){let idx=0;for(let z=0;z<f.support.length;z++)idx|=Number(bits[f.support[z]])<<z;return(f.table>>idx)&1;}
    if(value(A)&&value(B))table|=1<<m;
   }
   const id="d"+v+"_"+j,rec={id,kind:"factor",rule:"AND3",parents,support,table};
   if(j===3)rec.row={mask:vv.reduce((mask,e)=>mask|(1n<<BigInt(e)),0n).toString(),rhs:q[v]};
   proof.push(rec);factors.set(id,rec);last=id;
  }
 }
 must(proof.length===3*V,"AND count");
 let previous=proof[2].id,mask=BigInt(proof[2].row.mask),rhs=proof[2].row.rhs;
 for(let v=1;v<V;v++){
  const p=proof[3*v+2],id="x"+v;
  mask^=BigInt(p.row.mask);rhs^=p.row.rhs;
  proof.push({id,kind:"affine",rule:"XOR",parents:[previous,p.id],row:{mask:mask.toString(),rhs}});
  previous=id;
 }
 must(mask===0n&&rhs===1&&proof.length===4*V-1,"terminal");
 const fixture={graph:{name:"PRISM_C"+k,n:V,edges:G.edges},charges,clauses,proof,deleted,evenWitness:"0".repeat(E),properties:{essential:4*V}};
 return {fixture,metadata:{k,V,E,clauses:4*V,paid:4*V-1,models:"2^"+k,deletionModelsEach:"2^"+(k-2),rank:base.rank,rankPinned:V+2,exampleModel:base.bits}};
}
function main(){
 const fs=require("fs"),cp=require("child_process"),path=require("path"),os=require("os"),crypto=require("crypto");
 const file=path.join(process.cwd(),"experiments/arc/lspv2_341_independent_verify.js");
 const checker=fs.readFileSync(file);
 const gitBlob=crypto.createHash("sha1").update(Buffer.concat([Buffer.from("blob "+checker.length+"\0"),checker])).digest("hex");
 must(gitBlob==="fcb7d4ced8f922de14c0bda16263a8cc7853e8e0","original checker SHA mismatch");
 const ks=(process.argv[2]||"6,7,8,9").split(",").map(Number),dir=fs.mkdtempSync(path.join(os.tmpdir(),"lspv1-620-")),reports=[];
 try{
  for(const k of ks){
   const {fixture,metadata}=build(k),packet=JSON.stringify({fixtures:[fixture],summary:[null]})+"\n";
   const tmp=path.join(dir,k+".json");fs.writeFileSync(tmp,packet);
   const run=cp.spawnSync(process.execPath,[file,tmp],{encoding:"utf8",maxBuffer:32*1024*1024});
   must(run.status===0,"native checker rejected "+k+": "+run.stderr);
   const r=JSON.parse(run.stdout);
   must(r.cases.length===1&&r.cases[0].proofNodes===metadata.paid&&r.cases[0].allEssential&&r.cases[0].bridgeless,"native result wrong");
   reports.push({...metadata,accepted:true,assertions:r.checks,nativeCertifiedMinimum:r.cases[0].certifiedMinimum,packetBytes:Buffer.byteLength(packet),sha256:crypto.createHash("sha256").update(packet).digest("hex")});
  }
 }finally{fs.rmSync(dir,{recursive:true,force:true});}
 const out=JSON.stringify({checkerGitBlob:gitBlob,checkerMode:"unchanged OS Node subprocess",reports},null,2)+"\n";
 if(process.argv[3])fs.writeFileSync(process.argv[3],out);
 process.stdout.write(out);
}
if(typeof module!=="undefined"){module.exports={build,gram,solve};if(require.main===module)main()}
