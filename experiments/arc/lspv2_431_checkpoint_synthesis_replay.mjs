'use strict';
/* LSPV-2/431 finite checks. The unbounded recursion-theorem proof is in the report.
   Run with node experiments/arc/lspv2_431_checkpoint_synthesis_replay.mjs
   No packages, seed or external data required. */
function run() {
  let checks=0;
  function ok(x,message){if(!x)throw Error(message);checks++;}
  function boundedCounter(code,n) {
    if(!Array.isArray(code)||!Number.isInteger(n)||n<0)throw Error('input');
    for(const p of code) {
      if(!p||!['HALT','JMP','INC'].includes(p.op))throw Error('bad instruction');
      if(p.op!=='HALT'&&(!Number.isInteger(p.to)||p.to<0||p.to>=code.length))throw Error('bad jump');
      if(p.op==='INC'&&p.reg!==0)throw Error('bad register');
    }
    let pc=0,steps=0,counter=0;
    while(steps<n) {
      const p=code[pc];steps++;
      if(p.op==='HALT')return {bit:1,steps};
      if(p.op==='INC')counter++;
      pc=p.to;
    }
    return {bit:0,steps};
  }
  const loop=[{op:'JMP',to:0}];
  const halt=[{op:'HALT'}];
  const delay=Array.from({length:24},(_,i)=>({op:'INC',reg:0,to:i+1}));
  delay.push({op:'HALT'});
  for(let n=0;n<=64;n++){
    ok(boundedCounter(loop,n).bit===0,'nonhalt');
    ok(boundedCounter(halt,n).bit===Number(n>=1),'early halt');
    ok(boundedCounter(delay,n).bit===Number(n>=25),'late halt');
  }
  const boundary=32;
  ok(boundedCounter(delay,boundary).bit===1,'exact value');
  ok(boundedCounter(delay,Math.floor(Math.log2(boundary))).bit===0,'log shortcut fails');
  ok(boundedCounter(halt,32).bit!==0,'constant zero fails');
  ok(boundedCounter(loop,32).bit!==1,'constant one fails');
  function twoSAT(clauses) {
    if(!Array.isArray(clauses))return 'MALFORMED';
    let m=0,empty=false;
    for(const c of clauses) {
      if(!Array.isArray(c)||c.length>2)return 'MALFORMED';
      if(c.length===0)empty=true;
      for(const l of c) {
        if(!Number.isSafeInteger(l)||l===0||Math.abs(l)>1000)return 'MALFORMED';
        m=Math.max(m,Math.abs(l));
      }
    }
    if(empty)return 'UNSAT';
    const g=Array.from({length:2*m},()=>[]),rg=Array.from({length:2*m},()=>[]);
    const id=l=>2*(Math.abs(l)-1)+(l<0?1:0);
    function edge(a,b){g[id(a)].push(id(b));rg[id(b)].push(id(a));}
    for(const c of clauses){
      const a=c[0],b=c.length===1?a:c[1];
      edge(-a,b);edge(-b,a);
    }
    const vis=new Uint8Array(2*m),order=[],comp=Array(2*m).fill(-1);
    function dfs(v){vis[v]=1;for(const w of g[v])if(!vis[w])dfs(w);order.push(v);}
    for(let i=0;i<2*m;i++)if(!vis[i])dfs(i);
    let k=0;
    function rdfs(v){comp[v]=k;for(const w of rg[v])if(comp[w]<0)rdfs(w);}
    for(let i=order.length-1;i>=0;i--)if(comp[order[i]]<0){rdfs(order[i]);k++;}
    for(let j=0;j<m;j++)if(comp[2*j]===comp[2*j+1])return 'UNSAT';
    return 'SAT';
  }
  const yes=[[1,2],[-1,2],[-2,1]],no=[[1],[-1]];
  ok(twoSAT(yes)==='SAT','2SAT yes');
  ok(twoSAT(no)==='UNSAT','2SAT no');
  ok(twoSAT([[]])==='UNSAT','valid empty CNF clause');
  ok(twoSAT([])==='SAT','valid empty CNF conjunction');
  for(const bad of [[[0]],[[1,2,3]],[[1.5]],[[Infinity]],'bad',[[1001]]])
    ok(twoSAT(bad)==='MALFORMED','bad source');
  for(const p of [loop,halt,delay])for(const n of [1,5,24,25,32,64]){
    const ignored=boundedCounter(p,n).bit;
    ok((ignored===0||ignored===1)&&twoSAT(yes)==='SAT'&&twoSAT(no)==='UNSAT','final output unchanged');
  }
  const k4=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]];
  const cube=[];for(let a=0;a<8;a++)for(let j=0;j<3;j++){const b=a^(1<<j);if(a<b)cube.push([a,b]);}
  const families=[];
  for(const [name,h,edges] of [['K4',4,k4],['cube',8,cube]])for(let charge=0;charge<2;charge++) {
    const incident=Array.from({length:h},()=>[]);
    edges.forEach(([u,v],i)=>{incident[u].push(i);incident[v].push(i);});
    const clauses=[];
    for(let v=0;v<h;v++)for(let bits=0;bits<8;bits++){
      const parity=(bits&1)^((bits>>1)&1)^((bits>>2)&1);
      if(parity===(v===0?charge:0))continue;
      clauses.push(incident[v].map((e,i)=>((bits>>i)&1)?-(e+1):e+1));
    }
    ok(clauses.length===4*h&&clauses.every(c=>c.length===3),'exact Tseitin 3CNF');
    let witness=false;
    for(let mask=0;mask<2**edges.length;mask++){
      if(clauses.every(c=>c.some(l=>l>0?Boolean(mask&(1<<(l-1))):!Boolean(mask&(1<<(-l-1)))))){witness=true;break;}
    }
    ok(witness===(charge===0),'Tseitin parity');
    families.push({name,vertices:h,variables:edges.length,clauses:clauses.length,label:witness?'SAT':'UNSAT'});
  }
  let bad=0;
  for(const p of [[{op:'BAD'}],[{op:'JMP',to:2}],[{op:'INC',reg:1,to:0}]]) {
    try{boundedCounter(p,3);}catch(e){bad++;}
  }
  ok(bad===3,'bad guest-code controls');
  return {schema:'lspv2_431_v1',checks,verified:true,source_format:'finite 2SAT arrays, empty clause valid',guest_examples:3,families,late_halt_countercontrol:{n:32,threshold:25,log_budget:5},proof_scope:'finite tests only; theorem is separate recursion-theorem argument'};
}
if(typeof process!=='undefined'&&typeof console!=='undefined')console.log(JSON.stringify(run(),null,2));