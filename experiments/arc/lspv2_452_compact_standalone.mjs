// LSPV-2/452. Standalone graph-incidence gauge-orbit test, no dependencies.
import assert from 'node:assert/strict';
function test(name,n,edgeList,removed,charge){
  let E=edgeList.map(e=>e.slice().sort((a,b)=>a-b)).sort((a,b)=>a[0]-b[0]||a[1]-b[1]);
  let deg=Array(n).fill(0);for(let [u,v] of E){deg[u]++;deg[v]++}
  assert(deg.every(x=>x===3));
  let omit=new Set(removed),adj=Array.from({length:n},()=>[]);
  E.forEach(([u,v],j)=>{if(!omit.has(j)){adj[u].push(v);adj[v].push(u)}});
  let id=Array(n).fill(-1),groups=[],types=[];
  for(let i=0;i<n;i++)if(id[i]<0){let c=groups.length,stack=[i],vv=[],d=0;id[i]=c;
    while(stack.length){let v=stack.pop();vv.push(v);d+=adj[v].length;
      for(let w of adj[v])if(id[w]<0){id[w]=c;stack.push(w)}}
    groups.push(vv);types.push(d/2===vv.length-1?'tree':'cyclic');
  }
  let r=types.filter(x=>x==='tree').length,b=types.filter(x=>x==='cyclic').length,k=removed.length;
  assert(b>=1 && k<=n/2);
  let hist=new Map(),open=0;
  for(let mask=0;mask<2**k;mask++){
    let val=Array(n).fill(0);val[0]=charge;
    removed.forEach((e,j)=>{if((mask>>j)&1){let [u,v]=E[e];val[u]^=1;val[v]^=1}});
    let syndrome=groups.map(g=>g.reduce((x,v)=>x^val[v],0));
    if(types.every((t,i)=>t!=='tree'||syndrome[i]===0)){
      let key=syndrome.join('');hist.set(key,(hist.get(key)||0)+1);open++;
    }
  }
  assert.equal(open,2**(k-r));assert.equal(hist.size,2**(b-1));
  for(let v of hist.values())assert.equal(v,2**(k-r-b+1));
  assert.equal([...hist.keys()].filter(x=>!x.includes('1')).length,charge?0:1);
  return {graph:name,charge,open,orbits:hist.size};
}
function K4(){let e=[];for(let i=0;i<4;i++)for(let j=i+1;j<4;j++)e.push([i,j]);return e}
function cube(){let e=[];for(let i=0;i<8;i++)for(let j=0;j<3;j++)if(i<(i^(1<<j)))e.push([i,i^(1<<j)]);return e}
function petersen(){let e=[];for(let i=0;i<5;i++){e.push([i,(i+1)%5],[5+i,5+(i+2)%5],[i,5+i])}return e}
function prism(n){let e=[];for(let i=0;i<n;i++)e.push([i,(i+1)%n],[n+i,n+(i+1)%n],[i,n+i]);return e}
let fixtures=[['K4',4,K4(),[0,1]],['cube',8,cube(),[0,1,2]],['Petersen',10,petersen(),[0,1,2,3]],['prism16',16,prism(8),[0,1,2,3,4]]];
let out=[];for(let [name,n,E,S] of fixtures)for(let c of [0,1])out.push(test(name,n,E,S,c));
console.log(JSON.stringify({cases:out.length,passed:true,results:out}));
