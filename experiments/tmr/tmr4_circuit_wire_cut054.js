'use strict';
// tmr4-circuit-wire-cut054.v1; seed NONE; exhaustive, deterministic.
// Every gate is evaluated once in fixed topological order; no Boolean-network unfolding.
const assert = require('node:assert/strict');
const P = [2, 101];
function circuit(k, family) {
  const nodes = [], xs = [], ys = [];
  const add=(op,ins=[],side=null)=>{ const id=nodes.length; nodes.push({id,op,ins,side}); return id; };
  for(let i=0;i<k;i++)xs.push(add('INPUT',[],'X'));
  for(let i=0;i<k;i++)ys.push(add('INPUT',[],'Y'));
  const gate=(op,...ins)=>add(op,ins);
  const reduce=(op,terms)=>terms.reduce((a,b)=>a===null?b:gate(op,a,b),null);
  let out;
  if(family==='DISJ'||family==='HORN'){
    const pairs=family==='HORN'? [[0,0],[0,1],[1,1]]:Array.from({length:k},(_,i)=>[i,i]);
    out=reduce('AND',pairs.map(([i,j])=>gate('NAND',xs[i],ys[j])));
  } else if(family==='EQ') out=reduce('AND',xs.map((x,i)=>gate('XNOR',x,ys[i])));
  else if(family==='IP') out=reduce('XOR',xs.map((x,i)=>gate('AND',x,ys[i])));
  else if(family==='AFFINE') out=reduce('XOR',[...xs,...ys]);
  else if(family==='PRODUCT') out=gate('AND',gate('XOR',xs[0],xs[1]),gate('XOR',ys[0],ys[1]));
  else if(family==='SINGLETON') out=reduce('AND',[...xs,...ys].map(x=>gate('NOT',x)));
  else if(family==='SHARE') out=gate('OR',gate('AND',xs[0],ys[0]),gate('AND',xs[0],ys[1]));
  else if(family==='PAD') out=reduce('AND',Array.from({length:k-1},(_,i)=>gate('NAND',xs[i],ys[i])));
  else throw Error('unknown family '+family);
  assert.ok(out!==undefined);
  return {nodes,out,k,family};
}
function evaluate(C,x,y){const v=[];for(const a of C.nodes){
  const p=a.ins.map(i=>v[i]);let t;
  switch(a.op){case 'INPUT':t=a.side==='X'?((x>>a.id)&1):((y>>(a.id-C.k))&1);break;
    case 'AND':t=p[0]&p[1];break;case 'OR':t=p[0]|p[1];break;
    case 'XOR':t=p[0]^p[1];break;case 'NOT':t=1-p[0];break;
    case 'NAND':t=1-(p[0]&p[1]);break;case 'XNOR':t=1-(p[0]^p[1]);break;
    default:throw Error(a.op);
  }v.push(t);}return {output:v[C.out],values:v};}
function rank(matrix,p){const a=matrix.map(r=>r.map(v=>v%p));const R=a.length,C=a[0].length;
  let r=0;for(let c=0;c<C&&r<R;c++) {let pivot=r;while(pivot<R&&a[pivot][c]===0)pivot++;
    if(pivot===R)continue;[a[r],a[pivot]]=[a[pivot],a[r]];
    let inv=1;if(p!==2){while((inv*a[r][c])%p!==1)inv++;}
    for(let j=c;j<C;j++)a[r][j]=(a[r][j]*inv)%p;
    for(let i=r+1;i<R;i++)if(a[i][c]!==0){const m=a[i][c];for(let j=c;j<C;j++)a[i][j]=(a[i][j]-m*a[r][j]%p+p)%p;}
    r++;
  }return r;
}
function placement(C,mask){const g=C.nodes.filter(n=>n.op!=='INPUT');assert.ok(g.length<20);
  const side=C.nodes.map(n=>n.op==='INPUT'?n.side:null);g.forEach((n,i)=>{side[n.id]=(mask>>i)&1?'X':'Y';});
  const recipients=C.nodes.map(()=>new Set());let crossWires=0;
  for(const dest of C.nodes)for(const src of dest.ins){if(side[src]!==side[dest.id]){recipients[src].add(side[dest.id]);crossWires++;}}
  const senders=C.nodes.filter(n=>recipients[n.id].size>0).map(n=>n.id);
  // In a binary owner model one bit is sent once per producer to the opposite side,
  // regardless of the number of consumers there. Local fanout is free in this protocol.
  assert.ok(senders.every(i=>recipients[i].size===1));
  return {side,senders,e:senders.length,crossWires};
}
function verify(C){const size=1<<C.k,g=C.nodes.length-2*C.k;
  const results=Array.from({length:size},(_,x)=>Array.from({length:size},(_,y)=>evaluate(C,x,y)));
  const matrix=results.map(row=>row.map(z=>z.output));const ranks=P.map(p=>rank(matrix,p));
  let minE=Infinity, minPlacements=0, best=null, tests=0, rectangleTests=0, maxFanoutSaved=0;
  for(let mask=0;mask<(1<<g);mask++){
    const p=placement(C,mask);tests++;
    minE=Math.min(minE,p.e); if(p.e===minE){if(best===null||p.e<best.e)best={e:p.e,mask,crossWires:p.crossWires};minPlacements++;}
    maxFanoutSaved=Math.max(maxFanoutSaved,p.crossWires-p.e);
    const groups=new Map();
    for(let x=0;x<size;x++)for(let y=0;y<size;y++){
      const rr=results[x][y];const tr=p.senders.map(id=>rr.values[id]).join('');
      let group=groups.get(tr);if(!group){group={pairs:new Set(),accepted:new Set(),X:new Set(),Y:new Set()};groups.set(tr,group);}
      group.pairs.add(x*size+y);
      if(rr.output){group.accepted.add(x*size+y);group.X.add(x);group.Y.add(y);}
    }
    assert.ok(groups.size <= 2**p.e);
    let acceptTranscripts=0;
    for(const group of groups.values()){
      // Every full transcript identifies a rectangle, even before testing acceptance.
      const allX=new Set([...group.pairs].map(z=>Math.floor(z/size)));
      const allY=new Set([...group.pairs].map(z=>z%size));
      assert.equal(group.pairs.size,allX.size*allY.size);rectangleTests++;
      if(group.accepted.size){
        acceptTranscripts++;
        assert.equal(group.accepted.size,group.X.size*group.Y.size);rectangleTests++;
      }
    }
    for(const r of ranks)assert.ok(r<=acceptTranscripts);
    assert.ok(p.e<=p.crossWires);
  }
  const usedInputs=new Set(C.nodes.flatMap(n=>n.ins).filter(i=>C.nodes[i].op==='INPUT'));
  const usedX=[...usedInputs].filter(i=>C.nodes[i].side==='X').length;
  const usedY=[...usedInputs].filter(i=>C.nodes[i].side==='Y').length;
  assert.ok(minE<=Math.min(usedX,usedY));
  assert.ok(ranks.every(r=>r<=2**minE));
  return {family:C.family,k:C.k,variables:2*C.k,gates:g,wires:C.nodes.reduce((z,n)=>z+n.ins.length,0),
    rank_F2:ranks[0],rank_F101:ranks[1],minimum_crossing_producers:minE,
    sample_best_placement:best,unused_inputs:2*C.k-usedInputs.size,
    max_sharing_savings_in_bits:maxFanoutSaved,placements_checked:tests,rectangle_checks:rectangleTests};
}
const cases=[['DISJ',1],['DISJ',2],['DISJ',3],['DISJ',4],['EQ',1],['EQ',2],['EQ',3],['IP',1],['IP',2],['IP',3],['HORN',2],['AFFINE',2],['AFFINE',3],['SINGLETON',2],['PRODUCT',2],['SHARE',2],['PAD',3]];
const rows=cases.map(([f,k])=>verify(circuit(k,f)));
assert.ok(rows.find(z=>z.family==='DISJ'&&z.k===4).rank_F2===16);
assert.ok(rows.find(z=>z.family==='DISJ'&&z.k===4).gates===7);
assert.ok(rows.find(z=>z.family==='IP'&&z.k===3).rank_F2===3);
assert.ok(rows.find(z=>z.family==='IP'&&z.k===3).rank_F101===7);
assert.ok(rows.find(z=>z.family==='SHARE').max_sharing_savings_in_bits>=1);
const summary={revision:'tmr4-circuit-wire-cut054.v1',seed:null,prime_fields:P,
  status:'COMPUTATIONAL finite instances; mathematical theorem requires independent review',
  cases:rows.length,placements:rows.reduce((s,r)=>s+r.placements_checked,0),
  rectangle_checks:rows.reduce((s,r)=>s+r.rectangle_checks,0), failures:0,rows};
process.stdout.write(JSON.stringify(summary,null,2)+'\n');
