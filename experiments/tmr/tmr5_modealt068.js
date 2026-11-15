"use strict";
// Independent MODEALT068, reproducible native Node/V8, no dependencies.
function auditModealt068() {
  "use strict";
  const assert=(x,msg)=>{if(!x)throw new Error(msg||"assertion failed")};
  const counts={source_checks:0,proof_replays:0,cost_checks:0,mutant_rejections:0};
  const sort=a=>[...new Set(a)].sort((x,y)=>Math.abs(x)-Math.abs(y)||x-y);
  const key=a=>a.join(",");
  const width=x=>Math.ceil(Math.log2(x+1));
  function source(h){
    let es=[];
    if(h===4)es=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]];
    else{
      const seen=new Set();
      for(let i=0;i<h;i++)for(const w of [(i+1)%h,(i+h/2)%h]){
        const a=Math.min(i,w),b=Math.max(i,w),k=a+","+b;
        if(!seen.has(k)){seen.add(k);es.push([a,b])}
      }
    }
    const inc=Array.from({length:h},()=>[]),charges=Array(h).fill(0),clauses=[];
    charges[0]=1;
    es.forEach(([a,b],j)=>{inc[a].push(j+1);inc[b].push(j+1)});
    assert(inc.every(z=>z.length===3),"cubic");
    for(let v=0;v<h;v++)for(let a=0;a<8;a++){
      const bits=[a&1,(a>>1)&1,(a>>2)&1];
      if((bits[0]^bits[1]^bits[2])===charges[v])continue;
      clauses.push(sort(inc[v].map((e,j)=>bits[j]?-e:e)));
    }
    assert(clauses.length===4*h,"source count");
    for(let v=0;v<h;v++)for(let a=0;a<8;a++){
      const row=clauses.slice(4*v,4*v+4),bits=[a&1,(a>>1)&1,(a>>2)&1];
      const sat=row.every(c=>c.some(l=>{const bit=bits[inc[v].indexOf(Math.abs(l))];return l>0?bit===1:bit===0}));
      assert(sat===((bits[0]^bits[1]^bits[2])===charges[v]),"parity authentication");
      counts.source_checks++;
    }
    for(let e=1;e<=es.length;e++){assert(inc.filter(row=>row.includes(e)).length===2,"even incidence");counts.source_checks++}
    return {es,clauses};
  }
  function resolvent(l,r,p){
    if(!l.includes(p)||!r.includes(-p))return undefined;
    const c=sort([...l.filter(x=>Math.abs(x)!==p),...r.filter(x=>Math.abs(x)!==p)]);
    return c.some(x=>c.includes(-x))?null:c;
  }
  function derive(clauses,order){
    const lines=clauses.map(c=>({c,parents:null}));let active=lines.map((_,i)=>i);
    for(const p of order){
      const pos=active.filter(i=>lines[i].c.includes(p));
      const neg=active.filter(i=>lines[i].c.includes(-p));
      const next=active.filter(i=>lines[i].c.every(l=>Math.abs(l)!==p));
      const seen=new Set(next.map(i=>key(lines[i].c)));
      for(const i of pos)for(const j of neg){
        const c=resolvent(lines[i].c,lines[j].c,p);
        if(c===null||c===undefined||seen.has(key(c)))continue;
        seen.add(key(c));lines.push({c,parents:[i,j,p]});next.push(lines.length-1);
      }
      active=next;
    }
    const root=active.find(i=>lines[i].c.length===0);assert(root!==undefined,"no refutation");
    const done=new Set(),ordered=[];
    function visit(i){if(done.has(i))return;done.add(i);const row=lines[i];if(row.parents){visit(row.parents[0]);visit(row.parents[1])}ordered.push(i)}
    visit(root);
    const names=new Map(ordered.map((v,i)=>[v,i+1])),ev=[];
    for(const i of ordered){
      if(lines[i].parents===null)ev.push(["SOURCE",i+1]);
      else{const [a,b,p]=lines[i].parents;ev.push(["RES",names.get(a),names.get(b),p])}
    }
    ev.push(["HALT",names.get(root)]);
    return ev;
  }
  function verify(clauses,ev,n){
    const lines=[];assert(ev.at(-1)[0]==="HALT");
    for(let k=0;k<ev.length;k++){
      const e=ev[k];
      if(e[0]==="SOURCE"){assert(e[1]>=1&&e[1]<=clauses.length);lines.push(clauses[e[1]-1])}
      else if(e[0]==="RES"){
        const [_,a,b,p]=e;
        assert(a>0&&a<=lines.length&&b>0&&b<=lines.length&&p>0&&p<=n,"invalid indices");
        const c=resolvent(lines[a-1],lines[b-1],p);assert(c!==undefined&&c!==null,"invalid pivot or tautology");lines.push(c)
      }else{assert(e[0]==="HALT"&&k===ev.length-1);assert(e[1]>0&&e[1]<=lines.length&&lines[e[1]-1].length===0,"HALT not empty")}
    }
    counts.proof_replays++;
  }
  const bits=(clauses,ev,n)=>{
    const w1=width(clauses.length),w2=width(ev.length-1),wp=width(n);
    return ev.reduce((s,e)=>s+2+(e[0]==="SOURCE"?w1:e[0]==="RES"?2*w2+wp:w2),0)
  };
  const xorBits=h=>h*(2+width(h))+(h-1)*(2+2*width(2*h))+2+width(2*h);
  function* permutations(a,start=0){
    if(start===a.length){yield a.slice();return}
    for(let i=start;i<a.length;i++){[a[start],a[i]]=[a[i],a[start]];yield* permutations(a,start+1);[a[start],a[i]]=[a[i],a[start]]}
  }
  function rng(seed){let s=seed>>>0;return ()=>{s^=s<<13;s^=s>>>17;s^=s<<5;return(s>>>0)/4294967296}}
  const result=[];
  for(const [h,count] of [[4,720],[6,1000],[8,150],[10,20]]){
    const {es,clauses}=source(h),n=es.length,initial=Array.from({length:n},(_,i)=>i+1),old=derive(clauses,initial);
    verify(clauses,old,n);let best=old,bestOrder=initial,bestBits=bits(clauses,old,n),tested=0;
    const take=order=>{
      const ev=derive(clauses,order);verify(clauses,ev,n);const b=bits(clauses,ev,n);counts.cost_checks++;tested++;
      if(b<bestBits||(b===bestBits&&ev.length<best.length)){best=ev;bestBits=b;bestOrder=order.slice()}
    };
    if(h===4){for(const p of permutations(initial.slice()))take(p)}
    else{const random=rng(76300+h);for(let i=0;i<count;i++){let x=initial.slice();for(let j=n-1;j>0;j--){const k=Math.floor(random()*(j+1));[x[j],x[k]]=[x[k],x[j]]}take(x)}}
    verify(clauses,best,n);
    let bad=best.map(e=>e.slice());const pivot=bad.find(e=>e[0]==="RES");assert(pivot!==undefined);pivot[3]=n+1;
    try{verify(clauses,bad,n);throw Error("mutated pivot accepted")}catch(e){assert(e.message!=="mutated pivot accepted");counts.mutant_rejections++}
    const sourceBits=xorBits(h);
    result.push({H:h,variables:n,clauses:clauses.length,trials:tested,exhaustive:h===4,
      original_res_events:old.length,original_res_bits:bits(clauses,old,n),
      alternate_res_events:best.length,alternate_res_bits:bestBits,
      alternate_variable_order:bestOrder,delta_res_bits:bits(clauses,old,n)-bestBits,
      xor_bits:sourceBits,entry_two_script_bits:Math.min(sourceBits,bestBits),
      macro_token_bits_in_different_grammar:8,entry_three_mode_bits_if_macro_authorized:Math.min(8,sourceBits,bestBits),
      H4_full_authenticated_alternative_trace:h===4?best:null});
  }
  return {id:"MODEALT068",version:"1",model:"fixed-proof-script replay, bit/event costs not physical TM work",
    deterministic:"seeded xorshift32 76300+H, exact H=4 permutation enumeration",
    counts,failures:0,results:result,scope:"finite traces verified; all-length separation OPEN"};
}
console.log(JSON.stringify(auditModealt068(),null,2));
