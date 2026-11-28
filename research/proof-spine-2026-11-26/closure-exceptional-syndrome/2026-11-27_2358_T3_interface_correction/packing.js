function packing(sha,compile){
 const ck=(x,m)=>{if(!x)throw Error(m||"check")},n=16,universe=1<<n,triples=s=>s.flatMap((_,i)=>[s.filter((_,j)=>j!==i).join(",")]),scopes=[];
 for(let a=0;a<n;a++)for(let b=a+1;b<n;b++)for(let c=b+1;c<n;c++)for(let d=c+1;d<n;d++)scopes.push([a,b,c,d]);
 let block=null,attempts=[];
 for(let seed0=271128;seed0<271138&&!block;seed0++){
  let seed=seed0>>>0,next=()=>{seed^=seed<<13;seed^=seed>>>17;seed^=seed<<5;return seed>>>0},S=scopes.slice(),seen=new Set(),rows=[],alive=Array.from({length:universe},(_,i)=>i).filter(i=>(i&1)===0),visits=0,previous=null;
  for(let i=S.length-1;i>0;i--){let j=next()%(i+1);[S[i],S[j]]=[S[j],S[i]]}
  for(let scope of S){let t=triples(scope);if(t.some(x=>seen.has(x)))continue;let sig=next()&14,mask=scope.reduce((m,v,i)=>m|((sig>>i&1)<<v),0),U=scope.reduce((m,v)=>m|1<<v,0),old=alive;alive=alive.filter(w=>{visits++;let z=(w^mask)&U;return z!==0&&z!==U});rows.push({scope,sig});t.forEach(x=>seen.add(x));if(!alive.length){previous=old;block={seed:seed0,rows:rows.slice(0,-1),removed:rows[rows.length-1],relativeSurvivors:previous,visits};break}}
  attempts.push({seed:seed0,rows:rows.length,survivors:alive.length,visits})
 }
 if(!block)return{status:"UNKNOWN seed cap",attempts};
 function valid(w,rows){return rows.every(({scope,sig})=>{let b=scope.map((v,i)=>(w>>v&1)^(sig>>i&1));return b.some(x=>x!==b[0])})}
 // independent full exhaustive truth-table evaluation, including global complement. Exact matching opposite-label controls.
 let good=[],invalidFull=0,checks=0;for(let w=0;w<universe;w++){checks++;if(valid(w,block.rows)){good.push(w);if(!valid(w,[block.removed]))invalidFull++}}ck(good.length>0&&invalidFull===good.length&&good.filter(w=>!(w&1)).join()===block.relativeSurvivors.join(),"block exact");
 const [u,v]=block.removed.scope,rel=((block.removed.sig&1)^((block.removed.sig>>1)&1));ck(good.every(w=>((w>>u&1)^(w>>v&1))===rel));ck(good.some(w=>!(w>>u&1))&&good.some(w=>w>>u&1));
 // choose twist of last block so sum of induced parity is 1; YES neighbor flips the same endpoint back.
 function make(t,NO){
  let nv=t+(n-2)*t,C=[],groups=[],maps=[];
  for(let i=0;i<t;i++){let map=[],next=t+(n-2)*i+1;for(let j=0;j<n;j++)map.push(j===u?i+1:j===v?(i+1)%t+1:next++);let twist=i===t-1?(Number(NO)^((t%2)*rel)):0;maps.push({map,twist});for(let f of block.rows){let c=f.scope.map((j,k)=>map[j]*(((f.sig>>k&1)^(j===v?twist:0))?-1:1));groups.push({scope:c.map(Math.abs),clauseIDs:[C.length+1,C.length+2],signs:c});C.push(c,c.map(l=>-l))}}
  let dimacs=`p cnf ${nv} ${C.length}\n`+C.map(c=>c.join(" ")+" 0\n").join("");return{C,nvars:nv,dimacs,groups,maps}
 }
 function certificate(F,t,NO){
  let tripleMap=new Map(),quadChecks=0,privateTriples=0;
  for(let g of F.groups){let s=g.scope.slice().sort((a,b)=>a-b);ck(s.length===4&&new Set(s).size===4);for(let T of triples(s)){ck(!tripleMap.has(T),"shared triple");tripleMap.set(T,g.clauseIDs[0]);privateTriples++}}
  // Explicit check every multiplier high-degree support, on exact grouped ANF, independent from structural inference.
  const polynomials=F.groups.map(g=>{let P=new Set([0n]);function times(P,v,positive){let T=new Set();const toggle=x=>T.has(x)?T.delete(x):T.add(x);for(let m of P){if(positive)toggle(m);toggle(m|(1n<<BigInt(v-1)))}return T}for(let l of g.signs)P=times(P,Math.abs(l),l>0);let Q=new Set([0n]);for(let l of g.signs)Q=times(Q,Math.abs(l),l<0);for(let m of Q)P.has(m)?P.delete(m):P.add(m);return P});
  const wt=x=>{let r=0;while(x){x&=x-1n;r++}return r};
  for(let i=0;i<polynomials.length;i++){let P=polynomials[i],top=[...P].filter(m=>wt(m)===3);ck(top.length===4&&[...P].every(m=>wt(m)<=3),"grouped ANF");}
  for(let v=1;v<=F.nvars;v++){let seen=new Set();for(let P of polynomials){let Q=new Set();for(let x of P){let y=x|(1n<<BigInt(v-1));Q.has(y)?Q.delete(y):Q.add(y)}let top=[...Q].filter(m=>wt(m)===4);ck(top.length>0,"no overflow");for(let y of top){ck(!seen.has(y),"overflow collision");seen.add(y);quadChecks++}}}
  // Verify full root NO by parity of all interface equations; construct exact YES and deletion witnesses.
  let phase=F.maps.map(a=>rel^a.twist),par=phase.reduce((a,b)=>a^b,0);ck(par===Number(NO));
  let verifyWitness=0;function witness(skip){let a=new Map();a.set(skip===null?1:((skip+1)%t)+1,0);for(let j=0;j<t;j++)for(let i=0;i<t;i++)if(i!==skip){let u=i+1,v=(i+1)%t+1;if(a.has(u))a.set(v,a.get(u)^phase[i]);else if(a.has(v))a.set(u,a.get(v)^phase[i]);}
   for(let i=0;i<t;i++)if(i!==skip){let {map,twist}=F.maps[i],wantU=a.get(i+1),wantV=a.get((i+1)%t+1),w=good.find(w=>(w>>u&1)===wantU&&((w>>v&1)^twist)===wantV);ck(w!==undefined,"local lift");map.forEach((q,j)=>{let bit=(w>>j&1)^(j===v?twist:0);if(a.has(q))ck(a.get(q)===bit,"inconsistent lift");a.set(q,bit)})}
   let rowsPer=block.rows.length*2;for(let k=0;k<F.C.length;k++){if(skip!==null&&Math.floor(k/rowsPer)===skip)continue;ck(F.C[k].some(l=>a.get(Math.abs(l))===+(l>0)),"lift");verifyWitness++}return Array.from({length:F.nvars},(_,i)=>a.get(i+1)||0)}
  let yes=NO?null:witness(null),deletion=NO?Array.from({length:t},(_,i)=>({block:i,witness:witness(i)})):[];
  let hash=sha(F.dimacs),alias=`T3-NAE4-PACK-RING-${t}-${NO?"NO":"YES"}`;return{problem_id:"DIMACS-CNF-v1",alias,short_id:alias+"@"+hash.slice(0,12),instance_id:"DIMACS-CNF-v1:sha256:"+hash,original_N_bits:F.dimacs.length*8,guard_id:"EMPTY",residual_id:"ROOT",original_ids:{variables:[1,F.nvars],clauses:[1,F.C.length]},n:F.nvars,m:F.C.length,groupedRank:F.groups.length,privateTriples,quadChecks,width2ProbeCount:1+2*F.nvars+2*F.nvars*(F.nvars-1),phase,par,verifyWitness,yes,deletion,dimacs:F.dimacs,sourceMap:F.maps}
 }
 let result=[];for(let t of [3,6,12])for(let no of [true,false]){let F=make(t,no),q=certificate(F,t,no);if(t===3&&no){let G=compile(F),s=JSON.stringify(G.network)+"\n",map=JSON.stringify(G.source_map)+"\n";q.native={instance_id:"STRICT-EB4-v1:sha256:"+sha(s),N_bits:s.length*8,vertices:G.network.types.length,edges:G.network.edges.length,map_sha256:sha(map),scope:"compiled native bytes authenticated; no claim of PC/RUP stagnation after compiler auxiliary introduction"}}result.push(q)}
 return{status:"PROVED WITH SCOPE",attempts,block:{...block,n,good,checks,invalidFull,shared:[u,v],relativeParity:rel},instances:result}
}
const fs=require('node:fs'),crypto=require('node:crypto');const c=fs.readFileSync(process.argv[2],'utf8');const compile=Function(c.slice(c.indexOf('function compile'),c.indexOf('function auditLocal'))+'return compile')(),sha=s=>crypto.createHash('sha256').update(s,'utf8').digest('hex');console.log(JSON.stringify(packing(sha,compile),null,2));
