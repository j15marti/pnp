
function twoSAT(n,F,W,cap){
 let g=Array.from({length:2*n},()=>[]),r=Array.from({length:2*n},()=>[]),idx=l=>2*(Math.abs(l)-1)+Number(l<0);
 function add(a,b){g[a].push(b);r[b].push(a);W.arcBuild++}
 for(let [a,b] of F){if(W.arcBuild+W.arcVisits>cap)return {status:"UNKNOWN"};let u=idx(a),v=idx(b);add(u^1,v);add(v^1,u)}
 let seen=new Uint8Array(2*n),order=[],S=Array(2*n).fill(-1),over=false;
 function visit(u){seen[u]=1;for(let v of g[u]){if(++W.arcVisits+W.arcBuild>cap){over=true;return}if(!seen[v])visit(v);if(over)return}order.push(u)}
 for(let u=0;u<2*n;u++)if(!seen[u]){visit(u);if(over)return {status:"UNKNOWN"}}
 function rev(u,k){S[u]=k;for(let v of r[u]){if(++W.arcVisits+W.arcBuild>cap){over=true;return}if(S[v]===-1)rev(v,k);if(over)return}}
 let k=0;for(let i=order.length-1;i>=0;i--)if(S[order[i]]<0){rev(order[i],k++);if(over)return {status:"UNKNOWN"}}
 for(let j=0;j<n;j++)if(S[2*j]===S[2*j+1])return {status:"UNSAT",conflict:j+1};
 let z=Array.from({length:n},(_,j)=>Number(S[2*j]>S[2*j+1]));if(!F.every(c=>c.some(l=>z[Math.abs(l)-1]===Number(l>0))))throw Error("2SAT witness");return {status:"SAT",z}
}
function deletionTest(r,cap=3000000){
 let n=r.boundary,E=r.edgeVars.map(([a,b])=>[a+1,b+1]),hard=E,soft=E.map(([a,b])=>[-a,-b]),W={arcBuild:0,arcVisits:0,tests:0},t=Date.now(),m=soft.length,ans=null,excluded=[],witness=null;
 // Exactly two allowed exclusions suffices since deleting more soft clauses cannot hurt.
 for(let i=0;i<m&&!ans;i++)for(let j=i+1;j<m;j++){let F=hard.concat(soft.filter((_,k)=>k!==i&&k!==j)),a=twoSAT(n,F,W,cap);W.tests++;if(a.status==="UNKNOWN"){ans="UNKNOWN";break}if(a.status==="SAT"){let k=E.filter(([u,v])=>a.z[u-1]&&a.z[v-1]).length;if(k>2||!hard.every(c=>c.some(l=>a.z[l-1])))throw Error("soft witness");ans="SAT";witness={z:a.z,removed:[i,j],blocked:k};break}excluded.push([i,j,a.conflict])}
 if(!ans)ans="UNSAT";if(ans!=="UNKNOWN"&&ans!==r.answer)throw Error("deletion disagreement");
 return {instance:r.instance_id,guard:"EMPTY",residual:"ROOT",N:r.N,boundary:n,slack:2,decision:ans,work:W,cap,excluded,witness,ms:Date.now()-t}
}
function gadgets(){
 // exhaustive local violation minimum for paths (a or u), (!u or b), hard replicas 3 (k=2).
 let checks=0;for(let a=0;a<2;a++)for(let b=0;b<2;b++){for(let c of [1,3]){let m=Infinity;for(let w=0;w<2**c;w++){let t=0;for(let i=0;i<c;i++){checks++;let u=(w>>i)&1;t+=Number(!(a||u))+Number(!(!u||b))}m=Math.min(m,t)}if(m!==(a||b?0:c))throw Error("gadget")}}
 return checks
}

// Load pinned check.js, then call deletionTest for each cactus record.
