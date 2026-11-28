
function replayInterface(c,Q,S){
 let F=JSON.parse(c.residual),L=Q.L,R=Q.R,B=Q.b;
 const canon=x=>x.map(z=>JSON.stringify(z)).sort().join("\n");
 if(canon([...L,...R])!==canon(F))throw Error("factor partition");
 let lv=new Set(L.flatMap(f=>f[0])),rv=new Set(R.flatMap(f=>f[0]));
 let boundary=sort([...lv].filter(v=>rv.has(v)));if(J(boundary)!==J(B))throw Error("boundary");
 function decode(T){return T.map(([s,h,o])=>({s,m:BigInt("0x"+h),o}))}
 let a=reindex(decode(L)),b=reindex(decode(R)),C={L:clauses(a.F),R:clauses(b.F)},V={L:a.vars,R:b.vars};
 let rows=0,visits=0,nodes=0,seen=new Set(),supports={L:0,R:0};
 function close(C,p){let m=new Map(p),change=true;while(change){change=false;for(let row of C){let sat=false,unknown=[];for(let l of row){visits++;let v=m.get(Math.abs(l));if(v===undefined)unknown.push(l);else if(v===Number(l>0)){sat=true;break}}if(sat)continue;if(!unknown.length)return {bad:true,m};if(unknown.length===1){let l=unknown[0];m.set(Math.abs(l),Number(l>0));change=true}}}return {bad:false,m}}
 function tree(C,t,p){nodes++;let r=close(C,p);if(r.bad)return;if(t===0)throw Error("false proof leaf");let v=t[0];if(!Number.isInteger(v)||v<1||v>Math.max(...C.flat().map(Math.abs)))throw Error("branch index");if(r.m.has(v)){tree(C,t[r.m.get(v)?2:1],[...r.m]);return}tree(C,t[1],[...r.m,[v,0]]);tree(C,t[2],[...r.m,[v,1]])}
 for(let r of S.rows){if(seen.has(r.w)||r.w<0||r.w>=2**B.length)throw Error("guard index");seen.add(r.w);if(r.status!=="DAG"&&r.status!=="UP")continue;let k=r.side,p=B.map((v,i)=>[V[k].indexOf(v)+1,(r.w>>i)&1]);if(p.some(([v])=>!v))throw Error("guard map");tree(C[k],r.status==="UP"?0:r.tree,p);rows++;supports[k]++}
 return {rows,all:rows===2**B.length,visits,nodes,supports,boundary:B.length,interiors:[lv.size-B.length,rv.size-B.length]}
}
function audit(x){return x.map(z=>({name:z.name,cases:z.cases.map(c=>({kind:c.kind,small:replayInterface(c,{L:c.left,R:c.right,b:c.boundary},c.smallResponses),balanced:c.balanced?.b?replayInterface(c,c.balanced,c.balanced.responses):null}))}))}

// Evaluate with the pinned T1 check.js before calling audit(checkpoints).
