// Additional parity controls for rank-backdoor experiment.
function extra(){
 const check=(v,m)=>{if(!v)throw Error(m)};
 function count(n,E,c,deleted=-1){const clauses=[];for(let i=0;i<E.length;i++){const [u,v]=E[i];for(let q=0;q<2;q++)for(let s=0;s<2;s++)clauses.push([u,v,n+i, s,s^(1^c[i]),s^q]);}
 let z=0;for(let x=0;x<(1<<(n+E.length));x++)if(clauses.every((a,j)=>j===deleted||a.slice(0,3).some((p,i)=>((x>>p)&1)!==a[3+i])))z++;return z}
 let checks=0;for(let n=3;n<=7;n++){const E=Array.from({length:n},(_,i)=>[i,(i+1)%n]),c=Array(n).fill(0);c[0]=1;check(count(n,E,c)===0,"odd charge");for(let j=0;j<4*n;j++){check(count(n,E,c,j)===2**(n-1),"single clause");checks++}}
 const E=[[0,1],[1,2],[2,0],[3,4]],n=5,c=Array(4).fill(0);check(count(n,E,c)===2**(4+2),"two components");c[0]=1;check(count(n,E,c)===0,"unbalanced component");
 return {singleCNFClauseDeletionNeighbors:checks,disconnectedControls:2};
}
console.log(JSON.stringify(extra()));
