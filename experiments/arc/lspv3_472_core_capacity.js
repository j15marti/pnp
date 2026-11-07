'use strict';
// LSPV-3/472 reproducible source-core/arity audit.
// node experiments/arc/lspv3_472_core_capacity.js
// Neither historical R_mix341 accepted-byte checker nor official cake_xlrup executed.
function run() {
  let checks=0;
  function ok(c,m){checks++;if(!c)throw Error(m);}
  const families=[
    ['K4',4,[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]]],
    ['K3,3',6,Array.from({length:9},(_,i)=>[Math.floor(i/3),3+i%3])],
    ['cube',8,Array.from({length:8},(_,i)=>[0,1,2].filter(b=>!(i&(1<<b))).map(b=>[i,i^(1<<b)])).flat()]
  ];
  function src(h,edges,odd) {
    const inc=Array.from({length:h},()=>[]);
    edges.forEach(([a,b],i)=>{inc[a].push(i+1);inc[b].push(i+1);});
    inc.forEach(v=>ok(v.length===3,'not cubic'));
    const charge=Array(h).fill(0);if(odd)charge[0]=1;
    const clauses=[],groups=[];
    for(let v=0;v<h;v++){
      const ids=[];
      for(let pattern=0;pattern<8;pattern++) {
        const b=[pattern&1,(pattern>>1)&1,(pattern>>2)&1];
        if((b[0]^b[1]^b[2])!==charge[v]) {
          ids.push(clauses.length);
          clauses.push(inc[v].map((e,k)=>b[k]?-e:e));
        }
      }
      ok(ids.length===4,'not four signed clauses');
      groups.push(ids);
      for(let pattern=0;pattern<8;pattern++){
        let x=Array(edges.length).fill(0);
        inc[v].forEach((e,k)=>x[e-1]=(pattern>>k)&1);
        let value=ids.every(i=>satClause(clauses[i],x));
        ok(value===(((pattern&1)^((pattern>>1)&1)^((pattern>>2)&1))===charge[v]),'bad local parity encoding');
      }
    }
    return{clauses,groups,charge,inc};
  }
  function satClause(clause,x){return clause.some(l=>l>0?x[l-1]===1:x[-l-1]===0);}
  function evaluate(clauses,n){
    let models=0;const deletion=Array(clauses.length).fill(false);
    for(let mask=0;mask<(1<<n);mask++){
      const x=Array.from({length:n},(_,i)=>(mask>>i)&1);
      let bad=[];
      clauses.forEach((c,i)=>{if(!satClause(c,x))bad.push(i);});
      if(!bad.length)models++;
      if(bad.length===1)deletion[bad[0]]=true;
      checks++;
    }
    return{models,indispensable:deletion.filter(Boolean).length};
  }
  // Theoretical capacity: sum(indegree-1) >= number_of_distinct_source_ancestors-1.
  // A source reference and a paid-node reference are separate namespaces.
  function audit(m,nodes){
    const ns=new Set(),ss=new Set();
    function walk(i){
      ok(i>=0&&i<nodes.length,'bad node');
      if(ns.has(i))return;ns.add(i);
      for(let p of nodes[i]){
        if(p[0]==='s'){ok(p[1]>=0&&p[1]<m,'bad source ID');ss.add(p[1]);}
        else {ok(p[0]==='n'&&p[1]<i,'invalid parent / cyclic');walk(p[1]);}
      }
    }
    walk(nodes.length-1);
    const edgeCount=[...ns].reduce((s,i)=>s+nodes[i].length,0);
    const capacity=edgeCount-ns.size;
    ok(capacity>=ss.size-1,'ancestry capacity violated');
    return{paid:ns.size,source_ancestors:ss.size,capacity,max_arity:Math.max(...[...ns].map(i=>nodes[i].length))};
  }
  const cases=[];
  for(let [name,h,edges] of families){
    const odd=src(h,edges,true),even=src(h,edges,false),m=odd.clauses.length;
    const oddEval=evaluate(odd.clauses,edges.length),evenEval=evaluate(even.clauses,edges.length);
    ok(oddEval.models===0&&oddEval.indispensable===m,'odd not minimally UNSAT');
    ok(evenEval.models===(1<<(edges.length-h+1)),'even control failed');
    ok(m===4*h,'wrong original 3CNF size');
    const native=[],last=[];
    for(let group of odd.groups){
      let p=['s',group[0]];
      for(let j=1;j<4;j++){
        native.push([p,['s',group[j]]]);p=['n',native.length-1];
      }
      last.push(p);
    }
    let running=last[0];
    for(let j=1;j<last.length;j++){
      native.push([running,last[j]]);running=['n',native.length-1];
    }
    const direct=[],ports=[];
    for(let group of odd.groups){direct.push(group.map(i=>['s',i]));ports.push(['n',direct.length-1]);}
    direct.push(ports);direct.push([['n',direct.length-1]]);
    const b=audit(m,native),d=audit(m,direct);
    ok(b.paid===4*h-1&&b.capacity===m-1&&b.max_arity===2,'binary sharp bound');
    ok(d.paid===h+2&&d.capacity===m-1&&d.max_arity===h,'high arity sharp bound');
    ok(b.source_ancestors===m&&d.source_ancestors===m,'missing source in refutation topology');
    let badNative=direct.some(node=>node.length>2);
    ok(badNative,'unlicensed multi-premise record accepted as native');
    // Corrupt signed source and check it is no longer the stated parity encoding.
    let corrupt=JSON.parse(JSON.stringify(odd));
    corrupt.clauses[0][0]*=-1;
    let differs=false;
    for(let p=0;p<8;p++){
      let x=Array(edges.length).fill(0),inc=corrupt.inc[0];
      inc.forEach((e,k)=>x[e-1]=(p>>k)&1);
      let all=corrupt.groups[0].every(i=>satClause(corrupt.clauses[i],x));
      if(all!==((((p&1)^((p>>1)&1)^((p>>2)&1)))===1))differs=true;
    }
    ok(differs,'corrupt original source accepted');
    ok(even.charge.reduce((a,b)=>a^b,0)===0,'even charge falsely refutable by XOR');
    cases.push({name,h,variables:edges.length,original_clause_count:m,odd_models:0,
      indispensable_original_clauses:oddEval.indispensable,even_models:evenEval.models,
      native_binary_paid:b.paid,native_binary_capacity:b.capacity,
      high_arity_records:d.paid,high_arity_capacity:d.capacity,
      graph_edges:edges,charge:odd.charge,original_signed_clauses:odd.clauses,
      native_inference_parents:native,external_high_arity_parents:direct});
  }
  // Syntactic DAG-only reconvergence fixture. This is NOT a semantic refutation.
  const shared=audit(4,[
    [['s',0],['s',1]],
    [['n',0],['s',2]],
    [['n',0],['s',3]],
    [['n',1],['n',2]]
  ]);
  ok(shared.paid===4&&shared.source_ancestors===4&&shared.capacity===4,'double-counted shared vertex');
  return{status:'PASS',model:'original cubic Tseitin source plus declared binary and external high-arity dependency topologies',
    check_count:checks,shared_DAG_graph_only:shared,
    limitations:'not a historical native checker; external high-arity nodes not officially XLRUP-accepted; source-core counting does not imply semantic derivability',
    cases};
}
if(typeof module!=='undefined'&&require.main===module)console.log(JSON.stringify(run(),null,2));
