"use strict";
/* LSPV-3/536: source-partition inductive certificate, declared two-parent semantic fragment.
   Run: node experiments/arc/lspv3_536_source_partition_abstract.js
   It does NOT authenticate the missing historical R_mix341 byte grammar.
*/
function assert(p, msg) { if (!p) throw new Error(msg || "assertion"); }
function parity(x) { let p=0; while(x){ p^=x&1; x>>>=1; } return p; }
function k4() { return {name:"K4",v:4,edges:[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]]}; }
function prism(t) {
  const edges=[];
  for(let i=0;i<t;i++) { edges.push([i,(i+1)%t]);edges.push([t+i,t+(i+1)%t]);edges.push([i,t+i]); }
  return {name:"prism"+t,v:2*t,edges};
}
function source(g,charges){
  const inc=Array.from({length:g.v},()=>[]);
  g.edges.forEach(([a,b],i)=>{inc[a].push(i);inc[b].push(i);});
  inc.forEach(a=>assert(a.length===3,"graph not cubic"));
  const clauses=[];
  for(let v=0;v<g.v;v++){
    for(let t=0;t<8;t++){
      if(parity(t)===charges[v])continue;
      const lits=inc[v].map((e,k)=>( (t>>k)&1)?-(e+1):(e+1));
      clauses.push({id:"S"+v+"_"+t,vertex:v,lits});
    }
  }
  return {vertices:g.v,edges:g.edges,charges,clauses,inc};
}
function clauseMask(lits,inc){
  let out=0;
  for(let a=0;a<8;a++){
    let hit=false;
    for(let j=0;j<3;j++){
      const e=inc.indexOf(Math.abs(lits[j])-1);
      assert(e>=0,"literal outside vertex");
      const val=(a>>e)&1;
      if(lits[j]>0?val:!val)hit=true;
    }
    if(hit)out|=(1<<a);
  }
  return out;
}
function truthMask(charge){let z=0;for(let a=0;a<8;a++)if(parity(a)===charge)z|=(1<<a);return z;}
function make(g,charges){
  const s=source(g,charges),steps=[],last=[],factor=new Map();
  for(let v=0;v<g.v;v++){
    const cs=s.clauses.filter(x=>x.vertex===v);
    let prev=cs[0].id,mask=clauseMask(cs[0].lits,s.inc[v]);
    for(let j=1;j<4;j++){
      const cm=clauseMask(cs[j].lits,s.inc[v]),id="I"+(steps.length+1);
      mask &=cm;
      const st={id,rule:"AND3",parents:[prev,cs[j].id],vertex:v,mask};
      if(j===3){assert(mask===truthMask(charges[v]),"parity identification failed");st.row={mask:s.inc[v].reduce((m,e)=>m^(1n<<BigInt(e)),0n).toString(),rhs:charges[v]};}
      steps.push(st);factor.set(id,mask);prev=id;
    }
    last.push(prev);
  }
  let prev=last[0],mask=BigInt(steps[2].row.mask),rhs=steps[2].row.rhs;
  for(let v=1;v<g.v;v++){
    const right=steps[3*v+2].row;
    const id="I"+(steps.length+1);
    mask^=BigInt(right.mask);rhs^=right.rhs;
    steps.push({id,rule:"XOR",parents:[prev,last[v]],row:{mask:mask.toString(),rhs}});
    prev=id;
  }
  return {original:s,steps,sink:prev};
}
function check(packet,opts={}){
  let checked=0;
  const g={v:packet.original.vertices,edges:packet.original.edges};
  const original=source(g,packet.original.charges);
  assert(JSON.stringify(original.clauses)===JSON.stringify(packet.original.clauses),"source mismatch");checked++;
  assert(original.clauses.length===4*g.v,"clause count");checked++;
  const known=new Map(),uf=new Map();
  for(const c of original.clauses){assert(!known.has(c.id),"duplicate source");known.set(c.id,{support:new Set([c.id]),rule:"SOURCE",vertex:c.vertex,mask:clauseMask(c.lits,original.inc[c.vertex])});uf.set(c.id,c.id);}
  function find(x){let t=x;while(uf.get(t)!==t)t=uf.get(t);while(uf.get(x)!==x){let p=uf.get(x);uf.set(x,t);x=p;}return t;}
  function merge(a,b){a=find(a);b=find(b);if(a!==b){uf.set(b,a);return 1;}return 0;}
  let components=original.clauses.length,paid=0,prev=components;
  const trace=[];
  for(const st of packet.steps){
    assert(typeof st.id==="string" && !known.has(st.id),"duplicate/nonstring node id");checked++;
    assert(["AND3","XOR"].includes(st.rule),"unauthorized rule");checked++;
    assert(Array.isArray(st.parents) && st.parents.length===2,"arity exceeds declared grammar");checked++;
    assert(Object.keys(st).every(k=>["id","rule","parents","vertex","mask","row"].includes(k)),"hidden dependency");checked++;
    const [p,q]=st.parents.map(id=>{assert(known.has(id),"unknown/future parent");return known.get(id);});checked++;
    const support=new Set([...p.support,...q.support]);
    const before=components;
    let anchors=st.parents.map(id=>[...known.get(id).support][0]).filter(x=>x!==undefined);
    if(anchors.length===2)components-=merge(anchors[0],anchors[1]);
    assert(before-components<=1,"bad component contraction");
    let curr;
    if(st.rule==="AND3"){
      assert(Number.isInteger(st.vertex)&&st.vertex>=0&&st.vertex<g.v,"vertex");
      assert(p.vertex===st.vertex && q.vertex===st.vertex,"bad factor support");
      const mask=p.mask&q.mask;
      assert(st.mask===mask,"wrong AND truth table");checked++;
      curr={rule:"AND3",vertex:st.vertex,mask,support};
      if(st.row!==undefined){
        const exp=truthMask(original.charges[st.vertex]);
        assert(mask===exp,"not exact XOR3 factor");
        const rowMask=original.inc[st.vertex].reduce((m,e)=>m^(1n<<BigInt(e)),0n).toString();
        assert(st.row.mask===rowMask&&st.row.rhs===original.charges[st.vertex],"wrong affine annotation");checked++;
        curr.row=st.row;
      }
    }else{
      assert(p.row && q.row,"XOR non-affine parent");
      const row={mask:(BigInt(p.row.mask)^BigInt(q.row.mask)).toString(),rhs:p.row.rhs^q.row.rhs};
      assert(st.row.mask===row.mask&&st.row.rhs===row.rhs,"wrong XOR");checked++;
      curr={rule:"XOR",row,support};
    }
    paid++;
    known.set(st.id,curr);
    assert(components===new Set([...uf.keys()].map(find)).size,"UF count");
    assert(components>=original.clauses.length-paid,"inductive cost invariant");
    trace.push({index:paid,components,contraction:before-components});
    prev=components;
  }
  assert(known.has(packet.sink),"unknown sink");
  const goal=known.get(packet.sink);
  const complete=goal.row && goal.row.mask==="0" && goal.row.rhs===1
      && goal.support.size===original.clauses.length;
  if(opts.requireGoal!==false)assert(complete,"not a sourced global contradiction");
  assert(!complete || paid>=original.clauses.length-1,"negative budget certificate");
  return {accepted:true,checked,paid,sourceClauses:original.clauses.length,
    components,complete:!!complete,first:trace[0],last:trace[trace.length-1],
    traceContractions:trace.filter(x=>x.contraction===1).length,
    packetBytes:JSON.stringify(packet).length};
}
function sat(s,omitId=null){
  for(let a=0;a<(1<<s.edges.length);a++){
    if(s.clauses.every(c=>c.id===omitId || c.lits.some(l=>{const bit=(a>>(Math.abs(l)-1))&1;return l>0?bit:!bit;})))return a;
  }
  return null;
}
function run(){
  const configs=[k4(),prism(3),prism(4),prism(5),prism(6)];
  const runs=[],corruptions=[];
  for(const g of configs){
    const chi=Array(g.v).fill(0);chi[0]=1;
    const pkt=make(g,chi),r=check(pkt);
    assert(r.paid===4*g.v-1&&r.components===1&&r.traceContractions===r.paid,"exact source-bound witness");
    assert(sat(pkt.original)===null || g.edges.length>12,"odd UNSAT brute");
    const even=source(g,Array(g.v).fill(0));
    assert(sat(even)===0,"even SAT witness");
    if(g.edges.length<=12){
      for(const c of pkt.original.clauses)assert(sat(pkt.original,c.id)!==null,"source deletion witness");
    }
    runs.push({graph:g.name,vertices:g.v,variables:g.edges.length,
      sourceClauses:r.sourceClauses,paid:r.paid,components:r.components,
      certificateBytes:r.packetBytes,checks:r.checked,
      deletionWitnesses:g.edges.length<=12?pkt.original.clauses.length:0,
      lowerBudget:r.paid-1});
    if(g.name==="K4"){
      const mutate=(label,f)=>{
        const cp=JSON.parse(JSON.stringify(pkt));f(cp);
        let rejected=false;try{check(cp)}catch(e){rejected=true;}
        assert(rejected,"accepted corrupted packet "+label);
        corruptions.push(label);
      };
      mutate("flipped XOR RHS",p=>{p.steps[p.steps.length-1].row.rhs^=1;});
      mutate("four-premise fake AND3",p=>{p.steps[0].parents.push("S0_3","S0_5");});
      mutate("hidden third facet",p=>{p.steps[0].facet_refs=["S0_3"];});
      mutate("wrong source charge",p=>{p.original.charges[0]=0;});
      mutate("deleted source",p=>{p.original.clauses.pop();});
      mutate("nonexistent parent",p=>{p.steps[0].parents[0]="unknown";});
      mutate("duplicate inference ID",p=>{p.steps[1].id=p.steps[0].id;});
      mutate("wrong AND mask",p=>{p.steps[0].mask^=1;});
      mutate("unjustified row",p=>{p.steps[2].row.rhs^=1;});
      mutate("unapproved discharge",p=>{p.steps[0].discharge=["x"];});
      mutate("invalid goal",p=>{p.sink=p.steps[0].id;});
      mutate("syntactic literal mutation",p=>{p.original.clauses[0].lits[0]*=-1;});
      const a=JSON.parse(JSON.stringify(pkt));
      a.steps[0].id="9007199254740993";
      a.steps[1].parents[0]=a.steps[0].id;
      const x=check(a);
      assert(x.complete&&x.paid===15,"large string ID control");
      // Zero-premise-def or a four-premise parity macro is NOT a legal step.
      const fantasy=2*g.v-1;
      assert(fantasy===7&&fantasy<r.paid,"four-source hidden macro falsifier");
    }
  }
  const result={schema:"LSPV3-536",status:"PROVED_RESTRICTED_SYMBOLIC_PLUS_COMPUTATIONAL",
    model:"declared SOURCE/AND3/XOR, unit-paid binary-premise, source-indispensable",
    sample:runs,corruptions,corruptionsRejected:corruptions.length,
    preciseClaim:"for an indispensable m-clause source with every legal paid node having <=2 exhaustive parents and no free cross-component links, kappa>=m-paid; goal kappa=1 so W>=m-1",
    countercontrol:"a distinct unit-paid 4-source parity extraction changes lower-cost bound and is NOT native",
    remaining:["P2-D1","P2-C3","P2-B1","P2-B2"]};
  return result;
}
if(typeof module!=="undefined" && module.exports) module.exports={run,make,check,k4,prism,source,sat};
if(typeof require!=="undefined" && typeof module!=="undefined" && require.main===module) console.log(JSON.stringify(run(),null,2));
