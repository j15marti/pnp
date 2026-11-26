function liftAudit(){
 const F=[[1,2,3],[1,4,5],[2,4,6],[3,5,6],[-1,-2,-4],[-1,-3,-6],[-2,-3,-5],[-4,-5,-6]],D=[1,5],S=[2,3,4,6];
 const W=[[0,7,10,13,15,3],[0,7,11,13,14,3],[0,8,10,12,15,3],[4,2,8,1,17,19],[4,2,9,1,17,18],[4,6,9,10,1,3],[5,2,8,1,16,19]];
 const e=[];for(let v of D)for(let s of [1,-1]){let a=F.flatMap((c,i)=>c.includes(v*s)?[i]:[]);e.push({a:a[0],b:a[1],v,s})}for(let [i,c] of F.entries())for(let l of c){let v=Math.abs(l);if(S.includes(v))e.push({a:i,b:8+S.indexOf(v),v,s:Math.sign(l)})}
 let checks=0;function A(x,m){checks++;if(!x)throw Error(m)}function connected(n,edges){let a=Array.from({length:n},()=>[]);for(let [u,v] of edges){a[u].push(v);a[v].push(u)}let q=[0],seen=new Set(q);for(let i=0;i<q.length;i++)for(let v of a[q[i]])if(!seen.has(v)){seen.add(v);q.push(v)}return seen.size===n}
 const shifted=4;A(e[shifted].a===0&&e[shifted].v===2,"shift identity");A(connected(12,e.filter((_,i)=>i!==shifted).map(x=>[x.a,x.b])),"base minus shift connected");
 A(new Set(W.flat()).size===e.length,"all edges supported");
 let results=[];
 for(let k of [1,2,3,5,10,25,50,100]){
 let source=[],edges=[],cov=new Set();for(let t=0;t<k;t++)for(let [i,c] of F.entries())source.push(c.map(l=>Math.sign(l)*(Math.abs(l)+6*((i===0&&l===2?(t+1)%k:t)))));
 for(let t=0;t<k;t++)for(let [i,x] of e.entries())edges.push({a:12*t+x.a,b:12*(i===shifted?(t+1)%k:t)+x.b,v:x.v+6*(i===shifted?(t+1)%k:t),s:x.s});
 A(connected(12*k,edges.map(x=>[x.a,x.b])),"connected");
 let counts=Array.from({length:6*k},()=>[0,0]),seen=new Set();for(let c of source){A(c.length===3&&new Set(c.map(Math.abs)).size===3&&c.every(l=>Math.sign(l)===Math.sign(c[0])),"grammar");let key=c.slice().sort((a,b)=>a-b).join();A(!seen.has(key),"unique");seen.add(key);for(let l of c)counts[Math.abs(l)-1][+(l>0)]++}A(counts.every(c=>c[0]===2&&c[1]===2),"exact22");
 for(let w of W){let hit=Array(12*k).fill(0),pairCount=Array(2*k).fill(0),sign={};for(let t=0;t<k;t++)for(let i of w){let j=20*t+i,x=edges[j];cov.add(j);hit[x.a]++;hit[x.b]++;if(i<4)pairCount[2*t+Math.floor(i/2)]++;A(sign[x.v]===undefined||sign[x.v]===x.s,"sign");sign[x.v]=x.s;let ca=source[8*Math.floor(x.a/12)+x.a%12];A(ca.includes(x.v*x.s),"edge source a");if(i<4){let cb=source[8*Math.floor(x.b/12)+x.b%12];A(cb.includes(x.v*x.s),"edge source b")}}
 A(hit.every(x=>x===1)&&pairCount.every(x=>x===1),"matching and labels");A(source.every(c=>c.some(l=>sign[Math.abs(l)]===Math.sign(l))),"SAT witness")}
 A(cov.size===edges.length,"all lift edges supported");let deg=Array(12*k).fill(0);for(let x of edges){deg[x.a]++;deg[x.b]++}let c=0,s=0;for(let i=0;i<deg.length;i++){if(i%12<8){A(deg[i]===3,"clause degree");c++}else{A(deg[i]===4,"singleton degree");s++}}
 results.push({k,n:6*k,clauses:8*k,edges:20*k,clauseAmbiguous:c,singletonAmbiguous:s,b:Math.min(c,s),connected:true,allEdgesCovered:true,witnesses:W.length})
 }
 return {base:{F,D,S,shifted,e,witnesses:W},results,checks}
}
console.log(JSON.stringify(liftAudit(),null,2));
