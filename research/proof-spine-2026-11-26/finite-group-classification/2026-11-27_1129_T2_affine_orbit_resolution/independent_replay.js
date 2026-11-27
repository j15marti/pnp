function replay(G,cert,forest=false){
 const P=4*G.types.length,pa=Int32Array.from({length:P},(_,i)=>i),ph=new Uint8Array(P);let union=0,ops=0,restricts=0,units=0,nodes=0,pairs=0,checks=0;
 function root(x){if(pa[x]===x)return[x,0];let [a,b]=root(pa[x]);ph[x]^=b;pa[x]=a;return[a,ph[x]]}
 function link(a,b,s){union++;let [u,p]=root(a),[v,q]=root(b);let d=p^q^s;if(u===v){if(d)throw Error("signed inconsistency");return}if(u>v){pa[u]=v;ph[u]=d}else{pa[v]=u;ph[v]=d}}
 for(const [a,b,s] of G.edges)link(a,b,s);
 for(let i=0;i<G.types.length;i++)if(G.types[i]==="E")for(let j=1;j<4;j++)link(4*i,4*i+j,0);
 const rows=[];for(let i=0;i<G.types.length;i++)if(G.types[i]==="B")rows.push([i,Array.from({length:4},(_,j)=>root(4*i+j))]);
 const ids=[...new Set(rows.flatMap(([i,l])=>l.map(x=>x[0])))].sort((a,b)=>a-b),n=ids.length,C=1n<<BigInt(n),mask=C-1n,ix=new Map(ids.map((x,i)=>[x,1n<<BigInt(i)]));
 const low=r=>{let a=r&mask;return a&-a};
 const encode=([i,p])=>ix.get(i)^(p?C:0n);
 function ge(R){let a=R.slice(),k=0;for(;;){let p=0n;for(let j=k;j<a.length;j++){let q=low(a[j]);if(q&&(!p||q<p))p=q}if(!p)break;let j=a.findIndex((r,i)=>i>=k&&!!(r&p));[a[j],a[k]]=[a[k],a[j]];for(let i=0;i<a.length;i++)if(i!==k){ops++;if(a[i]&p)a[i]^=a[k]}k++}if(a.slice(k).some(x=>x===C))return null;return a.slice(0,k)}
 function dedup(F){let seen=new Set();return F.filter(e=>{let k=e.join(",");if(seen.has(k))return false;seen.add(k);return true})}
 const parity=ge(rows.map(([i,l])=>l.map(encode).reduce((a,b)=>a^b,0n)));if(!parity)throw Error("parity");
 const reduce=x=>{for(let q of parity){ops++;if(x&low(q))x^=q}return x};
 let F=dedup(rows.map(([i,l])=>ge(l.slice(1).map(v=>reduce(encode(l[0])^encode(v))))).filter(e=>e!==null));
 // Verify source local truth sets: parity and non-equality are precisely B4 for all sixteen physical words.
 for(let w=0;w<16;w++){let count=0;for(let i=0;i<4;i++)count+=w>>i&1;if((count===2)!==(count%2===0&&count!==0&&count!==4))throw Error("B4 identity")}
 let fdim=n-parity.length,initial=F.length,free=new Set(ids.map((_,i)=>1n<<BigInt(i)).filter(b=>!parity.some(r=>low(r)===b)));
 const count=(R,d)=>R===null?0n:1n<<BigInt(d-R.length);
 let forestResult=null;
 if(forest){let weights=F.map(e=>count(e,fdim)),sum=weights.reduce((a,b)=>a+b,0n),seen=Array(F.length).fill(false),best=Array(F.length).fill(-1n),cost=0n,fp=0;best[0]=0n;for(let z=0;z<F.length;z++){let j=-1;for(let i=0;i<F.length;i++)if(!seen[i]&&(j<0||best[i]>best[j]))j=i;seen[j]=true;cost+=best[j];for(let i=0;i<F.length;i++)if(!seen[i]){fp++;let v=count(ge([...F[i],...F[j]]),fdim);if(v>best[i])best[i]=v}}forestResult={pairs:fp,numerator:(sum-cost).toString(),denominator:(1n<<BigInt(fdim)).toString(),ratio:Number(sum-cost)/Number(1n<<BigInt(fdim))}}
 function restrict(R,b,value){restricts++;return ge(R.map(r=>r&b?(r^b^(value?C:0n)):r))}
 function cond(F,r){let p=low(r);if(!p)throw Error("bad guard");return dedup(F.map(e=>ge(e.map(a=>a&p?a^r:a))).filter(e=>e!==null))}
 for(const [i,k,j,m] of cert.trace){let h=1n<<BigInt(i);if(!free.has(h))throw Error("not a free coordinate");let A=F.filter(e=>e.some(r=>r&h)),O=F.filter(e=>!e.some(r=>r&h)),out=[];if(A.length!==k||k>3)throw Error("affected");for(let a=0;a<A.length;a++)for(let b=a+1;b<A.length;b++){pairs++;const X=A[a],Y=A[b];let T=ge([...X,...Y.map(r=>r&h?r^C:r)]);let Q=null;if(T!==null){let u=T.find(r=>r&h);if(!u)throw Error("missing pivot");Q=ge(T.filter(r=>r!==u).map(r=>r&h?r^u:r))}
 // Independent projected two-orientation coverage check, including empty intersections.
 const [x0,x1,y0,y1]=[restrict(X,h,0),restrict(X,h,1),restrict(Y,h,0),restrict(Y,h,1)];
 const I=x0===null||y1===null?null:ge([...x0,...y1]),J=x1===null||y0===null?null:ge([...x1,...y0]);
 const d=free.size-1;
 for(const Z of [I,J])if(Z!==null){if(Q===null||Q.some(r=>ge([...Z,r^C])!==null))throw Error("projection inclusion")}
 const U=I===null||J===null?null:ge([...I,...J]);
 if(count(Q,d)!==count(I,d)+count(J,d)-count(U,d))throw Error("projection coverage");
 checks++;if(Q!==null)out.push(Q)}
 F=dedup([...O,...out]);free.delete(h);if(out.length!==j||F.length!==m)throw Error("size mismatch");
 }
 const allowed=free.size;
 function walk(F,T,used){nodes++;for(const s of T.unit||[]){const q=BigInt("0x"+s),p=low(q);if(!p||used.has(p)||!F.some(e=>e.length===1&&e[0]===(q^C)))throw Error("unit certificate");units++;used.add(p);F=cond(F,q)}
 if(T.conflict){if(!F.some(e=>!e.length))throw Error("false conflict");return}
 const q=BigInt("0x"+T.split),p=low(q);if(!p||used.has(p)||!Array.isArray(T.children)||T.children.length!==2||q&C)throw Error("branch");used.add(p);walk(cond(F,q),T.children[0],new Set(used));walk(cond(F,q^C),T.children[1],new Set(used))}
 const remain=F.length;
 walk(F,cert.tree,new Set());return {n,rank:parity.length,initial,remaining:remain,free:allowed,union,ops,restricts,units,nodes,pairs,checks,forest:forestResult}
}
module.exports={replay};
