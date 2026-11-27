function run(){
 let checks=0;const ck=(v,s)=>{checks++;if(!v)throw Error("check "+checks+" "+s)};
 const mod=(x,d)=>((x%d)+d)%d;
 const val=x=>{let k=0;while(x%2===0){k++;x/=2}return k};
 function gcd(a,b){while(b)[a,b]=[b,a%b];return a}
 // Counts 1<=y<=H, y%2^j=0, (y+shift)%d=residue.
 function count(H,j,d,shift,residue){let P=2**j,g=gcd(P,d),r=mod(residue-shift,d);if(r%g)return 0;
 let D=d/g,c=0;while(c<D&&mod(P*c-r,d)!==0)c++;ck(c<D,"CRT");let y=P*c,period=P*D;if(y===0)y=period;return y>H?0:1+Math.floor((H-y)/period)}
 function machine(m,d,W){let B=Array.from({length:m},(_,k)=>Array.from({length:d},(_,shift)=>{
 let z=0;for(let j=0;j<k;j++)for(let r=0;r<d;r++)z+=(count(2**k-1,j,d,shift,r)-count(2**k-1,j+1,d,shift,r))*W[r][j];return z}));
 function step(k,rem,tz,bit){let z=0;if(bit){let shift=mod(rem*mod(2**(k+1),d),d);z=B[k][shift];if(tz>=0)z+=W[shift][k+1+tz]}
 return [mod(2*rem+bit,d),bit?0:tz<0?-1:tz+1,z]}
 function eval0(X){let rem=0,tz=-1,z=0;for(let k=m-1;k>=0;k--){let b=(X>>k)&1,[r,t,c]=step(k,rem,tz,b);rem=r;tz=t;z+=c}return z}
 return{step,eval0}}
 function direct(W,X){let z=0;for(let x=1;x<X;x++)z+=W[x%W.length][val(x)];return z}
 function joint(m,forms,U){let C=forms.map(f=>machine(m,f.W.length,f.W)),n=forms.length,M=new Map([["start",{s:Array.from({length:n},()=>[0,0,-1]),tight:1,z:0,u:0}]]),peak=1,trans=0;
 for(let k=m-1;k>=0;k--){let T=new Map();for(let R of M.values())for(let b=0;b<=1;b++){let ub=(U>>k)&1;if(R.tight&&b>ub)continue;let tight=R.tight&&b===ub?1:0;
 for(let bits=0;bits<2**n;bits++){trans++;let z=R.z,s=[],ok=true;for(let j=0;j<n;j++){let f=forms[j],[c,rem,tz]=R.s[j],v=(bits>>j)&1,c1=2*c+v-f.a*b-((f.b>>k)&1);if(Math.abs(c1)>Math.abs(f.a)+2){ok=false;break}let [r,t,w]=C[j].step(k,rem,tz,v);z+=w;s.push([c1,r,t])}if(!ok)continue;
 let key=[tight,...s.flat()].join(","),prev=T.get(key);if(!prev||z<prev.z)T.set(key,{s,tight,z,u:2*R.u+b})}}
 M=T;peak=Math.max(peak,M.size)}
 let best=null;for(let R of M.values())if(R.s.every(s=>s[0]===0)&&(!best||R.z<best.z))best=R;return{cost:best.z,u:best.u,peak,trans}}
 let seed=763199;const rnd=()=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed/4294967296};
 let prefix=0,joints=0,maxPeak=0,maxTrans=0,oddStrides=0;
 for(let z=0;z<60;z++){let m=4+z%4,d=1+z%7,W=Array.from({length:d},()=>Array.from({length:m},()=>Math.floor(21*rnd())-10)),M=machine(m,d,W);
 for(let x=0;x<2**m;x++){ck(M.eval0(x)===direct(W,x),"prefix");prefix++}
 if(d%2===1&&d>1)oddStrides++;
 let U=Math.floor((2**m-1)/4),forms=Array.from({length:3},(_,i)=>{let a=[1,-2,3][i],b=i===1?2*U:Math.floor(rnd()*(2**m-Math.abs(a)*U));return{a,b,W:Array.from({length:1+(z+i)%5},()=>Array.from({length:m},()=>Math.floor(15*rnd())-7))}});
 let J=joint(m,forms,U),best=Infinity;for(let u=0;u<=U;u++)best=Math.min(best,forms.reduce((s,f)=>s+direct(f.W,f.a*u+f.b),0));ck(J.cost===best,"joint");ck(forms.reduce((s,f)=>s+direct(f.W,f.a*J.u+f.b),0)===best,"backpointer");joints++;maxPeak=Math.max(maxPeak,J.peak);maxTrans=Math.max(maxTrans,J.trans)
 }
 return{checks,prefix,joints,oddStrides,maxPeak,maxTrans,scope:"general numerical-stride dyadic prefix machine and three signed affine endpoint functions, abstract controls only; JS Number safe for tested m<=7, proof uses binary integers for general m"}
}
console.log(JSON.stringify(run(),null,2));
