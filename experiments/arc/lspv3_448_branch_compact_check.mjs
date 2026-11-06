#!/usr/bin/env node
// LSPV-3/448 standalone source-authenticated K4 two-arm Resolution checker.
// Usage: node lspv3_448_branch_compact_check.mjs full_packet_p1.json [...]
// The complete Python producer and independently written full hostile-control
// checker are in LSPV3_448_BRANCH_DISCHARGE_REPRO.zip.
// NOT an execution of an authenticated historical R_mix341 binary checker.
import fs from 'node:fs';
import crypto from 'node:crypto';
function assert(p,m){if(!p)throw Error(m);}
function canon(a){return [...new Set(a)].sort((x,y)=>Math.abs(x)-Math.abs(y)||x-y);}
function equal(a,b){return JSON.stringify(a)===JSON.stringify(b);}
function source(){
  const edges=[];for(let i=0;i<4;i++)for(let j=i+1;j<4;j++)edges.push([i,j]);
  const charges=[1,0,0,0],cs=[];
  for(let v=0;v<4;v++){
    const es=edges.map(([a,b],i)=>(v===a||v===b)?i+1:0).filter(Boolean);
    for(let a=0;a<8;a++){
      const bits=[(a>>2)&1,(a>>1)&1,a&1];
      if((bits[0]^bits[1]^bits[2])===charges[v])continue;
      cs.push(canon(es.map((x,i)=>bits[i]?-x:x)));
    }
  }
  const dim='p cnf 6 16\n'+cs.map(c=>c.join(' ')+' 0\n').join('');
  return {cs,dim,sha:crypto.createHash('sha256').update(dim,'ascii').digest('hex')};
}
function verifyNodes(nodes,clauses,assumption){
  let assumed=0;
  nodes.forEach((n,i)=>{
    assert(n.id===i&&equal(n.clause,canon(n.clause)), 'id/canonical');
    assert(n.parents instanceof Array,'parents');
    if(n.kind==='SOURCE'){
      assert(n.source_index===i&&i<16&&equal(n.clause,clauses[i]),'source spoof');
      assert(n.parents.length===0,'source parents');
    }else if(n.kind==='ASSUME'){
      assert(assumption!==null && i===16 && assumed++===0,'not a legal temporary assumption');
      assert(equal(n.clause,[assumption])&&n.parents.length===0,'assumption sign');
    }else{
      assert(n.kind==='RES'&&n.parents.length===2,'unlicensed rule');
      const [a,b]=n.parents,p=n.pivot;
      assert(a<i&&a>=0&&b<i&&b>=0,'cyclic/bad reference');
      const A=nodes[a].clause,B=nodes[b].clause;
      assert(A.includes(p)&&B.includes(-p),'pivot polarity');
      const C=canon([...A.filter(x=>x!==p),...B.filter(x=>x!==-p)]);
      assert(!C.some(x=>C.includes(-x))&&equal(C,n.clause),'wrong resolvent');
    }
  });
  if(assumption!==null) assert(assumed===1,'absent assumption');
}
function ancestors(nodes,root){
  const result=new Set(),pending=[root];
  while(pending.length){
    const i=pending.pop();
    assert(i>=0&&i<nodes.length,'bad ancestor');
    if(result.has(i))continue;
    result.add(i);pending.push(...nodes[i].parents);
  }
  return result;
}
function check(packet){
  const {cs,dim,sha}=source();
  assert(packet.source_sha256===sha && packet.source_ascii===dim,'source bytes/hash');
  assert(equal(packet.source_clauses,cs),'source definition');
  assert(packet.branches.length===2,'missing AND arm');
  const x=packet.branches[0].assumption;
  assert(x>0&&x<=6&&packet.branches[1].assumption===-x,'bad split');
  const branchClauses=[];
  for(const B of packet.branches){
    verifyNodes(B.branch.nodes,cs,B.assumption);
    assert(equal(B.branch.nodes[B.branch.root].clause,[]),'unproved branch');
    assert(ancestors(B.branch.nodes,B.branch.root).has(16),'assumption not used');
    assert(equal(B.result_clause,[-B.assumption]),'failed discharge');
    branchClauses.push(B.result_clause);
  }
  verifyNodes(packet.compiled.nodes,cs,null);
  const L=packet.compiled.nodes,root=packet.compiled.root,A=ancestors(L,root);
  assert(equal(L[root].clause,[]),'not a refutation');
  assert(packet.branches.every(b=>A.has(b.result_ref)&&equal(L[b.result_ref].clause,b.result_clause)),'branch reference missing');
  const final=L[root];assert(final.kind==='RES'&&Math.abs(final.pivot)===x,'missing RES join');
  const paid=[...A].filter(i=>L[i].kind==='RES').length;
  const sources=[...A].filter(i=>L[i].kind==='SOURCE').length;
  assert(paid===31&&sources===16,'fixture work or provenance drift');
  // Independent truth-label check of this *finite original input*, not proof hardness.
  for(let mask=0;mask<64;mask++){
    const sat=cs.every(c=>c.some(z=>(z>0)===Boolean((mask>>(Math.abs(z)-1))&1)));
    assert(!sat,'source is unexpectedly SAT');
  }
  return {pivot:x,verified:true,paid_RES:paid,indexed_sources:sources,goal_ancestors:A.size,source_sha256:sha};
}
const argv=process.argv.slice(2);
assert(argv.length>0,'Usage: node lspv3_448_branch_compact_check.mjs full_packet_p1.json [...]');
for(const f of argv)console.log(JSON.stringify(check(JSON.parse(fs.readFileSync(f,'utf8')))));
