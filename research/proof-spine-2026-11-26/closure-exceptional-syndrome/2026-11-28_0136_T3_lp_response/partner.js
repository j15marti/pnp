function partner(D,pack,sha){
 const ck=(q,m)=>{if(!q)throw Error(m||"check")},pop=w=>{let a=0;while(w){w&=w-1;a++}return a};
 const choose=(b,k)=>Array.from({length:2**b},(_,w)=>Array.from({length:b},(_,i)=>i).filter(i=>w>>i&1)).filter(a=>a.length===k);
 function lift(B,d){let b=2*d+1,Q=choose(b,d+1),C=[];for(let c of B.C){let rows=[[]];for(let l of c)rows=rows.flatMap(r=>Q.map(q=>r.concat(q.map(i=>Math.sign(l)*((Math.abs(l)-1)*b+i+1)))));C.push(...rows)}return C}
 const bytes=(n,C)=>"p cnf "+n+" "+C.length+"\n"+C.map(c=>c.join(" ")+" 0").join("\n")+"\n";
 function response(d){let b=2*d+1,count=0,checks=0,min=2**b,max=0,examples=[];let words=Array.from({length:2**b},(_,i)=>i);for(let mask of words){if(pop(mask)>d)continue;for(let p of words){if((p&mask)!==p)continue;let c=[0,0];for(let w of words){checks++;if((w&mask)===p)c[+(pop(w)>d)]++}let h=pop(mask),a=pop(p),q=b-h,t=d+1-a;let expected=[0,0];for(let w=0;w<2**q;w++)expected[+(pop(w)>=t)]++;ck(c.join()===expected.join()&&c.every(x=>x>0),"fiber counts");min=Math.min(min,...c);max=Math.max(max,...c);count++;if(h===d&&examples.length<3)examples.push({mask,p,c})}}
 // Same singleton means, different phase marginal: uniform singleton vs mix zero and all-one, prob 1/b.
 let A=Array.from({length:b},(_,i)=>1<<i),B=[0,(1<<b)-1],wA=A.map(()=>1),wB=[b-1,1],den=b;for(let i=0;i<b;i++)ck(A.reduce((s,x,j)=>s+(x>>i&1)*wA[j],0)===B.reduce((s,x,j)=>s+(x>>i&1)*wB[j],0),"marginal equality");ck(A.every(w=>pop(w)<=d)&&pop(B[1])>d,"phase difference");return{d,b,guards:count,checks,min,max,examples,collision:{den,A,wA,B,wB,phaseNumerators:[0,1]}}}
 let tables=[1,2,3].map(response),out=[];
 for(let f of D.family.filter(f=>f.m===3||f.m===17)){let d=f.d,b=2*d+1,L=lift(f.base,d),Y=lift(f.yesBase,d),raw=bytes(f.base.n*b,L),yr=bytes(f.yesBase.n*b,Y);ck(sha(raw)===f.source.sha&&raw.length*8===f.source.N,"peer NO hash");ck(sha(yr)===f.yes.sha&&yr.length*8===f.yes.N,"peer YES hash");
 // Independently group complete lifted clauses by signed phase row and verify all original rows.
 let Q=choose(b,d+1),counts=new Map(),rowChecks=0;
 for(let c of L){let M=new Map();for(let l of c){let v=Math.abs(l)-1,z=Math.floor(v/b)+1,s=Math.sign(l),k=z*s;if(!M.has(k))M.set(k,[]);M.get(k).push(v%b);rowChecks++}ck([...M.values()].every(v=>v.length===d+1&&new Set(v).size===d+1),"quota");let key=[...M.keys()].join(",");counts.set(key,(counts.get(key)||0)+1)}
 ck(counts.size===f.base.C.length&&f.base.C.every(c=>counts.get(c.join(","))===Q.length**c.length),"phase row counts");ck(new Set(L.map(c=>c.join(","))).size===L.length,"duplicate");
 // Each complete phase factor pair admits a distribution with singleton 1/2.
 let local=[];for(let i=0;i<f.base.C.length;i+=2){let C=f.base.C.slice(i,i+2),V=[...new Set(C.flat().map(Math.abs))].sort((a,b)=>a-b),S=[];for(let w=0;w<2**V.length;w++)if(C.every(c=>c.some(l=>Boolean(w>>V.indexOf(Math.abs(l))&1)===(l>0))))S.push(w);let pair=S.find(w=>S.includes(w^((1<<V.length)-1)));ck(pair!==undefined,"complementary local support");local.push({V,pair:[pair,pair^((1<<V.length)-1)]})}
 // Independently force selector by two equality paths, verify path constraint endpoints in explicit phase rows.
 let m=f.m,C=f.base.C;let F=[];for(let j=0;j<2;j++){let start=j===0?2:m+2,end=start+m-1,off=j*m*2;for(let v=start;v<end;v++){let i=off+(v-start)*2;ck(C[i].join()===(-v)+","+(v+1)&&C[i+1].join()===v+","+(-(v+1)),"path equality")}let g=j===0?1:-1,i=off+2*(m-1);ck(C[i].join()===[g,start,end].join()&&C[i+1].join()===[g,-start,-end].join(),"guarded end");F.push(g)}
 ck(F[0]===-F[1],"contradiction");
 let W=Array(f.yesBase.n+1).fill(0);W[1]=1;let checks=0;for(let c of Y){checks++;ck(c.some(l=>Boolean(W[Math.floor((Math.abs(l)-1)/b)+1])===(l>0)),"YES lift")}
 let deletion=[];for(let j=0;j<2;j++)for(let k=0;k<m;k++){let a=Array(f.base.n+1).fill(0);a[1]=j===0?0:1;let start=j===0?2:m+2;if(k<m-1)for(let v=start+k+1;v<start+m;v++)a[v]=1;let omitted=j*m+k;for(let i=0;i<C.length;i++)if(Math.floor(i/2)!==omitted)ck(C[i].some(l=>Boolean(a[Math.abs(l)])===(l>0)),"parent removal");deletion.push({factor:omitted,phaseWitness:a})}
 out.push({m,d,n:f.base.n*b,clauses:L.length,source:f.source,yes:f.yes,phaseRows:f.base.C,local,phaseRowLiteralChecks:rowChecks,yesChecks:checks,deletion,selectorForced:F,guardsPerBlock:tables.find(t=>t.d===d).guards,compactInterfaceBits:1,phaseVariables:f.base.n})
 }
 // Ring exact quotient conditional LP contradiction, from verified local block supports.
 let rings=[];for(let x of pack.instances.filter(z=>z.par===1)){ck(sha(x.dimacs)===x.instance_id.split(":").at(-1)&&8*x.dimacs.length===x.original_N_bits,"ring hash");let edge=x.sourceMap.map(z=>({u:z.map[pack.block.shared[0]],v:z.map[pack.block.shared[1]],b:pack.block.relativeParity^+z.twist}));ck(edge.every((e,i)=>e.v===edge[(i+1)%edge.length].u),"ring orientation");let chains=[];for(let p of [0,1]){let a=p,seq=[p];for(let e of edge){a^=e.b;seq.push(a)}ck(a===1-p,"conditional LP");chains.push({pin:[edge[0].u,p],seq,contradiction:[p,a]})}
 rings.push({instance:x.short_id,instance_id:x.instance_id,N:x.original_N_bits,original_ids:x.original_ids,edges:edge,chains,unconditionalFractionalMarginal:"1/2",coverage:"two complementary single-coordinate pins"})
 }
 return{tables,out,rings}
}
const fs=require('node:fs'),sha=s=>require('node:crypto').createHash('sha256').update(s).digest('hex');console.log(JSON.stringify(partner(...process.argv.slice(2).map(p=>JSON.parse(fs.readFileSync(p,'utf8'))),sha),null,2));
