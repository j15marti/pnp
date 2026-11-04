'use strict';
// Independent exhaustive evaluator for fixed bounded examples; no Python imports.
function php(h) {
  const p=(i,j)=>(i-1)*h+j;
  const src=[];
  for(let i=1;i<=h+1;i++)src.push(Array.from({length:h},(_,j)=>p(i,j+1)));
  for(let j=1;j<=h;j++)for(let i=1;i<=h+1;i++)for(let k=i+1;k<=h+1;k++)src.push([-p(i,j),-p(k,j)]);
  return src;
}
function defs(h){
  const n=h*(h+1);let g=[],cl=[];const p=(i,j)=>(i-1)*h+j;
  for(let i=1;i<=h;i++)for(let j=1;j<h;j++){
    const z=n+g.length+1,a=p(i,j),b=p(i,h),c=p(h+1,j);
    g.push([z,a,b,c]);cl.push([z,-a],[z,-b,-c],[-z,a,b],[-z,a,c]);
  }return {g,cl};
}
function satClause(cl,bits){return cl.some(x=>(x>0?bits[x]:1-bits[-x])===1)};
function sat(cl,bits){return cl.every(c=>satClause(c,bits))}
let cnt=0,out=[];
for(let h=1;h<=3;h++){
  const src=php(h),{g,cl}=defs(h),n=h*(h+1);let xcnt=0,invalidCnf=0;
  for(let mask=0;mask<2**n;mask++){
    const v=Array(n+g.length+1).fill(0);
    for(let i=1;i<=n;i++)v[i]=(mask>>>(i-1))&1;
    for(const [z,a,b,c] of g)v[z]= +(v[a]===1 || (v[b]===1&&v[c]===1));
    if(!sat(cl,v))throw Error('legitimate extension rejected');cnt++;
    if(sat(src,v))throw Error('PHP SAT');cnt++;
    for(const [z] of g){const alt=v.slice();alt[z]=1-alt[z];if(sat(cl,alt))throw Error('nonunique extension');cnt++}
    if(h===2){
      // Exhaustive independent clause-subset projection for each x.
      for(let S=0;S<2**src.length;S++){
        const subset=src.filter((_,i)=>(S>>i)&1);
        const orig=sat(subset,v);let found=false;
        for(let q=0;q<2**g.length;q++){
          const w=v.slice();for(let k=0;k<g.length;k++)w[g[k][0]]=(q>>k)&1;
          if(sat(subset,w)&&sat(cl,w))found=true;
        }
        if(orig!==found)throw Error('subset projection failure');cnt++;
      }
    }
    xcnt++;
  }
  if(h===2) { // Hostile check: silently reverse one signed gate literal and catch wrong extension.
    const broken=cl.map(row=>row.slice());broken[0][0]*=-1;
    let witness=false;
    for(let mask=0;mask<2**n;mask++) {
      const v=Array(n+g.length+1).fill(0);for(let i=1;i<=n;i++)v[i]=(mask>>>(i-1))&1;
      for(const [z,a,b,c] of g)v[z]=+(v[a]||(v[b]&&v[c]));
      if(!sat(broken,v)){witness=true;break}
    }
    if(!witness) throw Error('corrupted definition was accepted');cnt++;
  }
  out.push({holes:h,clauses:src.length,gates:g.length,checkedOriginalValuations:xcnt});
}
console.log(JSON.stringify({verifier:'independent NodeJS',checks:cnt,examples:out,corruptionDetected:true},null,2));