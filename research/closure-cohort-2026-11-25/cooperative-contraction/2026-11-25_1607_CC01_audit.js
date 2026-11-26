// Node-compatible exhaustive audit, not a polynomial chart generator.
function audit(){
 let seed=20261125;const rnd=n=>{seed=(Math.imul(1664525,seed)+1013904223)>>>0;return seed%n;};
 const parity=x=>{let p=0;while(x){p^=1;x&=x-1;}return p;};
 const pop=x=>{let p=0;while(x){p++;x&=x-1;}return p;};
 const rank=rows=>{let b=new Map();for(let x of rows){while(x){let j=31-Math.clz32(x);if(b.has(j))x^=b.get(j);else{b.set(j,x);break;}}}return b.size;};
 const form=(rows,a)=>rows.reduce((x,v,i)=>x^(((a>>i)&1)?v:0),0);
 let stats={seed:20261125,random:0,deficits:{},offset_checks:0,sat:0,unsat:0,charts:0,rank_full_charts:0,degree_checks:0,cover_basis_total:0,successful_extensions:0,core_lift_checks:0,strict_one_checks:0,strict_one_missing_max:0,fixed_first_chart_misses:0,chain_controls:[]};
 const check=(x,msg)=>{if(!x)throw Error(msg);};
 function test(G,n){
  const m=G.length;let best=-1,C=0;
  for(let s=0;s<1<<m;s++){let r=rank(G.flatMap((g,i)=>(s>>i)&1?g:[])),d=pop(s)-r;if(d>best){best=d;C=s;}else if(d===best)C&=s;}
  const H=G.filter((g,i)=>(C>>i)&1),r=rank(H.flat()),delta=H.length-r;check(delta===best,"least core");
  stats.deficits[delta]=(stats.deficits[delta]||0)+1;
  let pos=[],K=0;for(let g of H){pos.push(K);K+=g.length;}
  let cols=Array.from({length:n},(_,j)=>H.flat().reduce((a,v,i)=>a|(((v>>j)&1)<<i),0));
  let comp=[],b=cols.slice();for(let j=0;j<K;j++)if(rank([...b,1<<j])>rank(b)){comp.push(1<<j);b.push(1<<j);}
  const q=comp.length;check(q===K-r,"quotient");
  const Z=Array.from({length:1<<q},(_,i)=>form(comp,i));
  const rowBits=H.map(g=>(1<<g.length)-1);
  let ref=0n;const witnesses=[];
  for(let z=0;z<Z.length;z++){
   const s=Z[z];let found=-1;
   for(let x=0;x<1<<n;x++){if(H.every((g,i)=>g.some((v,j)=>parity(v&x)^((s>>(pos[i]+j))&1)))){found=x;break;}}
   witnesses.push(found);stats.offset_checks++;if(found>=0){ref|=1n<<BigInt(z);stats.sat++;}else stats.unsat++;
  }
  const pool=H.map(g=>Array.from({length:(1<<g.length)-1},(_,i)=>i+1).filter(a=>pop(a)<=2));
  const B=new Map();let union=0n,all=0n,first=null;
  const add=v=>{while(v){const j=v.toString(2).length-1;if(B.has(j))v^=B.get(j);else{B.set(j,v);return true;}}return false;};
  function visit(a,i){
   if(i<H.length){for(const v of pool[i])visit([...a,v],i+1);return;}
   stats.charts++;const rows=a.map((v,i)=>form(H[i],v));if(rank(rows)!==r)return;stats.rank_full_charts++;
   // Enumerate distinct attainable RHSs for this chart only.
   const image=new Set();for(let x=0;x<1<<n;x++)image.add(rows.reduce((v,row,i)=>v|(parity(row&x)<<i),0));
   let truth=0n,table=[];
   for(let z=0;z<Z.length;z++){
    const rhs=a.reduce((v,u,i)=>v|((1^parity(u&(Z[z]>>pos[i])))<<i),0);
    const yes=image.has(rhs);table.push(+yes);if(yes)truth|=1n<<BigInt(z);
   }
   check(table.reduce((a,b)=>a+b,0)===2**(q-delta),"flat size");
   check((truth&~ref)===0n,"spurious chart");
   if(first===null)first=truth;
   const coef=table.slice();for(let j=0;j<q;j++)for(let z=0;z<coef.length;z++)if(z&(1<<j))coef[z]^=coef[z^(1<<j)];
   check(coef.every((v,i)=>!v||pop(i)<=delta),"degree");stats.degree_checks++;
   all|=truth;if(add(truth))union|=truth;
  }
  visit([],0);
  check(all===ref&&union===ref,"incomplete union");
  let D=0;for(let z=0;z<1<<q;z++)if(pop(z)<=delta)D++;
  check(B.size<=D,"basis bound");stats.cover_basis_total+=B.size;
  if(first!==null&&first!==ref)stats.fixed_first_chart_misses++;
  // Model-driven chart acquisition using brute independent-transversal reference.
  let acquired=0n,k=0;
  for(let z=0;z<Z.length;z++)if(witnesses[z]>=0&&!(acquired&(1n<<BigInt(z)))){
   const x=witnesses[z],s=Z[z];const y=H.map((g,i)=>g.reduce((v,row,j)=>v|((parity(row&x)^((s>>(pos[i]+j))&1))<<j),0));
   let sel=null;
   function choose(a,i){if(sel)return;if(i===H.length){if(rank(a.map((v,j)=>form(H[j],v)))===r)sel=a;return;}for(const v of pool[i])if(parity(v&y[i]))choose([...a,v],i+1);}
   choose([],0);check(sel!==null,"witness chart discovery");
   let rows=sel.map((v,i)=>form(H[i],v)),image=new Set();for(let xx=0;xx<1<<n;xx++)image.add(rows.reduce((v,row,i)=>v|(parity(row&xx)<<i),0));
   let t=0n;for(let zz=0;zz<Z.length;zz++){let rhs=sel.reduce((v,u,i)=>v|((1^parity(u&(Z[zz]>>pos[i])))<<i),0);if(image.has(rhs))t|=1n<<BigInt(zz);}
   check((t&(1n<<BigInt(z)))!==0n,"new witness absent");acquired|=t;k++;stats.successful_extensions++;
  }
  check(acquired===ref&&k<=D,"witness progress");
  if(delta===1){const miss=Z.length-witnesses.filter(x=>x>=0).length;check(miss<=1,"strict singleton");stats.strict_one_checks++;stats.strict_one_missing_max=Math.max(stats.strict_one_missing_max,miss);}
  // All offsets on original system: compare core feasibility, and every feasible core private observation has some extension.
  let fullK=G.reduce((a,g)=>a+g.length,0);
  if(fullK<=9){let gp=[],j=0;for(let g of G){gp.push(j);j+=g.length;}
   for(let s=0;s<1<<fullK;s++){
    let good=new Set(),core=new Set();
    for(let x=0;x<1<<n;x++){let a=G.map((g,i)=>g.some((v,j)=>parity(v&x)^((s>>(gp[i]+j))&1)));let obs=H.flat().reduce((v,row,i)=>v|(parity(row&x)<<i),0);if(a.every((v,i)=>v||!((C>>i)&1)))core.add(obs);if(a.every(Boolean))good.add(obs);}
    check(core.size===good.size&&[...core].every(v=>good.has(v)),"outside extension");stats.core_lift_checks++;
   }
  }
 }
 // Random mixed packet widths, including nontrivial private rank-zero rows.
 for(let t=0;t<180;t++){let n=1+rnd(4),m=1+rnd(4),G=[];for(let i=0;i<m;i++){let k=1+rnd(3);G.push(Array.from({length:k},()=>rnd(1<<n)));}test(G,n);stats.random++;}
 // Four-line cube from AB05 and a second independent copy (smaller component separately).
 test([[2,4],[1,6],[2,5],[1,4]],3);
 // Rank-1 cycle private observations and independent second-coordinate offsets:
 // q=m+1. Test small exact instances; larger family uses direct parity reasoning.
 for(let m=2;m<=5;m++){const g=Array.from({length:m},(_,i)=>[i===m-1?(1<<(m-1))-1:1<<i,0]);test(g,m-1);}
 for(const m of [2,4,8,32,128,512]){
  const q=m+1;stats.chain_controls.push({m,each_quotient_dimension:q,total_deficit:2,missing_count_formula:`2^${q+1}-1`,minimum_indicator_degree:2});
 }
 return stats;
}
console.log(JSON.stringify(audit(),null,2));
