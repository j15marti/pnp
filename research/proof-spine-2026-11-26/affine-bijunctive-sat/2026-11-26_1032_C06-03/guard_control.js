function control(){
  let checks=0,seed=6112633;function assert(b){checks++;if(!b)throw Error("control failed")}
  function rnd(n){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n}
  function rank(V){let m=new Map();for(let x of V){while(x){let k=31-Math.clz32(x);if(!m.has(k)){m.set(k,x);break}x^=m.get(k)}}return m.size}
  let maxRise=0;
  for(let t=0;t<500;t++){let q=3+rnd(8),A=[],B=[],K=[];for(let i=0;i<1+rnd(10);i++)A.push(rnd(1<<q));for(let i=0;i<1+rnd(10);i++)B.push(rnd(1<<q));for(let i=0;i<rnd(q+1);i++)K.push(rnd(1<<q));
    let g=rank(K),old=rank(A)+rank(B)-rank([...A,...B]),after=rank([...A,...K])+rank([...B,...K])-rank([...A,...B,...K])-g;
    assert(after<=old+g);maxRise=Math.max(maxRise,after-old);
  }
  // Native connected chain with h=0, all a_i free; add explicit XOR guards
  // relating a_{2j},a_{2j+1} to two global phase bits and literal offsets.
  const b=8,n=6*b,C=[];for(let k=0;k<b;k++)for(let i=0;i<6;i++)C.push([6*k+(i+5)%6,6*k+i,6*k+(i+1)%6]);for(let k=0;k<b-1;k++){let a=6*k+3,c=6*(k+1);[C[a][1],C[c][1]]=[C[c][1],C[a][1]]}
  let support=[],neighbors=[];
  for(let omit=-1;omit<4;omit++){let S=[];for(let u=0;u<2;u++)for(let v=0;v<2;v++){let x=Array(n).fill(0);for(let j=0;j<4;j++){let a=u^(1^((j>>0)&1)),d=v^(1^((j>>1)&1));for(let [k,f] of [[2*j,a],[2*j+1,d]]){x[6*k+1]=x[6*k+4]=f;x[6*k+2]=x[6*k+5]=1-f}}
    assert(C.every(c=>c.reduce((s,i)=>s+x[i],0)===1));assert(x[0]===0);
    // Anchor u=a_6, v=a_7 (j=3); every other phase is a signed copy.
    assert([0,1,2,3].every(j=>x[6*(2*j)+1]===(x[37]^(1^(j&1)))&&x[6*(2*j+1)+1]===(x[43]^(1^((j>>1)&1)))));
    let sat=[0,1,2,3].every(j=>j===omit||!(x[6*(2*j)+1]&&x[6*(2*j+1)+1]));assert(sat===(omit===u+2*v));if(sat)S.push(u+2*v)
  }if(omit<0)support=S;else neighbors.push(S)}
  assert(support.length===0&&neighbors.every((s,j)=>s.length===1&&s[0]===j));
  return {seed:6112633,checks,quotientTests:500,maxRise,nativeGuardedControl:{n,clauses:C.length,support,oneOmissionSupports:neighbors,scope:"explicit guards, not unguarded source; independent direct witness/phase truth table, not median solver"}}
}
console.log(JSON.stringify(control(),null,2));
