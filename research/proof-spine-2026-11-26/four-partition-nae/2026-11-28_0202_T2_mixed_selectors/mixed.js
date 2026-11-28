
function run(sha){
const enc=x=>JSON.stringify(x)+"\n",mod=(a,q)=>((a%q)+q)%q;
function generate(q,yes){
 let triples=[];for(let a=0;a<q;a++)for(let b=0;b<q;b++)triples.push([a,b,(a+b)%q]);if(yes)triples.push([q-1,q/2,q-1]);
 const blocks=triples.map((_,i)=>[i+1]),groups=Array.from({length:q},()=>[]);let vars=triples.length,conflicts=0;
 triples.forEach((t,i)=>groups[t[0]].push(i));
 for(let i=0;i<triples.length;i++)for(let j=i+1;j<triples.length;j++){let A=triples[i],B=triples[j];if(A[1]===B[1]||A[2]===B[2]){vars++;blocks[i].push(vars);blocks[j].push(-vars);conflicts++;}}
 return {format:"SIGNED-MONOMIAL-TWO-RESOURCE-v1",q,triples,blocks,groups,vars};
}
function check(G,yes,sha){
 let {q,triples:T,blocks:B,groups,vars}=G,encG=enc(G),digest=sha(encG),id=G.format+":sha256:"+digest,counts=new Map(),visits=0,pairChecks=0,pairWords=0,conflicts=0;
 for(let i=0;i<B.length;i++)for(let l of B[i]){visits++;let v=Math.abs(l);if(!counts.has(v))counts.set(v,[]);counts.get(v).push([i,Math.sign(l)]);}
 if(counts.size!==vars)throw Error("variable incidence");
 let C=new Set();for(let [v,o] of counts){if(v<=T.length){if(o.length!==1||o[0][0]!==v-1||o[0][1]!==1)throw Error("private slack");}else{if(o.length!==2||o[0][1]!==-o[1][1])throw Error("bad conflict");let [i,j]=o.map(z=>z[0]);C.add(i+":"+j);}}
 for(let i=0;i<T.length;i++)for(let j=i+1;j<T.length;j++){pairChecks++;let a=T[i],b=T[j],need=a[1]===b[1]||a[2]===b[2];if(C.has(i+":"+j)!==need)throw Error("conflict graph");if(need)conflicts++;}
 if(groups.flat().length!==T.length||new Set(groups.flat()).size!==T.length||groups.some((g,a)=>g.some(i=>T[i][0]!==a)))throw Error("groups");
 function match(c){let owner=new Map(),pathVisits=0;function go(a,seen){for(let i of groups[a]){pathVisits++;let r=T[i][c];if(seen.has(r))continue;seen.add(r);if(!owner.has(r)||go(owner.get(r),seen)){owner.set(r,a);return true;}}return false;}let size=0;for(let a=0;a<q;a++)if(go(a,new Set()))size++;return {size,pathVisits};}
 let left=match(1),right=match(2);if(left.size!==q||right.size!==q)throw Error("projection match");
 let certificate={problem_id:G.format,instance:"MIXED-CYCLIC-"+q+(yes?"-YES":"-NO")+"@"+digest.slice(0,12),instance_id:id,original_N_bits:encG.length*8,guard_id:"EMPTY",residual_id:"ROOT",original_ids:{phases:[0,T.length-1],variables:[1,vars],groups:[0,q-1]},parents:[],q,yes};
 if(!yes){
  // Exact rational packet: each group choice uniform 1/q, each distinct pair has weight 1/(q*(q-2)) on compatible choices.
  for(let a=0;a<q;a++)for(let b=a+1;b<q;b++){let ma=new Map(),mb=new Map();for(let i of groups[a])for(let j of groups[b]){pairWords++;if(T[i][1]===T[j][1]||T[i][2]===T[j][2])continue;ma.set(i,(ma.get(i)||0)+1);mb.set(j,(mb.get(j)||0)+1);}if(groups[a].some(i=>ma.get(i)!==q-2)||groups[b].some(j=>mb.get(j)!==q-2))throw Error("pair packet");}
  let rowChecks=0;for(let [a,b,c] of T){rowChecks++;if(mod(c-a-b,q)!==0)throw Error("mod relation");}
  let sum=q*(q-1)/2;if(mod(sum,q)===0||mod(2*sum,q)!==0)throw Error("sum certificate");
  Object.assign(certificate,{claim:"UNSAT by cyclic residue conservation; both resource projections have perfect matchings and group-pair marginal packet feasible",proof:{modulus:q,resourceSum:sum,residue:mod(sum,q),allTriplesChecked:rowChecks,pairWeightDenominator:q*(q-2),singletonWeightDenominator:q}});
 }else{
  let chosen=[];for(let a=0;a<q;a++){let b=a<q/2?a:a<q-1?a+1:q/2,c=a===q-1?q-1:(a+b)%q;let i=T.findIndex(t=>t[0]===a&&t[1]===b&&t[2]===c);if(i<0)throw Error("missing witness");chosen.push(i);}
  if(new Set(chosen.map(i=>T[i][1])).size!==q||new Set(chosen.map(i=>T[i][2])).size!==q)throw Error("bad matching");
  let x=new Uint8Array(vars+1),active=new Set(chosen);for(let i of chosen)for(let l of B[i])x[Math.abs(l)]=Number(l>0);for(let i=0;i<T.length;i++)if(!active.has(i))x[i+1]=0;for(let i=0;i<B.length;i++)if(B[i].every(l=>x[Math.abs(l)]===Number(l>0))!==active.has(i))throw Error("lift");
  Object.assign(certificate,{claim:"SAT with checked original-variable lift",proof:{chosen,assignment:Array.from(x.slice(1))}});
 }
 const certbytes=enc(certificate);
 return {certificate,certificate_id:"CERT-v1:sha256:"+sha(certbytes),visits,pairChecks,pairWords,conflicts,left,right,phases:T.length,vars};
}
return [4,6,10,16,24].flatMap(q=>[false,true].map(yes=>check(generate(q,yes),yes,sha)));
}

if(require.main===module){const crypto=require('node:crypto');console.log(JSON.stringify(run(s=>crypto.createHash('sha256').update(s,'utf8').digest('hex')),null,2));}
