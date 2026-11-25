const run = function run(){
 const out={seed:19201124,small:0,sat:0,unsat:0,cutChecks:0,localCuts:0,joins:0,pairAttempts:0,peakKeys:0,peakWidth:0,closurePins:0,closureRejects:0,hullChecks:0,assertions:0,scaling:[]};let seed=out.seed;
 const rnd=n=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n};
 const bit=i=>1n<<BigInt(i), parity=x=>{let p=0;while(x){x&=x-1n;p^=1}return p};
 function ck(v){out.assertions++;if(!v)throw Error("assert "+out.assertions)}
 function add(B,x){while(x){let i=x.toString(2).length-1;if(B[i])x^=B[i];else{B[i]=x;return true}}return false}
 function basis(xs){let B=[];for(let x of xs)add(B,x);return B}
 const rank=B=>B.filter(Boolean).length;
 function inside(B,x){while(x){let i=x.toString(2).length-1;if(!B[i])return false;x^=B[i]}return true}
 function linear(rows, rhs, d){let B=[],R=[];for(let j=0;j<rows.length;j++){let x=rows[j],v=rhs[j];while(x){let i=x.toString(2).length-1;if(B[i]){x^=B[i];v^=R[i]}else{B[i]=x;R[i]=v;break}}if(!x&&v)return null}return {B,R}}
 function source(n,edges,types,pins=[]){let ports=Array.from({length:n},()=>[]);edges.forEach(([u,v,s],i)=>{ports[u].push([i,0]);ports[v].push([i,s])});ck(ports.every(p=>p.length===4));let rows=[],rhs=[];const push=(r,b)=>{rows.push(r);rhs.push(b)};
 for(let v=0;v<n;v++){let p=ports[v];if(types[v]==="E"){for(let j=1;j<4;j++)push(bit(p[0][0])^bit(p[j][0]),p[0][1]^p[j][1])}else push(p.reduce((a,[e])=>a^bit(e),0n),p.reduce((a,[,s])=>a^s,0))}
 for(let [e,x] of pins)push(bit(e),x);return {n,edges,types,pins,ports,rows,rhs}}
 function localClosure(S){let rows=S.rows.slice(),rhs=S.rhs.slice(),d=S.edges.length;for(;;){let L=linear(rows,rhs,d);if(!L){out.closureRejects++;return null}let change=false;for(let v=0;v<S.n&&!change;v++){if(S.types[v]!=="B")continue;let p=S.ports[v],allowed=[];for(let z=0;z<16;z++){if(parity(BigInt(z))||z===0||z===15)continue;let rr=rows.concat(p.map(([e])=>bit(e))),bb=rhs.concat(p.map(([,s],j)=>((z>>j)&1)^s));if(linear(rr,bb,d))allowed.push(z)}
 if(!allowed.length){out.closureRejects++;return null}
 for(let a=1;a<16;a++){let b=parity(BigInt(a&allowed[0]));if(!allowed.every(z=>parity(BigInt(a&z))===b))continue;let r=0n;for(let j=0;j<4;j++)if((a>>j)&1){r^=bit(p[j][0]);b^=p[j][1]}if(!inside(L.B,r)){rows.push(r);rhs.push(b);out.closurePins++;change=true;break}}}if(!change)return {rows,rhs}}}
 function compile(S){let nv=4*S.n,edges=[],groups=Array.from({length:S.n},()=>[]),tag=0,targets=[],decode=[];
 const ae=(u,v,g,o,src=-1)=>{let j=edges.length;edges.push({u,v,g,o,src});groups[o].push(j);return j};
 for(let v=0;v<S.n;v++){let p=4*v;if(S.types[v]==="B"){let a=nv++,b=nv++;for(let j=0;j<4;j++){ae(p+j,a,0n,v);ae(p+j,b,0n,v)}}else{let t=bit(tag++);ae(p,p+1,t,v);ae(p+2,p+3,t,v)}}
 for(let i=0;i<S.edges.length;i++){let [u,v,s]=S.edges[i],p=4*u+S.ports[u].findIndex(x=>x[0]===i),q=4*v+S.ports[v].findIndex(x=>x[0]===i),g=0n;for(let [e,b] of S.pins)if(e===i){let j=tag++;g^=bit(j);if(b)targets.push(j)}
 let j;if(s){let mid=nv++;j=ae(p,mid,g,u,i);ae(mid,q,0n,u)}else j=ae(p,q,g,u,i);decode.push(j)}
 let cols=edges.map(e=>bit(e.u)^bit(e.v)^(e.g<<BigInt(nv))),target=(bit(nv)-1n);for(let j of targets)target^=bit(nv+j);
 return {nv,edges,groups,cols,target,decode}}
 function width(G,left){let set=new Set(left),A=basis(G.cols.filter((_,i)=>set.has(i))),B=basis(G.cols.filter((_,i)=>!set.has(i)));return rank(A)+rank(B)-rank(basis(G.cols))}
 function cutcheck(S,G,L){let V=new Set(L),cross=[];S.edges.forEach(([u,v],i)=>{if(V.has(u)!==V.has(v))cross.push(bit(i))});let sr=rank(basis(S.rows)),w=rank(basis(S.rows.concat(cross)))-sr;
 let left=G.groups.flatMap((g,v)=>V.has(v)?g:[]);ck(width(G,left)===w);out.cutChecks++;return w}
 function targetWitness(cols,t){let B=[],C=[];for(let j=0;j<cols.length;j++){let x=cols[j],c=bit(j);while(x){let i=x.toString(2).length-1;if(B[i]){x^=B[i];c^=C[i]}else{B[i]=x;C[i]=c;break}}}let c=0n;while(t){let i=t.toString(2).length-1;if(!B[i])return null;t^=B[i];c^=C[i]}return c}
 function tree(a){if(a.length===1)return a[0];let k=a.length>>1;return [tree(a.slice(0,k)),tree(a.slice(k))]}
 function dp(S,G){let ref=targetWitness(G.cols,G.target);if(ref===null)return {count:0n};let n=G.edges.length,need=G.nv/2;if(!Number.isInteger(need))return {count:0n};let maxW=0,maxK=0;
 function walk(t){let L,R,ids;if(typeof t==="number")ids=[t];else{L=walk(t[0]);R=walk(t[1]);ids=L.ids.concat(R.ids)}let set=new Set(ids),other=basis(G.cols.filter((_,i)=>!set.has(i))),w=rank(basis(ids.map(i=>G.cols[i])))+rank(other)-rank(basis(G.cols));maxW=Math.max(maxW,w);let M=new Map;
 function insert(s,k,c,a,B){if(k>need||!inside(other,s))return;let key=s.toString()+":"+k,old=M.get(key);if(!old){M.set(key,{s,k,c,a,B:basis(B.filter(Boolean))});return}old.c+=c;add(old.B,old.a^a);for(let x of B)if(x)add(old.B,x)}
 if(typeof t==="number"){let r=(ref&bit(t))?G.cols[t]:0n;insert(r,0,1n,0n,[]);insert(r^G.cols[t],1,1n,G.edges[t].src<0?0n:bit(G.edges[t].src),[])}else{out.joins++;for(let a of L.M.values())for(let b of R.M.values()){out.pairAttempts++;insert(a.s^b.s,a.k+b.k,a.c*b.c,a.a^b.a,a.B.concat(b.B))}}
 maxK=Math.max(maxK,M.size);return {ids,M}}
 let R=walk(tree(G.groups.map(g=>tree(g))));out.peakKeys=Math.max(out.peakKeys,maxK);out.peakWidth=Math.max(out.peakWidth,maxW);let x=R.M.get("0:"+need);return x?{count:x.c,a:x.a,B:x.B,maxW,maxK}:{count:0n,maxW,maxK}}
 function valid(S,x){return S.pins.every(([e,b])=>Number((x>>BigInt(e))&1n)===b)&&S.ports.every((p,v)=>{let k=p.reduce((a,[e,s])=>a+(Number((x>>BigInt(e))&1n)^s),0);return S.types[v]==="B"?k===2:k===0||k===4})}
 function reference(S){let words=[];for(let x=0n;x<bit(S.edges.length);x++)if(valid(S,x))words.push(x);return words}
 function check(S,label,known=null){let G=compile(S),cl=localClosure(S);let w=0;for(let k=1;k<S.n;k++)w=Math.max(w,cutcheck(S,G,Array.from({length:k},(_,i)=>i)));if(S.n<=5)for(let x=1;x<(1<<S.n)-1;x++)cutcheck(S,G,Array.from({length:S.n},(_,i)=>i).filter(i=>x>>i&1));
 let ans=dp(S,G),factor=bit(S.types.filter(t=>t==="B").length),words=known===null?reference(S):null,C=known===null?BigInt(words.length):known;ck(ans.count===C*factor);ck(!!cl||C===0n);if(C){ck(valid(S,ans.a));if(cl)ck(cl.rows.every((r,i)=>parity(r&ans.a)===cl.rhs[i]));if(words){let B=basis(words.map(x=>x^words[0]));ck(rank(B)===rank(ans.B));ck(inside(B,ans.a^words[0]));ck(ans.B.every(x=>!x||inside(B,x)));out.hullChecks++;if(cl)for(let x of words)ck(cl.rows.every((r,i)=>parity(r&x)===cl.rhs[i]))}}
 if(known===null){out.small++;if(C)out.sat++;else out.unsat++}else out.scaling.push({label,sourceCount:C.toString(),matchingCount:ans.count.toString(),prefixWidth:w,dpWidth:ans.maxW??null,peakKeys:ans.maxK??null});
 }
 const k5=()=>{let e=[];for(let i=0;i<5;i++)for(let j=i+1;j<5;j++)e.push([i,j,0]);return e};
 function dc(n){let e=[];for(let i=0;i<n;i++)for(let j=0;j<2;j++)e.push([i,(i+1)%n,0]);return e}
 for(let i=0;i<24;i++){let n=i%2?4:5,e=n===5?k5():dc(n);e.forEach(x=>x[2]=(rnd(17)>>1)&1);let t=Array.from({length:n},()=>rnd(7)<3?"E":"B");check(source(n,e,t,i%3===0?[[rnd(e.length),rnd(2)]]:[]),"small")}
 check(source(5,k5(),Array(5).fill("B")),"K5 balanced");let e=k5();e[0][2]=1;check(source(5,e,Array(5).fill("E")),"odd signed E cycle");
 for(let n of [8,16,32]){let e=dc(n),t=Array(n).fill("B");check(source(n,e,t),"double cycle "+n,bit(n)+2n);let pins=[];for(let i=0;i<e.length;i++)if(e[i][0]===0||e[i][1]===0)pins.push([i,1]);check(source(n,e,t,pins),"all four pinned "+n,0n)}
 return out
};
console.log(JSON.stringify(run(),null,2));
