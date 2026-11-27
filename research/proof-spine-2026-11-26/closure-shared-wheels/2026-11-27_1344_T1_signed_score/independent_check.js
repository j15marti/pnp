function exactNegativeControls(){
 const out=[];
 // independent integer certificates of the all-even signed Fano chains
 for(const r of [1,2,4,5,8,16,32,64]){
 let C=[];for(let j=0;j<r;j++)for(let i=0;i<7;i++)C.push([7*j+i+1,7*j+(i+1)%7+1,7*j+(i+3)%7+1]);for(let j=0;j<r-1;j++){let a=7*j+1,b=7*(j+1);[C[a][0],C[b][0]]=[C[b][0],C[a][0]]}C=C.map(a=>a.map(v=>v%3===1?-v:v));
 let I=new Map(),local=0;for(let c of C){for(let l of c)I.set(l,(I.get(l)||0)+1);for(let w=0;w<8;w++){let count=0;for(let j=0;j<3;j++){let x=w>>j&1,v=x-Number(c[j]<0);count+=v*v}if(count>0&&count%2===0&&count!==2)throw Error("wrong score transfer");local++}}
 if(I.size!==7*r||[...I.values()].some(x=>x!==3)||2*C.length%3===0)throw Error("bad certificate");
 out.push({r,clauses:C.length,localTruthChecks:local,distinctSignedVariables:I.size,leftDivisibleBy3:true,right:2*C.length,rightResidue:2*C.length%3,refuted:true})
 }
 const C=[[1,2],[1,-2],[-1,2],[-1,-2]],m=4,M=6,mod=x=>(x%M+M)%M,enc=a=>a.reduce((z,x,i)=>z+mod(x)*M**i,0),dec=z=>Array.from({length:m},(_,i)=>Math.floor(z/M**i)%M),add=(a,b)=>enc(dec(a).map((x,i)=>x+dec(b)[i]));let B=C.map(c=>c.filter(x=>x<0).length),S=[1,2].map(v=>[0,enc(C.map(c=>c.reduce((z,l)=>z+(Math.abs(l)===v?(l>0?1:-1):0),0)))]);for(let i=0;i<m;i++)S.push([enc(C.map((_,j)=>i===j?-1:0)),enc(C.map((_,j)=>i===j?-2:0))]);let A=new Set([0]),work=0;for(let V of S){let X=new Set();for(let x of A)for(let y of V){X.add(add(x,y));work++}A=X}let target=enc(B.map(x=>-x));if(A.has(target)||Array.from({length:4},(_,w)=>w).some(w=>C.every(c=>c.some(l=>!!(w&1<<(Math.abs(l)-1))===(l>0)))))throw Error("CRT false");
 return {conservation:out,crtNegative:{clauses:C,attained:A.size,target,transitions:work,NO:true},localTruthChecks:out.reduce((s,x)=>s+x.localTruthChecks,0)}
}
console.log(JSON.stringify(exactNegativeControls(),null,2));
