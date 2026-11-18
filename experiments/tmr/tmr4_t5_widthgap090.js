'use strict';
// TMR-4/090: complete original-label cofactor minimum-width audit, no packages.
const R=(a,b)=>((b-a+10)%5===1||(b-a+10)%5===3);
const dec=(z,k,b)=>{let a=Array(k).fill(0);for(let i=k-1;i>=0;i--){a[i]=z%b;z=Math.floor(z/b)}return a};
const sat=(a,E)=>E.every(e=>R(a[e[0]],a[e[1]]));
const perms=a=>a.length?a.flatMap((v,i)=>perms(a.slice(0,i).concat(a.slice(i+1))).map(p=>[v].concat(p))):[[]];
const ord=perms([0,1,2,3]), pairs=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]];
let statuses={UNSAT:0,edgeless:0,SAT:0},hist={},clauses=0,orders=0;
for(let code=0;code<729;code++){
 let z=code,E=[];
 for(const [u,v] of pairs){let d=z%3;z=Math.floor(z/3);if(d)E.push(d===1?[u,v]:[v,u]);}
 let Z=0;
 for(let i=0;i<625;i++){
  let a=dec(i,4,5),ok=sat(a,E);Z+=ok?1:0;clauses++;
  // Evaluate actual literal clauses for invalid 3-bit labels and forbidden pairs.
  let bits=a.flatMap(x=>[!!(x&4),!!(x&2),!!(x&1)]),pass=true;
  const forbid=(v,x)=>[0,1,2].some(k=>bits[3*v+k]!==!!(x&(1<<(2-k))));
  for(let v=0;v<4;v++)for(let x=5;x<8;x++)if(!forbid(v,x))pass=false;
  for(const [u,v] of E)for(let x=0;x<5;x++)for(let y=0;y<5;y++)if(!R(x,y)&&!(forbid(u,x)||forbid(v,y)))pass=false;
  if(ok!==pass)throw Error('literal CNF mismatch');
 }
 let kind=!E.length?'edgeless':Z?'SAT':'UNSAT',best=Infinity;
 for(const p of ord){
  let w=0;
  for(let d=0;d<4;d++){
   let sig=new Set();
   for(let x=0;x<5**d;x++){
    let pre=dec(x,d,5),s='';
    for(let y=0;y<5**(4-d);y++){
     let tail=dec(y,4-d,5),a=Array(4);
     for(let j=0;j<d;j++)a[p[j]]=pre[j];
     for(let j=d;j<4;j++)a[p[j]]=tail[j-d];
     s+=sat(a,E)?'1':'0';
    }
    sig.add(s);
   }
   w=Math.max(w,sig.size);
  }
  if((!Z&&w!==1)||(Z&&E.length&&w<5))throw Error('width-gap contradiction');
  best=Math.min(best,w);orders++;
 }
 statuses[kind]++;hist[kind+'_'+best]=(hist[kind+'_'+best]||0)+1;
}
let masks=0;
for(let direction=0;direction<2;direction++)for(let x=0;x<32;x++)for(let y=0;y<32;y++){
 let a=0,b=0;
 for(let u=0;u<8;u++)for(let v=0;v<8;v++)if(u<5&&v<5&&(x&(1<<u))&&(y&(1<<v))&&(direction?R(v,u):R(u,v))){a|=1<<u;b|=1<<v;}
 if(a>31||b>31)throw Error('bad valid code mask');masks++;
}
const result={revision:'tmr4-090-repo-standalone-v1',statuses,hist,graphs:729,orders,pointwise_cnf:clauses,masks,errors:0};
console.log(JSON.stringify(result));
