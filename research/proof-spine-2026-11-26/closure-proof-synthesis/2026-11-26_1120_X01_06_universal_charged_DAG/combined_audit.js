console.log(JSON.stringify((function combined(){
 let checks=0,pairs=0,yes=0,no=0,lifts=0;
 const ok=(x,msg="")=>{if(!x)throw Error("check "+checks+" "+msg);checks++};
 const lit=(l,x)=>Boolean(x[Math.abs(l)])===(l>0),sat=(C,x)=>C.every(c=>c.some(l=>lit(l,x)));
 const bits=(x,n)=>Array.from({length:n},(_,i)=>(x>>i)&1);
 const gamma=x=>{const b=x.toString(2);return "0".repeat(b.length-1)+b};
 const rows=(C,n)=>{const w=Math.ceil(Math.log2(n+1));return C.map(c=>c.map(l=>(l>0?"1":"0")+Math.abs(l).toString(2).padStart(w,"0")).join("")).join("")};
 const head=(n,m)=>"1".repeat(n)+"0"+gamma(m+1);
 const pins=(x,a,b,t)=>[[t?x:-x,a,b],[t?x:-x,a,-b],[t?x:-x,-a,b],[t?x:-x,-a,-b]];
 function build(u,v){
  const k=u.length,L=[],M=[],R=[];
  for(let i=0;i<k;i++){
   L.push(...pins(i+1,k+2*i+1,k+2*i+2,u[i]));
   M.push([5*k+3*i+1,5*k+3*i+2,5*k+3*i+3]);
   R.push(...pins(i+1,3*k+2*i+1,3*k+2*i+2,v[i]));
  }
  const src=[...L,...M,...R],n0=8*k,m0=src.length,n=n0+m0+3,U=n-1,V=n,p=1;
  const F=[];src.forEach((c,j)=>{const [a,b,c0]=c.map(l=>Math.sign(l)*(Math.abs(l)+1)),y=n0+j+2;F.push([-p,a,y],[-y,b,c0])});
  F.push([p,U,V],[p,U,-V],[p,-U,V],[p,-U,-V]);
  const S=Array(n+1).fill(0);S[U]=S[V]=1;
  ok(sat(F.slice(0,-1),S)&&!sat(F,S));
  ok(F.every(c=>c.length===3&&new Set(c.map(Math.abs)).size===3&&c.every(l=>Math.abs(l)<=n)));
  const expected=u.every((x,i)=>x===v[i]);
  if(expected){
   const a=Array(n0+1).fill(0);for(let i=0;i<k;i++){a[i+1]=u[i];a[5*k+3*i+1]=1}ok(sat(src,a));const w=Array(n+1).fill(0);w[p]=1;
   for(let i=1;i<=n0;i++)w[i+1]=a[i];
   src.forEach((c,j)=>w[n0+j+2]=lit(c[0],a)?0:1);
   ok(sat(F,w));lifts++;
  }else{
   const i=u.findIndex((x,i)=>x!==v[i]);ok(i>=0&&L[4*i][0]===-R[4*i][0]); // exact pin contradiction
  }
  const l=rows(F.slice(0,8*k),n),mid=rows(F.slice(8*k,10*k),n),r=rows(F.slice(10*k),n),h=head(n,F.length);
  return {n,m:F.length,l,mid,r,h,N:h.length+l.length+mid.length+r.length,Nminus:head(n,F.length-1).length+rows(F.slice(0,-1),n).length,expected};
 }
 for(let k=1;k<=5;k++){
  let lmap=new Map(),rmap=new Map(),mid,h,N;
  for(let a=0;a<2**k;a++)for(let b=0;b<2**k;b++){
   const z=build(bits(a,k),bits(b,k));ok(z.expected===(a===b));
   if(!lmap.has(a))lmap.set(a,z.l);else ok(lmap.get(a)===z.l);
   if(!rmap.has(b))rmap.set(b,z.r);else ok(rmap.get(b)===z.r);
   if(mid===undefined){mid=z.mid;h=z.h;N=z.N}
   ok(z.mid===mid&&z.h===h&&z.N===N);
   pairs++;if(z.expected)yes++;else no++;
  }
  ok(new Set(lmap.values()).size===2**k&&new Set(rmap.values()).size===2**k);
 }
 const scales=[];
 for(let k of [8,32,128,512,2048]){
  const u=Array.from({length:k},(_,i)=>+(i%3===0)),v=u.slice();v[k-1]^=1;
  const a=build(u,u),b=build(u,v);ok(a.expected&&!b.expected&&a.h===b.h&&a.l===b.l&&a.mid===b.mid&&a.r!==b.r&&a.N===b.N);
  scales.push({k,finalVariables:a.n,finalClauses:a.m,penultimateBits:a.Nminus,finalBits:a.N,commonGapBits:a.mid.length,entropyBits:k});
 }
 return{checks,pairs,yes,no,lifts,scales}
})(),null,2));
