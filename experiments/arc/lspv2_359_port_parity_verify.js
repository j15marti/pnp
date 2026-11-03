// Independent semantic source, DAG, and witness checker for public raw (not imported from producer).
// Usage: node lspv2_359_port_parity_verify.js full_raw.json
const fs=require('fs');
function verify(input){
 let checks=0;const a=(b,m)=>{checks++;if(!b)throw Error(m)};
 let total=0,witnesses=0,sign_flips=0;
 for(const f of input.samples){
  const h=f.h, n=3*h,db=new Map();
  a(f.n===n&&f.clauses.length===8*h&&f.proof.length===8*h-1,"counts");
  for(const s of f.clauses){
   const c=s.chain,i=s.index,inc=[i===1?1:h+2+c*(h-1)+i-1,i===h?2:h+2+c*(h-1)+i,i+2];
   a(s.lits.length===3&&s.lits.every((l,k)=>Math.abs(l)===inc[k]),"bad source incidence");
   const p=s.lits.reduce((v,l)=>v^(l<0?1:0),0),expected=+(c===1&&i===h);
   a(p!==expected,"wrong source parity");
   let t=0;for(let v=0;v<8;v++)if(s.lits.some((l,k)=>((v>>k)&1)===(l>0?1:0)))t|=1<<v;
   db.set(s.id,{kind:"factor",support:inc,table:t});
  }
  for(const d of f.deletion){
   const cl=f.clauses.find(s=>s.id===d.id);
   a(!!cl&&d.assignment.length===n&&/^[01]+$/.test(d.assignment),"witness encoding");
   const val=[0,...Array.from(d.assignment,Number)];
   for(const s of f.clauses)a(s.lits.some(l=>val[Math.abs(l)]===(l>0?1:0))===(s.id!==cl.id),"deletion fails");
   for(const l of cl.lits)a(val[Math.abs(l)]===(l<0?1:0),"flip fails"),sign_flips++;
   witnesses++;
  }
  for(const p of f.proof){
   const x=db.get(p.parents[0]),y=db.get(p.parents[1]);a(!!x&&!!y,"parent");
   let v;
   if(p.rule==="AND3"){
    a(x.kind==="factor"&&y.kind==="factor"&&x.support.join()===y.support.join(),"and support");
    a((x.table&y.table)===p.table,"and output");
    v={kind:"factor",support:p.support,table:p.table};
    if(p.row){
     a(p.row.mask==="0x"+p.support.reduce((m,w)=>m|(1n<<BigInt(w-1)),0n).toString(16),"row mask");
     for(let t=0;t<8;t++)a(((p.table>>t)&1)===+((((t&1)^((t>>1)&1)^((t>>2)&1)))===p.row.rhs),"row parity");
     v.row=p.row;
    }
   } else if(p.rule==="XOR"){
    a(!!x.row&&!!y.row,"xor types");
    a(p.row.mask==="0x"+(BigInt(x.row.mask)^BigInt(y.row.mask)).toString(16),"xor mask");
    a(p.row.rhs===(x.row.rhs^y.row.rhs),"xor rhs");v={kind:"affine",row:p.row};
   }else throw Error("unknown rule");
   db.set(p.id,v);total++;
  }
  const final=db.get(f.proof[f.proof.length-1].id);
  a(final.row.mask==="0x0"&&final.row.rhs===1,"not contradiction");
  a(f.projection_sizes[0]===2**(h+1)&&f.projection_sizes[1]===2**(h+1),"projection count");
  a(f.bounds.min_projected_clauses===2**(h+1),"port-CNF floor");
 }
 return {checks,genuine_paid_nodes:total,deletion_witnesses:witnesses,sign_flips};
}
const input=JSON.parse(fs.readFileSync(process.argv[2]||'full_raw.json','utf8'));console.log(JSON.stringify(verify(input),null,2));
