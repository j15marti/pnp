function main(){
 const M={gauss:0,pairAttempts:0,massQueries:0,closureSweeps:0,pins:0,conditionalChoices:0,referenceWords:0,assertions:0,peakKeys:0,energyQueries:0};
 const p2=n=>1n<<BigInt(n),low=x=>x&-x,par=x=>{let b=0n;while(x){b^=1n;x&=x-1n;}return b;};
 function ck(v){M.assertions++;if(!v)throw Error("assert "+M.assertions);}
 function canon(rows){M.gauss++;let a=[];for(let [v,b] of rows){for(let [w,c] of a)if(v&low(w)){v^=w;b^=c;}if(!v){if(b)return null;continue;}let p=low(v);a=a.map(([w,c])=>w&p?[w^v,c^b]:[w,c]);a.push([v,b]);a.sort((x,y)=>low(x[0])<low(y[0])?-1:1);}return a;}
 const key=a=>a.map(([v,b])=>v.toString(16)+":"+b).join(",");
 function combine(ts){let a=new Map;for(let [r,c] of ts){if(r===null||!c)continue;let k=key(r);a.set(k,[r,c+(a.get(k)?.[1]??0n)]);}let t=[...a.values()].filter(x=>x[1]);M.peakKeys=Math.max(M.peakKeys,t.length);return t;}
 const one=[[[],1n]];
 function prod(a,b){if(a.length*b.length>200000)throw Error("cap");let t=[];for(let [u,c] of a)for(let [v,d] of b){M.pairAttempts++;t.push([canon([...u,...v]),c*d]);}return combine(t);}
 function mass(t,n,g=[]){M.massQueries++;let s=0n;for(let [a,c] of t){let q=canon([...a,...g]);if(q)s+=c*p2(n-q.length);}return s;}
 function val(t,x){return t.reduce((s,[a,c])=>s+(a.every(([v,b])=>par(v&x)===b)?c:0n),0n);}
 function project(t,m){return combine(t.map(([a,c])=>{let z=a.filter(([v])=>low(v)>=p2(m)).map(([v,b])=>[v>>BigInt(m),b]);return [z,c*p2(m-a.length+z.length)];}));}
 function bool(f,d){let powers=[one],s=[p2(d)];for(let j=1;j<=5;j++){powers.push(prod(powers[j-1],f));s.push(mass(powers[j],d));}let [_,a,b,c,e,h]=s;if(!a)return {t:[],den:1n};let D=a*c-b*b;
 if(D===0n){ck(a*e===b*c&&a*h===c*c);return {t:combine(f.map(([r,v])=>[r,v*a])),den:b};}
 let u=b*c-a*e,v=b*e-c*c; // solve b*u+c*v=-a with corrected determinant below
 // Matrix [[b,c],[c,e]], RHS [-a,-b].
 D=b*e-c*c;u=-a*e+b*c;v=-b*b+a*c;
 if(!D||c*u+e*v!==-b*D||b*u+c*v!==-a*D||e*u+h*v!==-c*D)return null;
 if(D<0n){D=-D;u=-u;v=-v;}
 return {t:combine([...f.map(([r,z])=>[r,-u*z]),...powers[2].map(([r,z])=>[r,-v*z])]),den:D};
 }
 function close(t,n,g=[]){let q=canon(g);if(!q)return null;while(true){M.closureSweeps++;if(!mass(t,n,q))return null;let found=false;for(let i=0;i<n;i++){let a=canon([...q,[p2(i),0n]]),b=canon([...q,[p2(i),1n]]);if(!a||!b)continue;if(!mass(t,n,a)){q=b;found=true;}else if(!mass(t,n,b)){q=a;found=true;}if(found){M.pins++;break;}}if(!found)return q;}}
 function witness(t,n,g=[]){let q=close(t,n,g);if(!q)return null;for(let i=0;i<n;i++){let a=canon([...q,[p2(i),0n]]),b=canon([...q,[p2(i),1n]]);if(!a||!b)continue;M.conditionalChoices++;q=close(t,n,mass(t,n,a)>0n?a:b);ck(q!==null);}let x=q.reduce((s,[v,b])=>s|(b?low(v):0n),0n);ck(val(t,x)>0n);return x;}
 function nullbasis(a,n){let piv=new Set(a.map(([v])=>low(v).toString())),b=[];for(let i=0;i<n;i++)if(!piv.has(p2(i).toString())){let v=p2(i);for(let [r] of a)if(r&p2(i))v|=low(r);b.push(v);}return b;}
 const particular=a=>a.reduce((x,[v,b])=>x|(b?low(v):0n),0n);
 function chars(a,n,p){let u=p;for(let [r] of a)if(u&low(r))u^=r;return u?0n:(par(p&particular(a))?-1n:1n)*p2(n-a.length);}
 function rankspace(t,n){let fft=t.map(([a,c])=>({g:nullbasis(a,n).map(v=>[v,0n]),p:particular(a),c:c*p2(n-a.length)})),pairs=[];for(let f of fft)for(let g of fft){M.pairAttempts++;pairs.push({a:canon([...f.g,...g.g]),p:f.p^g.p,c:f.c*g.c});}
 function energy(q){M.energyQueries++;let s=0n;for(let v of pairs){let a=canon([...v.a,...q]);if(a)s+=v.c*chars(a,n,v.p);}ck(s>=0n);return s;}
 let B=[];while(true){let h=null;for(let v of nullbasis(B,n))if(energy([[v,1n]])>0n){h=v;break;}if(h===null)return B;let q=[[h,1n]],w=0n;for(let j=0;j<n;j++){let test=[...q,[p2(j),0n]];if(energy(test)>0n)q=test;else{q.push([p2(j),1n]);w|=p2(j);}}B=canon([...B,[w,0n]]);}}
 function direct(arr,d){let a=[];for(let w=0;w<2**d;w++){let s=0n;for(let x=0;x<arr.length;x++)s+=(par(BigInt(w&x))?-arr[x]:arr[x]);if(s)a.push([BigInt(w),0n]);}return canon(a);}
 let rows=[],fano=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]];
 function check(label,t,m,d,ref){let n=m+d,root=close(t,n),f=project(t,m),a=Array.from({length:2**d},()=>0n);for(let x=0;x<2**n;x++){M.referenceWords++;let b=ref(x)?1n:0n;ck(val(t,BigInt(x))===b);a[x>>m]+=b;}for(let z=0;z<a.length;z++)ck(val(f,BigInt(z))===a[z]);let k=new Set(a.filter(x=>x).map(String)).size,B=bool(f,d),total=a.reduce((x,y)=>x+y,0n);ck(!!B===(k<=2));ck(!!root===(total>0n));let rank=null,projected=a.filter(x=>x).length;if(B){let b=a.map(x=>x?1n:0n);for(let z=0;z<b.length;z++)ck(val(B.t,BigInt(z))===B.den*b[z]);let r=rankspace(B.t,d);ck(key(r)===key(direct(b,d)));rank=r.length;ck(mass(B.t,d)===B.den*BigInt(projected));if(projected){let z=a.findIndex(x=>x>0n),g=Array.from({length:d},(_,i)=>[p2(m+i),BigInt(z>>i&1)]);let x=witness(t,n,g);ck(x!==null&&ref(Number(x)));}}
 rows.push({label,sourceModels:String(total),projected,distinct:k,rank,certified:!!B});}
 for(let skip=-1;skip<14;skip++){let t=one;for(let i=0;i<14;i++)if(i!==skip)t=prod(t,[[[],1n],[canon(fano[i>>1].map(j=>[p2(j),BigInt(i&1)])),-1n]]);check("Fano "+skip,t,4,3,x=>fano.every((e,j)=>[0,1].every(b=>2*j+b===skip||!e.every(i=>(x>>i&1)===b))));}
 for(let mask=0;mask<256;mask++){let t=one;for(let x=0;x<8;x++)if(mask>>x&1)t=prod(t,[[[],1n],[canon([0,1,2].map(i=>[p2(i),BigInt(x>>i&1)])),-1n]]);check("cube "+mask,t,1,2,x=>!(mask>>x&1));}
 // A real private fiber with count depending on every exterior bit, but support depending on two.
 let scale=[];for(let d of [4,8,16,32]){let m=d+1,n=m+d,A=canon([[p2(m),0n],[p2(m+1),0n]]),W=canon(Array.from({length:d-2},(_,i)=>[p2(m+i+2),0n]));let t=prod([[[],1n],[A,-1n]],[[[[1n,0n]],1n],[canon([[1n,1n],...W]),1n]]);
 ck(close(t,n)!==null);let f=project(t,m),B=bool(f,d);ck(B!==null);let E=canon([[1n,0n],[2n,0n]]);let residual=combine([...B.t,[[], -B.den],[E,B.den]]);ck(mass(prod(residual,residual),d)===0n);let rank=d<=8?rankspace(B.t,d).length:2;ck(rank===2);let x=p2(m);ck(val(t,x)===1n);scale.push({d,m,positiveFiberCounts:[String(p2(m-1)),String(p2(m))],supportRank:rank,countRankAnalytical:d,projected:String(mass(B.t,d)/B.den),countTerms:f.length,supportTerms:B.t.length,rankMethod:d<=8?"energy":"exact identity and analytic rank"});}
 let hostile=[];for(let d of [2,4,8]){let f=combine([[[],1n],...Array.from({length:d},(_,i)=>[[[p2(i),1n]],p2(i)])]);ck(bool(f,d)===null);hostile.push({d,distinct:String(p2(d)),declined:true});}
 return {summary:{cases:rows.length,sourceSAT:rows.filter(x=>x.sourceModels!=="0").length,sourceUNSAT:rows.filter(x=>x.sourceModels==="0").length,certified:rows.filter(x=>x.certified).length,unknown:rows.filter(x=>!x.certified).length,certifiedSAT:rows.filter(x=>x.certified&&x.sourceModels!=="0").length},meter:M,scale,hostile,rows};
}
console.log(JSON.stringify(main(),null,2));
