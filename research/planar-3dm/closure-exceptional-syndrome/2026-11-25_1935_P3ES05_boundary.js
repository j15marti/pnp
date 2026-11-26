/* P3ES05 color-bound audit; node.js */
const boundaryAudit=function boundaryAudit(){
 const result={cuts:0,rank2Productive:0,threeColorBoundaryCuts:0,twoBoundaryCuts:0,maxRank2Witness:null,bySource:[]};
 const bit=i=>1n<<BigInt(i),rank=V=>{const B=new Map();for(let v of V){while(v){const p=v.toString(2).length-1;if(B.has(p))v^=B.get(p);else{B.set(p,v);break}}}return B.size};
 const U="013 021 110 113 221 222 231 300 302 330",V=U+" 002",Q="001 010 011 100 101 110",C="000 001 010 011 100 101 110 111";
 for(const [name,s,n] of [["U",U,4],["V",V,4],["Q",Q,2],["octahedron",C,2]]){
 const T=s.split(" ").map(t=>[...t].map(Number)),m=T.length,A=T.map(t=>t.reduce((v,x,c)=>v|bit(c*n+x),0n)),t=bit(3*n)-1n,rt=rank(A.concat(t));let r2=0,b3=0,b2=0,max=-1,ex=null;
 for(let mask=1;mask<(1<<m)-1;mask++){
  const L=A.filter((_,i)=>mask&(1<<i)),R=A.filter((_,i)=>!(mask&(1<<i))),SL=L.reduce((a,b)=>a|b,0n),SR=R.reduce((a,b)=>a|b,0n),boundary=SL&SR,privateL=SL&~SR;
  const bs=Array.from({length:3*n},(_,i)=>i).filter(i=>boundary&bit(i));const b=bs.length;
  const P=[0,1,2].map(c=>{let p=0;for(let v=c*n;v<(c+1)*n;v++)if(privateL&bit(v))p^=1;return p});
  const h=[1,2].map(c=>bs.reduce((z,v,i)=>z^((Math.floor(v/n)===0||Math.floor(v/n)===c)?bit(i):0n),0n)^((P[0]^P[c])?bit(b):0n));
  const bound=b+1-rank(h),k=rank(L)+rank(R.concat(t))-rt;
  if(k>bound)throw Error("color bound");result.cuts++;max=Math.max(max,k);
  if(b===3&&new Set(bs.map(v=>Math.floor(v/n))).size===3){if(k>2)throw Error("three-color cut");b3++;result.threeColorBoundaryCuts++}
  if(b===2){if(k>2)throw Error("two-boundary cut");b2++;result.twoBoundaryCuts++}
  if(k===2&&L.length>=4){r2++;result.rank2Productive++;if(!ex||R.length>ex.R.length)ex={L:T.filter((_,i)=>mask&(1<<i)).map(t=>t.join("")),R:T.filter((_,i)=>!(mask&(1<<i))).map(t=>t.join("")),boundary:bs,bound,k}}
 }
 result.bySource.push({name,m,rank2Productive:r2,threeColorBoundaryCuts:b3,twoBoundaryCuts:b2,maxRank:max,example:ex});
 }
 return result
};
console.log(JSON.stringify(boundaryAudit(),null,2));
