// BA08 exact product spectral span, GF(2), deterministic. node BA08_check.js
const stats={gaussian:0,pairs:0,energy:0,closure:0,assertions:0};
const bit=i=>1n<<BigInt(i);
function parity(x){let p=0;while(x){x&=x-1n;p^=1}return p}
const hi=x=>x.toString(2).length-1;
const pow=n=>1n<<BigInt(n);
function check(x){stats.assertions++;if(!x)throw Error("assertion "+stats.assertions)}
function solve(n,eq){
 stats.gaussian++;
 const piv=new Map();
 for(let [a,b] of eq){while(a){let j=hi(a);if(!piv.has(j)){piv.set(j,[a,b]);break}let t=piv.get(j);a^=t[0];b^=t[1]}if(!a&&b)return null}
 const js=[...piv.keys()].sort((a,b)=>a-b);
 function lift(x,hom){for(let j of js){let [a,b]=piv.get(j);if(parity(a&x)!==(hom?0:b))x^=bit(j)}return x}
 const ker=[];for(let j=0;j<n;j++)if(!piv.has(j))ker.push(lift(bit(j),true));
 return {a:lift(0n,false),ker,rank:piv.size};
}
const orth=(n,rows)=>solve(n,rows.map(x=>[x,0])).ker;
const rank=(n,rows)=>solve(n,rows.map(x=>[x,0])).rank;
const roweq=(mask,b)=>[mask,b];
function prep(f){
 const r=f.rows.length;
 return {...f,r,terms:f.terms.flatMap(t=>{let s=solve(r,t.eq);return s?[{...t,amp:t.c*pow(r-s.rank),phase:s.a,orth:s.ker}]:[]})};
}
function coeff(f,u){let z=0n;for(let t of f.terms)if(t.orth.every(a=>!parity(a&u)))z+=parity(t.phase&u)?-t.amp:t.amp;return z}
function localPair(f,da,db,pins,h){
 let z=0n;
 for(let a of f.terms)for(let b of f.terms){
 stats.pairs++;
 let eq=pins.concat(a.orth.map(x=>[x,parity(x&da)]),b.orth.map(x=>[x,parity(x&db)]));
 let s=solve(f.r,eq);if(!s)continue;
 let phase=a.phase^b.phase^h;
 if(s.ker.some(x=>parity(x&phase)))continue;
 let v=a.amp*b.amp*pow(s.ker.length);
 if(parity(phase&s.a)^parity(a.phase&da)^parity(b.phase&db))v=-v;
 z+=v;
 }
 return z;
}
function localValue(f,u){return f.terms.reduce((a,t)=>a+(t.eq.every(([x,b])=>parity(x&u)===b)?t.c:0n),0n)}
function obs(f,z){let u=0n;f.rows.forEach((x,j)=>{if(parity(x&z))u|=bit(j)});return u}
function compile(d,input,cap=4){
 // Certified closure: reject locally identically-zero factors, discard locally
 // constant nonzero factors (record scalar). Exact local squared norm and mean.
 // No semantic global closure. No SAT branching in this evaluator.
 let fs=input.map(prep),scalar=1n;
 while(true){stats.closure++;let changed=false;
 for(let i=0;i<fs.length;i++){let f=fs[i];let norm=localPair(f,0n,0n,[],0n),m=coeff(f,0n);
 if(norm===0n)return {zero:true,span:[],count:0n,delta:0};
 if(norm===m*m){check(m%pow(f.r)===0n);scalar*=m/pow(f.r);fs.splice(i,1);changed=true;break}
 }if(!changed)break}
 let rows=fs.flatMap(f=>f.rows),M=rows.length;
 let dep=orth(M,Array.from({length:d},(_,j)=>rows.reduce((a,x,i)=>a|(x&bit(j)?bit(i):0n),0n)));
 let delta=dep.length;if(delta>cap)return {unknown:true,delta};
 let ds=[0n];for(let a of dep)ds=ds.concat(ds.map(x=>x^a));
 // Pick pivot coordinates of dependency basis; fixing them zero defines transversal.
 let pp=new Map();for(let a of dep){while(a){let j=hi(a);if(!pp.has(j)){pp.set(j,a);break}a^=pp.get(j)}}
 let fixed=new Map([...pp.keys()].map(j=>[j,0]));
 let off=0;for(let f of fs){f.off=off;f.mask=pow(f.r)-1n;off+=f.r}
 const part=(f,x)=>(x>>BigInt(f.off))&f.mask;
 function energy(extra,h=0n){
 stats.energy++;let pins=new Map(fixed);for(let [j,b] of extra){if(pins.has(j)&&pins.get(j)!==b)return 0n;pins.set(j,b)}
 let sum=0n;for(let a of ds)for(let b of ds){let term=1n;
 for(let f of fs){let e=[];for(let [j,v] of pins)if(j>=f.off&&j<f.off+f.r)e.push([bit(j-f.off),v]);let phase=obs(f,h);term*=localPair(f,part(f,a),part(f,b),e,phase);if(!term)break}
 sum+=term;
 }return sum;
 }
 function outside(extra,h){let x=energy(extra),y=energy(extra,h);check((x-y)%2n===0n);let e=(x-y)/2n;check(e>=0n);return e}
 let zero=energy([])===0n,span=[];
 if(!zero){
 while(true){let h=orth(d,span).find(h=>outside([],h)>0n);if(h===undefined)break;
 let prefix=[];for(let j=0;j<M;j++)if(!fixed.has(j)){let q=prefix.concat([[j,0]]);prefix=outside(q,h)>0n?q:prefix.concat([[j,1]])}
 let w=0n;for(let [j,b] of prefix)if(b)w^=rows[j];check(parity(w&h)===1);span.push(w);
 }
 }
 let num=0n;for(let a of ds){let t=1n;for(let f of fs)t*=coeff(f,part(f,a));num+=t}
 num*=scalar;let count;if(d>=M)count=num*pow(d-M);else {check(num%pow(M-d)===0n);count=num/pow(M-d)}
 return {span,count,delta,zero};
}
const one={c:1n,eq:[]};
const event=(r,b,c=-1n)=>({c,eq:Array.from({length:r},(_,j)=>[bit(j),Number((BigInt(b)>>BigInt(j))&1n)])});
function brute(d,fs){let vals=Array.from({length:2**d},(_,z)=>fs.reduce((p,f)=>p*localValue(f,obs(f,BigInt(z))),1n));let span=[];for(let w=0;w<vals.length;w++){let v=vals.reduce((a,x,z)=>a+(parity(BigInt(w&z))?-x:x),0n);if(v)span.push(BigInt(w))}return {count:vals.reduce((a,b)=>a+b,0n),span}}
let results={cube:{SAT:0,UNSAT:0},random:{SAT:0,UNSAT:0,unknown:0},scaling:[],fano:{SAT:0,UNSAT:0,unknown:0}};
function compare(d,fs,bucket){let a=compile(d,fs),b=brute(d,fs);if(a.unknown){bucket.unknown=(bucket.unknown||0)+1;return}check(a.count===b.count);let r=rank(d,b.span);check(rank(d,a.span)===r);check(rank(d,a.span.concat(b.span))===r);bucket[b.count>0n?"SAT":"UNSAT"]++}
for(let mask=0;mask<256;mask++){let terms=[one];for(let j=0;j<8;j++)if(mask>>j&1)terms.push(event(3,j));compare(3,[{rows:[1n,2n,4n],terms}],results.cube)}
let seed=0xBA08;function rnd(n){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return (seed>>>8)%n}
for(let k=0;k<60;k++){let fs=[];for(let j=0;j<3;j++){let a=rnd(5),b=(a+1+rnd(4))%5;let terms=[one,event(2,rnd(4))];if(k%4===0){let t=event(2,rnd(4));terms.push(t,{...t,c:1n})}fs.push({rows:[bit(a),bit(b)],terms})}compare(5,fs,results.random)}
for(let r of [4,8,16,32]){let fs=[{rows:Array.from({length:r},(_,j)=>bit(j)),terms:[one,event(r,0)]},{rows:[1n,2n],terms:[one,event(2,0)]}];let a=compile(r,fs);check(a.delta===2);check(rank(r,a.span)===2);check(rank(r,a.span.concat([1n,2n]))===2);check(a.count===3n*pow(r-2));results.scaling.push({r,delta:a.delta,effective:2,count:String(a.count)})}
const lines=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]];
for(let k=-1;k<14;k++){let fs=lines.map((l,i)=>({rows:l.map(bit),terms:[one,...(k===2*i?[]:[event(3,0)]),...(k===2*i+1?[]:[event(3,7)])]}));let a=compile(7,fs),b=brute(7,fs);check(b.count===(k<0?0n:5n));if(a.unknown)results.fano.unknown++;else check(a.count===b.count);results.fano[b.count>0n?"SAT":"UNSAT"]++}
console.log(JSON.stringify({results,stats,seed:"0xBA08"},null,2));