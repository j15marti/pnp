const experiment=function experiment(){
 // Scope: F2^d; rows [integer bit mask, RHS]; d<=8 in this audit. Empty guards are allowed.
 const parity=x=>{let p=0;while(x){p^=1;x&=x-1}return p};
 function rank(rows,d){let B=new Map();for(let [a,b] of rows){while(a){let i=31-Math.clz32(a);if(!B.has(i)){B.set(i,[a,b]);break}let r=B.get(i);a^=r[0];b^=r[1]}if(!a&&b)return -1}return B.size}
 function solve(d,G){let queries=0,intersections=0;function count(extra=[]){queries++;let s=0;for(let m=0;m<2**G.length;m++){let R=extra.slice(),p=0;for(let i=0;i<G.length;i++)if(m&(1<<i)){p^=1;R.push(...G[i])}let r=rank(R,d);intersections++;if(r>=0)s+=(p?-1:1)*2**(d-r)}return s}
 let size=count();if(!size)return {size,eq:[],queries,intersections};let p=0,fix=[];for(let i=0;i<d;i++){let a=1<<i;if(count(fix.concat([[a,0]]))>0)fix.push([a,0]);else{fix.push([a,1]);p|=a}}
 let basis=[];for(let g of G){if(rank(g,d)<0)continue;let v=g.find(([a,b])=>parity(a&p)!==b);if(!v)throw Error("bad point");basis.push(v[0])}
 let normals=new Set([0]);for(let a of basis)for(let b of [...normals])normals.add(a^b);
 let eq=[];for(let a of normals)if(a){let b=parity(a&p);if(count([[a,1-b]])===0)eq.push([a,b])}
 return {size,eq,queries,intersections}
 }
 let seed=20261127;function rand(){seed^=seed<<13;seed^=seed>>>17;seed^=seed<<5;return seed>>>0}
 let total=0,queries=0,intersections=0,empty=0,nonempty=0,rankTight=0,nontrivial=0,fullHull=0,maxGuards=0,assignmentChecks=0,normalChecks=0;
 function test(d,G){let r=solve(d,G),S=[];for(let p=0;p<2**d;p++){assignmentChecks++;if(!G.some(g=>g.every(([a,b])=>parity(a&p)===b)))S.push(p)}if(r.size!==S.length)throw Error("count mismatch");let E=[];if(S.length)for(let a=1;a<2**d;a++){normalChecks++;let b=parity(a&S[0]);if(S.every(p=>parity(a&p)===b))E.push([a,b])}let key=x=>x.map(y=>y.join(",")).sort().join(";");if(key(E)!==key(r.eq))throw Error("hull mismatch");if(S.length){nonempty++;let rr=rank(E,d);if(rr>G.length)throw Error("rank bound");if(rr===G.length)rankTight++;if(rr>0)nontrivial++;else fullHull++}else empty++;total++;queries+=r.queries;intersections+=r.intersections;maxGuards=Math.max(maxGuards,G.length)}
 for(let d=1;d<=8;d++)for(let i=0;i<100;i++){let k=rand()%6,G=Array.from({length:k},()=>Array.from({length:1+rand()%(d+1)},()=>[rand()%(2**d),rand()&1]));test(d,G)}
 for(let d=1;d<=5;d++){test(d,Array.from({length:d},(_,i)=>[[1<<i,1]]));test(d,[[[1,0]],[[1,1]]]);}
 return {seed:20261127,total,queries,intersections,empty,nonempty,rankTight,nontrivial,fullHull,maxGuards,assignmentChecks,normalChecks};
};
console.log(JSON.stringify(experiment(),null,2));
