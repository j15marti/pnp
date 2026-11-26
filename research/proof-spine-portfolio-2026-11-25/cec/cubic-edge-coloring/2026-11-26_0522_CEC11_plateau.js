function audit(){
 const E=[[0,1],[0,4],[0,5],[1,2],[1,7],[2,3],[2,6],[3,6],[3,7],[4,5],[4,7],[5,6]],n=8, A=(x,m)=>{if(!x)throw Error(m)};
 let ms=[];function rec(v,m){if(!v.length){ms.push(m);return}let u=v[0];for(let i=0;i<E.length;i++)if(E[i].includes(u)){let w=E[i].find(x=>x!==u);if(v.includes(w))rec(v.filter(x=>x!==u&&x!==w),[...m,i])}}rec([...Array(n).keys()],[]);
 function odd(m){let v=new Set([...Array(n).keys()]),o=0;while(v.size){let q=[[...v][0]];v.delete(q[0]);for(let i=0;i<q.length;i++)E.forEach((e,j)=>{if(!m.includes(j)&&e.includes(q[i])){let w=e.find(x=>x!==q[i]);if(v.delete(w))q.push(w)}});o+=q.length%2}return o}
 function D(x){return E.map(([u,v],j)=>(x>>u&1)===(x>>v&1)?j:-1).filter(j=>j>=0)}function cost(x,m){return D(x).filter(j=>!m.includes(j)).length}
 let m0=ms.find(m=>m.map(j=>E[j].join("")).sort().join(",")==="01,23,47,56"),m1=ms.find(m=>m.map(j=>E[j].join("")).sort().join(",")==="04,17,23,56");
 A(m0&&m1&&odd(m0)===2&&odd(m1)===0,"matches");
 let c15=ms.map(m=>cost(15,m)),c29=ms.map(m=>cost(29,m));
 A(cost(15,m0)===2&&Math.min(...c15)===2&&c15.filter(x=>x===2).length===1&&cost(29,m0)===2&&cost(29,m1)===0,"plateau and tie escape");
 for(const m of ms)A(Math.min(...Array.from({length:128},(_,x)=>cost(x,m)))===odd(m),"oddness minimization");
 return {E,matchings:ms.map(m=>({edges:m.map(i=>E[i]),oddCycles:odd(m),cost15:cost(15,m),cost29:cost(29,m)})),cut15:D(15).map(i=>E[i]),cut29:D(29).map(i=>E[i]),initial:m0.map(i=>E[i]),escape:m1.map(i=>E[i]),exactComparisons:ms.length*128};
}
console.log(JSON.stringify(audit(),null,2));
