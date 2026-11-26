function audit(){
 let checks=0;const assert=(b)=>{if(!b)throw Error("assert "+checks);checks++};const f=s=>"1".repeat(s.length)+"0"+s;const bin=n=>n.toString(2);
 const rules=[[0,1,0,0,1,0,1,2],[0,2,0,2,2,0,1,2],[2,1,0,0,1,0,1,2],[2,2,0,2,2,0,1,2],[2,0,0,1,0,0,2,2]];
 const code=rules.flat().map(n=>f(bin(n))).join("");
 const enc=(x,t)=>f(code)+f(x)+f(bin(t));
 function parse(w){let j=0;function get(){let n=0;while(w[j]==="1"){j++;n++}if(w[j++]!=="0"||j+n>w.length)throw Error("frame");let s=w.slice(j,j+n);j+=n;return s}let c=get(),x=get(),t=BigInt("0b"+get());if(!/^0*$/.test(w.slice(j)))throw Error("pad");return {c,x,t}}
 function accept(x,t){let state=0,i=0;for(let j=0;j<t;j++){let a=i<x.length?Number(x[i])+1:0;let r=rules.find(r=>r[0]===state&&r[1]===a&&r[2]===0);if(!r)return false;state=r[3];if(state===1)return true;if(r[6]===1)i++}return false}
 let controls=[];for(let m of [1,2,4,8,16,32,64,128,256,512,1024,2048]){let x="0".repeat(m-1)+"1",y="0".repeat(m),a=enc(x,m+1),b=enc(y,m+1);for(let [w,v] of [[a,true],[b,false],[enc(x,m),false]]){let z=parse(w);assert(z.c===code);assert(z.t<=BigInt(w.length)**2n);assert(accept(z.x,Number(z.t))===v)}assert(a.length===b.length);controls.push({m,N:a.length,clock:m+1})}
 const S=5,subs=[0,1,4,5];let monotone=0,antitone=0,both=0,falseAccept=0,falseReject=0,nonmonotone=0,filterChecks=0;
 for(let root=0;root<3;root++)for(let q0=0;q0<3;q0++)for(let q1=0;q1<3;q1++)for(let leaf=0;leaf<16;leaf++){
  const run=mask=>{let a=(mask>>root)&1,q=a?q1:q0,b=(mask>>q)&1;return (leaf>>(2*a+b))&1};
  const values=Array.from({length:8},(_,j)=>run(j));let inc=true,dec=true;for(let a=0;a<8;a++)for(let b=0;b<8;b++)if((a&b)===a){if(values[a]>values[b])inc=false;if(values[a]<values[b])dec=false}
  let fa=!run(S)&&subs.some(j=>run(j)),fr=!!run(S)&&subs.some(j=>!run(j));
  if(inc)monotone++;if(dec)antitone++;if(inc&&dec)both++;if(!inc&&!dec)nonmonotone++;if(fa)falseAccept++;if(fr)falseReject++;assert(!inc||!fa);assert(!dec||!fr);
  for(let known=0;known<8;known++){let allowed=subs.filter(j=>((j^S)&known)===0);assert(allowed.includes(S));if(known===7)assert(allowed.length===1);filterChecks++}
 }
 return {checks,controls,controllers:432,monotone,antitone,both,nonmonotone,falseAccept,falseReject,filterChecks,limitations:"Actual encoded two-tape last-bit controls; abstract depth-two oracle decision trees with three query identities, not an implementation of the diagonal compiler or hierarchy theorem."}
}
console.log(JSON.stringify(audit(),null,2));
