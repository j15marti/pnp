// Self-contained LSPV-2 PORT-PARITY-MARGINAL359 source/certificate producer.
// Usage: node lspv2_359_port_parity_marginal.js [output.json]
const fs=require('fs');
function make(h){
 const n=3*h, rows=[],clauses=[],proof=[],db=new Map(),rowIds=[];
 const pos=(c,i)=>i===0?1:i===h?2:h+2+c*(h-1)+i;
 for(let c=0;c<2;c++)for(let i=1;i<=h;i++){
  const support=[pos(c,i-1),pos(c,i),i+2],charge=+(c===1&&i===h),leaves=[];
  rows.push({chain:c,index:i,charge,support});
  for(let pat=0;pat<8;pat++){
   if(((pat&1)^((pat>>1)&1)^((pat>>2)&1))===charge)continue;
   const lits=support.map((v,j)=>((pat>>j)&1)?-v:v),id="s"+clauses.length;
   clauses.push({id,chain:c,index:i,pat,lits});
   let table=0;for(let t=0;t<8;t++)if(lits.some((l,j)=>((t>>j)&1)==(l>0?1:0)))table|=1<<t;
   db.set(id,{id,kind:"factor",support,table});leaves.push(id);
  }
  let cur=db.get(leaves[0]);
  for(let k=1;k<4;k++){
   const v=db.get(leaves[k]),p={id:"d"+proof.length,kind:"factor",rule:"AND3",parents:[cur.id,v.id],support,table:cur.table&v.table};
   proof.push(p);db.set(p.id,p);cur=p;
  }
  const expected=Array.from({length:8},(_,t)=>(((t&1)^((t>>1)&1)^((t>>2)&1))===charge)?1<<t:0).reduce((a,b)=>a|b,0);
  if(cur.table!==expected)throw Error("bad parity normalization");
  cur.row={mask:"0x"+support.reduce((a,v)=>a|(1n<<BigInt(v-1)),0n).toString(16),rhs:charge};rowIds.push(cur.id);
 }
 let agg=db.get(rowIds[0]);for(let j=1;j<rowIds.length;j++){
  const row=db.get(rowIds[j]),p={id:"d"+proof.length,kind:"affine",rule:"XOR",parents:[agg.id,row.id],
   row:{mask:"0x"+(BigInt(agg.row.mask)^BigInt(row.row.mask)).toString(16),rhs:agg.row.rhs^row.row.rhs}};
  proof.push(p);db.set(p.id,p);agg=p;
 }
 if(agg.row.mask!=="0x0"||agg.row.rhs!==1||proof.length!==8*h-1)throw Error("not exact contradiction");
 const deleted=[];
 for(const clause of clauses){
  const c=clause.chain,j=clause.index,val=Array(n+1).fill(0);
  rows[c*h+j-1].support.forEach((x,b)=>val[x]=(clause.pat>>b)&1);
  for(let i=j-1;i>=1;i--){
   const r=rows[c*h+i-1],[a,b,z]=r.support;val[z]=0;val[a]=val[b]^r.charge;
  }
  for(let i=j+1;i<=h;i++){
   const r=rows[c*h+i-1],[a,b,z]=r.support;val[z]=0;val[b]=val[a]^r.charge;
  }
  for(let i=1;i<=h;i++){
   const r=rows[(1-c)*h+i-1],[a,b,z]=r.support;
   if(i<h)val[b]=val[a]^val[z]^r.charge;
   else if((val[a]^val[b]^val[z])!==r.charge)throw Error("nonextendible witness");
  }
  if(clauses.filter(s=>!s.lits.some(l=>val[Math.abs(l)]===(l>0?1:0))).map(s=>s.id).join(",")!==clause.id)throw Error("bad unique source witness");
  deleted.push({id:clause.id,assignment:val.slice(1).join("")});
 }
 const ports=[1,2,...Array.from({length:h},(_,i)=>i+3)];
 const dimacs=`p cnf ${n} ${clauses.length}\n`+clauses.map(s=>s.lits.join(" ")+" 0\n").join("");
 return {h,n,ports,rows,clauses,proof,deletion:deleted,projection_sizes:[2**(h+1),2**(h+1)],
  bounds:{source_minimum:8*h-1,proof_nodes:proof.length,min_projected_clauses:2**(h+1)},dimacs};
}
const data={version:'LSPV2-PORT-PARITY-MARGINAL359/public-v1',samples:[1,2,3,4,6,8,12].map(make)};
fs.writeFileSync(process.argv[2]||'full_raw.json',JSON.stringify(data,null,2)+'\n');
console.log(JSON.stringify(data.samples.map(f=>({h:f.h,clauses:f.clauses.length,nodes:f.proof.length,port_CNF_floor:f.bounds.min_projected_clauses})),null,2));
