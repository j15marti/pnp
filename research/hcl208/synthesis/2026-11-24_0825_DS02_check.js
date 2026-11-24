function experiment(){
 const F=[[1,2,3],[1,4,5],[1,6,7],[2,4,6],[2,5,7],[3,4,7],[3,5,6]];
 const nae=(a,b,c)=>[[a,b,c],[-a,-b,-c]];
 const vars=cs=>[...new Set(cs.flat().map(Math.abs))].sort((a,b)=>a-b);
 const check=(cs,a)=>cs.every(c=>c.some(l=>a[Math.abs(l)]===(l>0?1:0)));
 function* search(cs,vs,pin,ctr){const stack=[{...pin}];while(stack.length){let a=stack.pop(),bad=false,change=true;ctr.nodes++;while(change&&!bad){change=false;for(const c of cs){ctr.scans++;let open=[],sat=false;for(const l of c){ctr.literals++;let v=a[Math.abs(l)];if(v===undefined)open.push(l);else if(v===(l>0?1:0))sat=true;}if(sat)continue;if(!open.length){bad=true;break;}if(open.length===1){let l=open[0];a[Math.abs(l)]=l>0?1:0;ctr.forced++;change=true;}}}if(!bad){let v=vs.find(v=>a[v]===undefined);if(v===undefined){if(!check(cs,a))throw Error("bad witness");return a;}ctr.branches++;stack.push({...a,[v]:1},{...a,[v]:0});}yield null;}return false;}
 function ref(cs){let vs=vars(cs),count=0;for(let i=0;i<2**vs.length;i++){let a={};vs.forEach((v,j)=>a[v]=(i>>j)&1);if(check(cs,a))count++;}return count;}
 function solve(regs,lazy){let c={nodes:0,scans:0,literals:0,forced:0,branches:0,outerChecks:0,rounds:0,verified:0,retired:0};let all=regs.flat();let vs=regs.map(vars);let shared=[...new Set(vs.flat().filter(v=>vs.filter(s=>s.includes(v)).length>1))].sort((a,b)=>a-b);let jobs=[];let rows=vs.map((v,i)=>{let b=v.filter(x=>shared.includes(x));let arr=[];for(let m=0;m<2**b.length;m++){let pin={};b.forEach((x,j)=>pin[x]=(m>>j)&1);let job={i,b,m,pin,status:0,w:null,gen:search(regs[i],v,pin,c),live:true};arr.push(job);jobs.push(job);}return {b,arr};});
 let initial=jobs.length;
 function outer(){let live=new Set(),lower=null,upper=0;for(let m=0;m<2**shared.length;m++){c.outerChecks++;let a={};shared.forEach((x,j)=>a[x]=(m>>j)&1);let js=rows.map(r=>r.arr[r.b.reduce((s,x,j)=>s+(a[x]<<j),0)]);if(js.some(j=>j.status===-1))continue;upper++;js.forEach(j=>live.add(j));if(js.every(j=>j.status===1)&&lower===null){lower={...a};for(const j of js)for(const [x,v] of Object.entries(j.w)){if(lower[x]!==undefined&&lower[x]!==v)throw Error("guard collision");lower[x]=v;}}}return {live,lower,upper};}
 while(true){let o=outer();if(lazy){for(const j of jobs)if(j.status===0&&j.live&&!o.live.has(j)){j.live=false;c.retired++;}if(o.lower||!o.upper){if(o.lower&&!check(all,o.lower))throw Error("global lift");return {...c,sat:!!o.lower,initial,finished:jobs.filter(j=>j.status!==0).length,unknown:jobs.filter(j=>j.status===0).length};}}
 if(!lazy&&jobs.every(j=>j.status!==0)){if(o.lower&&!check(all,o.lower))throw Error("eager lift");return {...c,sat:!!o.lower,initial,finished:initial,unknown:0};}
 c.rounds++;for(const j of jobs){if(j.status!==0||!j.live)continue;let a=j.gen.next();if(a.done){j.status=a.value?1:-1;j.w=a.value||null;if(j.w){if(!check(regs[j.i],j.w)||Object.entries(j.pin).some(([v,x])=>j.w[v]!==x))throw Error("pin mismatch");c.verified++;}}}
 }
 }
 const cases=[];function add(name,regs,expected){let a=solve(regs,true),b=solve(regs,false);if(a.sat!==b.sat||a.sat!==expected)throw Error(name);cases.push({name,expected,lazy:a,eager:b});}
 for(let k=-1;k<14;k++){let cs=F.flatMap(e=>nae(...e));if(k>=0)cs.splice(k,1);add("Fano owner "+k,[cs.filter((_,i)=>i%3===0),cs.filter((_,i)=>i%3===1),cs.filter((_,i)=>i%3===2)],ref(cs)>0);}
 let seed=20825;function rnd(n){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n;}
 for(let k=0;k<100;k++){let cs=[];for(let i=0;i<3+rnd(12);i++){let s=new Set();while(s.size<3)s.add(1+rnd(6));cs.push([...s].map(v=>rnd(2)?v:-v));}let regs=[cs.filter((_,i)=>i%2===0),cs.filter((_,i)=>i%2===1)];add("random "+k,regs,ref(cs)>0);}
 // DR02 SAT switch, Fano expanded to signed 3-CNF. Ports 1,2; private IDs >=3.
 function sw(source){let a=1,b=2,next=3+Math.max(...source.flat().map(Math.abs));let cs=[];for(const clause of source){let [l1,l2,l3]=clause.map(l=>Math.sign(l)*(Math.abs(l)+2));let t=next++,u=next++;cs.push(...nae(-b,l1,t),...nae(-t,l2,u),...nae(-u,l3,a));}return cs;}
 let source=F.flatMap(e=>nae(...e));let eq=[[-1,2],[1,-2]],ne=[[1,2],[-1,-2]];
 add("DR02 equal SAT",[sw(source),eq],true);add("DR02 unequal UNSAT",[sw(source),ne],false);add("DR02 neighbor unequal SAT",[sw(source.slice(1)),ne],true);
 // Unrelated hard row job: explicit equality and inequality regions contradict
 // for every shared word while the switch has not been fully acquired.
 add("DR02 contradictory outside",[sw(source),eq,ne],false);
 let sums={cases:cases.length,sat:cases.filter(x=>x.expected).length,unsat:cases.filter(x=>!x.expected).length,early:cases.filter(x=>x.lazy.unknown>0).length};
 for(const mode of ["lazy","eager"]){sums[mode]={};for(const key of Object.keys(cases[0][mode]).filter(k=>k!=="sat"))sums[mode][key]=cases.reduce((s,x)=>s+x[mode][key],0);}
 return {seed:20825,sums,cases};
}
console.log(JSON.stringify(experiment(),null,2));
