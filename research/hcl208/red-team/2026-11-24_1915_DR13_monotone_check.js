function check(){
 const fano=[[1,2,3],[1,4,5],[1,6,7],[2,4,6],[2,5,7],[3,4,7],[3,5,6]];
 const val=(x,l)=>((x>>(Math.abs(l)-1))&1)^(l<0?1:0);
 const sat=(x,C)=>C.every(c=>{const a=val(x,c[0]),b=val(x,c[1]),d=val(x,c[2]);return a!==b||b!==d});
 const eq=[0,0];for(let x=0;x<128;x++)if(sat(x,fano.slice(1))){if(val(x,1)!==val(x,2)||val(x,1)!==val(x,3))throw Error("equality");eq[val(x,1)]++}
 if(eq[0]!==5||eq[1]!==5)throw Error("weight");
 const C=[[2,-3,-4],[-4,2,1],[-4,-3,1],[3,-4,1]];
 let n=4;const M=[],neg=new Map();
 function positive(l){if(l>0)return l;const p=-l;if(neg.has(p))return neg.get(p);
  const v=++n,q=++n,w=++n,aux=[++n,++n,++n,++n];neg.set(p,v);const map=[0,p,q,w,...aux];
  for(const c of fano.slice(1))M.push(c.map(i=>map[i]));
  M.push([p,q,v]);return v
 }
 const mapped=C.map(c=>c.map(positive));M.push(...mapped);
 const F=M.map(c=>c.slice());F[F.length-1][0]*=-1;
 let a=0,b=0,delta=0;for(let x=0;x<2**n;x++){const h=sat(x,M),j=sat(x,F);if(h&&!j)throw Error("non-nested");a+=Number(h);b+=Number(j);delta+=Number(j&&!h)}
 if(a!==150||b!==200||delta!==50)throw Error("count");
 return {gadgetCountsPerColor:eq,variables:n,owners:M.length,complementGadgets:neg.size,fullWords:2**n,rootCount:a,flipCount:b,difference:delta,root:M,neighbor:F}
}
console.log(JSON.stringify(check(),null,2));
