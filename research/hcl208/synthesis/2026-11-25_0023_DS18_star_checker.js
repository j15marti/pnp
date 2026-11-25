function starTest(){
let checks=0;const check=(x,msg)=>{checks++;if(!x)throw Error(msg)};let seed=173;
const rnd=n=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return (seed>>>8)%n};
let cases=[];for(let t=0;t<82;t++){
 let n=4,C=[];if(t===0)C=[[1],[-1]];else if(t===1)C=[[1,2,3]];else for(let i=0;i<3+rnd(9);i++){let v=[];while(v.length<3){let a=1+rnd(n);if(!v.some(z=>Math.abs(z)===a))v.push(rnd(2)?a:-a)}C.push(v);}
 let E=C.concat([[n+1],[n+2],[n+3]]),q=n+3;
 const sat=(c,x)=>c.some(l=>!!(x&(1<<(Math.abs(l)-1)))===(l>0));
 let orig=0,missing=0;for(let x=0;x<(1<<q);x++){if(x<(1<<n)&&C.every(c=>sat(c,x)))orig++;if(E.every(c=>sat(c,x)))missing++;}
 check(orig===missing,"SAT lift count");
 let R=Array.from({length:q},(_,i)=>[0,1].map(b=>E.map((c,j)=>[c,j]).filter(([c])=>!c.some(l=>Math.abs(l)===i+1&&b===+(l>0))).map(([,j])=>j)));
 // Every center row has support in each leaf; every two leaf assignments have common center.
 for(let i=0;i<q;i++){for(let j=0;j<E.length;j++)check(R[i].some(a=>a.includes(j)),"center AC");for(let b=0;b<2;b++){check(R[i][b].length>0,"leaf AC");for(let k=i+1;k<q;k++)for(let z=0;z<2;z++)check(R[i][b].some(j=>R[k][z].includes(j)),"pair PC");}}
 let zero=0;for(let x=0;x<(1<<q);x++){let a=E.map((_,j)=>j).filter(j=>R.every((r,i)=>r[(x>>i)&1].includes(j)));if(!a.length)zero++;check(!a.length===E.every(c=>sat(c,x)),"projection identity");}
 check(zero===orig,"no-fill equivalence");cases.push({clauses:C,sourceModels:orig,unsafeAssignments:zero,centerRows:E.length,safe:zero===0});
}
return {checks,cases,safe:cases.filter(c=>c.safe).length,unsafe:cases.filter(c=>!c.safe).length};
}
console.log(JSON.stringify(starTest(),null,2));
