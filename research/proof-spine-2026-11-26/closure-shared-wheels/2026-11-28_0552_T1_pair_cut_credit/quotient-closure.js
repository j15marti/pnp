function closure(res,cap=2000000) {
 let counts={pivot:0,mask:0,pair:0,word:0,verify:0},events=0,proof=[],rounds=[];
 const tick=k=>{counts[k]++;if(++events>cap)throw Error("cap")};
 const lo=v=>v&-v, hi=v=>1n<<BigInt(v.toString(2).length-1),par=v=>{let p=0;while(v){v&=v-1n;p^=1}return p};
 const R=res.regions.map(r=>({F:r.forms.map(([v,c])=>(BigInt("0x"+v)<<1n)|BigInt(c)),W:r.allowed.slice()}));
 function put(B,v,high=false){while(v&~1n){tick("pivot");let p=high?hi(v&~1n):lo(v&~1n);if(B.has(p))v^=B.get(p);else{B.set(p,v);return 1}}return v===1n?-1:0}
 function reduce(B,v){let z=0n;while(v&~1n){tick("pivot");let p=lo(v&~1n);if(B.has(p))v^=B.get(p);else{z^=p;v^=p}}return z^v}
 function legal(F,w,K){tick("verify");let B=new Map();for(let v of K.values())if(put(B,v,true)<0)return false;return F.every((v,i)=>put(B,v^BigInt(w>>i&1),true)>=0)}
 function equations(F){let B=new Map(),E=[];for(let i=0;i<F.length;i++){let x=F[i],m=1<<i;while(x&~1n){tick("pivot");let q=lo(x&~1n);if(!B.has(q)){B.set(q,[x,m]);break}let [v,t]=B.get(q);x^=v;m^=t}if(!(x&~1n))E.push([m,Number(x&1n)])}return E}
 let K=new Map(),decision="UNKNOWN",capped=false,terminal=null;
 const rows=()=>R.reduce((a,r)=>a+r.W.length,0),start=rows();
 try{outer:for(let sweep=0;sweep<=start+res.sharedDimension;sweep++){
 let prevRank=K.size,prevRows=rows();for(let i=0;i<R.length;i++){let {F,W}=R[i];if(!W.length){decision="NO";terminal={i};break outer}for(let m=1;m<2**F.length;m++){tick("mask");let p=par(BigInt(m&W[0]));if(!W.every(w=>par(BigInt(m&w))===p))continue;let v=BigInt(p);for(let j=0;j<F.length;j++)if(m>>j&1)v^=F[j];let t=put(K,v);if(t){proof.push({type:"affine",i,m,p,row:v.toString(16)});if(t<0){decision="NO";terminal={i,m};break outer}}}}
 let Q=R.map(r=>r.F.map(v=>reduce(K,v))),S=Q.map(F=>F.reduce((a,v)=>a|(v&~1n),0n));
 // Independent checker uses original forms and global K, not reduced forms.
 for(let i=0;i<R.length;i++){let r=R[i],E=equations(Q[i]);let removed=r.W.filter(w=>{tick("word");return E.some(([m,b])=>par(BigInt(m&w))!==b)});for(let w of removed)if(legal(r.F,w,K))throw Error("bad global filter");if(removed.length){proof.push({type:"local",i,removed});r.W=r.W.filter(w=>!removed.includes(w));if(!r.W.length){decision="NO";terminal={i};break outer}}}
 for(let i=0;i<R.length;i++)for(let j=i+1;j<R.length;j++){tick("pair");if(!(S[i]&S[j]))continue;let a=R[i],b=R[j],F=[...Q[i],...Q[j]],shift=a.F.length,E=equations(F);if(!E.some(([m])=>(m&((1<<shift)-1))&&(m>>shift)))continue;let U=new Set(),V=new Set();for(let u of a.W)for(let v of b.W){tick("word");let w=u+(v<<shift);if(E.every(([m,t])=>par(BigInt(m&w))===t)){U.add(u);V.add(v)}}let di=a.W.filter(w=>!U.has(w)),dj=b.W.filter(w=>!V.has(w));if(di.length||dj.length){for(let u of di)for(let v of b.W)if(legal([...a.F,...b.F],u+(v<<shift),K))throw Error("bad I");for(let v of dj)for(let u of a.W)if(legal([...a.F,...b.F],u+(v<<shift),K))throw Error("bad J");proof.push({type:"pair",i,j,di,dj});a.W=a.W.filter(w=>U.has(w));b.W=b.W.filter(w=>V.has(w));if(!a.W.length||!b.W.length){decision="NO";terminal={i,j};break outer}}}
 rounds.push({sweep,rowsBefore:prevRows,rowsAfter:rows(),rankBefore:prevRank,rankAfter:K.size});if(prevRows===rows()&&prevRank===K.size)break;
 }}catch(e){if(e.message!=="cap")throw e;capped=true}
 return {start,rows:rows(),rank:K.size,decision,capped,terminal,rounds,counts,events,proof,equations:[...K.values()].map(v=>v.toString(16)),remaining:R.map(r=>r.W)};
}
module.exports=closure;
