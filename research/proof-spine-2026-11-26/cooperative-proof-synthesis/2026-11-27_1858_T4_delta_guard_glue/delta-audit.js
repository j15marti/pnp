function deltaAudit(d,H){
 const {cert,raw,summary}=d,V=cert.chart.variables,F=cert.chart.factors;
 const C=F.flatMap(f=>Array.from({length:2**f.vs.length},(_,w)=>w).filter(w=>!f.ok.includes(w)).map(w=>f.vs.map((v,i)=>w>>i&1?-v:v)));
 const root=raw.baseline, S=[],D=[],J=[];let scans=0,hints=0,checkOps=0,rollbacks=0,peakDepth=0;
 function unit(g,subset){const a=new Map(g.map(l=>[Math.abs(l),+(l>0)]));let reason=[];while(true){let changed=false;for(let i of subset){scans++;let row=C[i];if(row.some(l=>a.get(Math.abs(l))===+(l>0)))continue;let u=row.filter(l=>!a.has(Math.abs(l)));if(!u.length)return reason.concat(i);if(u.length===1){a.set(Math.abs(u[0]),+(u[0]>0));reason.push(i);changed=true}}if(!changed)throw Error("nonconflict")}}
 function checkHint(g,rs){let a=new Map(g.map(l=>[Math.abs(l),+(l>0)]));for(let j=0;j<rs.length;j++){let row=C[rs[j]];if(!row)throw Error("invalid row");checkOps+=row.length;if(row.some(l=>a.get(Math.abs(l))===+(l>0)))throw Error("satisfied hint");let u=row.filter(l=>!a.has(Math.abs(l)));if(j===rs.length-1){if(u.length)throw Error("not contradiction");return}if(u.length!==1)throw Error("not unit");a.set(Math.abs(u[0]),+(u[0]>0))}throw Error("empty hint")}
 const indices=C.map((_,i)=>i);
 function visit(t,g,parent,lit){let id=D.length,kind=t.leaf?0:t.v;S.push([g.slice(),kind]);D.push([parent,lit,kind]);J.push(null);peakDepth=Math.max(peakDepth,g.length);if(t.leaf){let rs=unit(g,indices);checkHint(g,rs);hints+=rs.length;J[id]=rs;return}g.push(-t.v);visit(t.L,g,id,-t.v);g.pop();rollbacks++;g.push(t.v);visit(t.U,g,id,t.v);g.pop();rollbacks++}
 visit(root,[],-1,0);
 function replay(records){let paths=[],children=records.map(()=>[]),checks=0;for(let i=0;i<records.length;i++){let [p,l,v]=records[i];if(i===0){if(p!==-1||l!==0)throw Error("root");paths.push([])}else{if(p<0||p>=i||records[p][2]!==Math.abs(l)||paths[p].some(x=>Math.abs(x)===Math.abs(l)))throw Error("parent");children[p].push(l);paths.push(paths[p].concat(l))}if(JSON.stringify(paths[i])!==JSON.stringify(S[i][0])||v!==S[i][1])throw Error("guard mismatch");checks+=paths[i].length}for(let i=0;i<records.length;i++){let v=records[i][2],ch=children[i].sort((a,b)=>a-b);if(JSON.stringify(ch)!==JSON.stringify(v?[-v,v]:[]))throw Error("coverage")}return checks}
 let replaySlots=replay(D),rejected=0;for(let mode=0;mode<3;mode++){let z=D.map(x=>x.slice());if(mode===0)z[1][0]=1;else if(mode===1)z[1][1]*=-1;else z[0][2]=0;try{replay(z)}catch{rejected++}}
 const len=x=>JSON.stringify(x).length, flip=(p,m)=>p.has(m)?p.delete(m):p.add(m),xor=(p,q)=>{let a=new Set(p);for(let m of q)flip(a,m);return a}, deg=m=>{let z=0;while(m){m&=m-1n;z++}return z}, bit=v=>1n<<BigInt(V.indexOf(v)), degree=p=>Math.max(0,...[...p].map(deg));
 function indicator(row){let p=new Set([0n]);for(let l of row){let m=bit(Math.abs(l)),q=new Set();for(let z of p){if(l>0)flip(q,z);flip(q,z|m)}p=q}return p}
 let x=bit(root.v),dmax=3,ops=0;
 function restrict(p,b){let q=new Set();for(let m of p){if(m&x){if(b)flip(q,m^x)}else flip(q,m)}return q}
 function add(M,p){p=new Set(p);while(p.size){let lead=[...p].reduce((a,b)=>a>b?a:b);if(!M.has(lead)){M.set(lead,p);return true}ops+=M.get(lead).size;p=xor(p,M.get(lead))}return false}
 let A=[new Map(),new Map()],G=new Map();for(let row of C){let p=indicator(row);if(degree(p)<=dmax)add(G,p);for(let b=0;b<2;b++){let q=restrict(p,b);if(degree(q)<=dmax)add(A[b],q)}}
 let top=new Map(),glued=new Map(),witnesses=[];
 for(let b=0;b<2;b++)for(let p of A[b].values()){
 let pair=b?[new Set(),new Set(p)]:[new Set(p),new Set()],t=new Set([...p].filter(m=>deg(m)===dmax));while(t.size){let lead=[...t].reduce((a,b)=>a>b?a:b);if(!top.has(lead)){top.set(lead,{t,pair});break}let old=top.get(lead);ops+=old.t.size+old.pair[0].size+old.pair[1].size;t=xor(t,old.t);pair=[xor(pair[0],old.pair[0]),xor(pair[1],old.pair[1])]}
 if(!t.size){let out=new Set(pair[0]);for(let m of xor(pair[0],pair[1]))flip(out,m|x);if(degree(out)>dmax)throw Error("degree");for(let b=0;b<2;b++)if(xor(restrict(out,b),pair[b]).size)throw Error("lift");if(!add(glued,out))throw Error("kernel dependence");witnesses.push([...out].map(String))}
 }
 if(glued.size!==A[0].size+A[1].size-top.size)throw Error("rank formula");
 let combined=new Map(G),newRank=0;for(let p of glued.values())if(add(combined,p))newRank++;
 return {id:summary.id,N:summary.N,full:summary.full,chart_id:cert.chart_id,guard:"EMPTY",anchor:cert.map.anchor_port,treeNodes:D.length,leaves:J.filter(Boolean).length,peakDepth,rollbackEdges:rollbacks,fullGuardBytes:len(S),deltaBytes:len(D),hybridBytes:len([D,J]),guardLiteralSlots:S.reduce((a,b)=>a+b[0].length,0),deltaLiteralSlots:D.length-1,replaySlots,hintScans:scans,hintCount:hints,hintCheckLiteralVisits:checkOps,tamperRejected:rejected,degree:dmax,split:root.v,branchRanks:A.map(x=>x.size),topRank:top.size,gluedRank:glued.size,originalRank:G.size,newRank,rankOps:ops,delta:D,hintLists:J,gluedPolynomials:witnesses,sourceChart:cert.chart,sourceMap:cert.map,chartHash:cert.chartHash,mapHash:cert.mapHash};
}
module.exports=deltaAudit;
