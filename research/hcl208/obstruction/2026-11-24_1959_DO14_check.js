"use strict";
function run(){
 let seed=0xD0142026; const rnd=n=>{seed^=seed<<13;seed^=seed>>>17;seed^=seed<<5;return (seed>>>0)%n};
 let out={seed:"0xD0142026",cases:0,guards:0,model_checks:0,closure_scans:0,owner_checks:0,insertions:0,assertions:0,neighbor_comparisons:0,root_controls:[],max_amplification:0,hostile:null};
 function ok(c){out.assertions++;if(!c)throw Error("assertion "+out.assertions)}
 const parity=x=>{let p=0;while(x){x&=x-1;p^=1}return p};
 function reduce(B,r,b=0){for(let i=B.length-1;i>=0;i--)if((r>>i&1)&&B[i]){r^=B[i][0];b^=B[i][1]}return [r,b]}
 function add(B,r,b=0){[r,b]=reduce(B,r,b);if(!r)return b?-1:0;B[31-Math.clz32(r)]=[r,b];return 1}
 const rank=B=>B.filter(Boolean).length, clone=B=>B.slice(), make=n=>Array(n).fill(null);
 const rows=e=>[(1<<e[0])^(1<<e[1]),(1<<e[0])^(1<<e[2])];
 function envelope(B,E){let C=make(B.length);for(let x of B)if(x)add(C,x[0]);let mark=new Set(),change=true;
 while(change){change=false;for(let i=0;i<E.length;i++){if(mark.has(i))continue;let [a,b]=rows(E[i]);if([a,b,a^b].some(r=>!reduce(C,r)[0])){mark.add(i);add(C,a);add(C,b);change=true;break}}}return {C,mark}}
 function close(B,E,S){let C=clone(B),steps=0,trace=[];for(;;){out.closure_scans++;let change=false;
 for(let i=0;i<E.length;i++){out.owner_checks++;let [a,b]=rows(E[i]),allowed=[];for(let w=0;w<4;w++){if(w===S[i])continue;let T=clone(C);if(add(T,a,w&1)>=0&&add(T,b,w>>1)>=0)allowed.push(w)}
 if(!allowed.length)return {bad:true,C,steps,trace:trace.concat([[i,"bad"]])};
 for(let j=1;j<=3;j++){let val=parity(j&allowed[0]);if(!allowed.every(w=>parity(j&w)===val))continue;let r=(j&1?a:0)^(j&2?b:0);let z=add(C,r,val);ok(z>=0);if(z){out.insertions++;steps++;trace.push([i,r,val]);change=true;break}}
 if(change)break}if(!change)return {bad:false,C,steps,trace}}}
 function fits(B,x){return B.every(t=>!t||parity(t[0]&x)===t[1])}
 function sat(E,S,x){return E.every((e,i)=>{let [a,b]=rows(e);return (parity(a&x)+2*parity(b&x))!==S[i]})}
 function models(n,E,S,B){let M=[];for(let x=0;x<1<<n;x++){out.model_checks++;if(fits(B,x)&&sat(E,S,x))M.push(x)}return M}
 function threshold(n,E){let t=E.length;for(let mask=1;mask<1<<E.length;mask++){let j=0,B=make(n);for(let i=0;i<E.length;i++)if(mask>>i&1){j++;for(let r of rows(E[i]))add(B,r)}if(2*rank(B)<3*j)t=Math.min(t,j-1)}return t}
 function audit(n,E,S,B,t,doNeighbors){out.guards++;let h=rank(B),env=envelope(B,E),cl=close(B,E,S),M=models(n,E,S,B);ok(cl.bad?M.length===0:JSON.stringify(M)===JSON.stringify(models(n,E,S,cl.C)));ok(cl.trace.every(z=>env.mark.has(z[0])));ok(cl.C.every(z=>!z||!reduce(env.C,z[0])[0]));ok(rank(env.C)<=h+env.mark.size);if(2*h<t){ok(env.mark.size<=2*h);ok(rank(env.C)<=3*h)}if(h)out.max_amplification=Math.max(out.max_amplification,rank(env.C)/h);
 if(doNeighbors)for(let i=0;i<E.length;i++)if(!env.mark.has(i)){for(let f=1;f<=3;f++){let V=S.slice();V[i]^=f;let c2=close(B,E,V);ok(JSON.stringify(cl)===JSON.stringify(c2));out.neighbor_comparisons++}}return {h,t,q:env.mark.size,final:rank(cl.C),envRank:rank(env.C),bad:cl.bad,models:M.length}}
 const fano=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]], F=Array(7).fill(0),t=threshold(7,fano);
 out.root_controls.push(audit(7,fano,F,make(7),t,true));for(let i=0;i<7;i++)for(let j=1;j<=3;j++){let s=F.slice();s[i]=j;let a=audit(7,fano,s,make(7),t,false);ok(a.models===10);out.root_controls.push(a)}
 for(let z=0;z<80;z++){let n=7+rnd(4),E=[];for(let k=0;k<100&&E.length<8;k++){let e=[rnd(n),rnd(n),rnd(n)].sort((a,b)=>a-b);if(new Set(e).size!==3||E.some(q=>q.filter(x=>e.includes(x)).length>1))continue;E.push(e)}
 let S=E.map(()=>rnd(4)),t=threshold(n,E);out.cases++;
 for(let k=0;k<6;k++){let B=make(n),x=rnd(1<<n),h=k%4;while(rank(B)<h){let r=1+rnd((1<<n)-1);add(B,r,parity(r&x))}audit(n,E,S,B,t,k<3)}}
 for(let k=0;k<128;k++){let B=make(7);let x=rnd(128),h=k%3;while(rank(B)<h){let r=1+rnd(127);add(B,r,parity(r&x))}audit(7,fano,F,B,t,true)}
 let n=12,E=Array.from({length:10},(_,i)=>[0,1,i+2]),B=make(n);add(B,3,0);out.hostile=audit(n,E,E.map(()=>0),B,threshold(n,E),false);ok(out.hostile.final===11);
 return out
}
console.log(JSON.stringify(run(),null,2));
