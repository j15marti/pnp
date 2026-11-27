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
 let results=[];for(let r of [3,4,8,16,32,64,128,256]){let f=Array.from({length:r},(_,i)=>i+1),o=encode(f,f),N=o.bits.length;assert(N===3*o.n+2+2*Math.floor(Math.log2(o.m+1))+3*o.m*(o.w+1)+o.w,"N");assert(decode(o.bits).unsat,"diagonal");
 let D=6*(r-2)*(o.w+1)-1,h=Array.from({length:r},(_,i)=>Math.log2(i+1)).reduce((a,b)=>a+b,0),positions=new Set(),tested=0,candidates=0,travel=0,head=0;
 // For both copies of each map field, use same changed ID bit in both padded occurrences.
 // One coordinate per group must be queried by an exact bit-probe algorithm.
 for(let side of [0,1])for(let i=0;i<r;i++)for(let b=0;b<o.w;b++){let j=((r+f[i])^(1<<b))-r;if(j<1||j>r)continue;let k=side?6*r+1+4*i:5+4*i;let a=bitpos(o,k,b),q=bitpos(o,k+2,b);assert(!positions.has(a)&&!positions.has(q)&&a!==q,"disjoint group");positions.add(a);positions.add(q);candidates++;
 if(r<=64||tested<24){let ff=f.slice(),gg=f.slice();(side?gg:ff)[i]=j;let t=encode(ff,gg);let dif=[];for(let k=0;k<N;k++)if(o.bits[k]!==t.bits[k])dif.push(k);assert(dif.length===2&&dif.includes(a)&&dif.includes(q),"exact two bit perturbation");let dec=decode(t.bits);assert(dec&&!dec.unsat,"offdiag recognition");witness(ff,gg);tested++;}}
 // Fixed read schedule of first copies for all map field bits; on a read-only tape
 // head motion charged, no claims about parser or actual complete TM.
 for(let i=0;i<r;i++)for(let b=0;b<o.w;b++)for(let k of [5+4*i,6*r+1+4*i]){let p=bitpos(o,k,b);travel+=Math.abs(p-head);head=p;}travel+=head;
 let bad=o.bits.slice(0,-1)+(o.bits.endsWith("0")?"1":"0");assert(decode(bad)===null,"malformed release");let alpha=[0,...o.alpha].map(Number),beta=[0,...o.beta].map(Number);let fails=a=>o.cls.filter(q=>!q.some(l=>a[Math.abs(l)]===(l>0?1:0))).length;assert(fails(alpha)===1&&fails(beta)===1,"adjacent witnesses");
 results.push({r,N,D,h,groups:candidates,tested,readOnlyHeadTravel:travel,readOnlySpanTimesTravel:N*travel,staticRatio:D*h/(N*N/8),expectedMinProbes:r>3?2*(r-1)*(Math.log2(r))-2*Math.log2(r):null});}
 // Exact MFC-13 source sumset and T2 syzygy check, using original plane vectors.
 let H=[15,32,13,17,14,36,11,53,10,39],count=Array(64).fill(0);for(let i=0;i<243;i++){let j=i,t=0;for(let k=0;k<5;k++){let s=j%3+1;j=Math.floor(j/3);if(s&1)t^=H[2*k];if(s&2)t^=H[2*k+1];}count[t]++;}
 assert(count.reduce((a,b)=>a+b,0)===243&&count[29]===0,"MFC hole");
 const masks=[1,5,8,2,12,15,1,2,4,8],offsets=[1,0,1,1,1,0,0,0,0,0],parity=x=>{let p=0;while(x){p^=x&1;x>>=1;}return p;};
 let words=0;for(let z=0;z<16;z++){let x=masks.map((m,i)=>parity(m&z)^offsets[i]);let t=x.reduce((a,b,i)=>a^(b?H[i]:0),0);assert(t===29,"chart");let f=Array.from({length:5},(_,i)=>(1^x[2*i])&(1^x[2*i+1]));let [a,b,c,d]=[z&1,(z>>1)&1,(z>>2)&1,(z>>3)&1];let val=((b^d^(b&d))&f[0])^((a^c)&f[1])^f[2]^((c^d^(c&d))&f[3])^f[4];assert(val===1,"syzygy");words++;}
 return {results,mfc:{total:243,hole:count[29],otherHoles:count.map((v,i)=>v?null:i).filter(v=>v!==null),chartWords:words}};
}
console.log(JSON.stringify(transport(),null,2));
