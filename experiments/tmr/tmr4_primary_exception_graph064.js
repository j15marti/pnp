const result=(function audit064(){
  function graph(m){
    const nodes=["r"],edge=[];
    for(let i=0;i<m;i++){nodes.push(`a${i}`);nodes.push(`l${i+1}`)}
    for(let i=1;i<m;i++){edge.push([`a${i-1}`,`a${i}`],[`l${i}`,`a${i}`])}
    edge.push([`a${m-1}`,"r"],[`l${m}`,"r"],["l1","r"]);
    return {nodes,edge};
  }
  function certificate(G){
    const succ=Object.fromEntries(G.nodes.map(v=>[v,[]]));
    for(const [s,t] of G.edge) if(!succ[s].includes(t))succ[s].push(t);
    const height={r:0};
    function h(v){if(height[v]!==undefined)return height[v];return height[v]=1+Math.max(...succ[v].map(h))}
    for(const v of G.nodes)h(v);
    const p={};
    for(const v of G.nodes)if(v!=="r")p[v]=succ[v].slice().sort((a,b)=>height[b]-height[a]||a.localeCompare(b))[0];
    const children=Object.fromEntries(G.nodes.map(v=>[v,[]]));
    for(const [v,t]of Object.entries(p))children[t].push(v);
    const d=Math.max(...Object.values(children).map(x=>x.length));
    if(d>2)return {accepted:false,reason:"primary branching > 2"};
    const label={};
    function r(v){if(label[v])return label[v];const a=children[v].map(r);return label[v]=a.length===0?1:a.length===1?a[0]:Math.max(...a)+(a[0]===a[1]?1:0)}
    r("r");const order=[];
    function emit(v){for(const u of children[v].slice().sort((a,b)=>label[b]-label[a]||a.localeCompare(b)))emit(u);order.push(v)}
    emit("r");const pos=Object.fromEntries(order.map((v,i)=>[v,i]));
    for(const [s,t]of G.edge)if(pos[s]>=pos[t])return {accepted:false,reason:"nonprimary arc backward"};
    let e=0,q=0,qt=0,delta=0;
    for(const v of G.nodes)if(v!=="r")delta=Math.max(delta,...succ[v].map(t=>pos[t]-pos[v]));
    for(let j=0;j<order.length;j++){
      let lc=0,lp=0,le=0;
      for(const v of G.nodes)if(v!=="r"&&pos[v]<=j){
        const a=succ[v].some(t=>pos[t]>j), b=pos[p[v]]>j, c=succ[v].some(t=>t!==p[v]&&pos[t]>j);
        lc+=a?1:0;lp+=b?1:0;le+=c?1:0;
        if(a&&!b&&!c)throw Error("missed live source");
      }
      q=Math.max(q,lc);qt=Math.max(qt,lp);e=Math.max(e,le);
    }
    if(q>qt+e||qt>1+Math.floor(Math.log2(order.length)))throw Error("bound failed");
    return {accepted:true,K:order.length,q_primary:qt,e_extra:e,q_exact:q,delta,primary_max_indegree:d};
  }
  const tested=[];
  for(const m of [3,4,5,8,12,16,32,64,128,256]){
    const a=certificate(graph(m));
    if(!a.accepted)throw Error(`witness rejected ${m}`);
    tested.push({m,...a});
  }
  const bad={nodes:["a","b","r"],edge:[["a","r"],["b","a"],["a","b"]]};
  let rejected_cycle=false;try{certificate(bad)}catch(e){rejected_cycle=true}
  return {revision:"TMR4_PRIMARY_EXCEPTION_GRAPH064_v1",status:"COMPUTATIONAL",scope:"Independent structural-only core witness; not an original-source semantic compiler",cases:tested.length,records:tested,rejected_cycle,failures:0};
})();
console.log(JSON.stringify(result));
