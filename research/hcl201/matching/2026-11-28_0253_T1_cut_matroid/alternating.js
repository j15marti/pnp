
function alternating(H,q){
 let F=flow(H,q),d=H.length,scans=0;if(F.val!==d)return {status:"BASE-NO",flow:F,scans};
 let M=Array(q).fill(-1);for(let [u,v,c,f] of F.arcs)if(u<d&&v>=d&&v<d+q&&f){assert(f===1&&M[v-d]===-1,"matching");M[v-d]=u}
 let U=[],rev=Array.from({length:q},()=>[]);for(let v=0;v<q;v++)if(M[v]<0)U.push(v);else for(let w of H[M[v]]){rev[w].push(v);scans++}
 let sets=Array.from({length:q},()=>[]),paths=[];
 for(let u of U){let seen=new Map([[u,-1]]),Q=[u];for(let i=0;i<Q.length;i++){let w=Q[i];for(let v of rev[w]){scans++;if(!seen.has(v)){seen.set(v,w);Q.push(v)}}}for(let v of Q)sets[v].push(u);paths.push([...seen])}
 let multi=sets.findIndex(x=>x.length>1),loops=sets.map((s,v)=>s.length===0?v:-1).filter(v=>v>=0),classes=U.map(u=>sets.map((s,v)=>s.length===1&&s[0]===u?v:-1).filter(v=>v>=0));
 return {status:multi<0?"EXACT-PAIR-QUOTIENT":"HIGHER-ORDER-NEEDED",k:U.length,loops,classes,sets,paths,M,U,scans,flow:F,multi}
}
function altVerify(H,q,R,D){
 assert(R.status==="EXACT-PAIR-QUOTIENT"&&approximate(R,D),"lift precondition");let deleted=new Set(D),match=R.M.slice(),used=new Set();
 for(let v of D){if(match[v]<0)continue;let u=R.sets[v][0],next=new Map(R.paths[R.U.indexOf(u)]),w=v;
 let seq=[w];while(w!==u){let b=next.get(w);assert(b!==undefined&&b>=0&&!seq.includes(b),"path");seq.push(b);w=b}
 for(let a of seq){assert(!used.has(a),"path intersection");used.add(a)}for(let i=seq.length-2;i>=0;i--){let a=seq[i],b=seq[i+1];assert(match[a]>=0&&H[match[a]].includes(b)&&match[b]===-1,"path reassignment");match[b]=match[a];match[a]=-1}
 }
 let demands=match.filter(x=>x>=0);assert(demands.length===H.length&&new Set(demands).size===H.length&&match.every((x,v)=>x<0||!deleted.has(v)&&H[x].includes(v)),"witness");return match
}
function altTest(){let counts={graphs:0,baseNO:0,exact:0,high:0,words:0,lifts:0},grow=[];function go(H,q){let A=alternating(H,q),R=recognize(H,q);counts.graphs++;assert(A.status===R.status,"status mismatch");if(A.status==="BASE-NO"){counts.baseNO++;return}if(A.status!=="EXACT-PAIR-QUOTIENT"){counts.high++;return}counts.exact++;for(let w=0;w<2**q;w++){let D=Array.from({length:q},(_,j)=>j).filter(j=>(w>>j)&1);counts.words++;let yes=approximate(A,D);assert(yes===indep(H,q,D),"exactness");if(yes){altVerify(H,q,A,D);counts.lifts++}}}
 for(let w=0;w<256;w++)go(Array.from({length:2},(_,i)=>Array.from({length:4},(_,j)=>j).filter(j=>(w>>(4*i+j))&1)),4);let seed=9317;for(let i=0;i<100;i++)go(Array.from({length:3},()=>Array.from({length:5},(_,j)=>j).filter(()=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return (seed>>>29)>=3})),5);
 for(let d of [4,8,16,32,64,128]){let H=Array.from({length:d},(_,i)=>[2*i,2*i+1]),q=2*d,A=alternating(H,q),D=Array.from({length:d},(_,i)=>2*i),m=altVerify(H,q,A,D);grow.push({d,q,k:A.k,flowScans:A.flow.scans,reachScans:A.scans,certificate:A,lift:m})}
 return {counts,grow}
}

// Load after pinned T1 check.js and cut-matroid.js; call altTest().
