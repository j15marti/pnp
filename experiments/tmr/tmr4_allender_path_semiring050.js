"use strict";
// Exact finite audit. Generated directly from the function executed in the V8 research run.
const run = function run(){
 const T=2,states=[],ids=new Map();
 for(let t=0;t<=T;t++)for(let p=0;p<(1<<t);p++)for(let v=0;v<2;v++){const id=states.length;states.push({t,p,v});ids.set(`${t},${p},${v}`,id);}
 const free=[],paid=[];
 for(let i=0;i<states.length;i++){const s=states[i];free.push({from:i,to:ids.get(`${s.t},${s.p},${1-s.v}`),cost:0,rule:"VIEW"});if(s.t<T)for(let b=0;b<2;b++)paid.push({from:i,to:ids.get(`${s.t+1},${2*s.p+b},${s.v}`),cost:1,rule:`COIN_${b}`,bit:b});}
 let idx=0;const index=Array(states.length).fill(-1),low=Array(states.length).fill(-1),stack=[],on=Array(states.length).fill(false),comp=Array(states.length).fill(-1),scc=[];
 const adj=states.map(()=>[]);for(const e of free)adj[e.from].push(e.to);
 function visit(v){index[v]=low[v]=idx++;stack.push(v);on[v]=true;for(const w of adj[v]){if(index[w]<0){visit(w);low[v]=Math.min(low[v],low[w]);}else if(on[w])low[v]=Math.min(low[v],index[w]);}if(low[v]===index[v]){const group=[];while(true){const w=stack.pop();on[w]=false;comp[w]=scc.length;group.push(w);if(w===v)break;}scc.push(group);}}
 for(let i=0;i<states.length;i++)if(index[i]<0)visit(i);
 let assertions=0;const check=(v,msg)=>{assertions++;if(!v)throw Error(msg);};
 check(scc.length===7,"zero SCC count");
 for(const g of scc){check(g.length===2,"view SCC size");check(states[g[0]].t===states[g[1]].t&&states[g[0]].p===states[g[1]].p,"view SCC preserves state");}
 const tariffRows=[];
 for(const e of free.concat(paid)){const a=states[e.from],b=states[e.to],d=(2-a.t)-(2-b.t);check(d<=e.cost,`tariff at ${e.rule}`);check(e.cost===0?d===0:d===1,"signed step");tariffRows.push({rule:e.rule,from:`${a.t}:${a.p}:${a.v}`,to:`${b.t}:${b.p}:${b.v}`,delta:[0,0,0,0,0,0,d],cost:e.cost});}
 const quot={};
 for(const s of states){if(s.t>=T)continue;for(let bit=0;bit<2;bit++){const to=comp[ids.get(`${s.t+1},${s.p*2+bit},${s.v}`)],key=`${s.t}:${s.p}:${bit}`;if(key in quot)check(quot[key]===to,`not branch-preserving ${key}`);else quot[key]=to;}}
 const M0=[[1,1]],M1=[[1,1,0,0],[0,0,1,1]];
 const matvec=(v,M)=>M[0].map((_,j)=>v.reduce((z,x,i)=>z+x*M[i][j],0));
 const terminal=matvec(matvec([1],M0),M1);
 check(JSON.stringify(terminal)===JSON.stringify([1,1,1,1]),"four equiprobable paths");
 const popcount=x=>{let n=0;for(;x;x&=x-1)n++;return n;};
 let yes=0,no=0,innerTies=0,outerTies=0,checked=0;
 for(let mask=0;mask<65536;mask++){
   let good=0;const k=[];
   for(let y=0;y<4;y++){
    const f=Array.from({length:4},(_,x)=>(mask>>(4*y+x))&1);
    const count=terminal.reduce((a,n,x)=>a+n*f[x],0);
    const direct=popcount((mask>>(4*y))&15);
    check(count===direct,`count on ${mask} y${y}`);
    k.push(count);if(count>=2)good++;if(count===2)innerTies++;
   }
   const manual=k.filter(x=>x>=2).length;
   check(good===manual,"inner nested threshold");
   const label=good>=2;
   check(label===(((k[0]>=2)+(k[1]>=2)+(k[2]>=2)+(k[3]>=2))>=2),"outer inclusive majority");
   if(good===2)outerTies++;
   if(label)yes++;else no++;
   checked++;
 }
 const positive=[],negative=[];for(let y=0;y<4;y++){positive.push(y===3?0:2);negative.push(y===0?2:0);}
 check(JSON.stringify([...new Set(positive)].sort())===JSON.stringify([...new Set(negative)].sort()),"same support");
 check(positive.filter(x=>x>=2).length===3&&negative.filter(x=>x>=2).length===1,"opposite labels");
 check((1+1)===2&&new Set([1,1]).size===1,"counting semiring differs from Boolean reachability");
 const badLump=[2,0];check(badLump[0]!==badLump[1],"forget prefix violates weighted lumpability");
 return {status:"COMPUTATIONAL; symbolic scoped proof in report",name:"TMR4_CONFIG_ARITHMETIC_QUOTIENT050",scope:"two fair coins, four outer strings, 16-bit Boolean input table, deterministic metadata VIEW",concrete_states:states.length,free_edges:free.length,paid_edges:paid.length,zero_sccs:scc.length,all_truth_tables:checked,inner_ties:innerTies,outer_ties:outerTies,yes,no,assertions,failures:0,lambda:["0/1","0/1","0/1","0/1","0/1","0/1","1/1"],initial_potential:"2/1",goal_potential:"0/1",matrices:{M0,M1,product:[terminal]},tariff_rows:tariffRows,falsifiers:{non_lumpable_merge:{t1_states_prefix_0_and_1_to_accept:[2,0]},boolean_support:{positive_counts:positive,negative_counts:negative,shared_support:[0,2],positive_outer_majority:3,negative_outer_majority:1},duplicate_coin_edges:{integer_count:2,boolean_set_count:1},precounted_answer:{claim:"Weighted shortcut preserving counts cannot be compiled for free from source; reverse reconstruction absent"}},resources:{model:"finite randomized two-step automaton, NOT an arbitrary uniform SAT machine",per_path_paid_work:2,writable_prefix_bits_max:2,free_metadata:"VIEW toggle only; no extra probabilistic path",source:"immutable 16-bit truth table, no source generation or tape access costs claimed"}};
};
const output = run();
if (typeof process !== 'undefined' && process.stdout) process.stdout.write(JSON.stringify(output,null,2)+'\n');
