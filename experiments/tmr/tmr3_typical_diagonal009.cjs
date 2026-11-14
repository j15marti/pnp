"use strict";
/* TMR-3/009: source-splice and union-bound census. NOT a physical TM simulator. */
const audit = function audit(){
  const ck=(x,m)=>{if(!x)throw Error(m)};
  const w=n=>Math.max(1,Math.ceil(Math.log2(5*n)));
  const binary=(v,k)=>v.toString(2).padStart(k,"0");
  function block(n,i,bank,b){
    let t="",k=w(n),v=(bank?3*n:n)+2*i;
    for(let u=0;u<2;u++)for(let z=0;z<2;z++)t+=String(1-b)+binary(i,k)+u+binary(v,k)+z+binary(v+1,k);
    return t;
  }
  function encode(n,m,a,b){
    let t="1".repeat(5*n)+"0"+"1".repeat(8*n)+"0";
    for(let p=0;p<n;p+=m)for(let bank=0;bank<2;bank++)
      for(let i=p;i<Math.min(n,p+m);i++)t+=block(n,i,bank,(bank?b:a)[i]);
    return t;
  }
  function decode(n,m,t){
    const k=w(n),g=12*(k+1),len=13*n+2+2*n*g;
    if(t.length!==len || !t.startsWith("1".repeat(5*n)+"0"+"1".repeat(8*n)+"0"))return null;
    const a=Array(n),b=Array(n);let p=13*n+2;
    for(let j=0;j<n;j+=m)for(let bank=0;bank<2;bank++)
      for(let i=j;i<Math.min(n,j+m);i++){
        let chunk=t.slice(p,p+g),b0=1-Number(chunk[0]);
        if(chunk!==block(n,i,bank,b0))return null;
        (bank?b:a)[i]=b0;p+=g;
      }
    return {a,b,sat:a.every((x,i)=>x===b[i])};
  }
  function cuts(n,m){
    const g=12*(w(n)+1),h=13*n+2,q=Math.floor(m/2),out=[];
    if(m<2)return out;
    for(let base=0;base+m<=n;base+=m)
      for(let u=q*g;u<m*g;u++)out.push({base,c:h+2*base*g+u});
    return out;
  }
  let seed=0x31415926;
  const rand=()=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed;};
  let cases=0,splices=0,unequal=0,member_checks=0;
  const probabilities=[];
  for(const n of [2,3,4,8,16,24,32,64,128,256])for(const m of [1,2,3,4,8,16,24,32,64,128,256]){
    if(m>n)continue;
    let L=13*n+2+24*n*(w(n)+1),q=Math.floor(m/2),cs=cuts(n,m);
    ck(cs.length===(m<2?0:Math.floor(n/m)*(m-q)*12*(w(n)+1)),"cut count");
    for(let test=0;test<3;test++){
      const a=Array.from({length:n},()=>rand()&1);
      const b=test===0?a.slice():Array.from({length:n},()=>rand()&1);
      const x=decode(n,m,encode(n,m,a,b));
      ck(x!==null&&x.sat===a.every((z,i)=>z===b[i]),"canonical parse");
      cases++;
    }
    if(q>0){
      let use=cs.length<=12?cs:[cs[0],cs[Math.floor(cs.length/3)],cs[Math.floor(2*cs.length/3)],cs[cs.length-1]];
      let count=Math.min(16,2**q);
      for(const {base,c} of use)for(let x=0;x<count;x++)for(let y=0;y<count;y++){
        let a=new Array(n).fill(0),b=new Array(n).fill(0);
        for(let j=0;j<q;j++){a[base+j]=(x>>j)&1;b[base+j]=(y>>j)&1;}
        let left=encode(n,m,a,a),right=encode(n,m,b,b);
        let merged=left.slice(0,c)+right.slice(c);
        ck(merged===encode(n,m,a,b),"exact syntax-preserving splice");
        let z=decode(n,m,merged);ck(z && z.sat===(x===y),"spliced SAT label");
        member_checks++;splices++;if(x!==y)unequal++;
      }
    }
    if(m>=16){
      let g=12*(w(n)+1),K=Math.floor(n/m)*(q*g-1);
      ck(cs.length>=K && K>=n*q*g/(4*m),"selected-cut inequality");
      let fail=K*Math.pow(2,-q/2);
      probabilities.push({n,m,L,q,K,union_bound_failure:fail,lower_bound_probability:Math.max(0,1-fail)});
    }
  }
  ck(unequal>0,"no opposite label");
  return {id:"TMR3-TYPICAL-DIAGONALS009",status:"COMPUTATIONAL",model:"original grouped/batched unary-header 3-CNF; finite source splices only, no physical TM crossing simulation",seed:"0x31415926",cases,splices,unequal_splices:unequal,member_checks,probability_rows:probabilities,failures:0};
};
if (typeof require!=="undefined" && require.main===module) console.log(JSON.stringify(audit(),null,2));
if (typeof module!=="undefined") module.exports={audit};
