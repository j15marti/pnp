function BA11tree(){
 const M={solves:0,xors:0,termPairs:0,treeCalls:0,treeEdges:0,localCountCalls:0,closureScans:0,pins:0,assertions:0,referenceWords:0,verifiedLifts:0,peakMatrixEntries:0};
 const bit=i=>1n<<BigInt(i), pow2=bit;function dot(a,b){let x=a&b,p=0;while(x){x&=x-1n;p^=1}return p}
 function ok(x,s){M.assertions++;if(!x)throw Error(s)}
 function solve(d,eq){M.solves++;let m=new Map();for(let [a,b] of eq){while(a){let p=a.toString(2).length-1;if(!m.has(p)){m.set(p,[a,b]);break}let [u,v]=m.get(p);a^=u;b^=v;M.xors++}if(!a&&b)return null}let keys=[...m.keys()].sort((a,b)=>a-b);
 function fill(x,h){for(let p of keys){let [a,b]=m.get(p);if(dot(a,x)!==(h?0:b))x^=bit(p)}return x}
 return {a:fill(0n,false),K:Array.from({length:d},(_,i)=>i).filter(i=>!m.has(i)).map(i=>fill(bit(i),true))}}
 function proj(A,offset,k){let mask=pow2(k)-1n, a=(A.a>>BigInt(offset))&mask,B=A.K.map(x=>(x>>BigInt(offset))&mask),K=solve(k,B.map(x=>[x,0])).K;return {dim:k-K.length,eq:K.map(w=>[w,dot(w,a)])}}
 function val(ts,x){return ts.reduce((s,t)=>s+(t.eq.every(([a,b])=>dot(a,x)===b)?t.c:0n),0n)}
 function compile(nodes,edges){
   if(edges.length!==nodes.length-1)return null;
   const adj=nodes.map(()=>[]);for(let e=0;e<edges.length;e++){let {u,v}=edges[e];adj[u].push([v,e]);adj[v].push([u,e])}
   let seen=new Set([0]),order=[0],parent=[-1],pe=[-1];for(let u of order)for(let [v,e] of adj[u])if(!seen.has(v)){seen.add(v);order.push(v);parent[v]=u;pe[v]=e}
   if(order.length!==nodes.length)return null;
   let P=[];for(let i=0;i<nodes.length;i++){let n=nodes[i],offset=0,loc=[];for(let e of n.edges){loc.push([e,offset,edges[e].r]);offset+=edges[e].r}let d=offset+n.private,ts=[];
     for(let t of n.terms){let A=solve(d,t.eq);if(!A)continue;let all=proj(A,0,offset),parts=loc.map(([e,o,k])=>[e,proj(A,o,k)]);if(parts.reduce((s,p)=>s+p[1].dim,0)!==all.dim)return null;
       ts.push({c:t.c*pow2(A.K.length-all.dim),by:Object.fromEntries(parts.map(([e,p])=>[e,p.eq]))})}
     P.push({ts,d,loc})}
   const Q=edges.map(()=>[]),matrix=edges.map((ed,e)=>{let a=P[ed.u].ts,b=P[ed.v].ts;return a.map(t=>b.map(s=>{M.termPairs++;return solve(ed.r,[...t.by[e],...s.by[e]])}))});
   M.peakMatrixEntries=Math.max(M.peakMatrixEntries,matrix.reduce((s,a)=>s+a.reduce((v,b)=>v+b.length,0),0));
   function count(){M.treeCalls++;let dp=[];for(let u of order.slice().reverse()){let x=P[u].ts.map(t=>t.c);for(let [v,e] of adj[u])if(parent[v]===u){M.treeEdges++;let mat=matrix[e],ed=edges[e];for(let i=0;i<x.length;i++){let total=0n;for(let j=0;j<dp[v].length;j++){let A=ed.u===u?mat[i][j]:mat[j][i];if(!A)continue;let B=Q[e].length?solve(ed.r,[...Q[e],...solve(ed.r,A.K.map(w=>[w,0])).K.map(w=>[w,dot(w,A.a)])]):A;if(B)total+=pow2(B.K.length)*dp[v][j]}x[i]*=total}}dp[u]=x}return dp[0].reduce((a,b)=>a+b,0n)}
   function localCount(i,extra=[]){M.localCountCalls++;let n=nodes[i],p=P[i],eq=extra.slice();for(let [e,o] of p.loc)for(let [a,b] of Q[e])eq.push([a<<BigInt(o),b]);let total=0n;for(let t of n.terms){let A=solve(p.d,[...eq,...t.eq]);if(A)total+=t.c*pow2(A.K.length)}return total}
   // Certified local coordinate closure over actual edge variables; deductions kept in Q.
   // Private variables are chosen only after the exterior guard has been fixed.
   function close(){for(;;){let change=false;for(let i=0;i<nodes.length;i++){M.closureScans++;if(!localCount(i))return false;for(let [e,o,k] of P[i].loc){let fixed=new Set(Q[e].map(([a])=>String(a)));for(let j=0;j<k;j++){let w=bit(j);if(fixed.has(String(w)))continue;let a=localCount(i,[[w<<BigInt(o),0]]),b=localCount(i,[[w<<BigInt(o),1]]);if(!a||!b){Q[e].push([w,a?0:1]);M.pins++;change=true;break}}if(change)break}if(change)break}if(!change)return true}}
   function verify(words,privates){for(let i=0;i<nodes.length;i++){let x=0n,o=0;for(let e of nodes[i].edges){x|=words[e]<<BigInt(o);o+=edges[e].r}x|=privates[i]<<BigInt(o);ok(val(nodes[i].terms,x)===1n,"source witness")}M.verifiedLifts++}
   return {count,close,verify,Q,P};
 }
 const one=()=>[{c:1n,eq:[]}], neg=f=>[...one(),...f.map(t=>({c:-t.c,eq:t.eq}))], mul=(f,g)=>f.flatMap(t=>g.map(s=>({c:t.c*s.c,eq:[...t.eq,...s.eq]}))), shift=(f,o)=>f.map(t=>({c:t.c,eq:t.eq.map(([w,b])=>[w<<BigInt(o),b])}));
 function pred(r){let A=[[1n,0],[2n,0]],B=Array.from({length:r-2},(_,i)=>[bit(i+2),0]);return [{c:1n,eq:A},{c:1n,eq:B},{c:-1n,eq:[...A,...B]}]}
 function chain(m,r,opposite){let E=Array.from({length:m},(_,i)=>({u:i,v:i+1,r})),p=pred(r),n=[{edges:[0],private:0,terms:p}];for(let i=1;i<m;i++){let q=shift(p,r);n.push({edges:[i-1,i],private:0,terms:[...one(),...p.map(t=>({c:-t.c,eq:t.eq})),...q.map(t=>({c:-t.c,eq:t.eq})),...mul(p,q).map(t=>({c:2n*t.c,eq:t.eq}))]})}n.push({edges:[m-1],private:0,terms:opposite?neg(p):p});return [n,E]}
 const out={chain:[],star:[],hostile:[]};
 for(let [m,r] of [[2,4],[4,8],[6,16],[8,32]])for(let opp of [false,true]){let [n,E]=chain(m,r,opp),t=compile(n,E);ok(t!==null,"chain compile");ok(t.close(),"stagnant local closure");let count=t.count(),a=pow2(r-2)+3n,expected=opp?0n:a**BigInt(m);ok(count===expected,"chain count");if(!opp)t.verify(E.map(()=>0n),n.map(()=>0n));
   if(m===2&&r===4){let ref=0n;for(let x=0n;x<pow2(2*r);x++){M.referenceWords++;let a=x&(pow2(r)-1n),b=x>>BigInt(r);if(val(n[0].terms,a)&&val(n[1].terms,x)&&val(n[2].terms,b))ref++}ok(ref===count,"exhaustive chain")}
   out.chain.push({m,r,overlap:m*r,opposite:opp,count:String(count),maxTerms:Math.max(...n.map(x=>x.terms.length))})}
 for(let [m,r] of [[3,4],[12,8]]){let E=Array.from({length:m},(_,i)=>({u:0,v:i+1,r})),n=[{edges:E.map((_,i)=>i),private:0,terms:[...one(),{c:-1n,eq:Array.from({length:m*r},(_,i)=>[bit(i),0])}]}];for(let i=0;i<m;i++)n.push({edges:[i],private:0,terms:pred(r)});let t=compile(n,E);ok(t!==null&&t.close(),"star compile");let C=t.count(),expected=(pow2(r-2)+3n)**BigInt(m)-1n;ok(C===expected,"star count");let w=E.map(()=>0n);w[0]=4n;t.verify(w,n.map(()=>0n));out.star.push({m,r,overlap:m*r,count:String(C)})}
 let diag=[{edges:[0],private:0,terms:one()},{edges:[0,1],private:0,terms:[{c:1n,eq:[[3n,0]]}]},{edges:[1],private:0,terms:one()}];
 ok(compile(diag,[{u:0,v:1,r:1},{u:1,v:2,r:1}])===null,"diagonal must decline");out.hostile.push("non-Cartesian diagonal: UNKNOWN");
 let n=[{edges:[0],private:1,terms:[...one(),{c:-1n,eq:[[1n,0],[2n,0]]}]},{edges:[0],private:0,terms:one()}],E=[{u:0,v:1,r:1}],t=compile(n,E);ok(t!==null&&t.close()&&t.count()===3n,"private projection");t.verify([0n],[1n,0n]);out.hostile.push("private nonaffine fibers: count 3");
 return {out,ledger:M};
}
console.log(JSON.stringify(BA11tree(),null,2));
