"use strict";
// Independent LSPV-4/498 weighted Hamming family check; not an FLMV machine.
const run=function independentV8() {
  "use strict";
  const summaries = [], failures = [];
  let comparedPairs = 0, singleBitMutants = 0, totalMembers = 0;
  function graph(n) {
    let H,L,R,edges,matching;
    if(n==="K33"){
      H=6;L=[0,1,2];R=[3,4,5];edges=[];for(let u of L)for(let v of R)edges.push([u,v]);
      matching=L.map(u=>[u,u+3]);
    } else if(n==="Q3"){
      H=8;L=[0,3,5,6];R=[1,2,4,7];edges=[];
      for(let u=0;u<H;u++)for(let v=u+1;v<H;v++)if([1,2,4].includes(u^v))edges.push([u,v]);
      matching=L.map(u=>[u,u^1]);
    } else {
      H=14;L=[0,1,2,3,4,5,6];R=L.map(u=>u+7);edges=[];
      for(let u of L)for(let k of [0,1,3])edges.push([u,7+(u+k)%7]);
      matching=L.map(u=>[u,u+7]);
    }
    const key=e=>[...e].sort((a,b)=>a-b).join("/");
    const matchingKeys=new Set(matching.map(key));
    const other=edges.filter(e=>!matchingKeys.has(key(e)));
    if(other.length!==H||matching.length!==H/2)throw Error("invalid graph "+n);
    return {H,L,R,matching,other,name:n};
  }
  function make(g,a,b){
    const {H,L,R,matching,other}=g, width=Math.ceil(Math.log2(2*H+1));
    const head="11100011"+"1".repeat(H)+"0"+"1".repeat(2*H)+"0";
    const bits=[];
    for(let v of [...L,...R]){
      const ids=[];
      for(let j=0;j<matching.length;j++)if(matching[j].includes(v)){
        ids.push(2*j+1+((v<H && L.includes(v)?a:b)>>j&1));
      }
      for(let j=0;j<other.length;j++)if(other[j].includes(v))ids.push(H+j+1);
      ids.sort((x,y)=>x-y);
      if(ids.length!==3||new Set(ids).size!==3)throw Error("nonproper");
      for(let t=0;t<8;t++){
        const signs=[(t>>2)&1,(t>>1)&1,t&1];
        if((signs[0]^signs[1]^signs[2])!==(v===0?1:0)){
          for(let i=0;i<3;i++)bits.push(String(signs[i])+ids[i].toString(2).padStart(width,"0"));
        }
      }
    }
    return head+bits.join("")+"10";
  }
  const hd=(a,b)=>{let k=a^b,r=0;while(k){r+=k&1;k>>=1;}return r;};
  const distance=(x,y)=>{if(x.length!==y.length)throw Error("length");let d=0;for(let i=0;i<x.length;i++)d+=x[i]!==y[i];return d;};
  for(const name of ["K33","Q3","HEAWOOD"]){
    const g=graph(name),m=g.H/2, all=new Map();
    for(let a=0;a<2**m;a++)for(let b=0;b<2**m;b++){
      const s=make(g,a,b);
      if(all.has(s))throw Error("duplicate member");
      all.set(s,[a,b]);
    }
    const words=[...all.keys()];
    const selected=name==="HEAWOOD"?
      [...new Set([words[0],words[1],words[1<<m],words[1<<(m-1)],...words.filter((x,i)=>i%257===0)])]: words;
    let min=Infinity, pairCount=0;
    for(let i=0;i<selected.length;i++)for(let j=i+1;j<selected.length;j++){
      const x=selected[i],y=selected[j], [a,b]=all.get(x),[c,d]=all.get(y);
      let exact=0;
      for(let k=0;k<m;k++){
        const w=4*hd(2*k+1,2*k+2);
        exact+=w*((((a>>k)&1)!==((c>>k)&1)?1:0)+(((b>>k)&1)!==((d>>k)&1)?1:0));
      }
      const got=distance(x,y);
      if(got!==exact)throw Error(`distance mismatch ${name} ${a} ${b} ${c} ${d} ${got} vs ${exact}`);
      min=Math.min(min,got); pairCount++; comparedPairs++;
    }
    if(min!==8)throw Error("wrong min distance "+name+" "+min);
    for(let x of selected)for(let i=0;i<x.length;i++){
      const other=x.slice(0,i)+(x[i]==="1"?"0":"1")+x.slice(i+1);
      if(all.has(other))throw Error(`singlebit code collision ${name} ${i}`);
      singleBitMutants++;
    }
    summaries.push({graph:name,H:g.H,N:words[0].length,m,members:words.length,
       tested_members:selected.length,minimum_distance:min,
       pairwise_distance_checks:pairCount,
       exact_one_bit_exclusions:selected.length*words[0].length});
    totalMembers+=words.length;
  }
  return {artifact:"LSPV4_498_JS_WEIGHTED_HAMMING",summaries,totalMembers,comparedPairs,
     singleBitMutants,failures,pass:true,native_FLMV:false,historical_Rmix341:false};
};
const result=run();
if(typeof process!=="undefined"&&process.stdout){process.stdout.write(JSON.stringify(result,null,2)+"\n");}
