// LSPV-1/431: exhaustive affine two-branch join, including empty branches.
// Self-contained Node.js, no external dependencies, deterministic.
const assert = require("assert").strict;
const pop = x => {let p=0;while(x){p^=x&1;x>>>=1;}return p};
let checks=0;
const ok = (x,msg) => {assert.ok(x,msg);checks++};
const equations = n => {
  const e=[];
  for(let v=0;v<(1<<n);v++) for(let c=0;c<2;c++){
    let mask=0n;
    for(let y=0;y<(1<<n);y++) if(pop(v&y)===c) mask|=1n<<BigInt(y);
    e.push({v,c,mask});
  }
  return e;
};
const spaces = n => {
  const all=(1n<<BigInt(1<<n))-1n, eq=equations(n), seen=new Set([all.toString()]), list=[all];
  for(let i=0;i<list.length;i++) for(const e of eq){
    const m=list[i]&e.mask, key=m.toString();
    if(!seen.has(key)){seen.add(key);list.push(m);}
  }
  return list;
};
const basisMap=(s,n)=>{
  if(s===0n)return null;
  const ys=[];
  for(let y=0;y<(1<<n);y++)if((s>>BigInt(y))&1n)ys.push(y);
  const m=new Map();
  for(let v=0;v<(1<<n);v++){
    const rhs=pop(v&ys[0]);
    if(ys.every(y=>pop(v&y)===rhs))m.set(v,rhs);
  }
  return m;
};
const actual=(s0,s1,n)=>{
  const union=s0|(s1<<BigInt(1<<n));
  return equations(n+1).filter(e=>(union & ~e.mask)===0n)
    .map(e=>2*e.v+e.c);
};
const predicted=(s0,s1,n)=>{
  const m0=basisMap(s0,n),m1=basisMap(s1,n),out=[];
  for(let v=0;v<(1<<n);v++)for(let a=0;a<2;a++)for(let c=0;c<2;c++){
    if(m0 && m0.get(v)!==c)continue;
    if(m1 && m1.get(v)!==(c^a))continue;
    out.push(2*(v|(a<<n))+c);
  }
  return out.sort((a,b)=>a-b);
};
const rows=[];
for(let n=1;n<=4;n++){
  const sp=spaces(n);
  ok(sp.length===[0,4,12,52,308][n],"affine-space count");
  const row={n,spaces:sp.length,pairs:0,bothNonempty:0,oneEmpty:0,bothEmpty:0,equationCandidates:0};
  for(const s0 of sp)for(const s1 of sp){
    const a=actual(s0,s1,n),p=predicted(s0,s1,n);
    ok(a.length===p.length,"size");ok(a.every((v,i)=>v===p[i]),"equation mismatch");
    const m0=basisMap(s0,n),m1=basisMap(s1,n);
    let dim;
    if(m0&&m1){
      const shared=[...m0.keys()].filter(v=>m1.has(v));
      dim=Math.log2(shared.length);
      const same=shared.filter(v=>m0.get(v)===m1.get(v)).length;
      ok(a.filter(z=>((z>>1)&(1<<n))===0).length===same,"guard-free equations");
      row.bothNonempty++;
    }else if(m0||m1){dim=Math.log2((m0||m1).size)+1;row.oneEmpty++;}
    else{dim=n+2;row.bothEmpty++;}
    ok(Number.isInteger(dim)&&a.length===2**dim,"dimension");
    row.pairs++;row.equationCandidates+=2**(n+2);
  }
  rows.push(row);
}
// Original-source K4 cubic Tseitin strict-3CNF controls.
const edges=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]];
const incident=Array.from({length:4},()=>[]);
edges.forEach(([u,v],i)=>{incident[u].push(i);incident[v].push(i);});
function clauses(charges){
  const cls=[];
  for(let u=0;u<4;u++)for(let a=0;a<8;a++)if(pop(a)!==charges[u])
    cls.push(incident[u].map((e,j)=>((a>>j)&1)?-(e+1):(e+1)));
  return cls;
}
const family={};
for(const [name,charges] of [["odd",[1,0,0,0]],["even",[0,0,0,0]]]){
  const cls=clauses(charges);
  const holds=(c,y)=>c.some(l=>(l>0)===Boolean((y>>(Math.abs(l)-1))&1));
  const models=Array.from({length:64},(_,i)=>i).filter(y=>cls.every(c=>holds(c,y)));
  const b=[models.filter(y=>(y&1)===0).length,models.filter(y=>(y&1)===1).length];
  ok(cls.length===16&&cls.every(c=>c.length===3&&new Set(c.map(Math.abs)).size===3));
  ok(models.length===(name==="odd"?0:8));
  ok(name==="odd"?b.every(z=>z===0):b.every(z=>z===4));
  family[name]={clauses:16,variables:6,models:models.length,splitCounts:b};
}
const result={status:"COMPUTATIONAL",rows,family,assertions:checks,
  disclaimer:"Semantic truth tables only, not an authenticated historical R_mix341 proof or a P-vs-NP transfer"};
console.log(JSON.stringify(result,null,2));
