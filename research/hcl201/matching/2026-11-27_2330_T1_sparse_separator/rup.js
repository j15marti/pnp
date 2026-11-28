function rup(F,seeds=[]){
let key=c=>c.slice().sort((a,b)=>a-b).join(","),R=F.map(c=>c.slice()),K=new Set(R.map(key)),visits=0,probes=0,sweeps=0,P=[],vars=[...new Set(R.flat().map(Math.abs))].sort((a,b)=>a-b),L=vars.flatMap(v=>[v,-v]),C=[[]];for(let i=0;i<L.length;i++){C.push([L[i]]);for(let j=0;j<i;j++)if(L[i]!==-L[j])C.push([L[j],L[i]])}
for(let c of seeds){if(!K.has(key(c))){K.add(key(c));R.push(c)}}
function up(c){let A=new Set(c.map(l=>-l));let changed=true;while(changed){changed=false;for(let row of R){let hit=false,n=0,u=0;for(let l of row){visits++;if(A.has(l)){hit=true;break}if(!A.has(-l)){n++;u=l}}if(hit)continue;if(n===0)return true;if(n===1){A.add(u);changed=true}}}return false}
let change=true;while(change){change=false;sweeps++;for(let c of C){if(K.has(key(c)))continue;if(visits>=10000000)return {status:"CAP",visits,probes,sweeps,P};probes++;if(up(c)){P.push(c);R.push(c);K.add(key(c));change=true;if(c.length===0)return {status:"UNSAT",visits,probes,sweeps,P}}}}return {status:"FIXED_POINT",visits,probes,sweeps,P};
}
module.exports=rup;
