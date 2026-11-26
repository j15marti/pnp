function signedAudit(){
 let checks=0;const ck=x=>{checks++;if(!x)throw Error("check "+checks)};
 let state=61126041;const r=n=>{state^=state<<13;state^=state>>>17;state^=state<<5;return (state>>>0)%n};
 let yes=0,no=0,assignments=0,charts=160;
 const bit=(x,i)=>x>>i&1,lit=(x,[i,s])=>bit(x,i)^s;
 for(let t=0;t<charts;t++){
  let n=2+r(5),m=1+r(4),h=Array.from({length:m},()=>[[r(n),r(2)],[r(n),r(2)]]),A=Array.from({length:r(4)},()=>[r(1<<n),r(2)]),p=n+m,
  rows=h.map((c,j)=>[[c[0][0],1^c[0][1]],[c[1][0],1^c[1][1]],[n+j,0]]);
  const pc=x=>{let k=0;for(;x;x&=x-1)k++;return k};
  const guard=x=>A.every(([a,b])=>pc(a&x)%2===b);
  let c=Array(p).fill(0),constant=0;
  for(let rr of rows)for(let [i,s] of rr){constant+=s;c[i]+=s?-1:1}
  let flip=c.reduce((v,w,i)=>v|((w<0?1:0)<<i),0),shift=constant+c.filter(w=>w<0).reduce((z,w)=>z+w,0),cost=c.map(Math.abs);
  let rhsRows=rows.map(rr=>rr.reduce((v,[i])=>v^(1<<i),0)),
  rhs=rows.map(rr=>1^rr.reduce((v,[i,s])=>v^s^((flip>>i)&1),0));
  let orig=0,extended=0,opt=Infinity;
  for(let x=0;x<1<<n;x++){
   const ok=guard(x)&&h.every(c=>c.some(l=>lit(x,l)));orig+=ok;
   let count=0;
   for(let s=0;s<1<<m;s++){let xx=x|(s<<n);if(guard(xx)&&rows.every(rr=>rr.reduce((z,l)=>z+lit(xx,l),0)===1))count++}
   ck(count===Number(ok));extended+=count;
  }
  for(let y=0;y<1<<p;y++){
   assignments++;
   let x=y^flip,total=rows.reduce((v,rr)=>v+rr.reduce((z,l)=>z+lit(x,l),0),0),w=shift+cost.reduce((v,c,i)=>v+c*bit(y,i),0);
   ck(total===w);let parity=rhsRows.every((a,j)=>pc(a&y)%2===rhs[j]);ck(parity===rows.every(rr=>rr.reduce((z,l)=>z^lit(x,l),0)===1));if(parity&&guard(x)){ck(w>=m);opt=Math.min(opt,w);ck((w===m)===rows.every(rr=>rr.reduce((z,l)=>z+lit(x,l),0)===1))}
  }
  ck(orig===extended);ck((opt===m)===(orig>0));if(orig)yes++;else no++;
 }
 return {checks,charts,yes,no,assignments,seed:61126041};
}
console.log(JSON.stringify(signedAudit(),null,2));
