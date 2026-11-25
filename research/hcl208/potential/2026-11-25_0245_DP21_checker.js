// Node.js: node checker.js BW17_frozen.json MS27_support_results.json
const fs=require('fs');
function checker(raw,tangent){
 let checks=0;const ok=(x,m)=>{checks++;if(!x)throw Error(m)};
 function comb(n,k){let out=[];function rec(a,i){if(a.length===k){out.push(a);return}for(let j=i;j<=n-k+a.length;j++)rec([...a,j],j+1)}rec([],0);return out}
 const key=a=>a.slice().sort((a,b)=>a-b).join(",");
 const parity=x=>{let p=0;while(x){p^=1;x&=x-1}return p?-1:1};
 const bit=(w,i)=>(w>>i)&1;
 function legal(O,S,w){return O.every(o=>!o.t.every(v=>S.includes(v))||!o.bad.includes(o.t.reduce((a,v,j)=>a+(bit(w,S.indexOf(v))<<j),0)))}
 function lift(n,O,C,D){
  let stats={triples:0,quads:0,tripleZeros:0,quadZeros:0,quadPos:0,forcedIntervals:0,extraZeros:0};
  const a=(S,w)=>D+comb(S.length,2).reduce((s,[i,j])=>s+(C.get(key([S[i],S[j]]))||0)*(bit(w,i)===bit(w,j)?1:-1),0);
  for(const S of comb(n,3)){stats.triples++;for(let w=0;w<8;w++){const v=a(S,w);ok(v>=0,"triple nonnegative");ok((v>0)===legal(O,S,w),"triple full support");stats.tripleZeros+=v===0}}
  for(const S of comb(n,4)){
   stats.quads++;let L=-Infinity,U=Infinity;for(let w=0;w<16;w++){let z=a(S,w);if(parity(w)===1)L=Math.max(L,-z);else U=Math.min(U,z)}
   ok(L<=U,"quartic interval");stats.forcedIntervals+=L===U;const q2=L+U;let vals=[];
   for(let w=0;w<16;w++){let v=2*a(S,w)+parity(w)*q2;ok(v>=0,"quad nonnegative");ok(v===0||legal(O,S,w),"forbidden zero");if(v===0){stats.quadZeros++;if(legal(O,S,w))stats.extraZeros++}else stats.quadPos++;vals.push(v)}
   for(let j=0;j<4;j++){const T=S.filter((_,i)=>i!==j);for(let w=0;w<8;w++){let v=0;for(let z=0;z<16;z++)if(T.every((x,i)=>bit(w,i)===bit(z,S.indexOf(x))))v+=vals[z];ok(v===4*a(T,w),"exact triple marginal")}}
  }ok(stats.extraZeros===0,"no extra zeros");return stats;
 }
 function signedInteger(n,O){
  const M=new Map([[0,1]]), get=k=>M.get(k)||0, set=(k,v)=>M.set(k,v), mask=S=>S.reduce((s,x)=>s|(1<<x),0);
  const edges=new Set();for(const o of O)for(const p of comb(3,2))edges.add(key(p.map(i=>o.t[i])));
  for(const o of O){const t=o.t,b=o.bad[0],z=[bit(b,0),bit(b,1),bit(b,2)],w4=z.reduce((x,y)=>x+y,0)-1,ws=[z[0]-w4,z[1]-w4,z[2],w4],words=[1,2,4,3].map(w=>w^b);ok(ws.reduce((a,b)=>a+b,0)===1,"integer normalization");for(let s=1;s<8;s++){const k=mask(t.filter((_,i)=>bit(s,i)));set(k,ws.reduce((a,w,j)=>a+((words[j]&s)===s?w:0),0))}}
  function poly(o,d,which){let p=new Map([[1<<d,1]]);for(let i=0;i<3;i++){let neg=bit(o.bad[0],i)^(which===0?1:0);let q=new Map();for(const [k,v] of p){if(neg)q.set(k,(q.get(k)||0)+v);let l=k|(1<<o.t[i]);q.set(l,(q.get(l)||0)+(neg?-v:v))}p=q}return p}
  const val=p=>[...p].reduce((s,[k,v])=>s+v*get(k),0);let extensions=0;
  for(const o of O)for(let d=0;d<n;d++)if(!o.t.includes(d)){
   let candidates=o.t.filter(v=>!edges.has(key([v,d])));ok(candidates.length>=2,"private triple");const k=mask([d,...candidates.slice(0,2)]),all=mask([d,...o.t]),p=poly(o,d,0),q=poly(o,d,1),sum=new Map(p);for(const [l,v] of q)sum.set(l,(sum.get(l)||0)+v);ok(sum.get(all)===0&&Math.abs(sum.get(k))===1,"unit pivot");set(k,get(k)-val(sum)/sum.get(k));ok(Math.abs(q.get(all))===1,"quartic pivot");set(all,get(all)-val(q)/q.get(all));ok(val(p)===0&&val(q)===0,"bad marginals");extensions++;
  }
  let words=0,zeros=0;for(let k=1;k<=4;k++)for(const S of comb(n,k))for(let w=0;w<1<<k;w++){let on=mask(S.filter((_,i)=>bit(w,i))),off=mask(S.filter((_,i)=>!bit(w,i)));let mass=0;for(let q=off;;q=(q-1)&off){mass+=parity(q)*get(on|q);if(!q)break}ok(Number.isInteger(mass),"integer");if(!legal(O,S,w)){ok(mass===0,`integer forbidden ${S} ${w} ${mass}`);zeros++}words++}return {extensions,words,zeros};
 }
 function base(O){let C=new Map();for(const o of O)for(const [i,j] of comb(3,2))C.set(key([o.t[i],o.t[j]]),bit(o.bad[0],i)===bit(o.bad[0],j)?-1:1);return C}
 const count=(n,O)=>{let c=0;for(let w=0;w<1<<n;w++)if(legal(O,Array.from({length:n},(_,i)=>i),w))c++;return c};
 let controls=[];for(let l=5;l<=8;l++){for(let mode=0;mode<3;mode++){const O=Array.from({length:l},(_,i)=>({t:[i,(i+1)%l,l+i],bad:[(mode*(i+3))%8,7^((mode*(i+3))%8)]}));controls.push({n:2*l,mode,models:count(2*l,O),lp:lift(2*l,O,base(O),3),integer:signedInteger(2*l,O)})}}
 const fano=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]].map(t=>({t,bad:[0,7]}));let fc=count(7,fano),neighbors=[];for(let i=0;i<7;i++)for(let b=0;b<3;b++){let a=fano.map((o,j)=>j===i?{t:o.t,bad:[1<<b,7^(1<<b)]}:o);neighbors.push(count(7,a))}ok(fc===0&&neighbors.every(x=>x===10),"Fano control");
 let C=new Map(tangent.edgeOrder.map((e,i)=>[e,-100-2*tangent.tangent[i]]));const BW=lift(raw.n,raw.O,C,300);let witness=12130883;ok(legal(raw.O,Array.from({length:raw.n},(_,i)=>i),witness),"actual BW17 witness");
 return {checks,controls,BW17:BW,sourceWitness:witness,Fano:{root:fc,neighbors},guard:"empty",limitations:"Finite controls; no generic LP/SNF backend, no K16 wide scope, no source witness acquisition. BW17 four-scope signed feasibility follows only from verified supplied witness."}
}
console.log(JSON.stringify(checker(JSON.parse(fs.readFileSync(process.argv[2])),JSON.parse(fs.readFileSync(process.argv[3]))),null,2));
