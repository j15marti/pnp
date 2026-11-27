/* Independent C06-12 audit, run with node. */
function audit(){
 const C=[[0,6,10],[1,6,7],[0,5,11],[2,6,11],[3,4,7],[3,8,9],[1,5,8],[3,9,11],[1,4,8],[2,5,10],[0,9,10],[2,4,7]];
 const S=[[0,2,3,9],[0,1,4,5,8,10],[1,3,5,7,8,11]];
 const h=3173, parity=x=>{let p=0;for(;x;x&=x-1n)p^=1;return p};
 let checks=0;const ok=(b)=>{checks++;if(!b)throw Error("check "+checks)};
 function rref(a,n){a=[...a];let p=[],r=0;for(let j=0;j<n;j++){let k=a.findIndex((v,i)=>i>=r&&((v>>BigInt(j))&1n));if(k<0)continue;[a[r],a[k]]=[a[k],a[r]];for(let i=0;i<a.length;i++)if(i!==r&&((a[i]>>BigInt(j))&1n))a[i]^=a[r];p.push(j);r++}return {a,p,none:a.includes(1n<<BigInt(n))}}
 function chart(a,n){let q=rref(a,n);if(q.none)return null;let f=Array.from({length:n},(_,i)=>i).filter(i=>!q.p.includes(i)),o=Array(n).fill(0n),b=0n;f.forEach((i,j)=>o[i]=1n<<BigInt(j));q.p.forEach((i,j)=>{for(let k=0;k<f.length;k++)if((q.a[j]>>BigInt(f[k]))&1n)o[i]|=1n<<BigInt(k);if(q.a[j]>>BigInt(n)&1n)b|=1n<<BigInt(i)});return {o,b,d:f.length}}
 function word(q,t){let x=q.b;for(let i=0;i<q.o.length;i++)if(parity(q.o[i]&t))x^=1n<<BigInt(i);return x}
 const mask=c=>c.reduce((v,i)=>v|(1n<<BigInt(i)),0n);
 const cw=[];for(let x=0;x<4096;x++)if(C.every(c=>c.reduce((z,i)=>z+((x>>i)&1),0)===1))cw.push(x);
 ok(JSON.stringify(cw)==="[15,624,3456]");ok(cw.every(x=>parity(BigInt(x&h))===0));
 let lr=[];for(let s of S){let v=Array.from({length:12},(_,i)=>s.reduce((k,j)=>k+C[j].includes(i),0));ok(v.every(x=>x%2===0));lr.push(v.reduce((z,x,i)=>z|((BigInt(x/2%2))<<BigInt(i)),0n)|(BigInt(s.length/2%2)<<12n))}
 ok(lr[0]===BigInt(h));
 let result=[];
 for(let m of [1,2,4,8,16,32,64]){
  let n=12*m,rows=[],lifts=[],guard=1n<<BigInt(n),triples=[],occ=Array.from({length:n},()=>[]),guards=[];
  for(let j=0;j<m;j++){
   for(let c of C)rows.push((mask(c)<<BigInt(12*j))|(1n<<BigInt(n)));
   for(let l of lr)lifts.push(((l&4095n)<<BigInt(12*j))|((l>>12n)<<BigInt(n)));
   guard|=BigInt(h)<<BigInt(12*j);
   for(let k=0;k<C.length;k++){let a=6*(12*j+k);for(let i=0;i<6;i++)triples.push([a+(i+5)%6,a+i,a+(i+1)%6]);for(let i=0;i<3;i++)occ[12*j+C[k][i]].push(a+i)}
  }
  for(let a of occ)for(let i=1;i<a.length;i++)guards.push([[a[0],a[i]],0]);
  guards.push([occ.flatMap((a,i)=>((BigInt(h)>>BigInt(i%12))&1n)?[a[0]]:[]),1]);
  let q=chart([...rows,guard],n);ok(q!==null);ok(q.d===3*m-1);ok(q.o.every(v=>v!==0n));for(let j=0;j<m;j++)for(let c of C)ok(new Set(c.map(i=>q.o[i+12*j])).size===3);
  ok(chart([...rows,guard,...lifts],n)===null);
  const deg=Array(triples.length).fill(0);for(let c of triples){ok(new Set(c).size===3);for(let i of c)deg[i]++}ok(deg.every(v=>v===3));
  result.push({copies:m,original_vars:triples.length,guard_count:guards.length,dimension:q.d,lift_rows:lifts.length,certificate_rows:4*m});
 }
 let prism=[];for(let x=0;x<64;x++)if(Array.from({length:6},(_,i)=>[i,(i+5)%6,(i+1)%6]).every(c=>c.reduce((z,i)=>z+((x>>i)&1),0)===1))prism.push(x);
 ok(JSON.stringify(prism)==="[9,18,36]");
 let seed=62125,rand=n=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n};
 let strict=0;
 for(let k=0;k<300;k++){
  let n=1+rand(5),m=1+rand(6),A=Array.from({length:m},()=>Array.from({length:n},()=>rand(7)-3)),b=Array.from({length:m},()=>rand(7)-3);
  let rows=A.map((a,j)=>mask(a.flatMap((v,i)=>v&1?[i]:[]))|(BigInt(b[j]&1)<<BigInt(n))),q=chart(rows,n);
  let trans=Array.from({length:n},(_,i)=>mask(A.flatMap((a,j)=>a[i]&1?[j]:[]))),L=chart(trans,m),extra=[],bad=false;
  for(let i=0;i<L.d;i++){let y=word(L,1n<<BigInt(i)),v=Array(n).fill(0),r=0;for(let j=0;j<m;j++)if(y>>BigInt(j)&1n){r+=b[j];for(let l=0;l<n;l++)v[l]+=A[j][l]}ok(v.every(x=>x%2===0));if(r&1){bad=true;break}extra.push(mask(v.flatMap((x,j)=>((x/2)&1)?[j]:[]))|(BigInt((r/2)&1)<<BigInt(n)))}
  let pred=bad?null:chart([...rows,...extra],n),actual=new Set(),got=new Set();
  for(let z=0;z<4**n;z++){let x=Array.from({length:n},(_,j)=>(z>>(2*j))&3);if(A.every((a,j)=>((a.reduce((s,v,i)=>s+v*x[i],0)-b[j])%4)===0))actual.add(Number(mask(x.flatMap((v,i)=>v&1?[i]:[]))))}
  if(pred)for(let t=0;t<2**pred.d;t++)got.add(Number(word(pred,BigInt(t))));
  ok(actual.size===got.size&&[...actual].every(x=>got.has(x)));if(q&&actual.size<2**q.d)strict++;
 }
 // Hostile control: integer solution of color selectors and pair slack, no Boolean K4 coloring.
 let x=Array.from({length:12},(_,i)=>i%3===0?1:0),H=Array.from({length:4},(_,i)=>[3*i,3*i+1,3*i+2]);
 for(let i=0;i<4;i++)for(let j=i+1;j<4;j++)for(let c=0;c<3;c++){H.push([3*i+c,3*j+c,x.length]);x.push(1-x[3*i+c]-x[3*j+c])}
 ok(H.every(c=>c.reduce((s,i)=>s+x[i],0)===1));for(let t=0;t<81;t++){let a=Array.from({length:4},(_,j)=>Math.floor(t/3**j)%3);ok(new Set(a).size<4)}
 return {checks,random_mod4:300,strict_random:strict,core:C,left_basis:S,core_words:cw,prism_words:prism,family:result,hostile_integer_witness:x,hostile_clauses:H}
}
console.log(JSON.stringify(audit(),null,2));
