// LSPV-1/483 independent guarded-Resolution finite control.
// This is NOT a historical R_mix341 checker or a full mixed-rule compiler.
const canon=a=>[...new Set(a)].sort((x,y)=>Math.abs(x)-Math.abs(y)||x-y);
const eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
function source(odd){
  const edges=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]],out=[];
  for(let v=0;v<4;v++){
    const es=edges.map((e,i)=>e.includes(v)?i+1:0).filter(Boolean);
    for(let b=0;b<8;b++){
      const bits=[b&1,(b>>1)&1,(b>>2)&1];
      if(bits.reduce((a,c)=>a+c,0)%2===(odd&&v===0?1:0))continue;
      out.push(canon(es.map((x,i)=>bits[i]?-x:x)));
    }
  }return out;
}
function models(F){let sum=0;for(let k=0;k<64;k++)
  if(F.every(C=>C.some(l=> l>0?!!(k&(1<<(l-1))):!(k&(1<<(-l-1))))))sum++;
  return sum;
}
function trial(s){
  const F=source(true),nodes=[];
  const add=(kind,c,parents=[],pivot=null,orig=null)=>{
    const id=nodes.length;nodes.push({id,kind,c:canon(c),parents,pivot,orig});return id;};
  const sids=F.map((c,i)=>add("src",c,[],null,i));
  const weak=(id,c)=>eq(nodes[id].c,canon(c))?id:add("weak",c,[id]);
  const resolve=(i,j,p)=>{
    const A=nodes[i].c,B=nodes[j].c;
    if(!A.includes(p)||!B.includes(-p))throw Error("invalid resolution");
    const C=canon(A.filter(x=>x!==p).concat(B.filter(x=>x!==-p)));
    if(C.some(x=>C.includes(-x)))throw Error("taut resolvent");
    return add("res",C,[i,j],p);};
  let leaves=new Map();
  for(let mask=0;mask<(1<<s);mask++){
    const ass=new Map(Array.from({length:s},(_,i)=>[i+1,(mask>>i)&1]));
    const guard=Array.from({length:s},(_,i)=>((mask>>i)&1)?-(i+1):i+1);
    const cur=new Map();
    for(let i=0;i<F.length;i++){
      const C=F[i];
      if(C.some(l=>ass.has(Math.abs(l))&&Number(l>0)===ass.get(Math.abs(l))))continue;
      const restricted=canon(C.filter(l=>!ass.has(Math.abs(l))));
      const key=JSON.stringify(restricted);
      if(!cur.has(key))cur.set(key,{c:restricted,id:weak(sids[i],canon([...restricted,...guard]))});
    }
    for(let v=s+1;v<=6;v++){
      const entries=[...cur.values()],newNodes=new Map();
      const pos=entries.filter(x=>x.c.includes(v)),neg=entries.filter(x=>x.c.includes(-v));
      for(const A of pos)for(const B of neg){
        const C=canon(A.c.filter(x=>x!==v).concat(B.c.filter(x=>x!==-v)));
        if(C.some(x=>C.includes(-x)))continue;
        const key=JSON.stringify(C);
        if(!cur.has(key)&&!newNodes.has(key))newNodes.set(key,{c:C,id:resolve(A.id,B.id,v)});
      }
      for(const [k,val] of cur)if(val.c.includes(v)||val.c.includes(-v))cur.delete(k);
      for(const [k,val] of newNodes)cur.set(k,val);
      if(cur.has("[]"))break;
    }
    if(!cur.has("[]"))throw Error("missing branch UNSAT proof");
    leaves.set(mask,cur.get("[]").id);
  }
  for(let depth=s-1;depth>=0;depth--){
    const next=new Map();
    for(let pre=0;pre<(1<<depth);pre++){
      const left=leaves.get(pre),right=leaves.get(pre+(1<<depth));
      // map: prefix bits are low bits, fixed bit at depth on right
      next.set(pre,resolve(left,right,depth+1));
    }leaves=next;
  }
  function verify(){
    for(let i=0;i<nodes.length;i++){
      const n=nodes[i],A=n.parents.map(p=>nodes[p]);
      if(n.id!==i||!eq(n.c,canon(n.c))||n.c.some(x=>n.c.includes(-x)))throw Error("bad line");
      if(n.kind==="src"){if(n.parents.length||!eq(n.c,F[n.orig]))throw Error("bad source");}
      else if(n.kind==="weak"){
        if(A.length!==1||n.parents[0]>=i||!A[0].c.every(x=>n.c.includes(x)))throw Error("bad weak");
      } else if(n.kind==="res"){
        if(A.length!==2||n.parents.some(p=>p>=i)||!A[0].c.includes(n.pivot)||!A[1].c.includes(-n.pivot)
          ||!eq(n.c,canon(A[0].c.filter(x=>x!==n.pivot).concat(A[1].c.filter(x=>x!==-n.pivot)))))
          throw Error("bad res");
      } else throw Error("unknown rule");
    }
    if(!eq(nodes[nodes.length-1].c,[]))throw Error("wrong final");
    return true;
  }
  verify();
  let rejected=0;
  const mutate=(index,key,val)=>{
    const old=nodes[index][key];nodes[index][key]=val;
    try{verify();}catch(e){rejected++;}
    nodes[index][key]=old;verify();
  };
  mutate(0,"c",[7]);mutate(nodes.length-1,"c",[1]);
  if(s){mutate(nodes.length-1,"parents",[nodes.length+30,nodes.length+31]);}
  const count=key=>nodes.filter(n=>n.kind===key).length;
  return {fixed_original_vars:s,all_AND_branches:1<<s,original_sources:16,
    source_nodes:count("src"),weakening_nodes:count("weak"),resolution_nodes:count("res"),
    total_nodes:nodes.length,malicious_rejected:rejected,final_empty:true};
}
function run(){
  if(models(source(true))!==0||models(source(false))!==8)throw Error("odd/even models");
  const rows=[0,1,2,3].map(trial);
  // gate dependency support: g1=x1 XOR x2; g2=g1 AND x3; |S|=3<=2d.
  const gates=[];for(let a=0;a<8;a++)gates.push([a,((a&1)^((a>>1)&1))&((a>>2)&1)]);
  return {status:"PASS",scope:"original-source guarded Resolution and 2-gate truth-table, not historical native checker",
    odd_models:0,even_models:8,rows,gates,corrupt_rejected:rows.reduce((a,r)=>a+r.malicious_rejected,0)};
}
const result=run();if(result.corrupt_rejected!==11)throw Error("corrupt controls");return result;
