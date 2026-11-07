'use strict';
// LSPV-2/461 independent compact online postorder OR-fold finite control.
// Source = signed proper ternary clauses with tagged owner IDs. Finite toy control only.
function run() {
  const I=512, V=4, p=(v,i)=>v*I+i, e=(v,i)=>(V+v)*I+i;
  let checks=0, calls=0, peak=0, bad=0;
  function valid(v,C) {
    for(const row of C) {
      if(row.length!==3 || new Set(row.map(Math.abs)).size!==3) throw Error("not proper 3CNF");
      for(const lit of row) {
        const x=Math.abs(lit), i=x%I, owner=Math.floor(x/I);
        const tag=Math.floor(owner/V), who=owner%V;
        if(!i || tag>1 || (tag===0 && who!==v) ||
          (tag===1 && !(i===1 && who>=2 && (who===v || Math.floor(who/2)===v)))) throw Error("ownership");
      }
    }
  }
  function SAT(C) {
    function solve(clauses,A) {
      while(true) {
        let rest=[],units=[];
        for(const c of clauses) {
          if(c.some(l=>A.has(Math.abs(l)) && A.get(Math.abs(l))===(l>0))) continue;
          const open=c.filter(l=>!A.has(Math.abs(l)));
          if(!open.length)return false;
          if(open.length===1)units.push(open[0]);
          rest.push(open);
        }
        if(!rest.length)return true;
        clauses=rest;
        if(!units.length)break;
        for(const l of units) {
          const x=Math.abs(l), b=l>0;
          if(A.has(x)&&A.get(x)!==b)return false;
          A.set(x,b);
        }
      }
      const x=Math.abs(clauses[0][0]);
      for(const b of [false,true]) {
        const next=new Map(A);next.set(x,b);
        if(solve(clauses,next))return true;
      }
      return false;
    }
    return solve(C,new Map());
  }
  function force(x,b,u,v) {
    let rows=[];
    for(const s of [-1,1]) for(const t of [-1,1])
      rows.push([(b?x:-x),s*u,t*v]);
    return rows;
  }
  for(const a of [false,true])for(const b of [false,true]){
    const x=e(2,1), y=e(3,1), r=p(1,1);
    const blocks={
      2:force(x,a,p(2,1),p(2,2)),
      3:force(y,b,p(3,1),p(3,2)),
      1:[[x,y,r],[x,y,-r]]
    };
    let stack=[];
    for(const v of [2,3,1]) {
      valid(v,blocks[v]);checks++;
      let children=[];
      if(v===1){const right=stack.pop(),left=stack.pop();children=[left,right];}
      const msg={};
      for(const pin of v===1?[null]:[0,1]) {
        let G=blocks[v].map(c=>c.slice());
        if(pin!==null)G.push([pin?e(v,1):-e(v,1)]);
        for(const child of children)
          for(const key of [0,1])if(!child.msg[key])
            G.push([key?-e(child.v,1):e(child.v,1)]);
        msg[pin===null?'root':pin]=SAT(G);calls++;
      }
      stack.push({v,msg});peak=Math.max(peak,stack.length);
    }
    const actual=stack[0].msg.root;
    const reference=SAT([...blocks[1],...blocks[2],...blocks[3]]);
    if(actual!==reference||actual!==(a||b))throw Error('ORfold disagreement');
    checks+=2;
    for(const [v,corrupt] of [
      [2,[[p(3,1),p(2,1),p(2,2)]]],
      [1,[[e(4,1),p(1,1),e(3,1)]]],
      [2,[[e(2,1),e(2,1),p(2,1)]]]
    ]) {try{valid(v,corrupt);throw Error('corrupt accepted');}
      catch(err){if(err.message==='corrupt accepted')throw err;bad++;}}
  }
  if(calls!==20 || checks!==20 || bad!==12)throw Error('counts');
  return {cases:4, checks, guest_calls:calls, rejected_corruptions:bad,
          peak_pending_tables:peak,status:'PASS',scope:'finite tagged-tree semantic control'};
}
console.log(JSON.stringify(run(),null,2));
