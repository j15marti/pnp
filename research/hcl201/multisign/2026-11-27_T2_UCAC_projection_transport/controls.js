const control=function control(){
 function rank(A){let M=new Map(),xor=0;for(let v of A){while(v){let p=v.toString(2).length-1;if(!M.has(p)){M.set(p,v);break}v^=M.get(p);xor++}}return{rank:M.size,xor}}
 const wt=m=>m.toString(2).split("1").length-1;
 function evalRank(n,d,S){let ms=Array.from({length:2**n},(_,i)=>i).filter(m=>wt(m)<=d),A=S.map(x=>ms.reduce((a,m,i)=>(x&m)===m?a|(1n<<BigInt(i)):a,0n)),r=rank(A);return{features:ms.length,models:S.length,vanish:ms.length-r.rank,phi:r.rank+n,xors:r.xor}}
 let rechart=[];for(let d=1;d<=5;d++){let n=d+2,plane=Array.from({length:2**(n-1)},(_,i)=>i),graph=plane.map(i=>i===2**(n-1)-1?i+2**(n-1):i),p=evalRank(n,d,plane),g=evalRank(n,d,graph);if(g.phi-p.phi!==1)throw Error("rechart");rechart.push({d,n,plane:p,graph:g,creditIncrease:g.phi-p.phi})}
 // Cross-scope cancellation surviving projection: x+y and y+z imply x+z.
 // Rows in basis (x,y,z). Eliminate y first, retain x+z.
 const p=rank([3n,6n]),surviving=3n^6n;if(surviving!==5n||p.rank!==2)throw Error("transport");
 let satWords=[0,7],projected=[...new Set(satWords.map(w=>(w&1)|((w>>1)&2)))];if(JSON.stringify(projected)!=="[0,3]")throw Error("projection");
 // Opposite-label extension x!=z after the same cancellation.
 if(satWords.some(w=>((w&1)^((w>>2)&1))===1))throw Error("unsat");
 return{rechart,crossScope:{initialRank:p.rank,retainedRank:1,sourceModels:satWords,projectedModels:projected,unsatControl:"x+y=0,y+z=0,x+z=1"}}
};
console.log(JSON.stringify(control(),null,2));
