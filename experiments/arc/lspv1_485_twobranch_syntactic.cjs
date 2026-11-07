// LSPV-1/485 | syntactic two-branch original-source Res(XOR) certificate.
'use strict';
function run(){
 let checks=0,verified=0;
 const ck=(b,s)=>{checks++;if(!b)throw Error(s)};
 const E=(m,b)=>m+":"+b,parse=s=>s.split(":").map(Number);
 const plus=(a,b)=>{let x=parse(a),y=parse(b);return E(x[0]^y[0],x[1]^y[1])};
 const neg=a=>{let x=parse(a);return E(x[0],x[1]^1)};
 const norm=a=>[...new Set(a)].sort(),eq=(a,b)=>JSON.stringify(norm(a))===JSON.stringify(norm(b));
 const edges=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]];
 const source=charge=>{
  let c=[];for(let v=0;v<4;v++){
   let incident=edges.map((p,i)=>p.includes(v)?i:-1).filter(i=>i>=0);
   for(let a=0;a<8;a++)if(((a&1)^((a>>1)&1)^((a>>2)&1))!==charge[v])
    c.push(incident.map((id,j)=>((a>>j)&1)?-(id+1):id+1));
  }return c
 };
 const F=source([1,0,0,0]),H=source([0,0,0,0]);
 const sat=(C,a)=>C.every(c=>c.some(l=>((a>>(Math.abs(l)-1))&1)===(l>0?1:0)));
 ck(F.length===16&&H.length===16,"source count");
 ck(Array.from({length:64},(_,i)=>i).filter(x=>sat(F,x)).length===0,"odd UNSAT");
 ck(Array.from({length:64},(_,i)=>i).filter(x=>sat(H,x)).length===8,"even SAT");
 let nodes=[],put=(r,c,meta={})=>{nodes.push({r,c:norm(c),...meta});return nodes.length-1};
 const S=F.map((c,k)=>put("SRC",c.map(l=>E(1<<(Math.abs(l)-1),l>0?1:0)),{k}));
 const B=Array.from({length:6},(_,i)=>put("BOOL",[E(1<<i,0),E(1<<i,1)],{i}));
 const w=(p,a)=>put("WEAK",[...nodes[p].c,...a],{p,a});
 const lin=(p,q,a,b)=>put("LIN",[...nodes[p].c.filter(t=>t!==a),...nodes[q].c.filter(t=>t!==b),plus(a,b)],{p,q,a,b});
 const drop=p=>put("DROP",nodes[p].c.filter(t=>t!=="0:1"),{p});
 // 4-case native syntactic Booleanity induction, not semantic weakening.
 const merge=(p,q,A,D)=>{
  let leaf=[];
  for(let x=0;x<2;x++)for(let y=0;y<2;y++){
   let a=E(A,x),b=E(D,y);
   leaf.push(w(lin(w(p,[neg(b)]),w(q,[neg(a)]),a,b),[neg(plus(a,b))]))
  }
  const l=drop(lin(leaf[0],leaf[1],E(D,1),E(D,0)));
  const r=drop(lin(leaf[2],leaf[3],E(D,1),E(D,0)));
  return drop(lin(l,r,E(A,1),E(A,0)));
 };
 let bool=B[0],mask=1;
 for(let i of [1,3,5]){bool=merge(bool,B[i],mask,1<<i);mask^=1<<i}
 ck(mask===43&&eq(nodes[bool].c,[E(mask,0),E(mask,1)]),"affine Booleanity");
 let root=[];
 for(let b=0;b<2;b++){
  let leaves=[];
  for(let a=0;a<64;a++){
   let k=F.findIndex(c=>!c.some(l=>((a>>(Math.abs(l)-1))&1)===(l>0?1:0)));
   ck(k>=0,"source coverage");
   let blocker=Array.from({length:6},(_,i)=>E(1<<i,1-((a>>i)&1)));
   leaves.push(w(S[k],[...blocker,E(mask,b^1)]));
  }
  for(let i=0;i<6;i++){
   let out=[];for(let j=0;j<leaves.length;j+=2)
    out.push(drop(lin(leaves[j],leaves[j+1],E(1<<i,1),E(1<<i,0))));
   leaves=out
  }
  ck(eq(nodes[leaves[0]].c,[E(mask,b^1)]),"every AND obligation paid");root.push(leaves[0]);
 }
 drop(lin(root[0],root[1],E(mask,1),E(mask,0)));
 function verify(a){
  for(let i=0;i<a.length;i++){
   let t=a[i],z;
   if(t.r==="SRC"){ck(Number.isInteger(t.k)&&t.k>=0&&t.k<F.length,"source ID");z=F[t.k].map(l=>E(1<<(Math.abs(l)-1),l>0?1:0))}
   else if(t.r==="BOOL"){ck(Number.isInteger(t.i)&&t.i>=0&&t.i<6,"Boolean axiom");z=[E(1<<t.i,0),E(1<<t.i,1)]}
   else if(t.r==="WEAK"){ck(t.p<i&&t.p>=0,"WEAK reference");z=[...a[t.p].c,...t.a]}
   else if(t.r==="LIN"){ck(t.p<i&&t.q<i&&t.p>=0&&t.q>=0,"LIN reference");
     ck(a[t.p].c.includes(t.a)&&a[t.q].c.includes(t.b),"LIN premise");
     z=[...a[t.p].c.filter(s=>s!==t.a),...a[t.q].c.filter(s=>s!==t.b),plus(t.a,t.b)]}
   else if(t.r==="DROP"){ck(t.p<i&&t.p>=0&&a[t.p].c.includes("0:1"),"DROP source");z=a[t.p].c.filter(s=>s!=="0:1")}
   else throw Error("unknown rule");
   ck(eq(t.c,z),"illegal inference");verified++
  }
  ck(a.at(-1).c.length===0,"missing final contradiction");
 }
 verify(nodes);let rejection=0;
 for(let id=0;id<6;id++){
  let bad=JSON.parse(JSON.stringify(nodes));
  if(id===0)bad[0].k=1;
  if(id===1)bad.at(-2).a="1:1";
  if(id===2)bad.at(-1).c=["0:1"];
  if(id===3)bad.at(-2).q=root[0];
  if(id===4)bad.at(-10).p=nodes.length+1;
  if(id===5)bad[2].r="ORACLE";
  try{verify(bad)}catch{rejection++}
 }
 ck(rejection===6,"corruptions rejected");
 let nonaff=0;
 for(let t=0;t<16;t++){
  let f=Array.from({length:4},(_,i)=>(t>>i)&1);
  let c=f[0],alpha=f[1]^c,beta=f[2]^c,gamma=f[3]^f[2]^f[1]^c;
  nonaff+=gamma;
  for(let x=0;x<2;x++)for(let y=0;y<2;y++)
   ck(((t>>(x+2*y))&1)===(c^(alpha&x)^(beta&y)^(gamma&x&y)),"ANF");
  if(gamma)for(let x=0;x<2;x++)for(let y=0;y<2;y++)
   ck(((t>>(x+2*y))&1)===(c^(alpha&x)^((beta^x)&y)),"one-input specialization")
 }
 ck(nonaff===8,"eight nonlinear tables");
 return {status:"PASS",model:"syntactic Res(XOR), not historical R_mix341",clauses:16,vars:6,branches:2,
  proof_nodes:nodes.length,verified_records:verified,corruptions_rejected:rejection,
  checked_binary_truth_tables:16,nonaffine_truth_tables:nonaff,checks};
}
if(typeof module!=="undefined")module.exports={run};