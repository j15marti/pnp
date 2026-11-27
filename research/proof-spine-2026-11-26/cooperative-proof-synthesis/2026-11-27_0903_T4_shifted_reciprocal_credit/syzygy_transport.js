const audit2=function audit2(){
 const H=[15,32,13,17,14,36,11,53,10,39], parity=x=>{let y=0;while(x){x&=x-1;y^=1}return y}, target=29;
 let rows=Array.from({length:6},(_,i)=>H.reduce((a,h,j)=>a|(((h>>i)&1)<<j),0)|(((target>>i)&1)<<10));
 let piv=[],r=0;
 for(let c=0;c<10;c++){let j=rows.findIndex((x,i)=>i>=r&&((x>>c)&1));if(j<0)continue;[rows[r],rows[j]]=[rows[j],rows[r]];for(let i=0;i<6;i++)if(i!==r&&(rows[i]>>c&1))rows[i]^=rows[r];piv.push(c);r++;}
 const free=Array.from({length:10},(_,i)=>i).filter(x=>!piv.includes(x));
 let masks=Array(10).fill(0),offs=Array(10).fill(0);
 free.forEach((c,i)=>masks[c]=1<<i);
 piv.forEach((c,i)=>{offs[c]=rows[i]>>10&1;free.forEach((f,j)=>masks[c]|=((rows[i]>>f)&1)<<j)});
 let Si=Array.from({length:5},(_,i)=>[masks[2*i],masks[2*i+1],masks[2*i]^masks[2*i+1]]);
 let W=[1,8,12], span=new Set([0]);for(let w of W)for(let x of [...span])span.add(x^w);
 if(span.size!==8||Si.some(s=>!s.some(x=>x&&span.has(x))))throw Error("cover");
 let cap2nodes=0;function cover(S,k){cap2nodes++;let u=Si.find(s=>!s.some(x=>x&&S.has(x)));if(!u)return true;if(!k)return false;for(let x of u){let T=new Set(S);for(let a of S)T.add(a^x);if(cover(T,k-1))return true;}return false;}
 if(cover(new Set([0]),2))throw Error("unexpected rank2 cover");
 let branches=[],branchChecks=0;const f=(i,z)=>(1^offs[2*i]^parity(masks[2*i]&z))&(1^offs[2*i+1]^parity(masks[2*i+1]&z));
 for(let s=0;s<8;s++){let zs=Array.from({length:16},(_,z)=>z).filter(z=>W.every((w,i)=>parity(w&z)===(s>>i&1)));let cert=0;for(let c=1;c<32;c++){if(zs.every(z=>{let x=0;for(let i=0;i<5;i++)if(c>>i&1)x^=f(i,z);return x===1;})){cert=c;break;}}
 if(!cert)throw Error("no identity");branches.push({s,zs,owners:Array.from({length:5},(_,i)=>i+1).filter(i=>cert>>(i-1)&1)});}
 for(let z=0;z<16;z++){let sum=0;for(let b of branches)if(W.every((w,i)=>parity(w&z)===(b.s>>i&1)))for(let i of b.owners)sum^=f(i-1,z);if(sum!==1)throw Error("global identity");branchChecks++;}
 // Exact encoded permutation source, following the November 21 report eqs 8-22.
 function encoding(pi,sigma){
 let r=pi.length,n0=3*r-2,m0=5*r-2,n=8*r-1,m=10*r,w=Math.ceil(Math.log2(n+1)),p=2*r+1,y=n0+1,u=y+1,v=y+2;
 let C=[];const add=(a,b)=>{C.push([a,b,p],[a,b,-p]);};
 for(let i=1;i<=r;i++)add(-i,r+pi[i-1]);
 if(r===3)C.push([1,2,3]);else{C.push([1,2,2*r+2]);for(let j=1;j<=r-4;j++)C.push([-(2*r+1+j),j+2,2*r+2+j]);C.push([-n0,r-1,r]);}
 for(let i=1;i<=r;i++)add(-i,-(r+sigma[i-1]));
 let B=[[y,u,v],[y,u,-v],[y,-u,v],[y,-u,-v]];
 C.forEach(([a,b,c],i)=>{let z=v+i+1;B.push([-y,a,z],[-z,b,c]);});
 if(C.length!==m0||B.length!==m)throw Error("counts");
 const bits=(a,k)=>a.toString(2).padStart(k,"0"),gamma=a=>"0".repeat(Math.floor(Math.log2(a)))+a.toString(2);
 const alpha=Array.from({length:n},(_,i)=>i+1===u?"1":"0").join(""),beta=Array.from({length:n},(_,i)=>i+1===u||i+1===v?"1":"0").join("");
 return "1".repeat(n)+"0"+gamma(m+1)+B.flat().map(l=>(l<0?"1":"0")+bits(Math.abs(l),w)).join("")+alpha+beta+bits(y,w);
 }
 function recognize(s){
 let i=0,reads=0;function read(){if(i>=s.length)throw Error("eof");reads++;return Number(s[i++]);}function number(k){let x=0;while(k--)x=x*2+read();return x;}
 let n=0;while(read())n++;let zeros=0;while(!read())zeros++;let m=2**zeros+number(zeros)-1,r=(n+1)/8,w=Math.ceil(Math.log2(n+1));if(!Number.isInteger(r)||r<3||m!==10*r)return null;
 let B=[];for(let j=0;j<m;j++){let c=[];for(let k=0;k<3;k++){let sign=read(),x=number(w);c.push(sign?-x:x)}B.push(c);}
 let pi=[],sig=[];for(let j=0;j<r;j++){pi.push(B[5+4*j][1]-r);sig.push(-B[6*r+1+4*j][1]-r);}
 let perm=a=>new Set(a).size===r&&a.every(x=>x>=1&&x<=r);
 if(!perm(pi)||!perm(sig))return null;
 // Consume trailer, verify exact encoding from recovered maps.
 while(i<s.length)read();let candidate=encoding(pi,sig),compare=0;if(candidate.length!==s.length)return null;
 for(let j=0;j<s.length;j++){compare++;if(candidate[j]!==s[j])return null;}
 let checks=0,eq=true;for(let j=0;j<r;j++){checks++;if(pi[j]!==sig[j])eq=false;}
 return {N:s.length,reads,compare,mapComparisons:checks,unsat:eq};
 }
 let transport=[];
 for(let r of [3,4,8,16,32,64,128,256]){let p=Array.from({length:r},(_,i)=>r-i),q=[...p];[q[0],q[1]]=[q[1],q[0]];
 let s=encoding(p,p),a=recognize(s),b=recognize(encoding(p,q)),corrupt=s.slice(0,-1)+(s.endsWith("1")?"0":"1");
 if(!a?.unsat||b?.unsat!==false||recognize(corrupt)!==null)throw Error("transport");
 let n=8*r-1,m=10*r,w=Math.ceil(Math.log2(n+1)),N=3*n+2+2*Math.floor(Math.log2(m+1))+3*m*(w+1)+w;
 if(N!==s.length)throw Error("N");
 transport.push({r,...a,offDiagonal:b.unsat,corruptRejected:true});}
 return {freeColumns:free,masks,offs,Si,W,cap2nodes,branches,branchChecks,transport};
};
console.log(JSON.stringify(audit2(),null,2));
