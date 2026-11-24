function main(){
 const L={closurePass:0,closureTests:0,closureDeletes:0,walshButterflies:0,productAttempts:0,orbitCandidates:0,pivotSubtractions:0,peakPivots:0,peakTerms:0,verified:0,referenceTuples:0};
 const assert=(b,m)=>{if(!b)throw Error(m)};
 const par=x=>{let p=0;while(x){p^=1;x&=x-1n}return p};
 const bit=(x,j)=>Number((x>>BigInt(j))&1n);
 const top=x=>x.toString(2).length-1;
 function lin(cols,b){let B=new Map(),K=[];for(let i=0;i<cols.length;i++){let x=cols[i],p=1n<<BigInt(i);while(x&&B.has(top(x))){let [y,z]=B.get(top(x));x^=y;p^=z}if(x)B.set(top(x),[x,p]);else K.push(p)}let p=0n;while(b&&B.has(top(b))){let [y,z]=B.get(top(b));b^=y;p^=z}return b?null:{p,K,B}}
 function hull(a){if(!a.length)return null;let h=lin(a.map(x=>x^a[0]),0n);return [a[0],[...h.B.values()].map(x=>x[0])]}
 function closure(F,b,h,q){let G=F.map(A=>A.map((r,i)=>({...r,id:i})));let target=(b<<BigInt(q))|BigInt(h);let tag=r=>(r.t<<BigInt(q))|BigInt(r.g);for(;;){L.closurePass++;if(G.some(A=>!A.length))return null;let changed=false;for(let i=0;i<G.length&&!changed;i++){let a=0n,C=[];for(let j=0;j<G.length;j++)if(j!==i){let H=hull(G[j].map(tag));a^=H[0];C.push(...H[1])}for(let k=0;k<G[i].length;k++){L.closureTests++;if(!lin(C,target^a^tag(G[i][k]))){G[i].splice(k,1);L.closureDeletes++;changed=true;break}}}if(!changed)return G}}
 function add(M,s,c,mod){let v=((M.get(s)||0n)+c)%mod;if(v<0n)v+=mod;if(v)M.set(s,v);else M.delete(s)}
 function fw(a){for(let j=1;j<a.length;j*=2)for(let i=0;i<a.length;i+=2*j)for(let k=0;k<j;k++){let x=a[i+k],y=a[i+k+j];a[i+k]=x+y;a[i+k+j]=x-y;L.walshButterflies++}return a}
 function orbit(P,d,mod){let keys=[...P.keys()],cs=[...P.values()],M=keys.length, piv=new Map(),Q=[];if(!M)return null;L.peakTerms=Math.max(L.peakTerms,M);
 function visit(z){L.orbitCandidates++;let actual=keys.map(s=>par(s&z)?mod-1n:1n);let v=actual.slice(),val=0n;for(let i=0;i<M;i++)val=(val+cs[i]*actual[i])%mod;if(val)return z;
 for(let i=0;i<M;i++)while(v[i]){let low=v[i]&-v[i],k=i+":"+low;let w=piv.get(k);if(!w){piv.set(k,v);Q.push(z);L.peakPivots=Math.max(L.peakPivots,piv.size);return null}for(let j=i;j<M;j++)v[j]=(v[j]-w[j]+mod)%mod;L.pivotSubtractions++}return null}
 let z=visit(0n);if(z!==null)return z;for(let i=0;i<Q.length;i++)for(let j=0;j<d;j++){z=visit(Q[i]^(1n<<BigInt(j)));if(z!==null)return z}return null}
 function solve(F,b,h,q){let masks=closure(F,b,h,q);if(!masks)return {status:"UNSAT"};let a=0n,C=[],A=[],maxr=0;
 for(let R of F){let T=[...new Set(R.map(r=>r.t))];let H=hull(T);if(!H||2**H[1].length!==T.length)return {status:"UNKNOWN"};let [off,B]=H,r=B.length,start=C.length;C.push(...B);a^=off;let groups=new Map();for(let i=0;i<R.length;i++){let p=lin(B,R[i].t^off);assert(p!==null,"coordinate");let j=Number(p.p);if(!groups.has(j))groups.set(j,[]);groups.get(j).push(i)}let mx=Math.max(...[...groups.values()].map(g=>g.length)),s=Math.ceil(Math.log2(mx)),len=2**(r+s);maxr=Math.max(maxr,r+s);let rows=[];for(let k=0;k<len;k++){let g=groups.get(k%(2**r));rows.push(g[Math.floor(k/2**r)%g.length])}A.push({start,r,s,rows,R})}
 let chart=lin(C,b^a);if(!chart)return {status:"UNSAT"};let d=chart.K.length,forms=C.map((_,i)=>{let u=0n;for(let j=0;j<chart.K.length;j++)if(bit(chart.K[j],i))u|=1n<<BigInt(j);return [bit(chart.p,i),u]});for(let f of A){f.forms=forms.slice(f.start,f.start+f.r);for(let j=0;j<f.s;j++)f.forms.push([0,1n<<BigInt(d++)])}
 let D=1n<<BigInt(maxr),den=D**BigInt(q),mod=2n*den,P=new Map([[0n,1n]]);for(let j=0;j<q;j++){let M=new Map();add(M,0n,BigInt(1+bit(BigInt(h),j))*D,mod);for(let f of A){let w=fw(f.rows.map(i=>BigInt(bit(BigInt(f.R[i].g),j))));for(let k=0;k<w.length;k++)if(w[k]){let s=0n,p=0;for(let l=0;l<f.forms.length;l++)if(bit(BigInt(k),l)){p^=f.forms[l][0];s^=f.forms[l][1]}add(M,s,(p?-1n:1n)*w[k]*(D/BigInt(w.length)),mod)}}let R=new Map();for(let [s,u] of P)for(let [t,v] of M){L.productAttempts++;add(R,s^t,u*v,mod)}P=R;L.peakTerms=Math.max(L.peakTerms,P.size)}
 let z=orbit(P,d,mod);if(z===null)return {status:"UNSAT"};let ids=A.map(f=>{let k=0;for(let l=0;l<f.forms.length;l++)k|=(f.forms[l][0]^par(f.forms[l][1]&z))<<l;return f.rows[k]});let t=0n,g=0;ids.forEach((id,i)=>{assert(masks[i].some(r=>r.id===id),"closure mask");t^=F[i][id].t;g^=F[i][id].g});assert(t===b&&g===h,"witness");L.verified++;return {status:"SAT",ids,d,terms:P.size}}
 function brute(F,b,q){let counts=Array(2**q).fill(0n);function rec(i,t,g){if(i===F.length){L.referenceTuples++;if(t===b)counts[g]++;return}for(let r of F[i])rec(i+1,t^r.t,g^r.g)}rec(0,0n,0);return counts}
 let seed=0xBD061220;function rnd(n){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n}
 const results={seed:"0xBD061220",random:{SAT:0,UNSAT:0,UNKNOWN:0},hardCount:[],scale:[],hostile:[]};
 for(let it=0;it<100;it++){let q=1+it%2,F=[];for(let i=0;i<2+it%3;i++){let off=BigInt(rnd(8)),v=BigInt(1+rnd(7)),R=[];for(let t of [off,off^v])for(let k=0,m=1+rnd(2);k<m;k++)R.push({t,g:rnd(2**q)});F.push(R)}let b=BigInt(rnd(8)),counts=brute(F,b,q);for(let h=0;h<2**q;h++){let x=solve(F,b,h,q);assert(x.status===(counts[h]?"SAT":"UNSAT"),"random");results.random[x.status]++}}
 // Compile truth tables with shared variable occurrence synchronization. A private multiplier
 // on each predicate contributes y*violation; mask is a free protected parity row.
 function compile(n,pred){let F=[],stars=Array(n).fill(0n),pos=0;for(let P of pred){let coords=P.vars.map(v=>{let c=1n<<BigInt(pos++);stars[v]^=c;return c});let R=[];for(let x=0;x<2**coords.length;x++){let t=0n;for(let j=0;j<coords.length;j++)if(bit(BigInt(x),j))t^=coords[j];for(let y=0;y<2;y++)R.push({t,g:y*P.bad(x)})}F.push(R)}for(let t of stars)F.push([{t:0n,g:0},{t,g:0}]);return F}
 function sourceCount(n,pred){let c=0;for(let x=0;x<2**n;x++)if(pred.every(p=>!p.bad(p.vars.reduce((s,v,j)=>s|(bit(BigInt(x),v)<<j),0))))c++;return c}
 function compiledCounts(n,pred){let c=[0n,0n];for(let x=0;x<2**n;x++)for(let y=0;y<2**pred.length;y++){let g=0;for(let j=0;j<pred.length;j++){let p=pred[j];g^=bit(BigInt(y),j)*p.bad(p.vars.reduce((s,v,k)=>s|(bit(BigInt(x),v)<<k),0))}c[g]++}return c}
 let cube=Array.from({length:8},(_,i)=>({vars:[0,1,2],bad:x=>+(x===i)}));
 let lines=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]];
 let fano=lines.map(vars=>({vars,bad:x=>+(x===0||x===7)}));
 let cases=[["cube",3,cube],...cube.map((_,i)=>["cube-delete-"+i,3,cube.filter((_,j)=>i!==j)]),["Fano",7,fano],...fano.flatMap((_,i)=>[0,7].map(a=>["Fano-relax-"+i+"-"+a,7,fano.map((p,j)=>j===i?{vars:p.vars,bad:x=>+(x===a)}:p)]))];
 for(let [name,n,p] of cases){let F=compile(n,p),sc=sourceCount(n,p),cc=compiledCounts(n,p),mask=[{t:0n,g:0},{t:0n,g:1}];assert(cc[0]-cc[1]===BigInt(sc)*(1n<<BigInt(p.length)),"gap");let x=solve([...F,mask],0n,0,1),y=solve([...F,[mask[0]]],0n,0,1);assert(x.status==="SAT"&&y.status==="SAT","masked decision");results.hardCount.push({name,sourceModels:sc,pinned:cc.map(String),rootEach:String(cc[0]+cc[1]),decision:x.status,pinnedDecision:y.status})}
 // Correlated guard hostile pair: each guard individually possible, their requested pair is not.
 let hostile=[[{t:0n,g:0},{t:1n,g:3}],[{t:0n,g:0},{t:1n,g:0}]];
 for(let h=0;h<4;h++){let x=solve(hostile,0n,h,2);assert(x.status===([0,3].includes(h)?"SAT":"UNSAT"),"correlated");results.hostile.push({h,status:x.status})}
 // Dense affine chart with no forced local rows, guard identity requires orbit exploration.
 // Each factor is a full 2-bit table, two copies share tag; duplicate nonlinear parity cancels.
 for(let k of [4,8,16,32,64]){let F=[];for(let i=0;i<k;i++){let R=Array.from({length:4},(_,j)=>({t:BigInt(j)<<BigInt(2*i),g:+(j===3)}));F.push(R);F.push(R)}let before={...L},x=solve(F,0n,1,1),y=solve(F,0n,0,1);assert(x.status==="UNSAT"&&y.status==="SAT","scale");results.scale.push({k,selectors:2*k,UNSAT:x.status,SAT:y.status,orbitCandidates:L.orbitCandidates-before.orbitCandidates,productAttempts:L.productAttempts-before.productAttempts,pivotSubtractions:L.pivotSubtractions-before.pivotSubtractions})}
 // Nonzero integer Walsh numerator can represent an identically even function; direct
 // module stress with no cancellation of sparse terms (2-adic parity, not real identity).
 for(let d of [4,8,16,32,64]){let P=new Map();for(let j=0;j<d;j++){P.set(1n<<BigInt(j),2n);P.set((1n<<BigInt(j))^1n<<(BigInt(d)),2n)}let mod=4n;let before={...L};assert(orbit(P,d+1,mod)===null,"even orbit");P.set(0n,2n);assert(orbit(P,d+1,mod)!==null,"odd orbit");results.scale.push({moduleBits:d+1,terms:P.size,orbitCandidates:L.orbitCandidates-before.orbitCandidates,pivotSubtractions:L.pivotSubtractions-before.pivotSubtractions})}
 results.ledger=L;return results;
}
console.log(JSON.stringify(main(),null,2));
