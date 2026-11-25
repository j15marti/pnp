// Node.js: node checker.js DR18.json BS17.json GD24.json S23.json
function run(input){
const [dr,bs,gd,src]=input;
const same=(a,b)=>a.id===b.id&&JSON.stringify(a.guard)===JSON.stringify(b.guard);
let checks=0;const check=(b,msg)=>{checks++;if(!b)throw Error(msg)};
const bits=(n)=>Array.from({length:n},(_,i)=>1n<<BigInt(i));
function solve(T,guard,mode){
T=T.map(o=>({...o,a:o.a.filter(w=>guard.every(([v,b])=>!o.v.includes(v)||+w[o.v.indexOf(v)]===b))}));
const n=T.length,d=T.map(o=>o.a.length),B=d.map(bits),D=d.map(k=>(1n<<BigInt(k))-1n),active=Array.from({length:n},(_,i)=>i),stack=[];
let C={compilePairs:0,arcTests:0,pathTests:0,pathRounds:0,pairDeletes:0,rowDeletes:0,treeTests:0,treeWeightTests:0,eliminated:0,searchNodes:0};
const R=Array.from({length:n},()=>Array(n));
for(let i=0;i<n;i++)for(let j=i+1;j<n;j++){
 const ov=T[i].v.map((v,k)=>[k,T[j].v.indexOf(v)]).filter(p=>p[1]>=0);
 R[i][j]=Array(d[i]).fill(0n);R[j][i]=Array(d[j]).fill(0n);
 for(let a=0;a<d[i];a++)for(let b=0;b<d[j];b++){C.compilePairs++;if(ov.every(([k,l])=>T[i].a[a][k]===T[j].a[b][l])){R[i][j][a]|=B[j][b];R[j][i][b]|=B[i][a]}}
}
function ac(dom,A,root=false){
 let changed=true;
 while(changed){changed=false;for(const i of A){if(!dom[i])return false;for(const j of A){if(i===j)continue;for(let a=0;a<d[i];a++)if(dom[i]&B[i][a]){C.arcTests++;if(!(R[i][j][a]&dom[j])){dom[i]^=B[i][a];if(root)C.rowDeletes++;changed=true;}}if(!dom[i])return false;}}}
 return true;
}
function pc(){
 while(true){if(!ac(D,active,true))return false;let changed=false;C.pathRounds++;
  for(let ii=0;ii<active.length;ii++)for(let jj=ii+1;jj<active.length;jj++){
   const i=active[ii],j=active[jj];
   for(const k of active){if(k===i||k===j)continue;
    // A full relation on either side makes this triangle redundant under AC; if domains change, next pass rechecks.
    let fi=true,fj=true;
    for(let a=0;a<d[i]&&fi;a++)if((D[i]&B[i][a])&&((R[i][k][a]&D[k])!==D[k]))fi=false;
    for(let b=0;b<d[j]&&fj;b++)if((D[j]&B[j][b])&&((R[j][k][b]&D[k])!==D[k]))fj=false;
    if(fi||fj)continue;
    for(let a=0;a<d[i];a++)if(D[i]&B[i][a]){
     const u=R[i][k][a]&D[k], v=R[i][j][a]&D[j];if(!v)continue;
     for(let b=0;b<d[j];b++)if(v&B[j][b]){C.pathTests++;if(!(u&R[j][k][b])){R[i][j][a]^=B[j][b];R[j][i][b]^=B[i][a];C.pairDeletes++;changed=true;}}
    }
   }
  }
  if(!changed)return ac(D,active,true);
 }
}
function tree(k){
 C.treeTests++;const ids=B[k].map((b,a)=>D[k]&b?a:-1).filter(a=>a>=0),q=ids.length;
 if(!q)return null;if(q===1)return {edges:[],deficit:0};
 const sets=new Set();
 for(const i of active)if(i!==k)for(let a=0;a<d[i];a++)if(D[i]&B[i][a]){const s=R[i][k][a]&D[k];if(!s)return null;if(s!==D[k])sets.add(s);}
 let W=Array.from({length:q},()=>new Int32Array(q)),target=0;
 for(const s of sets){let z=[];for(let i=0;i<q;i++)if(s&B[k][ids[i]])z.push(i);target+=z.length-1;for(let i=0;i<z.length;i++)for(let j=i+1;j<z.length;j++){W[z[i]][z[j]]++;W[z[j]][z[i]]++;C.treeWeightTests++;}}
 let seen=new Uint8Array(q),best=new Int32Array(q),par=new Int32Array(q).fill(0);seen[0]=1;for(let j=1;j<q;j++)best[j]=W[0][j];let sum=0,edges=[];
 for(let step=1;step<q;step++){let v=-1;for(let i=0;i<q;i++)if(!seen[i]&&(v<0||best[i]>best[v]))v=i;seen[v]=1;sum+=best[v];edges.push([ids[par[v]],ids[v]]);for(let j=0;j<q;j++)if(!seen[j]&&W[v][j]>best[j]){best[j]=W[v][j];par[j]=v;}}
 return {edges,deficit:target-sum};
}
let root=ac(D,active,true)?"OPEN":"UNSAT",deficits=[];
if(root==="OPEN"&&mode==="combined"){
 if(!pc())root="UNSAT";
 else while(active.length){let found=false;deficits=[];for(const k of active){const t=tree(k);deficits.push([T[k].id,t?.deficit??null]);if(t&&t.deficit===0){stack.push({k,A:active.filter(i=>i!==k),tree:t.edges});active.splice(active.indexOf(k),1);C.eliminated++;found=true;break;}}if(!found)break;if(!pc()){root="UNSAT";break;}}
 if(root==="OPEN"&&!active.length)root="SAT";
}
function dfs(dom){if(++C.searchNodes>20000)return undefined;if(!ac(dom,active))return null;let i=-1,k=Infinity;for(const j of active){let z=0;for(const b of B[j])if(dom[j]&b)z++;if(z>1&&z<k){i=j;k=z;}}if(i<0)return dom;
 for(const b of B[i])if(dom[i]&b){let q=dom.slice();q[i]=b;const w=dfs(q);if(w===undefined||w)return w;}return null;
}
let chosen=null,status=root;
if(root!=="UNSAT"){let w=root==="SAT"?D.slice():dfs(D.slice());if(w===undefined)status="UNKNOWN";else if(!w)status="UNSAT";else{status="SAT";chosen=Array(n).fill(-1);for(const i of active)chosen[i]=B[i].findIndex(b=>b===w[i]);for(const {k,A} of stack.slice().reverse()){let s=D[k];for(const j of A)s&=R[j][k][chosen[j]];check(s!==0n,"empty lift");chosen[k]=B[k].findIndex(b=>!!(b&s));}for(let i=0;i<n;i++){check(chosen[i]>=0,"missing row");for(let j=i+1;j<n;j++)check(!!(R[i][j][chosen[i]]&B[j][chosen[j]]),"bad pair");}}}
let partial=null;if(chosen){partial={};for(let i=0;i<n;i++)T[i].v.forEach((v,k)=>{let b=+T[i].a[chosen[i]][k];check(partial[v]===undefined||partial[v]===b,"bad shared bit");partial[v]=b;});}
return {root,status,counts:C,deficits,eliminationOrder:stack.map(x=>T[x.k].id),partial,retainedRows:D.map((s,i)=>T[i].a.filter((a,k)=>!!(s&B[i][k])).length)};
}
function lift(job,p){
 const s=bs.snapshots.find(x=>same(x,job)),g=gd.jobs.find(x=>same(x,job)),o=src.find(x=>x.id===job.id);check(!!s&&!!g&&!!o,"missing maps");
 let x=s.p.slice();for(const [v,b] of Object.entries(p)){check(x[v]===-1||x[v]===b,"pin conflict");x[v]=b;}
 for(const m of g.merges.slice().reverse()){let key=m.scope.map(v=>x[v]).join("");const l=m.rows.find(z=>z[0]===key);check(!!l,"missing GD lift");m.private.forEach((v,i)=>x[v]=+l[1][i]);}
 for(const e of s.eliminations.slice().reverse()){let key=e.u.reduce((a,v,i)=>{check(x[v]===0||x[v]===1,"unset BS boundary");return a+x[v]*2**i},0);let z=e.lift.find(a=>a[0]===key);check(!!z,"missing BS lift");x[e.v]=z[1];}
 x=x.map(v=>v===-1?0:v);for(const c of o.O){let w=c.t.reduce((a,v,i)=>a+x[v]*2**i,0);check(!(c.bad??[0,7]).includes(w),"source violation");}for(const [v,b] of job.guard)check(x[v]===b,"source guard");return x;
}
let jobs=[];for(const j of dr.results.filter(x=>x.mode==="pair")){let z={id:j.id,guard:j.guard};for(const mode of ["direct","combined"]){let a=solve(j.finalTables,j.guard,mode);if(a.status==="SAT")a.sourceWitness=lift(j,a.partial);z[mode]=a;}check(z.direct.status===z.combined.status,"different labels");jobs.push(z);}
const fano=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]];
const tbl=(cs)=>cs.map((v,id)=>({id,v,a:["100","010","110","001","101","011"]}));
let controls=[];for(const [name,T,expected] of [["Fano",tbl(fano),"UNSAT"],["Fano deletion",tbl(fano.slice(1)),"SAT"],["parity triangle",[[0,1],[1,2],[0,2]].map((v,id)=>({id,v,a:id===2?["01","10"]:["00","11"]})),"UNSAT"],["equality path",[[0,1],[1,2],[2,3]].map((v,id)=>({id,v,a:["00","11"]})),"SAT"]]){
 let z={name};for(const mode of ["direct","combined"]){let a=solve(T,[],mode);check(a.status===expected,"control label");z[mode]=a;}controls.push(z);
}
return {jobs,controls,checks};
}
const fs=require('fs'); console.log(JSON.stringify(run(process.argv.slice(2).map(p=>JSON.parse(fs.readFileSync(p,'utf8')))),null,2));
