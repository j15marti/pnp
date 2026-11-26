function audit(){
 let checks=0, seed=26112605; const rnd=()=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed/4294967296};
 const ok=x=>{checks++;if(!x)throw Error("assertion "+checks)};
 const A=[0,3,6,9,12,15],bit=(w,p)=>(w>>[3,2,1,0][p])&1;
 function geom(k){let faces=[],edges=[];for(let i=0;i<k;i++)for(let j=0;j<k;j++){let v=i*k+j;if(j+1<k)edges.push([v,v+1,1,3,0]);if(i+1<k)edges.push([v,v+k,2,0,1]);if(i+1<k&&j+1<k&&(i+j)%2===0)faces.push([v,v+1,v+k,v+k+1]);}
 let map=new Map;for(let f=0;f<faces.length;f++){let [a,b,c,d]=faces[f];for(let [u,v] of [[a,b],[a,c],[b,d],[c,d]]){let key=u*k*k+v;ok(!map.has(key));map.set(key,f)}}
 for(let e of edges)e.push(map.get(e[0]*k*k+e[1])??-1);return {k,faces,edges}}
 function labels(g,z){let a=Array(g.k*g.k).fill(0);for(let f=0;f<g.faces.length;f++)if(z[f]){let [u,v,w,x]=g.faces[f];a[u]|=6;a[v]|=3;a[w]|=12;a[x]|=9}return a}
 function chart(g,a,d,guard=[]){let k=g.k;for(let i=0;i<k;i++)for(let j=0;j<k;j++){let w=a[i*k+j];if(d===0&&((j===0&&bit(w,3))||(j===k-1&&bit(w,1))))return false;if(d===1&&((i===0&&bit(w,0))||(i===k-1&&bit(w,2))))return false}
 for(let [u,v,p,q,dir] of g.edges)if(dir===d&&bit(a[u],p)!==bit(a[v],q))return false;
 for(let [u,p,b] of guard)if((p%2===1?0:1)===d&&bit(a[u],p)!==b)return false;return true}
 // Independent two-state line automaton; accepts only singleton label per input cell.
 function line(g,a,d){let k=g.k;for(let l=0;l<k;l++){let st=0;for(let j=0;j<k;j++){let w=a[d===0?l*k+j:j*k+l];if(bit(w,d===0?3:0)!==st)return false;st=bit(w,d===0?1:2)}if(st!==0)return false}return true}
 function maskgrid(g,a){let k=g.k,n=k+2,m=[];for(let i=0;i<n;i++)for(let j=0;j<n;j++){let words;if(i>0&&j>0&&i<n-1&&j<n-1)words=[a[(i-1)*k+j-1],...((i+j)%2===0?[1,4,5]:[2,8,10])];else {let pins=i===0?(j===0?[[0,0],[3,0]]:j===n-1?[[0,0],[1,0]]:[[0,0],[2,0]]):i===n-1?(j===0?[[2,1],[3,0]]:j===n-1?[[2,1],[1,0]]:[[0,0],[2,1]]):[[1,0],[3,0]];words=Array.from({length:16},(_,w)=>w).filter(w=>pins.every(([p,b])=>bit(w,p)===b))}
 ok(new Set(words).size===4);m.push(words)}return m}
 function native(g,a){let n=g.k+2,m=maskgrid(g,a),states=new Set([0]);for(let i=0;i<n;i++){let next=new Set;for(let top of states){function visit(j,w,s){if(j===n){next.add(s);return}for(let x of m[i*n+j])if(bit(x,0)===((top>>j)&1)&&bit(x,3)===w)visit(j+1,bit(x,1),s|(bit(x,2)<<j))}visit(0,0,0);visit(0,1,0)}states=next}return states.has((1<<n)-1)}
 function cutset(g,S,d){return [...new Set(g.edges.filter(e=>e[4]===d&&e[5]>=0&&S[e[0]]!==S[e[1]]).map(e=>e[5]))]}
 function merge(a,b,S){return a.map((w,i)=>S[i]?w:b[i])}
 let out={seed:26112605,exhaustiveBalancedCuts:0,identityEntries:0,nativeComparisons:0,neighborPairs:0,guardedComparisons:0,scales:[]};
 for(let k of [2,3,4,8,36,64,128]){
 let g=geom(k),min=Infinity,minProduct=Infinity,cuts=0;
 for(let t=0;t<(k===3?512:k===4?128:40);t++){
 let S=Array.from({length:k*k},(_,i)=>k===3?Boolean((t>>i)&1):t===0?i%k<Math.floor(k/2):t===1?Math.floor(i/k)<Math.floor(k/2):rnd()<0.5),cnt=S.filter(Boolean).length;if(cnt<k*k/3||cnt>2*k*k/3)continue;
 cuts++;if(k===3)out.exhaustiveBalancedCuts++;
 let h=cutset(g,S,0),v=cutset(g,S,1),q=new Set([...h,...v]).size;min=Math.min(min,q);minProduct=Math.min(minProduct,h.length+v.length);
 if(k>=36)ok(q>=Math.ceil((k-2)/16));
 for(let d of [0,1]){let C=d===0?h:v;
 let codes=C.length<=5?Array.from({length:1<<C.length},(_,x)=>C.map((_,i)=>(x>>i)&1)):Array.from({length:4},()=>C.map(()=>rnd()<0.5?1:0));
 let labs=codes.map(c=>{let z=Array(g.faces.length).fill(0);C.forEach((f,i)=>z[f]=c[i]);return labels(g,z)});
 for(let i=0;i<labs.length;i++)for(let j=0;j<labs.length;j++){let a=merge(labs[i],labs[j],S);ok(chart(g,a,d)===codes[i].every((b,l)=>b===codes[j][l]));out.identityEntries++}
 }
 }
 for(let t=0;t<16;t++){let z=g.faces.map(()=>rnd()<.5?1:0),a=labels(g,z);ok(a.every(w=>A.includes(w)));ok(chart(g,a,0)&&chart(g,a,1));let b=a.slice(),i=Math.floor(rnd()*b.length);b[i]=A.find(w=>w!==b[i]);ok(!(chart(g,b,0)&&chart(g,b,1)));for(let x of [a,b]){for(let d of [0,1])ok(chart(g,x,d)===line(g,x,d));if(k<=3){ok(native(g,x)===(chart(g,x,0)&&chart(g,x,1)));out.nativeComparisons++}}out.neighborPairs++;
 let e=g.edges[Math.floor(rnd()*g.edges.length)],p=e[2],u=e[0],val=bit(a[u],p);for(let x of [val,1-val]){ok((chart(g,a,0,[[u,p,x]])&&chart(g,a,1,[[u,p,x]]))===(x===val));out.guardedComparisons++}
 }
 out.scales.push({k,faces:g.faces.length,cuts,minUnion:min,minDirectionalSum:minProduct})
 }
 return {...out,checks};
}
console.log(JSON.stringify(audit(),null,2));
