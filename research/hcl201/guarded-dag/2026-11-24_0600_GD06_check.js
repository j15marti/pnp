function runGD06(){
  let seed=0x2010600;
  function rnd(n){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return (seed>>>8)%n}
  const wt=x=>{let r=0;for(;x;x&=x-1)r++;return r};
  const parity=x=>wt(x)&1;
  function basis(xs){const b=[];for(let v of xs){for(const u of b)v=Math.min(v,v^u);if(v){b.push(v);b.sort((a,b)=>b-a)}}return b}
  function lin(cols,t){let b=[],ker=[];for(let j=0;j<cols.length;j++){let v=cols[j],c=1<<j;for(const [u,d] of b)if((v^u)<v){v^=u;c^=d}if(v){b.push([v,c]);b.sort((a,b)=>b[0]-a[0])}else ker.push(c)}
    let p=0;for(const [u,d] of b)if((t^u)<t){t^=u;p^=d}return t?null:{p,ker}}
  function combo(cols,m){let v=0;for(let j=0;j<cols.length;j++)if((m>>>j)&1)v^=cols[j];return v}
  function inter(a,b){return basis(lin(a.concat(b),0).ker.map(k=>combo(a,k)))}
  function span(xs){let a=[0];for(const x of basis(xs))a=a.concat(a.map(y=>y^x));return a}
  function color(f,x){return parity(f.g[0]&x)+2*parity(f.g[1]&x)}
  function state(F,x){let o=0,cols=[];for(let i=0;i<F.fs.length;i++){const z=F.fs[i].r[color(F.fs[i],x)];if(!z)return null;o^=z.o;cols.push(...z.cols)}return {o,cols}}
  function ranks(F){const mask=(1<<F.e)-1;let common=[],all=[];for(const f of F.fs){let spaces=f.r.filter(Boolean).map(z=>basis(z.cols.map(v=>v&mask)));if(!spaces.length)return null;common.push(...spaces.reduce(inter));all.push(...spaces.flat())}let w=basis(common).length;return {w,a:basis(all).length-w,all:basis(all)}}
  function feature(x,n,k){let v=1n,pos=1n;for(let i=0;i<n;i++){if(x&(1<<i))v|=1n<<pos;pos++}if(k>=2)for(let i=0;i<n;i++)for(let j=i+1;j<n;j++){if((x&(1<<i))&&(x&(1<<j)))v|=1n<<pos;pos++}return v}
  function insert(b,v){for(const u of b)if((v^u)<v)v^=u;if(!v)return false;b.push(v);b.sort((a,b)=>a>b?-1:a<b?1:0);return true}
  function* low(n,d,start=0,mask=0){yield mask;if(d>0)for(let i=start;i<n;i++)yield*low(n,d-1,i+1,mask|(1<<i))}
  function lift(F,x,t,k){let q=state(F,x);if(!q)return [];let sm=(1<<F.e)-1,r=lin(q.cols.map(v=>v&sm),(q.o&t*0^t)&sm); // offset correction below
    r=lin(q.cols.map(v=>v&sm),(q.o^t)&sm);if(!r)return [];
    let base=q.o^combo(q.cols,r.p);let ps=basis(r.ker.map(c=>combo(q.cols,c)>>>F.e));let out=[];for(const v of low(ps.length,k))out.push(x|(((base>>>F.e)^combo(ps,v))<<F.n));return out}
  function ref(F,t){const sm=(1<<F.e)-1,out=new Set();for(let x=0;x<(1<<F.n);x++){if(F.pin!==undefined&&(x&1)!==F.pin)continue;let acc=[0];for(const f of F.fs){let z=f.r[color(f,x)];if(!z){acc=[];break}let next=[];for(const a of acc)for(const b of span(z.cols))next.push(a^z.o^b);acc=next}for(const v of acc)if((v&sm)===t)out.add(x|((v>>>F.e)<<F.n))}return out}
  // All available colors and outside-span equations are already resolved on the supplied cell;
  // if a pin is present it is an exact affine cell. Fixed d=1 requires affine guard tables.
  function sparse(F,t,k,d=2){const rr=ranks(F),b=[],wits=[],count={selectors:0,lifts:0};if(!rr)return {b,wits,count};
    const n=F.n-(F.pin!==undefined?1:0);
    for(const y of low(n,d*(rr.a+2*k))){let x=F.pin===undefined?y:(y<<1)|F.pin;count.selectors++;for(const v of lift(F,x,t,k)){count.lifts++;if(insert(b,feature(v,F.n+F.fs.length,k)))wits.push(v)}}
    return {b,wits,count}}
  let R={seed:"0x2010600",randomProducts:0,targets:0,sat:0,unsat:0,spanComparisons:0,verifiedBasisWitnesses:0,selectorEvaluations:0,candidateLifts:0,referenceTuples:0,unstableProducts:0,errors:0,controls:[],scaling:[]};
  function check(F,t,label){const q=ref(F,t);R.targets++;R[q.size?"sat":"unsat"]++;R.referenceTuples+=q.size;for(let k=1;k<=2;k++){const a=sparse(F,t,k),b=[];for(const x of q)insert(b,feature(x,F.n+F.fs.length,k));if(a.b.length!==b.length||a.b.some(v=>{for(const u of b)if((v^u)<v)v^=u;return v!==0n}))throw Error("span "+label);for(const v of a.wits)if(!q.has(v))throw Error("witness");R.spanComparisons++;R.verifiedBasisWitnesses+=a.wits.length;R.selectorEvaluations+=a.count.selectors;R.candidateLifts+=a.count.lifts}return q.size}
  for(let z=0;z<80;z++){let n=3+rnd(3),e=2+rnd(3),h=2+rnd(2),fs=[];for(let i=0;i<h;i++){let stable=rnd(1<<e),p=1<<(e+i),g=[1<<rnd(n),1<<rnd(n)],r=[];for(let c=0;c<4;c++){let cols=[];if(stable)cols.push(stable^(rnd(2)?p:0));if(rnd(2))cols.push(rnd(1<<e)^(rnd(2)?p:0));if(rnd(3)===0)cols.push(p);r.push({o:rnd(2)?p:0,cols})}fs.push({g,r})}let F={n,e,fs};if(z%5===0)F.pin=rnd(2);let rr=ranks(F);R.randomProducts++;if(rr.a)R.unstableProducts++;for(let t=0;t<(1<<e);t++)check(F,t,"random "+z)}
  // Incompatible union: one guard chooses either syndrome e1 or e2, never both.
  const H={n:3,e:2,fs:[{g:[1,2],r:[{o:0,cols:[1]},{o:0,cols:[2]},{o:0,cols:[1]},{o:0,cols:[2]}]}]};
  for(let t=0;t<4;t++)R.controls.push({name:"exclusive directions",target:t,solutions:check(H,t,"exclusive")});
  // Availability pin is certified: only x0=0 colors exist.
  const A={n:4,e:2,pin:0,fs:[{g:[1,2],r:[{o:0,cols:[1|4]},null,{o:0,cols:[2|4]},null]}]};
  for(let t=0;t<4;t++)R.controls.push({name:"availability cell",target:t,solutions:check(A,t,"availability")});
  // h stable directions and one shared unstable direction, active iff x_i=1;
  // protected p_i is its actual coefficient. All guard tables are affine in x.
  for(const h of [4,8,12,14]){const e=h+1,shared=1<<h,fs=[];for(let i=0;i<h;i++){let p=1<<(e+i),base=1<<i;fs.push({g:[1<<i,0],r:[{o:0,cols:[base,0]},{o:0,cols:[base,shared|p]},{o:0,cols:[base,0]},{o:0,cols:[base,shared|p]}]})}let F={n:h,e,fs};let rr=ranks(F),a=sparse(F,shared,1,1);if(a.b.length!==2*h)throw Error("scale rank");for(const v of a.wits){let x=v&((1<<h)-1),p=v>>>h;if((p&~x)||parity(p)!==1)throw Error("scale witness")}R.scaling.push({h,stableRank:rr.w,unstableRank:rr.a,selectors:a.count.selectors,fullSelectors:2**h,candidateLifts:a.count.lifts,affineRank:a.b.length,expectedRank:2*h});}
  return R
}
console.log(JSON.stringify(runGD06(), null, 2));
