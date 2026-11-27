function transport(){
 const assert=(x,m)=>{if(!x)throw Error(m)};
 function source(f,g){let r=f.length,p=2*r+1,c=[];for(let i=0;i<r;i++)for(let s of [1,-1])c.push([-(i+1),r+f[i],s*p]);if(r===3)c.push([1,2,3]);else{c.push([1,2,p+1]);for(let j=1;j<=r-4;j++)c.push([-(p+j),j+2,p+j+1]);c.push([-(p+r-3),r-1,r]);}for(let i=0;i<r;i++)for(let s of [1,-1])c.push([-(i+1),-(r+g[i]),s*p]);return c;}
 function compile(f,g){let r=f.length,n0=3*r-2,y=n0+1,u=y+1,v=y+2,c=[];for(let a of [1,-1])for(let b of [1,-1])c.push([y,a*u,b*v]);source(f,g).forEach(([a,b,d],i)=>{let z=v+1+i;c.push([-y,a,z],[-z,b,d]);});return c;}
 function encode(f,g){let r=f.length,n=8*r-1,m=10*r,w=Math.ceil(Math.log2(n+1)),y=3*r-1,u=y+1,v=y+2;
 let gamma=(m+1).toString(2),header="1".repeat(n)+"0"+"0".repeat(gamma.length-1)+gamma,cls=compile(f,g);assert(cls.length===m,"m");
 let alpha=Array.from({length:n},(_,i)=>i+1===u?"1":"0").join(""),beta=Array.from({length:n},(_,i)=>i+1===u||i+1===v?"1":"0").join("");
 let body=cls.flatMap(c=>c.map(l=>(l<0?"1":"0")+Math.abs(l).toString(2).padStart(w,"0"))).join("");
 return {bits:header+body+alpha+beta+y.toString(2).padStart(w,"0"),cls,n,m,w,header:header.length,alpha,beta,y};}
 function decode(bits){let i=0;while(bits[i]==="1")i++;let n=i++;let z=0;while(bits[i]==="0"){z++;i++;}let m=parseInt(bits.slice(i,i+z+1),2)-1;i+=z+1;let r=(n+1)/8,w=Math.ceil(Math.log2(n+1));if(!Number.isInteger(r)||r<3||m!==10*r)return null;let c=[];for(let k=0;k<m;k++){let q=[];for(let j=0;j<3;j++){let s=bits[i++],l=parseInt(bits.slice(i,i+w),2);i+=w;q.push(s==="1"?-l:l);}c.push(q);}
 let f=[],g=[];for(let j=0;j<r;j++){f.push(c[5+4*j][1]-r);g.push(-c[6*r+1+4*j][1]-r);}if(f.concat(g).some(x=>x<1||x>r)||encode(f,g).bits!==bits)return null;return {f,g,unsat:f.every((x,j)=>x===g[j])};}
 function evalC(c,a){return c.every(q=>q.some(l=>a[Math.abs(l)]===(l>0?1:0)))}
 function witness(f,g){let r=f.length,n=8*r-1,n0=3*r-2,y=n0+1,u=y+1,v=y+2,j=f.findIndex((x,i)=>x!==g[i]);assert(j>=0,"offdiag");let a=new Uint8Array(n+1);a[j+1]=1;a[r+f[j]]=1;a[y]=1;for(let k=1;k<=r-3;k++)a[2*r+1+k]=Number(j+1>k+1);let s=source(f,g);assert(evalC(s,a),"source witness");for(let k=0;k<s.length;k++)a[v+1+k]=Number(a[Math.abs(s[k][0])]!==(s[k][0]>0?1:0));assert(evalC(compile(f,g),a),"target witness");return a;}
 function bitpos(o,k,b){return o.header+(3*k+1)*(o.w+1)+1+(o.w-1-b);}
 return {encode,decode,witness,bitpos};
}

function accessAudit(){
 const {encode,decode,witness,bitpos}=transport(),out=[];
 for(let r of [4,8,16,32,64,128,256]){
 let f=Array.from({length:r},(_,i)=>i+1),g=f.slice();[g[0],g[1]]=[g[1],g[0]];
 let yes=encode(f,g),no=encode(f,f),N=no.bits.length;
 if(!decode(no.bits).unsat||decode(yes.bits).unsat)throw Error("labels");witness(f,g);
 let L=[],R=[];for(let i=0;i<r;i++)for(let b=no.w-1;b>=0;b--){L.push(bitpos(no,5+4*i,b));R.push(bitpos(no,6*r+1+4*i,b))}
 let D=6*(r-2)*(no.w+1)-1,M=L.length;
 if(Math.min(...R)-Math.max(...L)<D)throw Error("cuts");
 for(let B of [...new Set([1,8,64,512,M].map(x=>Math.min(x,M)))]){
 let travel=0,head=0,cross=0,cut=Math.max(...L),bitReads=0,peak=0;
 const read=(p,bits)=>{travel+=Math.abs(p-head);if((head<=cut)!==(p<=cut))cross++;head=p;bitReads++;return bits[p]};
 for(let j=0;j<M;j+=B){let a=[];for(let k=j;k<Math.min(j+B,M);k++)a.push(read(L[k],no.bits));peak=Math.max(peak,a.length);for(let k=j;k<Math.min(j+B,M);k++)if(a[k-j]!==read(R[k],no.bits))throw Error("diag")}
 if(cross!==2*Math.ceil(M/B)-1)throw Error("crossings");out.push({r,N,D,M,B,readOnlyTravel:travel,centralCrossings:cross,bitReads,peakBuffer:peak,randomAccessReads:M,randomAccessLocalTravel:L.at(-1),remoteCutDistance:D*M});
 }
 // Independent both-label field comparison.
 if(L.every((p,i)=>yes.bits[p]===yes.bits[R[i]]))throw Error("neighbor not detected");
 }
 return out
}


function fingerprintAudit(transport){
 const {encode,decode,witness}=transport(), prime=n=>{for(let p=n;;p++){let ok=true;for(let q=2;q*q<=p;q++)if(p%q===0){ok=false;break}if(ok)return p}},hash=(a,x,p)=>a.reduce((h,v)=>(h*x+v)%p,0);
 function perms(a){if(a.length===0)return [[]];return a.flatMap((x,i)=>perms(a.filter((_,j)=>j!==i)).map(y=>[x,...y]))}
 let seed=314159265;function rnd(n){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n}
 function shuffle(r){let a=Array.from({length:r},(_,i)=>i+1);for(let i=r-1;i>0;i--){let j=rnd(i+1);[a[i],a[j]]=[a[j],a[i]]}return a}
 let out=[];
 for(let r of [4,8,16,32,64,128,256]){let p=prime(4*r),base=Array.from({length:r},(_,i)=>i+1),pairs=[];
 if(r===4){let P=perms(base);for(let f of P)for(let g of P)pairs.push([f,g])}
 else for(let i=0;i<30;i++){let f=shuffle(r),g=f.slice();pairs.push([f,f]);let a=rnd(r),b=(a+1+rnd(r-1))%r;[g[a],g[b]]=[g[b],g[a]];pairs.push([f,g]);pairs.push([f,shuffle(r)])}
 let same=0,diff=0,points=0,maxRoots=0,totalRoots=0,exactMismatches=0,witnesses=0;
 for(let [f,g] of pairs){let eq=f.every((v,i)=>v===g[i]);if(eq)same++;else diff++;
 let roots=0;for(let x=0;x<p;x++){points++;if(hash(f,x,p)===hash(g,x,p))roots++}
 if(eq?roots!==p:roots>r-1)throw Error("root bound");
 if(!eq){maxRoots=Math.max(maxRoots,roots);totalRoots+=roots}
 let exact=true;for(let x=0;x<r;x++)if(hash(f,x,p)!==hash(g,x,p)){exact=false;break}
 if(exact!==eq)throw Error("exact evaluator");
 // Authenticate both labels and witness for sample per size, exhaustive at r=4.
 if(r===4||witnesses<5){let d=decode(encode(f,g).bits);if(d.unsat!==eq)throw Error("encoding");if(!eq){witness(f,g);witnesses++}}
 }
 let N=encode(base,base).bits.length,h=Array.from({length:r},(_,i)=>Math.log2(i+1)).reduce((a,b)=>a+b,0);
 out.push({r,N,p,fieldBits:Math.ceil(Math.log2(p)),pairs:pairs.length,diagonal:same,offDiagonal:diff,points,maxRoots,totalRoots,averageCollision:totalRoots/(diff*p),theoremMaxError:(r-1)/p,exactMismatches,witnesses,onePassMemoryBits:Math.ceil(h),fourSweepMemoryBits:Math.ceil(h/4)});
 }return out
}
console.log(JSON.stringify({replay:accessAudit(),fingerprint:fingerprintAudit(transport)},null,2));
