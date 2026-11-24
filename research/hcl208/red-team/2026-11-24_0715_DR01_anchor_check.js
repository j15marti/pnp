function anchored(){
 const pop=x=>{let n=0;for(;x;x&=x-1)n++;return n};
 function subs(m){let z=[];for(let s=m;;s=(s-1)&m){z.push(s);if(!s)return z}}
 function close(S,E){let p;do{p=S;for(const e of E)if(pop(S&e.m)>=2)S|=e.m}while(p!==S);return S}
 let results=[];
 for(let g of [5,7,9]){
 let n=2*g,E=Array.from({length:g},(_,i)=>({m:(1<<i)|(1<<((i+1)%g))|(1<<(g+i)),sign:(i%2?1<<i:0)|(i%3===0?1<<(g+i):0)}));
 function local(C){return subs(C).filter(a=>E.every(e=>{if((C&e.m)!==e.m)return true;let q=(a^e.sign)&e.m;return q!==0&&q!==e.m}))}
 let anchors=0,freeExtensions=0,both=0,maxClosure=0,cache=new Map();
 function get(C){if(!cache.has(C))cache.set(C,local(C));return cache.get(C)}
 for(let S=0;S<1<<n;S++){if(pop(S)>3)continue;let C=close(S,E);maxClosure=Math.max(maxClosure,pop(C));for(let a of get(C)){anchors++;for(let v=0;v<n;v++){let b=1<<v;if(C&b)continue;let D=close(S|b,E),labels=0;for(let t of get(D))if((t&C)===a)labels|=1<<((t&b)?1:0);freeExtensions++;if(labels!==3)throw Error("failed anchored two-value extension");both++;}}}
 results.push({g,n,anchors,freeExtensions,both,maxClosure});
 }
 return results;
}
console.log(JSON.stringify(anchored(),null,2));
