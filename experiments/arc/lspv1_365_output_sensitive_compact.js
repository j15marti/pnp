'use strict';
// LSPV-1 OUTPUT-SENSITIVE-OPT365 compact deterministic finite Resolution experiment.
// This finite exhaustive enumerator is NOT the conditional polynomial SAT algorithm.
const cases=[
 ['empty','p cnf 1 1\n0\n','UNSAT',0],
 ['units','p cnf 1 2\n1 0\n-1 0\n','UNSAT',1],
 ['implication','p cnf 2 3\n1 2 0\n-1 0\n-2 0\n','UNSAT',2],
 ['cube','p cnf 2 4\n1 2 0\n1 -2 0\n-1 2 0\n-1 -2 0\n','UNSAT',3],
 ['signed_cube','p cnf 2 4\n-1 -2 0\n-1 2 0\n1 -2 0\n1 2 0\n','UNSAT',3],
 ['sat_units','p cnf 2 2\n1 0\n2 0\n','SAT',null],
 ['sat_near','p cnf 2 3\n1 2 0\n-1 2 0\n1 -2 0\n','SAT',null],
 ['sat_signed','p cnf 2 1\n-1 2 0\n','SAT',null]
];
function canonical(a){return [...new Set(a)].sort((x,y)=>Math.abs(x)-Math.abs(y)||x-y)}
function parse(s){
 const z=s.trim().split(/\n/).map(t=>t.trim()).filter(Boolean);
 const h=/^p cnf (\d+) (\d+)$/.exec(z.shift());
 if(!h)throw Error('header');
 const n=+h[1],m=+h[2],out=[];let c=[];
 for(const row of z)for(const item of row.split(/\s+/)){
   if(!/^-?(0|[1-9]\d*)$/.test(item))throw Error('token');
   const x=+item;if(Math.abs(x)>n)throw Error('variable');
   if(x===0){out.push(canonical(c));c=[]}else c.push(x);
 }
 if(c.length||out.length!==m)throw Error('count/framing');
 return {n,clauses:out}
}
function models(f){let total=0;for(let mask=0;mask<(1<<f.n);mask++)
 if(f.clauses.every(c=>c.some(x=>Boolean(mask&(1<<(Math.abs(x)-1)))===(x>0))))total++;return total}
function res(a,b,p){if(!a.includes(p)||!b.includes(-p))return null;
 const z=canonical([...a.filter(x=>x!==p),...b.filter(x=>x!==-p)]);
 return z.some(x=>z.includes(-x))?null:z
}
function budget(f,b){
 let Q=[{rows:f.clauses.map(c=>({c})),proof:[]}],visited=new Set();
 for(let head=0;head<Q.length;head++){
  const u=Q[head],rows=u.rows;
  if(rows.some(r=>r.c.length===0))return {yes:true,proof:u.proof,states:head+1};
  if(u.proof.length>=b)continue;
  const seen=new Set(rows.map(r=>r.c.join(',')));
  for(let i=0;i<rows.length;i++)for(let j=0;j<rows.length;j++)if(i!==j)
   for(const p of rows[i].c){const c=res(rows[i].c,rows[j].c,p);if(!c||seen.has(c.join(',')))continue;
     const step={parents:[i,j],pivot:p,clause:c},proof=[...u.proof,step];
     if(!c.length)return {yes:true,proof,states:head+1};
     const h=[...seen,c.join(',')].sort().join('|');
     if(!visited.has(h)){visited.add(h);Q.push({rows:[...rows,{c}],proof})}
   }
 }
 return {yes:false,proof:null,states:Q.length}
}
function check(f,p){const a=f.clauses.map(c=>c);
 for(const step of p){const [i,j]=step.parents;
  if(i>=a.length||j>=a.length||i<0||j<0)return false;
  const z=res(a[i],a[j],step.pivot);
  if(!z||z.join(',')!==step.clause.join(','))return false;a.push(z)
 }
 return a.some(c=>c.length===0)
}
function optimize(f){let log=[];function query(b){const r=budget(f,b);log.push([b,r.yes]);return r}
 if(query(0).yes)return {q:0,p:[],log};
 let hi=1;while(!query(hi).yes)hi*=2;
 let lo=0;while(hi-lo>1){const mid=(hi+lo)>>1;if(query(mid).yes)hi=mid;else lo=mid}
 const r=query(hi);return {q:hi,p:r.proof,log}
}
function k4(odd){let edges=[[1,2,3],[1,4,5],[2,4,6],[3,5,6]],rows=[];
 for(let v=0;v<4;v++)for(let a=0;a<8;a++){
   let parity=((a&1)+((a>>1)&1)+((a>>2)&1))%2;
   if(parity===(v===0?odd:0))continue;
   rows.push(edges[v].map((e,i)=>(a&(1<<i))?-e:e).join(' ')+' 0')
 }
 return 'p cnf 6 '+rows.length+'\n'+rows.join('\n')+'\n'
}
const result=[];let assertions=0,corrupt=0,queries=0;
for(const [name,src,label,expected] of cases){
 const f=parse(src),sat=models(f);
 if((sat>0?'SAT':'UNSAT')!==label)throw Error('label '+name);assertions++;
 if(label==='SAT'){result.push({name,label,models:sat});continue}
 const r=optimize(f);if(r.q!==expected||!check(f,r.p))throw Error('opt '+name);assertions+=2;
 for(let b=0;b<r.q;b++){if(budget(f,b).yes)throw Error('nonminimal');assertions++}
 for(const [b,ans] of r.log){if(budget(f,b).yes!==ans)throw Error('budget');queries++}
 if(r.q){const p=JSON.parse(JSON.stringify(r.p));p[p.length-1].pivot*=-1;
  if(check(f,p))throw Error('corruption');corrupt++}
 result.push({name,label,q:r.q,queries:r.log});
}
for(const [name,src] of [['no_end','p cnf 1 1\n1'],['badvar','p cnf 1 1\n2 0'],
 ['badcount','p cnf 2 2\n1 0'],['badheader','p cnf two 1\n1 0'],['noheader','1 0']]){
 let rejected=false;try{parse(src)}catch(e){rejected=true}
 if(!rejected)throw Error(name);assertions++;result.push({name,label:'MALFORMED'})
}
for(const odd of [0,1]){const f=parse(k4(odd)),sat=models(f);
 if((sat===0)!==Boolean(odd)||(!odd&&sat!==8))throw Error('parity');
 assertions++;result.push({name:odd?'K4odd':'K4even',label:odd?'UNSAT':'SAT',models:sat,minimum:'not searched'})
}
console.log(JSON.stringify({scope:'finite ordinary Resolution only',assertions,corrupt_rejected:corrupt,budget_queries:queries,results:result},null,2));
