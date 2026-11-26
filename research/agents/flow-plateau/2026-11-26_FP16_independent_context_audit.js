'use strict';
// Independent 6-port audit: bit masks, explicit alternating simple paths,
// not the Python partial-transition matching enumeration or blossom solver.
const V=[0,1,2,3,4,5], E=[];
for(let i=0;i<6;i++)for(let j=i+1;j<6;j++)E.push([i,j]);
const eid=(a,b)=>E.findIndex(([x,y])=>x===Math.min(a,b)&&y===Math.max(a,b));
function partial(v){if(!v.length)return [0];let [a,...tail]=v;let out=partial(tail);for(let b of tail)for(let w of partial(tail.filter(x=>x!==b)))out.push(w|(1<<eid(a,b)));return out;}
const pop=x=>{let c=0;while(x){x&=x-1;c++}return c};
const P=partial(V).filter(w=>pop(w)===3);
function path(U,C,i,j){
  function go(v,seen){for(let w of V){if((seen>>w)&1 || v===w || !(U&(1<<eid(v,w))))continue;if(w===j)return true;
    for(let z of V)if(z!==w&&!(seen&(1<<z))&&(C&(1<<eid(w,z)))&&go(z,seen|(1<<w)|(1<<z)))return true;
  }return false;}
  return go(i,1<<i);
}
const ctx=[];for(let i=0;i<6;i++)for(let j=i+1;j<6;j++)for(let C of partial(V.filter(v=>v!==i&&v!==j))){let lm=0;for(let k=0;k<P.length;k++)if(path(P[k],C,i,j))lm|=1<<k;ctx.push({i,j,C,lm});}
function multipart(U){for(let a of V)for(let b of V)for(let c of V)if(a!==b&&b!==c&&a!==c&&!(U&(1<<eid(a,b)))&&!(U&(1<<eid(b,c)))&&(U&(1<<eid(a,c))))return false;return true;}
function order3(U){function go(xs,used){if(xs.length===3)return true;for(let x of V)if(!(used&(1<<x)))for(let y of V)if(y!==x&&!(used&(1<<y))&&(U&(1<<eid(x,y)))&&xs.every(q=>!(U&(1<<eid(q,y))))&&go([...xs,x],used|(1<<x)|(1<<y)))return true;return false;}return go([],0);}
const cache=new Map();let multipartN=0,multipartSafe=0,multiUnions=0,boundedN=0,boundedSafe=0,nonMultiBounded=0,nonMultiSafe=0,totalSafe=0,shortMismatch=0,unsafeLong=0;
for(let mask=1;mask<32768;mask++){let U=0;for(let k=0;k<P.length;k++)if(mask&(1<<k))U|=P[k];if(!cache.has(U))cache.set(U,{multi:multipart(U),bounded:!order3(U),rel:ctx.filter(({i,j,C})=>path(U,C,i,j))});let {multi,bounded,rel}=cache.get(U);let safe=rel.every(c=>mask&c.lm);let short=rel.filter(c=>pop(c.C)<=1).every(c=>mask&c.lm);if(safe)totalSafe++;
 if(multi){multipartN++;if(safe)multipartSafe++;if(!bounded)throw Error('multipart order3');}
 if(bounded){boundedN++;if(safe)boundedSafe++;if(safe!==short)shortMismatch++;if(!multi){nonMultiBounded++;if(safe)nonMultiSafe++;}}
 if(!safe&&short)unsafeLong++;
}
multiUnions=[...cache.values()].filter(x=>x.multi).length;
if(shortMismatch)throw Error('bounded context certificate failed');
console.log(JSON.stringify({tables:32767,distinctUnions:cache.size,totalSafe,multipartN,multipartSafe,multiUnions,boundedN,boundedSafe,nonMultiBounded,nonMultiSafe,shortMismatch,unsafeLong}));
