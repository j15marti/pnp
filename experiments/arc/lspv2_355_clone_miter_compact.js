// CLONE-MITER-RES355 public macro producer: eight exact strict-Resolution certificate skeletons.
// Does not rerun 30 full miter DAGs; full producer and independent checker in local ZIP.
'use strict';
const canon = a => {
  const s=new Set(a);
  if([...s].some(v=>!Number.isInteger(v)||!v||s.has(-v))) throw Error('bad/tautological clause');
  return [...s].sort((x,y)=>Math.abs(x)-Math.abs(y)||Number(x<0)-Number(y<0));
};
const key = a => canon(a).join(',');
function res(a,b,p){
  if(!a.includes(p)||!b.includes(-p))throw Error('bad pivot');
  return canon([...a.filter(x=>x!==p),...b.filter(x=>x!==-p)]);
}
function gate(t,a,b,o){
  if(t==='AND')return [[-o,a],[-o,b],[o,-a,-b]].map(canon);
  let r=[];
  for(let x=0;x<2;x++)for(let y=0;y<2;y++)for(let z=0;z<2;z++)
    if(z!==(x^y))r.push(canon([x?-a:a,y?-b:b,z?-o:o]));
  return r;
}
function derive(t,s1,s2){
  const a=1,b=2,c=s1?1:3,d=s2?2:4,y=5,z=6;
  const nodes=[];
  for(const cl of gate(t,a,b,y).concat(gate(t,c,d,z),
     s1?[]:[canon([-a,c]),canon([a,-c])],
     s2?[]:[canon([-b,d]),canon([b,-d])]))
    nodes.push({cl,kind:'source'});
  const seen=new Map(nodes.map((n,i)=>[key(n.cl),i]));
  const goal=[key([-y,z]),key([y,-z])];
  for(let k=0;!(goal.every(g=>seen.has(g)));k++){
    if(k>=nodes.length||nodes.length>729)throw Error('closure failure');
    const lhs=nodes[k].cl;
    for(let i=0;i<k;i++){
      const rhs=nodes[i].cl;
      for(const p of lhs)if(rhs.includes(-p)){
        let out;
        try{out=res(lhs,rhs,p);}catch(e){continue;}
        if(!seen.has(key(out))){
          seen.set(key(out),nodes.length);
          nodes.push({cl:out,kind:'res',parents:[k,i],pivot:p});
        }
      }
    }
  }
  const ancestors=new Set();
  function retain(i){if(ancestors.has(i))return;ancestors.add(i);
    const n=nodes[i];if(n.kind==='res')n.parents.forEach(retain);}
  goal.forEach(x=>retain(seen.get(x)));
  const count=[...ancestors].filter(i=>nodes[i].kind==='res').length;
  for(const i of ancestors){
    const n=nodes[i];if(n.kind==='res'&&key(res(nodes[n.parents[0]].cl,nodes[n.parents[1]].cl,n.pivot))!==key(n.cl))
      throw Error('invalid certificate');
  }
  return {count,saturated:nodes.length,goals:goal.length};
}
const macros={};
for(const t of ['AND','XOR'])
  for(const s1 of [false,true])for(const s2 of [false,true])
    macros[t+':'+Number(s1)+Number(s2)]=derive(t,s1,s2);
const expected={'AND:00':8,'AND:01':6,'AND:10':6,'AND:11':4,
                'XOR:00':14,'XOR:01':10,'XOR:10':10,'XOR:11':6};
for(const [k,v] of Object.entries(macros))
  if(v.count!==expected[k])throw Error('unexpected macro '+k+' '+v.count);
const output={id:'CLONE_MITER_RES355',macro_counts:Object.fromEntries(
  Object.entries(macros).map(([k,v])=>[k,v.count])),max_macro:14,
  resulting_uniform_cost_bound:'14*g+2',verified_local_macros:8,
  note:'Constant-size local certificates; no unrestricted SAT oracle or mixed-calculus rule added'};
if(typeof module!=='undefined'&&require.main===module)console.log(JSON.stringify(output,null,2));
