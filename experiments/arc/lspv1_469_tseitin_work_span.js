'use strict';
/* LSPV-1/469. Original signed cubic Tseitin 3-CNF, declared-semantic
   R_mix341 AND3/GF(2) rules only. Historical accepted-byte checker
   is NOT executed and is NOT replaced by this independent program.
   Run: node experiments/arc/lspv1_469_tseitin_work_span.js */
function parity(x){let p=0;while(x){p^=x&1;x>>>=1;}return p;}
function ck(t,msg){if(!t)throw Error(msg);}
function graph(name){
  let h,edges=[];
  if(name==='K4'){h=4;for(let i=0;i<h;i++)for(let j=i+1;j<h;j++)edges.push([i,j]);}
  if(name==='K33'){h=6;for(let i=0;i<3;i++)for(let j=3;j<6;j++)edges.push([i,j]);}
  if(name==='cube'){h=8;for(let i=0;i<h;i++)for(let b=0;b<3;b++){let j=i^(1<<b);if(i<j)edges.push([i,j]);}}
  if(name==='Petersen'){h=10;for(let i=0;i<5;i++){edges.push([i,(i+1)%5]);edges.push([5+i,5+(i+2)%5]);edges.push([i,5+i]);}}
  if(name==='prism6'){h=12;for(let i=0;i<6;i++){edges.push([i,(i+1)%6]);edges.push([6+i,6+(i+1)%6]);edges.push([i,6+i]);}}
  ck(h>0,'graph');let inc=Array.from({length:h},()=>[]);
  edges.forEach(([a,b],i)=>{inc[a].push(i);inc[b].push(i);});
  ck(inc.every(a=>a.length===3),'not cubic');
  return {name,h,edges,inc};
}
function source(g,odd){
  const nodes=[],charges=Array(g.h).fill(0);if(odd)charges[0]=1;
  for(let v=0;v<g.h;v++){
    let ids=g.inc[v].slice().sort((a,b)=>a-b);
    for(let b=0;b<8;b++)if(parity(b)!==charges[v]){
      const lits=ids.map((id,k)=>((b>>k)&1)?-(id+1):id+1);
      nodes.push({kind:'src',parents:[],depth:0,vertex:v,ids,clause:lits,
        mask:Array.from({length:8},(_,a)=>lits.some((lit,k)=>((a>>k)&1)===(lit>0?1:0))?1:0)});
    }
  }
  ck(nodes.length===4*g.h,'four source clauses per vertex');
  return {nodes,charges};
}
function sxor(a,b){
  const s=new Set(a);for(const x of b){if(s.has(x))s.delete(x);else s.add(x);}
  return [...s].sort((x,y)=>x-y);
}
function build(g){
  const {nodes,charges}=source(g,true),rowRoots=[];
  const start=nodes.length;
  function addAnd(a,b){
    const x=nodes[a],y=nodes[b];
    ck(x.mask && y.mask && x.vertex===y.vertex,'AND3 local support');
    const node={kind:'AND3',parents:[a,b],depth:Math.max(x.depth,y.depth)+1,
      vertex:x.vertex,mask:x.mask.map((z,i)=>z&y.mask[i])};
    nodes.push(node);return nodes.length-1;
  }
  for(let v=0;v<g.h;v++){
    const ix=[];for(let i=0;i<start;i++)if(nodes[i].vertex===v)ix.push(i);
    ck(ix.length===4,'local sources');
    const a=addAnd(ix[0],ix[1]),b=addAnd(ix[2],ix[3]),c=addAnd(a,b);
    const expected=Array.from({length:8},(_,m)=>parity(m)===charges[v]?1:0);
    ck(JSON.stringify(nodes[c].mask)===JSON.stringify(expected),'local parity annotation');
    nodes[c].row=g.inc[v].slice().sort((x,y)=>x-y);nodes[c].rhs=charges[v];
    rowRoots.push(c);
  }
  function combine(xs){
    if(xs.length===1)return xs[0];
    const mid=Math.floor(xs.length/2),a=combine(xs.slice(0,mid)),b=combine(xs.slice(mid));
    const x=nodes[a],y=nodes[b];
    ck(x.row && y.row,'GF2 row parents');
    nodes.push({kind:'XOR',parents:[a,b],depth:Math.max(x.depth,y.depth)+1,
      row:sxor(x.row,y.row),rhs:x.rhs^y.rhs});
    return nodes.length-1;
  }
  const root=combine(rowRoots);
  ck(nodes[root].row.length===0 && nodes[root].rhs===1,'not a contradiction');
  return {g,nodes,root,original:start};
}
function structural(nodes,root,m,requireRooted){
  const anc=new Set(),stack=[root];
  while(stack.length){const i=stack.pop();ck(i>=0&&i<nodes.length,'bad pointer');
    if(anc.has(i))continue;anc.add(i);
    for(const j of nodes[i].parents){ck(j<i,'forward/cyclic reference');stack.push(j);}
  }
  const ids=[...anc],src=ids.filter(i=>nodes[i].kind==='src').length;
  if(requireRooted)ck(src===m,'missing indispensable original source');
  const paid=ids.length-src;
  const E=ids.reduce((s,i)=>s+nodes[i].parents.length,0);
  const defect=ids.reduce((s,i)=>s+(nodes[i].kind==='src'?0:2-nodes[i].parents.length),0);
  const cyclomatic=E-(ids.length-1);
  ck(cyclomatic>=0 && defect>=0,'connectivity or fanin invalid');
  ck(paid-(src-1)===cyclomatic+defect,'exact excess identity');
  return {m:src,q:paid,E,defect,cyclomatic,excess:paid-src+1};
}
function evalClause(c,a){return c.some(l=>(((a>>(Math.abs(l)-1))&1)===(l>0?1:0)));}
function countModels(src,n,omit){
  let count=0;
  for(let a=0;a<(1<<n);a++){
    if(src.every((c,i)=>i===omit || evalClause(c.clause,a)))count++;
  }
  return count;
}
function verify(p){
  const {g,nodes,root,original}=p;
  ck(original===4*g.h,'source count');
  const canonical=source(g,true).nodes;
  for(let i=0;i<original;i++)ck(JSON.stringify(nodes[i])===JSON.stringify(canonical[i]),'source authentication');
  for(let i=original;i<nodes.length;i++){
    const t=nodes[i];ck(t.parents.length===2 && t.parents.every(j=>j>=0&&j<i),'binary native parents');
    const x=nodes[t.parents[0]],y=nodes[t.parents[1]];
    ck(t.depth===Math.max(x.depth,y.depth)+1,'depth');
    if(t.kind==='AND3'){
      ck(x.vertex===t.vertex&&y.vertex===t.vertex,'AND3 locality');
      ck(JSON.stringify(t.mask)===JSON.stringify(x.mask.map((z,k)=>z&y.mask[k])),'AND3 false output');
      if(t.row){
        const rhs=source(g,true).charges[t.vertex];
        const expect=Array.from({length:8},(_,a)=>parity(a)===rhs?1:0);
        ck(JSON.stringify(t.mask)===JSON.stringify(expect),'false affine annotation');
        ck(JSON.stringify(t.row)===JSON.stringify(g.inc[t.vertex].slice().sort((a,b)=>a-b)),'row mask');
        ck(t.rhs===rhs,'row rhs');
      }
    }else if(t.kind==='XOR'){
      ck(x.row&&y.row,'XOR input');
      ck(JSON.stringify(t.row)===JSON.stringify(sxor(x.row,y.row)),'bad XOR mask');
      ck(t.rhs===(x.rhs^y.rhs),'bad XOR rhs');
    }else throw Error('unknown native rule '+t.kind);
  }
  ck(nodes[root].kind==='XOR' && nodes[root].row.length===0 && nodes[root].rhs===1,'terminal not false');
  const st=structural(nodes,root,original,true);
  ck(st.q===4*g.h-1 && st.cyclomatic===0 && st.defect===0,'work/tree minimum');
  const span=nodes[root].depth;
  ck(span===Math.ceil(Math.log2(original)),'nonoptimal span');
  const outdegree=Array(nodes.length).fill(0);
  for(let i=0;i<nodes.length;i++)for(const j of nodes[i].parents)outdegree[j]++;
  ck(outdegree.every((d,i)=>i===root?d===0:d===1),'optimum must be tree');
  return {family:g.name,vertices:g.h,edgeVariables:g.edges.length,
    original3Clauses:original,work:st.q,span,lowerWork:original-1,
    lowerSpan:Math.ceil(Math.log2(original)),cycles:st.cyclomatic,
    unaryDeficit:st.defect};
}
function run(){
  const cases=[],negatives=[];
  for(const name of ['K4','K33','cube','Petersen','prism6']){
    const p=build(graph(name)),summary=verify(p);
    if(p.g.edges.length<=12){
      const odd=countModels(p.nodes.slice(0,p.original),p.g.edges.length,-1);
      ck(odd===0,'odd model unexpectedly exists');
      for(let j=0;j<p.original;j++)ck(countModels(p.nodes.slice(0,p.original),p.g.edges.length,j)>0,'nonessential source');
      const even=source(p.g,false).nodes;
      const count=countModels(even,p.g.edges.length,-1);
      ck(count===(1<<(p.g.edges.length-p.g.h+1)),'even model count');
      summary.exhaustiveEvenModels=count;
      summary.exhaustiveDeletionWitnesses=p.original;
    }
    cases.push(summary);
    if(name==='K4'){
      function reject(label,change){const bad=JSON.parse(JSON.stringify(p));change(bad);
        try{verify(bad);}catch(e){negatives.push(label);return;}throw Error('corrupt accepted: '+label);}
      reject('changed original source literal',p=>{p.nodes[0].clause[0]*=-1;});
      reject('forged affine row',p=>{const j=p.nodes.findIndex(n=>n.kind==='AND3'&&n.row);p.nodes[j].rhs^=1;});
      reject('forged XOR row',p=>{p.nodes[p.root].row=[0];});
      reject('forged terminal charge',p=>{p.nodes[p.root].rhs=0;});
      reject('cyclic dependency',p=>{p.nodes[p.root].parents[0]=p.root;});
      reject('missing source dependency',p=>{const j=p.nodes.findIndex(n=>n.kind==='AND3');p.nodes[j].parents=[0,0];});
      reject('forged depth',p=>{p.nodes[p.root].depth=1;});
    }
  }
  // Two acyclic abstract graph accounting controls (not native logical proofs).
  const toy1=[{kind:'src',parents:[]},{kind:'src',parents:[]},
    {kind:'LOCAL',parents:[0]},{kind:'JOIN',parents:[2,1]}];
  const a=structural(toy1,3,2,true);
  ck(a.q===2&&a.defect===1&&a.cyclomatic===0,'unary accounting');
  const toy2=[{kind:'src',parents:[]},{kind:'src',parents:[]},
    {kind:'JOIN',parents:[0,1]},{kind:'JOIN',parents:[0,2]},
    {kind:'JOIN',parents:[2,3]}];
  const b=structural(toy2,4,2,true);
  ck(b.q===3&&b.cyclomatic===2&&b.defect===0,'reconvergent accounting');
  ck(negatives.length===7,'negative controls missing');
  return {schema:'LSPV1-469/v1',status:'PASS',classification:'PROVED/RESTRICTED declared-semantic model; computational finite checks',
    theorem:'q-(m-1)=cyclomatic+sum(2-indegree); min q=m-1 and min span=ceil(log2 m) on cubic odd-Tseitin',
    cases,negative_controls:negatives,
    abstract_graph_controls:[a,b],
    limitations:'Not the historical accepted-byte R_mix341 checker; no B1/B2/B3, no superpolynomial mixed lower bound, no actual parallel machine schedule'};
}
if(typeof module!=='undefined'&&require.main===module)console.log(JSON.stringify(run(),null,2));
