
function pairPass(X,maxPairs=40,cap=300000){
 let D=X.dict.map(b=>b.S.map(([y,w])=>({y:BigInt("0x"+y),w}))),b=BigInt("0x"+X.target),n=D.length,owners=new Map(),pairs=new Map(),events=0;
 for(let i=0;i<n;i++){let u=D[i].reduce((v,s)=>v|s.y,0n);while(u){let k=u&-u;u^=k;if(!owners.has(k))owners.set(k,[]);owners.get(k).push(i)}}
 for(let a of owners.values())for(let i=0;i<a.length;i++)for(let j=i+1;j<a.length;j++){let k=a[i]+","+a[j];pairs.set(k,(pairs.get(k)||0)+1);events++}
 let lex=[...pairs.keys()].map(k=>k.split(",").map(Number)).sort((a,b)=>a[0]-b[0]||a[1]-b[1]),pos=new Map(X.sp.map((x,i)=>[x,i]));
 let spectral=lex.slice().sort((a,b)=>Math.abs(pos.get(a[0])-pos.get(a[1]))-Math.abs(pos.get(b[0])-pos.get(b[1]))||a[0]-b[0]||a[1]-b[1]);
 let overlap=lex.slice().sort((a,b)=>pairs.get(b.join(","))-pairs.get(a.join(","))||a[0]-b[0]||a[1]-b[1]);
 // Use independent arms. No unverified deletion imported between them.
 function arm(name,order){let C=D.map(s=>s.slice()),counts={tests:0,xors:0,queries:0,attempted:0},drops=[],completed=0,status="PAIR-CAP";
 function add(B,x){while(x){counts.tests++;let k=x&-x;if(!B.has(k)){B.set(k,x);return}x^=B.get(k);counts.xors++}}
 function mem(B,x){while(x){counts.tests++;let k=x&-x;if(!B.has(k))return false;x^=B.get(k);counts.xors++}return true}
 for(let [i,j] of order.slice(0,maxPairs)){if(counts.tests>=cap){status="EVENT-CAP";break}counts.attempted++;let B=new Map(),t=b;
 for(let k=0;k<n;k++)if(k!==i&&k!==j){let a=C[k][0].y;t^=a;for(let v of C[k])add(B,v.y^a)}
 let L=new Set(),R=new Set();for(let a of C[i])for(let b of C[j]){counts.queries++;if(mem(B,t^a.y^b.y)){L.add(a);R.add(b)}}
 if(counts.tests>cap){status="EVENT-CAP";break}completed++;if(!L.size){status="EMPTY-PAIR";drops.push({i,j,empty:true,exteriorRank:B.size});break}
 let lostL=C[i].filter(x=>!L.has(x)),lostR=C[j].filter(x=>!R.has(x));if(lostL.length||lostR.length){drops.push({i,j,exteriorRank:B.size,lostL:lostL.map(x=>x.y.toString(16)),lostR:lostR.map(x=>x.y.toString(16))});C[i]=[...L];C[j]=[...R]}
 }let old=D.reduce((a,s)=>a+s.length,0),remaining=C.reduce((a,s)=>a+s.length,0);
 return {name,status,completed,old,remaining,drops,counts}}
 return {candidateCount:pairs.size,events,maxPairs,cap,arms:[arm("lex",lex),arm("spectral-neighbor",spectral),arm("shared-coordinate-overlap",overlap)]}
}
