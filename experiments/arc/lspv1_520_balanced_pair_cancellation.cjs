function audit(){
  const graphs=[];
  const complete=[];for(let u=0;u<4;u++)for(let v=u+1;v<4;v++)complete.push([u,v]);graphs.push(["K4",4,complete]);
  const bip=[];for(let u=0;u<3;u++)for(let v=3;v<6;v++)bip.push([u,v]);graphs.push(["K3,3",6,bip]);
  const cube=[];for(let u=0;u<8;u++)for(let b=0;b<3;b++){let v=u^(1<<b);if(u<v)cube.push([u,v])} graphs.push(["cube",8,cube]);
  const p=[];for(let u=0;u<5;u++){p.push([Math.min(u,(u+1)%5),Math.max(u,(u+1)%5)]);p.push([u,u+5]);p.push([Math.min(u+5,((u+2)%5)+5),Math.max(u+5,((u+2)%5)+5)])}graphs.push(["Petersen",10,p]);
  let assertions=0, seed=520;
  function random3(){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%3}
  function ck(v){assertions++;if(!v)throw Error("assertion "+assertions)}
  function tree(leaves){const vertices=leaves.map(x=>({left:{left:{index:x[0]},right:{index:x[1]}},right:{index:x[2]}}));function balanced(v){if(v.length===1)return v[0];let k=Math.floor(v.length/2);return {left:balanced(v.slice(0,k)),right:balanced(v.slice(k))}}return balanced(vertices)}
  function gather(t,path,m){if(t.index!==undefined){m.set(t.index,path);return}gather(t.left,path.concat("L"),m);gather(t.right,path.concat("R"),m)}
  function evalTree(t,terms,vals,removed){if(t.index!==undefined){if(removed.has(t.index))return 0;let [edge,sgn]=terms[t.index];return ((sgn*vals[edge])%3+3)%3}return (evalTree(t.left,terms,vals,removed)+evalTree(t.right,terms,vals,removed))%3}
  function sub(t,path){for(const d of path)t=d==="L"?t.left:t.right;return t}
  function context(t,path,terms,vals,removed){let sum=0;for(const d of path){let sibling=d==="L"?t.right:t.left;sum=(sum+evalTree(sibling,terms,vals,removed))%3;t=d==="L"?t.left:t.right}return sum}
  let results=[];
  for(const [name,h,edges] of graphs){
    const incidence=Array.from({length:h},()=>[]);
    for(let e=0;e<edges.length;e++){const [u,v]=edges[e];ck(u<v);incidence[u].push([e,1]);incidence[v].push([e,-1])}
    ck(incidence.every(z=>z.length===3));ck(edges.length===3*h/2);
    const terms=[],rows=[],endpoints=Array.from({length:edges.length},()=>[]);
    for(const line of incidence){let row=[];for(const t of line){const id=terms.length;terms.push(t);row.push(id);endpoints[t[0]].push(id)}rows.push(row)}
    const t=tree(rows);const pm=new Map();gather(t,[],pm);
    const height=Math.max(...[...pm.values()].map(x=>x.length));
    ck(height<=Math.ceil(Math.log2(h))+2);ck(terms.length===3*h);
    const nSamples=name==="K4"?729:200;
    let maxPath=0;
    for(let k=0;k<nSamples;k++){
      let n=k, vals=Array.from({length:edges.length},()=>random3());
      if(name==="K4"){vals=vals.map(()=>{let x=n%3;n=Math.floor(n/3);return x})}
      const removed=new Set(),base=evalTree(t,terms,vals,removed);
      ck(base===0);
      let sums=Array(h).fill(0);
      for(let i=0;i<edges.length;i++){const [u,v]=edges[i];sums[u]=(sums[u]+vals[i])%3;sums[v]=(sums[v]-vals[i]+3)%3}
      ck(sums.reduce((a,b)=>a+b,0)%3===base);
      for(let e=0;e<edges.length;e++){
        const [a,b]=endpoints[e],pa=pm.get(a),pb=pm.get(b);
        let d=0;while(d<pa.length&&d<pb.length&&pa[d]===pb[d])d++;
        ck(d<Math.min(pa.length,pb.length));
        const anc=sub(t,pa.slice(0,d));
        const pathA=pa.slice(d+1),pathB=pb.slice(d+1);
        const childA=pa[d]==="L"?anc.left:anc.right;
        const childB=pb[d]==="L"?anc.left:anc.right;
        const P=context(childA,pathA,terms,vals,removed),Q=context(childB,pathB,terms,vals,removed);
        const x=((terms[a][1]*vals[e])%3+3)%3,y=((terms[b][1]*vals[e])%3+3)%3;
        ck((x+y)%3===0);ck((P+x+Q+y)%3===(P+Q)%3);
        const before=evalTree(t,terms,vals,removed);
        removed.add(a);removed.add(b);
        const after=evalTree(t,terms,vals,removed);
        ck(before===after);
        maxPath=Math.max(maxPath,pa.length+pb.length);
      }
      ck(removed.size===3*h);ck(evalTree(t,terms,vals,removed)===0);
    }
    for(let P=0;P<3;P++)for(let Q=0;Q<3;Q++)for(let x=0;x<3;x++)ck((P+x+Q+(3-x)%3)%3===(P+Q)%3);
    const oldVars=9*h/2, binary=9*h/2, oldClauses=24*h, strict=oldClauses+binary;
    ck(Number.isInteger(oldVars)&&Number.isInteger(strict));ck(strict===57*h/2);
    results.push({graph:name,h,edges:edges.length,height,flows:nSamples,original_variables:oldVars,strict_variables:oldVars+1,original_clauses:oldClauses,strict_clauses:strict,max_combined_paths:maxPath,pair_path_budget:2*edges.length*(height+1)})
  }
  ck((1+1)%3!==0); // corrupted opposite-port sign
  return {status:"PASS",checks:assertions,seed:520,modulus:3,results,limitation:"Arithmetic macro/structure controls only; no full ER2 or historical R_mix341 Resolution packet verified."}
}
console.log(JSON.stringify(audit(),null,2));
