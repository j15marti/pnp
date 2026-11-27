// node independent_check.js compile.js benchmarks.json registry.json certificate.json
const fs=require('node:fs'),crypto=require('node:crypto');
function check(G,proof){
 const {types,edges}=G,n=types.length*4,par=Int32Array.from({length:n},(_,i)=>i),ph=new Uint8Array(n);
 function f(x){let r=x,t=0;while(par[r]!==r){t^=ph[r];r=par[r]}while(par[x]!==x){let y=par[x],s=ph[x];par[x]=r;ph[x]=t;t^=s;x=y}return r}
 function join(a,b,s){let u=f(a),v=f(b),z=ph[a]^ph[b]^s;if(u===v){if(z)throw Error("transport conflict");return}if(u>v)[u,v]=[v,u];par[v]=u;ph[v]=z}
 for(let v=0;v<types.length;v++)if(types[v]==="E")for(let k=1;k<4;k++)join(4*v,4*v+k,0);for(let [a,b,s] of edges)join(a,b,s);
 const norm=C=>C.slice().sort((a,b)=>a-b),key=C=>norm(C).join(","),F=new Map();
 let localChecks=0,joinChecks=0,clauseScans=0;
 // Independently enumerate all minimal forbidden partial assignments by recursively dropping coordinates.
 for(let v=0;v<types.length;v++)if(types[v]==="B"){
 const L=Array.from({length:4},(_,k)=>{let p=4*v+k;return (f(p)+1)*(ph[p]?-1:1)}),U=[...new Set(L.map(Math.abs))].sort((a,b)=>a-b);
 const vals=Array.from({length:2**U.length},(_,w)=>L.reduce((s,l)=>s+(((w>>U.indexOf(Math.abs(l)))&1)^Number(l<0)),0)===2);
 const evalC=(C,w)=>C.some(l=>((w>>U.indexOf(Math.abs(l)))&1)===Number(l>0));
 const forb=C=>{for(let w=0;w<vals.length;w++){localChecks++;if(vals[w]&&!evalC(C,w))return false===false?false:false}return true};
 // A clause is implied iff no legal assignment falsifies it.
 const implied=C=>{for(let w=0;w<vals.length;w++){localChecks++;if(vals[w]&&!evalC(C,w))return false}return true};
 let S=new Map();function visit(C){let k=key(C);if(S.has(k))return;S.set(k,true);if(!implied(C))return;let drops=C.map((_,i)=>C.filter((_,j)=>i!==j)).filter(implied);if(drops.length)drops.forEach(visit);else F.set(k,norm(C))}
 for(let w=0;w<vals.length;w++)if(!vals[w])visit(U.map((u,i)=>(w>>i)&1?-u:u));
 }
 function restrict(F,v,b){let l=b?v:-v,M=new Map();for(let C of F.values()){clauseScans++;if(C.includes(l))continue;let D=C.filter(x=>x!==-l);M.set(key(D),D)}return M}
 let R=restrict(F,proof.gauge,0); // exact global complement gauge; native rows all complement symmetric
 for(let l of proof.initialUnits){if(!R.has(String(l)))throw Error("invalid root unit");R=restrict(R,Math.abs(l),Number(l>0))}
 for(let st of proof.steps){let A=[],B=[];for(let C of R.values()){clauseScans++;if(C.includes(st.v))A.push(C);if(C.includes(-st.v))B.push(C)}let keys=cs=>cs.map(key).sort().join(";");if(keys(A)!==keys(st.positive)||keys(B)!==keys(st.negative))throw Error("missing incident factor");let U=[...new Set([...A,...B].flat().map(Math.abs))].filter(x=>x!==st.v);if(U.length>8)throw Error("scope cap");
 for(let C of st.resolvents)if(C.some(x=>!U.includes(Math.abs(x))))throw Error("new variable");
 for(let w=0;w<2**U.length;w++){let ev=(C,b)=>C.some(l=>(Math.abs(l)===st.v?b:(w>>U.indexOf(Math.abs(l)))&1)===Number(l>0));let x=[0,1].some(b=>[...A,...B].every(C=>ev(C,b))),y=st.resolvents.every(C=>ev(C,0));joinChecks++;if(x!==y)throw Error("projection mismatch")}
 for(let C of [...A,...B])R.delete(key(C));for(let C of st.resolvents)R.set(key(C),C);
 }
 let nodes=0;function replay(R,t){nodes++;while(true){if(R.has(""))return t[0]==="X";let U=[...R.values()].find(C=>C.length===1);clauseScans+=R.size;if(!U)break;R=restrict(R,Math.abs(U[0]),Number(U[0]>0))}
 if(!Array.isArray(t)||t.length!==3||!Number.isInteger(t[0])||![...R.values()].some(C=>C.some(l=>Math.abs(l)===t[0])))return false;
 return replay(restrict(R,t[0],0),t[1])&&replay(restrict(R,t[0],1),t[2])}
 if(!replay(R,proof.tree))throw Error("branch replay failure");return {localChecks,joinChecks,clauseScans,nodes,remainingClauses:R.size}
}
const [cp,bp,rp,pp]=process.argv.slice(2),c=fs.readFileSync(cp,'utf8'),compile=new Function(c.slice(c.indexOf('function compile'),c.indexOf('function auditLocal'))+';return compile')(),p=JSON.parse(fs.readFileSync(pp)),e=JSON.parse(fs.readFileSync(rp)).instances.find(x=>x.instance_id===p.instance_id),x=JSON.parse(fs.readFileSync(bp)).instances.find(x=>x.id===e.source_cnf.alias),g=compile(x),s=JSON.stringify(g.network)+'\n',sha=s=>crypto.createHash('sha256').update(s).digest('hex');if(sha(s)!==e.sha256||s.length*8!==e.N_bits||sha(x.dimacs)!==e.source_cnf.sha256||sha(JSON.stringify(g.source_map)+'\n')!==e.source_map_sha256||p.original_N_bits!==e.N_bits||p.guard_id!=='EMPTY'||p.residual_id!=='ROOT')throw Error('scope');console.log(check(g.network,p.proof));
