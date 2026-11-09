/* LSPV1/525 pinned upstream proof extension. Uses signed ER2, NOT historical R_mix341. */
"use strict";
const fs=require("fs"),path=require("path"),crypto=require("crypto");
function extend(b){
 const p=b.proof,m=x=>Math.abs(x)<=4?x:Math.sign(x)*(Math.abs(x)+3),norm=a=>[...new Set(a)].sort((x,y)=>Math.abs(x)-Math.abs(y)||x-y);
 const L=p.lines.map(x=>({...x,clause:x.clause.map(m),...(x.kind==="RES"?{pivot:m(x.pivot)}:{})}));
 const G=p.definitions.map(x=>({...x,id:x.id+3,a:m(x.a),b:m(x.b)})),goals=p.targets.map(x=>({...x,clause:x.clause.map(m)}));
 let next=27,r=p.paid_resolution_nodes;
 const line=(kind,c,meta={})=>{const id=L.length,clause=norm(c);if(clause.some(x=>clause.includes(-x)))throw Error("tautology");L.push({id,kind,clause,...meta});return id};
 const def=(a,b,label)=>{if(Math.abs(a)===Math.abs(b)||Math.abs(a)>=next||Math.abs(b)>=next)throw Error("bad ports");let id=next++,owner=G.length,facets=[];for(let [tag,c] of [["left",[-id,a]],["right",[-id,b]],["back",[id,-a,-b]]])facets.push(line("FACET",c,{tag,owner}));let x={owner,id,a,b,label,facets};G.push(x);return x};
 const res=(a,b,p,expected)=>{let u=a,v=b,A=L[a].clause,B=L[b].clause;if(A.includes(-p)&&B.includes(p)){u=b;v=a;}else if(!A.includes(p)||!B.includes(-p))throw Error("bad resolution");let c=norm([...L[u].clause.filter(x=>x!==p),...L[v].clause.filter(x=>x!==-p)]);if(expected&&JSON.stringify(c)!==JSON.stringify(norm(expected)))throw Error("bad target");r++;return line("RES",c,{left:u,right:v,pivot:p})};
 const Z=[-22,-24,-26],A=[5,6,7],U=goals.slice(4).map(g=>g.id),term=[[],[],[]],off=[[],[],[]];
 if(JSON.stringify(U.map(i=>L[i].clause))!==JSON.stringify([[-22],[24],[26]]))throw Error("unexpected base");
 for(let i=0;i<3;i++)for(let j=0;j<3;j++){term[i][j]=def(Z[i],A[j],`term_${i}_${j}`);if(i)off[i][j]=res(term[i][j].facets[0],U[i],Math.abs(Z[i]),[-term[i][j].id]);}
 const target=[];
 for(let k=0;k<3;k++){
  let t0=term[0][k],t1=term[1][(k+2)%3],t2=term[2][(k+1)%3],mid=def(-t0.id,-t1.id,"nor1_"+k),out=def(mid.id,-t2.id,"nor2_"+k);
  let positiveTerm=res(t0.facets[2],U[0],Math.abs(Z[0]),[t0.id,-A[k]]);
  let x=res(mid.facets[2],off[1][(k+2)%3],t1.id,[mid.id,t0.id]);x=res(x,t0.facets[1],t0.id,[mid.id,A[k]]);
  let y=res(out.facets[2],off[2][(k+1)%3],t2.id,[out.id,-mid.id]);const c1=res(x,y,mid.id,[out.id,A[k]]);
  let z=res(out.facets[0],mid.facets[0],mid.id,[-out.id,-t0.id]);const c2=res(z,positiveTerm,t0.id,[-out.id,-A[k]]);
  target.push({k,bit:-out.id,input:A[k],positive:c1,negative:c2});
 }
 if(L.length!==190||G.length!==34||r!==81)throw Error("size invariant");
 return {name:"LSPV1_525_ZERO_SUM_IDENTITY",model:"owner-qualified signed-AND2 ER2/Resolution, distinct from historical R_mix341",base_sha:b.base_sha,original_variable_bound:7,zero_units:U,targets:target,proof:{lines:L,defs:G,paid_defs:G.length,paid_res:r,paid_work:r+G.length}};
}
function main(){const src=fs.readFileSync(path.join(__dirname,"lspv1_524_strict3_inverse_cancellation.js"),"utf8");const sha=crypto.createHash("sha1").update("blob "+Buffer.byteLength(src)).update(Buffer.from([0])).update(src).digest("hex");if(sha!=="3fa42e25e02d05b9a915458a7f780e59fd828c12")throw Error("upstream SHA changed");let b=(new Function(src+";return main();"))();b.base_sha=sha;return extend(b)}
if(require.main===module)console.log(JSON.stringify(main(),null,2));
module.exports={main,extend};
