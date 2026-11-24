function runDO01(){
const E=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]], n=7, owners=E.flatMap((vs,e)=>[0,1].map(side=>({vs,e,side}))); 
const assert=(x,s)=>{if(!x)throw Error(s)};
const sum=(x,vs)=>vs.reduce((a,i)=>a+x[i],0);
const cost=(x,o)=>o.side?36-sum(x,o.vs):sum(x,o.vs);
const feasible=(x,os)=>os.every(o=>cost(x,o)<=24);
let result={models:0,sat:0,unsat:0,assignments:0,onePinStrict:0,twoPinLP:0,ownerSlack:0,scopeChecks:0,pathCostChecks:0,labels:[]};
for(let i=0;i<E.length;i++)for(let j=0;j<i;j++)assert(E[i].filter(v=>E[j].includes(v)).length<=1,"linear");
function strict(p,b){let x=Array(n).fill(6);if(p<0)return x;x[p]=12*b;for(const e of E)if(e.includes(p))for(const v of e)if(v!==p)x[v]=b?5:7;return x;}
function two(p,b,q,c){let x=Array(n).fill(6);x[p]=12*b;x[q]=12*c;if(b===c){const e=E.find(e=>e.includes(p)&&e.includes(q));if(e)x[e.find(v=>v!==p&&v!==q)]=12*(1-b);}return x;}
function slack(o,p,b){let x=Array(n).fill(6),target=o.side?24:12;if(p<0||!o.vs.includes(p)){for(const v of o.vs)x[v]=target/3;if(p>=0){x[p]=12*b;for(const e of E)if(e.includes(p)){let vs=e.filter(v=>v!==p);if(sum(x,e)<12||sum(x,e)>24){let j=vs.find(v=>!o.vs.includes(v));assert(j!==undefined,"linear slack");let k=vs.find(v=>v!==j);x[j]=12-x[k];}}}}else{x[p]=12*b;let vs=o.vs.filter(v=>v!==p),rem=target-x[p];x[vs[0]]=Math.min(12,rem);x[vs[1]]=rem-x[vs[0]];}return x;}
for(let relaxed=-1;relaxed<owners.length;relaxed++){const os=owners.filter((o,i)=>i!==relaxed);let solutions=[];result.models++;
for(let mask=0;mask<1<<n;mask++){let x=Array.from({length:n},(_,v)=>12*((mask>>v)&1));let pathCost=owners.map(o=>o.vs.reduce((a,v)=>a+Number((x[v]===12)!==Boolean(o.side)),0));for(let i=0;i<owners.length;i++)assert(12*pathCost[i]===cost(x,owners[i]),"row path cost");result.pathCostChecks+=owners.length;result.assignments++;if(feasible(x,os))solutions.push(mask);}
assert((solutions.length>0)===(relaxed>=0),"label");result[solutions.length?"sat":"unsat"]++;result.labels.push({relaxed,solutions:solutions.length,witness:solutions[0]??null});
for(let p=-1;p<n;p++)for(let b=0;b<(p<0?1:2);b++){let x=strict(p,b);assert(os.every(o=>cost(x,o)<24),"strict");result.onePinStrict++;
for(const o of os){let y=slack(o,p,b);assert(y.every(z=>z>=0&&z<=12)&&feasible(y,os)&&cost(y,o)===12&&(p<0||y[p]===12*b),"slack");result.ownerSlack++;}
if(p>=0)for(let q=p+1;q<n;q++)for(let c=0;c<2;c++){assert(feasible(two(p,b,q,c),os),"two pins");result.twoPinLP++;}
for(let e=0;e<E.length;e++){let vs=E[e], free=vs.filter(v=>v!==p), allowed=[];for(let z=0;z<1<<free.length;z++){let y=Array(n).fill(0);if(p>=0)y[p]=12*b;for(let i=0;i<free.length;i++)y[free[i]]=12*((z>>i)&1);if(os.filter(o=>o.e===e).every(o=>cost(y,o)<=24))allowed.push(z);}for(let a=1;a<1<<free.length;a++){let par=allowed.map(z=>{let s=0;for(let i=0;i<free.length;i++)s^=(a>>i&1)&(z>>i&1);return s;});assert(par.includes(0)&&par.includes(1),"affine hull");}result.scopeChecks++;}
}
}
const signatures=Array.from({length:n},(_,v)=>owners.map(o=>o.vs.includes(v)?(o.side?-1:1):0).join(","));
assert(new Set(signatures).size===n,"unique types");
return {...result,parameters:{n,m:E.length,p:6*E.length-n,log2C:4*E.length-n+1,delta:2*E.length-n+1,Pbad:2**n}};
}
console.log(JSON.stringify(runDO01(),null,2));
