/* P4SW07 weighted same-parity ternary matching gadget audit. Node.js 18+. */
function audit(){
 const assert=(x,m)=>{if(!x)throw Error(m)},pop=x=>{let n=0;while(x){x&=x-1;n++}return n};let seed=261126;function rnd(n){seed=(Math.imul(1664525,seed)+1013904223)>>>0;return seed%n}
 function gadget(table,parity){
  let t=parity?Array.from({length:8},(_,m)=>table[m^7]):table.slice(),e=[],ports=[0,1,2],n=4;
  if(t.every(x=>x===null))return null;
  let pair=[3,5,6].filter(x=>t[x]!==null);
  if(!pair.length){assert(t[0]!==null,"only zero");n=6;for(let i=0;i<3;i++)e.push([i,i+3,i===0?t[0]:0])}
  else {for(let m of pair){let j=[0,1,2].find(i=>!(m>>i&1));e.push([j,3,t[m]])}if(t[0]!==null){let m=pair[0],ij=[0,1,2].filter(i=>m>>i&1);e.push([ij[0],ij[1],t[0]-t[m]])}}
  if(parity){ports=ports.map(i=>{let j=n++;e.push([i,j,0]);return j})}return{n,e,ports}
 }
 function minmatch(g,mask){if(!g)return null;let left=(1<<g.n)-1;for(let i=0;i<3;i++)if(mask>>i&1)left&=~(1<<g.ports[i]);function go(S){if(!S)return 0;let i=Math.floor(Math.log2(S&-S)),z=null;for(let [a,b,w] of g.e){let j=a===i?b:b===i?a:-1;if(j>=0&&(S>>j&1)){let x=go(S^(1<<i)^(1<<j));if(x!==null&&(z===null||z>x+w))z=x+w}}return z}return go(left)}
 let jobs=0,comparisons=0,negative=0,maxVertices=0;for(let p=0;p<2;p++){let words=Array.from({length:8},(_,i)=>i).filter(i=>pop(i)%2===p);for(let mask=0;mask<16;mask++)for(let r=0;r<16;r++){let t=Array(8).fill(null);words.forEach((m,i)=>{if(mask>>i&1)t[m]=rnd(31)-10});let g=gadget(t,p);jobs++;if(g){maxVertices=Math.max(maxVertices,g.n);negative+=Number(g.e.some(e=>e[2]<0))}for(let m=0;m<8;m++){assert(minmatch(g,m)===t[m],"matching table mismatch");comparisons++}}}
 return{jobs,comparisons,negative_weight_gadgets:negative,maxVertices,limits:"Exhaustive support masks; 16 deterministic signed weight assignments each. Constant gadget verification by exact enumeration, not production blossom implementation. Global two-occurrence incidence condition required."}
}
console.log(JSON.stringify(audit(),null,2));
