function quotient(C,R){
 let events=0;const hi=v=>1n<<BigInt(v.toString(2).length-1);
 function put(B,v){while(v){events++;let p=hi(v);if(B.has(p))v^=B.get(p);else{B.set(p,v);return true}}return false}
 function red(B,v){let a=0n;while(v){events++;let p=hi(v);if(B.has(p))v^=B.get(p);else{a^=p;v^=p}}return a}
 const A=new Map(),par=x=>{let p=0;while(x){x&=x-1;p^=1}return p},F=R.regions.map(r=>r.forms.map(([s,c])=>(BigInt("0x"+s)<<1n)|BigInt(c)));
 for(let e of C.affineReclosure.affine){let {i,m,p,row}=e;let v=BigInt(p);for(let j=0;j<F[i].length;j++)if(m>>j&1)v^=F[i][j];if(v!==BigInt("0x"+row)||!R.regions[i].allowed.every(w=>par(m&w)===p))throw Error("row check");if(!put(A,v&~1n))throw Error("dependent")}
 const B=F.map(r=>r.map(f=>f&~1n)),D=B.map(r=>r.map(f=>red(A,f)));
 function profile(M,order){let n=order.length,L=[],R=[],a=new Map(),b=new Map();for(let i=0;i<n;i++){M[order[i]].forEach(v=>put(a,v));M[order[n-1-i]].forEach(v=>put(b,v));L.push(a.size);R[n-1-i]=b.size}return {rank:a.size,cuts:L.slice(0,-1).map((v,i)=>v+R[i+1]-a.size)}}
 const order=B.map((_,i)=>i),p0=profile(B,order),p1=profile(D,order);
 if(p0.cuts.some((v,i)=>p1.cuts[i]>v))throw Error("cut increases");
 return {beforeRank:p0.rank,afterRank:p1.rank,maximumCutBefore:Math.max(...p0.cuts),maximumCutAfter:Math.max(...p1.cuts),strictlyImprovedCuts:p0.cuts.filter((v,i)=>p1.cuts[i]<v).length,totalCutBefore:p0.cuts.reduce((a,b)=>a+b,0),totalCutAfter:p1.cuts.reduce((a,b)=>a+b,0),events,profiles:[p0.cuts,p1.cuts]};
}
const fs=require("node:fs");console.log(JSON.stringify(quotient(JSON.parse(fs.readFileSync(process.argv[2],"utf8")),JSON.parse(fs.readFileSync(process.argv[3],"utf8")))));
