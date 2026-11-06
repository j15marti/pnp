// LSPV-4/442 independent signed-source CNF unit-propagation referee.
// Usage: node lspv4_442_independent_check.mjs lspv4_442_graph_fixtures.json lspv4_442_up_bootstrap_results.json
// This host-language check does NOT simulate the FLMV machine or check native R_mix341 proofs.
import fs from 'node:fs';
const fixtures=JSON.parse(fs.readFileSync(process.argv[2]));
const expected=JSON.parse(fs.readFileSync(process.argv[3]));
let checks=0;
function ck(v,msg){checks++;if(!v)throw Error(msg)}
function choose(a,k,callback,p=0,pre=[]){
  if(pre.length===k){callback([...pre]);return}
  for(let i=p;i<=a.length-(k-pre.length);i++)choose(a,k,callback,i+1,[...pre,a[i]])
}
function clauses(edges,H,chi){
  const out=[];
  for(let v=0;v<H;v++){
    const ids=[];edges.forEach(([a,b],i)=>{if(a===v||b===v)ids.push(i)});
    ck(ids.length===3,'bad cubic source');
    for(let p=0;p<2;p++)for(let q=0;q<2;q++){
      const r=p^q^1^chi[v];
      out.push([p?-(ids[0]+1):ids[0]+1,q?-(ids[1]+1):ids[1]+1,r?-(ids[2]+1):ids[2]+1])
    }
  }
  return out
}
function up(clauses,initial){
  const values=new Map(initial);let forced=0,conflict=false;
  for(let round=0;round<100;round++){
    const units=[];
    for(const clause of clauses){
      let satisfied=false;const unknown=[];
      for(const literal of clause){
        const id=Math.abs(literal)-1;
        if(values.has(id)){
          if(values.get(id)===(literal>0?1:0)){satisfied=true;break}
        }else unknown.push(literal)
      }
      if(satisfied)continue;
      if(unknown.length===0){conflict=true;break}
      if(unknown.length===1)units.push([Math.abs(unknown[0])-1,unknown[0]>0?1:0])
    }
    if(conflict||units.length===0)break;
    let changed=false;
    for(const [id,value] of units){
      if(values.has(id)){if(values.get(id)!==value){conflict=true;break}}
      else {values.set(id,value);forced++;changed=true}
    }
    if(conflict||!changed)break
  }
  return {values,forced,conflict}
}
function bootstrap(edges,H,seeds){
  const active=new Set(seeds);let change=true;
  while(change){
    change=false;
    for(let v=0;v<H;v++){
      if(active.has(v))continue;
      let neighbors=0;
      for(const [a,b] of edges)
        if((a===v&&active.has(b))||(b===v&&active.has(a))) neighbors++;
      if(neighbors>=2){active.add(v);change=true}
    }
  }
  return active
}
const records=[];
for(const f of fixtures){
  const {name,H,edges,maxk,h}=f;
  const record={name,branches:0,contradictions:0,noncontradictory:0,
    max_new_edges:0,min_untouched:H,eligible_branches:0,worst_eligible_bootstrap:0};
  for(let parity=0;parity<2;parity++){
    const chi=Array(H).fill(0);chi[0]=parity;
    const formula=clauses(edges,H,chi),indices=[...Array(edges.length).keys()];
    for(let k=0;k<=maxk;k++) choose(indices,k,selected=>{
      const endpoints=new Set(selected.flatMap(id=>edges[id]));
      const active=bootstrap(edges,H,endpoints);
      for(let mask=0;mask<2**k;mask++){
        const seed=selected.map((id,pos)=>[id,(mask>>>pos)&1]);
        const result=up(formula,seed);
        const touched=new Set([...result.values.keys()].flatMap(id=>edges[id]));
        const unchanged=formula.filter(c=>c.every(l=>!result.values.has(Math.abs(l)-1))).length;
        ck(unchanged===4*(H-touched.size),'original 3-CNF unchanged count');
        ck(result.forced<=active.size,'unit-propagation forced-edge bound');
        if(k<(1+h)*H/16){
          ck(active.size<=8*k/(1+h)+1e-9,'threshold-two expansion bound');
          ck(unchanged>=4*(H-(2+16/(1+h))*k)-1e-9,'ternary-source survivor bound');
          record.eligible_branches++;
          record.worst_eligible_bootstrap=Math.max(record.worst_eligible_bootstrap,active.size)
        }
        record.branches++;
        record[result.conflict?'contradictions':'noncontradictory']++;
        record.max_new_edges=Math.max(record.max_new_edges,result.forced);
        record.min_untouched=Math.min(record.min_untouched,H-touched.size)
      }
    })
  }
  const ref=expected.cases.find(x=>x.graph===name);ck(!!ref,'fixture not found');
  for(const field of ['branches','contradictions','noncontradictory','max_new_edges',
                       'min_untouched','eligible_branches','worst_eligible_bootstrap'])
    ck(record[field]===ref[field],name+' '+field+' mismatch');
  records.push(record)
}
console.log(JSON.stringify({status:'PASS',checks,graphs:records}))
