"use strict";
// Exact signed 3-CNF source-bit test; no unrestricted asymptotic proof is inferred.
function build(m,b){
  const edge=new Map(),aux=new Map();let k=1;
  for(let v=0;v<m;v++)for(let u=v+1;u<m;u++)edge.set(v+","+u,k++);
  for(let v=0;v<m;v++)for(let j=0;j<m-4;j++)aux.set(v+","+j,k++);
  const rows=[],clauses=[];
  for(let v=0;v<m;v++){
    const e=[];for(let u=0;u<m;u++)if(u!==v)e.push(edge.get(Math.min(v,u)+","+Math.max(v,u)));
    const y=Array.from({length:m-4},(_,j)=>aux.get(v+","+j));
    const gates=[[e[0],e[1],y[0],0]];
    for(let j=1;j<m-4;j++)gates.push([y[j-1],e[j+1],y[j],0]);
    gates.push([y[m-5],e[m-3],e[m-2],b[v]]);
    for(const g of gates){
      rows.push([g.slice(0,3),g[3]]);
      for(let z=0;z<8;z++){
        const bits=[(z>>2)&1,(z>>1)&1,z&1];
        if((bits[0]^bits[1]^bits[2])!==g[3])clauses.push(g.slice(0,3).map((x,i)=>bits[i]?-x:x));
      }
    }
  }
  return {n:k-1,rows,clauses,m};
}

function solve(n,rows,freeze=[]){
  const piv=new Map();
  for(const [vars,bb] of rows.concat(freeze.map(([x,z])=>[[x],z]))){
    let mask=0n,rhs=bb;
    for(const x of vars)mask^=1n<<BigInt(x-1);
    while(mask){
      const h=mask.toString(2).length-1;
      const prev=piv.get(h);
      if(!prev){piv.set(h,[mask,rhs]);break;}
      mask^=prev[0];rhs^=prev[1];
    }
    if(mask===0n&&rhs)return null;
  }
  const a=new Uint8Array(n+1);
  for(const h of [...piv.keys()].sort((x,y)=>x-y)){
    const [mask,rhs]=piv.get(h);let z=rhs;
    for(let j=0;j<h;j++)if((mask>>BigInt(j))&1n)z^=a[j+1];
    a[h+1]=z;
  }
  return a;
}

function encode(n,clauses){
  const w=Math.max(1,Math.ceil(Math.log2(n)));
  let s="1".repeat(n)+"0"+"1".repeat(clauses.length)+"0";
  const offsets=[];
  for(const C of clauses){
    const row=[];
    for(const lit of C){
      row.push(s.length);
      s+=(lit<0?"1":"0")+Math.abs(lit).toString(2).padStart(w,"0");
    }
    offsets.push(row);
  }
  return {s,offsets,w};
}

function parse(s,n,M,w){
  const head="1".repeat(n)+"0"+"1".repeat(M)+"0";
  if(s.length!==head.length+3*M*(w+1)||!s.startsWith(head))return null;
  const clauses=[];let pos=head.length;
  for(let j=0;j<M;j++){
    const c=[];
    for(let t=0;t<3;t++){
      const sign=s[pos++],bits=s.slice(pos,pos+w);pos+=w;
      if((sign!=="0"&&sign!=="1")||!/^[01]+$/.test(bits))return null;
      const id=parseInt(bits,2);if(id<1||id>n)return null;
      c.push(sign==="1"?-id:id);
    }
    if(new Set(c.map(Math.abs)).size!==3)return null;
    clauses.push(c);
  }
  return clauses;
}

function satClause(C,a){return C.some(l=>a[Math.abs(l)]===(l>0?1:0));}

function audit(){
  const out={id:"TMR2-006-POLARITY-BIT-NECESSITY",status:"COMPUTATIONAL",
    cases:[],odd_unsat:0,even_sat:0,deletion_certificates:0,
    single_bit_opposite_label_neighbors:0,raw_source_parse_controls:0,
    unique_falsified_clause_controls:0,duplicate_negative_controls:0,
    disjoint_product_negative_controls:0,failures:0};
  const sizes=[6,8,10,12,14];
  for(const m of sizes){
    const patterns=[[1,...Array(m-1).fill(0)]];
    if(m<=12)patterns.push(Array.from({length:m},(_,i)=>[1,2,3].includes(i)?1:0));
    for(let q=0;q<patterns.length;q++){
      const f=build(m,patterns[q]),{s,offsets,w}=encode(f.n,f.clauses);
      if(solve(f.n,f.rows)!==null)throw Error("original odd must be UNSAT");
      out.odd_unsat++;
      if(parse(s,f.n,f.clauses.length,w)?.length!==f.clauses.length)throw Error("invalid original");
      const P=3*f.clauses.length;
      let here=0;
      for(let j=0;j<f.clauses.length;j++){
        const C=f.clauses[j];
        const frozen=C.map(l=>[Math.abs(l),l<0?1:0]);
        const witness=solve(f.n,f.rows.filter((_,i)=>i!==Math.floor(j/4)),frozen);
        if(witness===null)throw Error("deleted-clause witness missing "+m+" "+j);
        let bad=0;
        for(let t=0;t<f.clauses.length;t++){
          if(!satClause(f.clauses[t],witness)){bad++;if(t!==j)throw Error("other clause false "+m+" "+j+" "+t);}
        }
        if(bad!==1)throw Error("original witness not uniquely bad");
        out.deletion_certificates++;out.unique_falsified_clause_controls++;
        for(let p=0;p<3;p++){
          const bit=offsets[j][p];
          const flip=s[bit]==="0"?"1":"0";
          const neighbor=s.slice(0,bit)+flip+s.slice(bit+1);
          const parsed=parse(neighbor,f.n,f.clauses.length,w);
          if(!parsed)throw Error("mutated source not well formed");
          if(parsed[j][p]!==-C[p])throw Error("wrong literal mutation");
          for(let t=0;t<f.clauses.length;t++){
            if(!satClause(parsed[t],witness))throw Error("mutated source not SAT");
          }
          out.raw_source_parse_controls++;
          out.single_bit_opposite_label_neighbors++;
          here++;
        }
      }
      // Hostile negative: changing a duplicated added clause cannot repair an odd base.
      const dup=f.clauses.map(c=>c.slice());
      dup.push(f.clauses[0].slice());
      dup[dup.length-1][0]*=-1;
      if(dup.length!==f.clauses.length+1||solve(f.n,f.rows)!==null)throw Error("duplicate negative");
      out.duplicate_negative_controls++;
      // Two disjoint odd components: a flip in the first cannot affect the second.
      if(solve(f.n,f.rows)!==null)throw Error("disjoint control second remains UNSAT");
      out.disjoint_product_negative_controls++;
      out.cases.push({m,odd_pattern:q,N:f.n,M:f.clauses.length,L:s.length,
        sensitive_sign_bits:P,neighbors_checked:here,ratio:P/s.length});
    }
    const even=build(m,Array(m).fill(0));
    if(solve(even.n,even.rows)===null)throw Error("even-charge source UNSAT");
    out.even_sat++;
  }
  return out;
}

if(typeof require!=="undefined"&&require.main===module)console.log(JSON.stringify(audit(),null,2));
if(typeof module!=="undefined")module.exports={build,solve,encode,parse,satClause,audit};
