"use strict";
// TMR-2/007 independent cubic torus graph, parity-CNF, source and GF(2) test runner.
function graph(m) {
  const n=2*m*m, e=[], H=(i,j)=>i*m+((j+m)%m), V=(i,j)=>m*m+((i+m)%m)*m+j, I=(i,j)=>2*m*m+i*m+j;
  const v=(i,j,a)=>2*(i*m+j)+a;
  for(let i=0;i<m;i++)for(let j=0;j<m;j++){
    e.push([v(i,j,0),v(i,(j+1)%m,0)]);
    e.push([v(i,j,1),v((i+1)%m,j,1)]);
    e.push([v(i,j,0),v(i,j,1)]);
  }
  const a=Array.from({length:n},()=>[]); e.forEach(([u,vv],k)=>{a[u].push(k+1);a[vv].push(k+1)});
  const tri=[];
  for(let i=0;i<m;i++)for(let j=0;j<m;j++){
    // Edges in construction order: H(i,j)=3*(i*m+j)+1, V=+2, I=+3.
    tri.push([3*(i*m+((j+m-1)%m))+1,3*(i*m+j)+1,3*(i*m+j)+3]);
    tri.push([3*(((i+m-1)%m)*m+j)+2,3*(i*m+j)+2,3*(i*m+j)+3]);
  }
  return {m,n,e,a,tri};
}

function connected(g,removed=-1) {
  let start=0;while(start===removed)start++;
  const seen=new Set([start]), q=[start];
  for(let p=0;p<q.length;p++){let u=q[p];for(let [x,y] of g.e){let v=x===u?y:y===u?x:-1;if(v!==-1&&v!==removed&&!seen.has(v)){seen.add(v);q.push(v)}}}
  return seen.size===g.n-(removed>=0?1:0);
}

function compile(g,charges) {
  const clauses=[],rows=[];
  for(let k=0;k<g.n;k++){
    const ids=g.tri[k], b=charges[k];rows.push([ids,b]);
    for(let t=0;t<8;t++){let s=[(t>>2)&1,(t>>1)&1,t&1];if((s[0]^s[1]^s[2])!==b)clauses.push(ids.map((x,j)=>s[j]?-x:x))}
  }
  let N=g.e.length,M=clauses.length,w=Math.max(1,Math.ceil(Math.log2(N))),s="1".repeat(N)+"0"+"1".repeat(M)+"0",pos=[];
  for(const c of clauses)for(const x of c){pos.push(s.length);s+=(x<0?"1":"0")+Math.abs(x).toString(2).padStart(w,"0")}
  return {clauses,rows,source:s,pos,N,M,w,charges};
}

function recognize(s) {
  let p=0,N=0,M=0;
  while(s[p]==="1"){p++;N++}if(s[p++]!=="0")return null;
  while(s[p]==="1"){p++;M++}if(s[p++]!=="0")return null;
  let m=Math.round(Math.sqrt(N/3));
  if(m<3||3*m*m!==N||8*m*m!==M)return null;
  let w=Math.max(1,Math.ceil(Math.log2(N)));
  if(s.length!==p+3*M*(w+1))return null;
  let zsum=0, checked=0;
  const expectedTriple=(i,j,a)=>{
    let off=3*(i*m+j);
    return a===0?[3*(i*m+((j+m-1)%m))+1,off+1,off+3]:
       [3*(((i+m-1)%m)*m+j)+2,off+2,off+3];
  };
  for(let i=0;i<m;i++)for(let j=0;j<m;j++)for(let a=0;a<2;a++){
    let ids=expectedTriple(i,j,a),z=-1;
    for(let c=0;c<4;c++){
      let t=0;
      for(let h=0;h<3;h++){
        let ch=s[p++];if(ch!=="0"&&ch!=="1")return null;
        t=(t<<1)|(ch==="1"?1:0);
        const bits=s.slice(p,p+w);p+=w;
        if(bits.length!==w||!/^[01]+$/.test(bits)||parseInt(bits,2)!==ids[h])return null;
        checked+=w+1;
      }
      if(c===0)z=t===0?1:t===1?0:-1;
      if(z<0)return null;
      let allowed=z===0?[1,2,4,7]:[0,3,5,6];
      if(t!==allowed[c])return null;
    }
    zsum^=z;
  }
  if(p!==s.length)return null;
  return {m,N,M,checked,label:zsum?"UNSAT":"SAT",charge_xor:zsum};
}

function solve(N,rows,freeze=[]) {
  const piv=new Map();
  for(let [ids,b] of rows.concat(freeze.map(([id,b])=>[[id],b]))){
    let mask=0n, z=b;
    for(let id of ids)mask^=1n<<BigInt(id-1);
    while(mask){let k=mask.toString(2).length-1, prev=piv.get(k);if(!prev){piv.set(k,[mask,z]);break}mask^=prev[0];z^=prev[1]}
    if(mask===0n&&z)return null;
  }
  const ans=Array(N+1).fill(0), sorted=[...piv.keys()].sort((a,b)=>a-b);
  for(const k of sorted){
    let [mask,z0]=piv.get(k),z=z0,low=mask^(1n<<BigInt(k));
    while(low){let lowbit=low&-low,idx=lowbit.toString(2).length-1;z^=ans[idx+1];low^=lowbit}
    ans[k+1]=z;
  }
  return ans;
}

function audit() {
  let o={id:"TMR2-TORUS-CUBIC-STREAM007",status:"COMPUTATIONAL",cases:[],connectivity_deletion_checks:0,odd_unsat_checks:0,even_sat_checks:0,clause_deletion_witnesses:0,single_bit_sat_neighbors:0,sign_mutation_fastpath_rejections:0,structural_fastpath_rejections:0,independent_clause_evaluation:0,failures:0,notes:"Source-level native V8 checks with BigInt GF(2); not an instruction-level Turing machine."};
  for(let m of [3,4,5]){
    const g=graph(m);if(g.e.length!==3*m*m||g.n!==2*m*m||g.a.some(z=>z.length!==3))throw Error("size/degree");
    if(!connected(g))throw Error("disconnected");
    for(let v=0;v<g.n;v++){if(!connected(g,v))throw Error("not biconnected "+m+" "+v);o.connectivity_deletion_checks++}
    for(let kind of [0,1,2,3]){
      const charge=Array(g.n).fill(0);
      if(kind===0)charge[0]=1;
      if(kind===1)for(let i of [0,1,2])charge[i]=1;
      if(kind===3)for(let i of [0,1])charge[i]=1;
      const f=compile(g,charge),ans=recognize(f.source);
      const expected=kind<2?"UNSAT":"SAT";
      if(!ans||ans.label!==expected||ans.checked!==3*f.M*(f.w+1))throw Error("recognizer mismatch");
      if(expected==="UNSAT"){if(solve(f.N,f.rows)!==null)throw Error("odd system SAT");o.odd_unsat_checks++;}
      else{let witness=solve(f.N,f.rows);if(!witness)throw Error("even system UNSAT");o.even_sat_checks++;}
      o.cases.push({m,kind,label:expected,N:f.N,M:f.M,L:f.source.length,sign_bits:3*f.M,primal_tw_lower:(m-2)/2});
      if(expected==="UNSAT"){
        for(let c=0;c<f.M;c++){
          let lit=f.clauses[c], freeze=lit.map(x=>[Math.abs(x),+(x<0)]), rem=f.rows.filter((_,j)=>j!==Math.floor(c/4));
          let witness=solve(f.N,rem,freeze);if(!witness)throw Error("deletion not SAT");
          for(let k=0;k<f.M;k++){let satisfied=f.clauses[k].some(x=>witness[Math.abs(x)]==+(x>0));o.independent_clause_evaluation++;if(satisfied===(c===k))throw Error("unique false failure")}
          o.clause_deletion_witnesses++;
          for(let h=0;h<3;h++){
            let idx=3*c+h,p=f.pos[idx],orig=f.source[p],mut=f.source.slice(0,p)+(orig==="1"?"0":"1")+f.source.slice(p+1);
            if(mut.length!==f.source.length||recognize(mut)!==null)throw Error("source sign mutation accepted");o.sign_mutation_fastpath_rejections++;
            const changed=f.clauses.map((z,j)=>j===c?z.map((x,k)=>k===h?-x:x):z);
            if(!changed[c].some(x=>witness[Math.abs(x)]==+(x>0)))throw Error("flip no witness");
            o.single_bit_sat_neighbors++;
          }
        }
      }
      if(recognize(f.source+"0")!==null||recognize(f.source.slice(0,-1))!==null)throw Error("suffix/prefix mutation accepted");
      o.structural_fastpath_rejections+=2;
      if(m===3&&kind===0){
        let bad=f.source.slice(0,10)+"0"+f.source.slice(11);
        if(recognize(bad)!==null)throw Error("header mutation");o.structural_fastpath_rejections++;
      }
    }
  }
  return o;
}

if(typeof module!=="undefined"&&require.main===module) console.log(JSON.stringify(audit(),null,2));
if(typeof module!=="undefined") module.exports={graph,connected,compile,recognize,solve,audit};
