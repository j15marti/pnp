// LSPV-4/425 independent compact replay. Run with Node.js >=18.
let checks=0;
for(let k=2;k<=13;k++){
  const M=8*k+32, signatures=new Set();
  for(let mask=0;mask<(1<<(k-1));mask++){
    const f=Array.from({length:M},(_,i)=>i);
    const chain=[0],used=new Set([0]);
    for(let j=0;j<k;j++){
      const p=j===k-1?0:(mask>>j)&1;
      let next=-1;
      for(let v=1;v<M;v++)if(!used.has(v)&&(v&1)===p){next=v;break;}
      if(next<0)throw Error("fresh address unavailable");
      f[chain[j]]=next;chain.push(next);used.add(next);
    }
    let v=0,seq=[];
    for(let j=0;j<k;j++){v=f[v];seq.push(v&1);}
    if(seq[k-1]!==0)throw Error("terminal parity");
    const reversed=[...seq].reverse().join("");
    signatures.add(reversed.slice(1));
    let brute=[],bruteReads=0;
    for(let t=k;t>=1;t--){let u=0;for(let i=0;i<t;i++){u=f[u];bruteReads++}brute.push(u&1);}
    if(brute.join("")!==reversed||bruteReads!==k*(k+1)/2)throw Error("replay");
    let balanced=[],reads=0,maxStack=0;
    function run(a,b,start,depth){
      maxStack=Math.max(maxStack,depth);
      if(b===a+1){balanced.push(f[start]&1);reads++;return;}
      const mid=Math.floor((a+b)/2);
      let x=start;for(let j=a;j<mid;j++){x=f[x];reads++;}
      run(mid,b,x,depth+1);run(a,mid,start,depth+1);
    }
    run(0,k,0,1);
    if(balanced.join("")!==reversed||
       reads>k*(1+Math.ceil(Math.log2(k))/2)||
       maxStack>Math.ceil(Math.log2(k))+1)throw Error("balanced replay");
    checks+=5;
  }
  if(signatures.size!==(1<<(k-1)))throw Error("information count");
  checks++;
}
function tseitin(edges,odd){
  const vCount=Math.max(...edges.flat())+1,inc=Array.from({length:vCount},()=>[]);
  edges.forEach(([a,b],i)=>{inc[a].push(i+1);inc[b].push(i+1)});
  const clauses=[];
  for(let v=0;v<vCount;v++)for(let a=0;a<8;a++){
    const parity=((a&1)+((a>>1)&1)+((a>>2)&1))&1;
    if(parity===(odd&&v===0?1:0))continue;
    clauses.push(inc[v].map((id,j)=>((a>>j)&1)?-id:id));
  }
  let satisfiable=false;
  outer:for(let mask=0;mask<(1<<edges.length);mask++){
    for(let clause of clauses){
      if(!clause.some(l=>Boolean((mask>>(Math.abs(l)-1))&1)===(l>0)))continue outer;
    }
    satisfiable=true;break;
  }
  if(satisfiable===odd||clauses.length!==4*vCount)throw Error("Tseitin label");
  checks+=2;
}
const k4=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]];
const cube=[];
for(let v=0;v<8;v++)for(const b of [1,2,4])if(v<(v^b))cube.push([v,v^b]);
for(const edges of [k4,cube])for(const odd of [false,true])tseitin(edges,odd);
console.log(JSON.stringify({status:"COMPUTATIONAL",checks,parity_range:"2..13",cnf_controls:4}));
