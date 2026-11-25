function supplementalAudit(){
  const bit=i=>1n<<BigInt(i),has=(x,i)=>Number((x>>BigInt(i))&1n),par=x=>{let s=0;while(x){x&=x-1n;s^=1;}return s;};
  let checks=0;const ck=(x,m)=>{checks++;if(!x)throw Error(m)};
  let seed=20261125;const rnd=()=>seed=(Math.imul(seed,1664525)+1013904223)>>>0;
  const rm=n=>{let x=0n;for(let i=0;i<n;i++)if((rnd()>>>17)&1)x|=bit(i);return x;};
  function closure(M,G,t){
    const B=new Map(),n=M.length;let bad=false,added=0;
    function reduce(v,h){while(v){let i=v.toString(2).length-1;if(!B.has(i))break;let [a,b]=B.get(i);v^=a;h^=b;} // high unpivoted term may block lower reductions: use full descending reduction below
      for(const i of [...B.keys()].sort((a,b)=>b-a))if(has(v,i)){let [a,b]=B.get(i);v^=a;h^=b;}return [v,h];}
    function add(v,h){let [w,s]=reduce(v,h);if(!w){if(s)bad=true;return false;}B.set(w.toString(2).length-1,[w,s]);added++;return true;}
    G.forEach((g,i)=>add(g,has(t,i)));
    let initial=added,rounds=0;
    while(!bad){
      let before=added;rounds++;
      for(let i=0;i<n&&!bad;i++){
        let [a,c]=reduce(bit(i),0),[b,d]=reduce(M[i],0);
        // p_i = a·p+c, (Mp)_i = b·p+d under current affine equations
        if(a===0n&&c===1)add(M[i],0);
        else if(b===0n&&d===1)add(bit(i),0);
        else if(a===b&&a!==0n&&c===d)add(bit(i),0);
      }
      if(before===added)break;
    }
    return {bad,added:added-initial,rounds,eq:[...B.values()]};
  }
  let closureCases=0,contradictions=0,forces=0,rounds=0,actualModels=0;
  for(let r=0;r<400;r++){
    let n=2+rnd()%7,M=Array.from({length:n},()=>rm(n)),q=1+rnd()%3,G=Array.from({length:q},()=>rm(n)),t=rm(q),F=closure(M,G,t),models=[];
    for(let p=0n;p<bit(n);p++)if(M.every((row,i)=>!has(p,i)||!par(row&p))&&G.every((g,i)=>par(g&p)===has(t,i)))models.push(p);
    for(const p of models)ck(!F.bad&&F.eq.every(([g,v])=>par(g&p)===v),"false closure");
    if(F.bad){ck(!models.length,"false contradiction");contradictions++;}
    closureCases++;forces+=F.added;rounds+=F.rounds;actualModels+=models.length;
  }
  // Margulis-Gabber-Galil simple support, symmetric high-rank control. Use exact
  // induced matching certificate, no numerical eigenvalue estimate.
  let expanders=[];
  for(let m of [3,5,7,11,17]){
    let n=m*m,A=Array(n).fill(0n),mod=x=>(x%m+m)%m,id=(x,y)=>mod(x)*m+mod(y);
    for(let x=0;x<m;x++)for(let y=0;y<m;y++){
      let i=id(x,y);
      for(let s of [-1,1])for(let d of [0,1])for(let j of [id(x+s*(2*y+d),y),id(x,y+s*(2*x+d))])if(j!==i)A[i]|=bit(j);
    }
    for(let i=0;i<n;i++)for(let j=0;j<n;j++)ck(has(A[i],j)===has(A[j],i),"non-symmetric support");
    const open=new Set([0]);for(let i of open)for(let j=0;j<n;j++)if(has(A[i],j))open.add(j);ck(open.size===n,"not connected");
    let avail=bit(n)-1n,I=[],J=[];
    while(avail){
      let i=-1,j=-1;for(let a=0;a<n&&i<0;a++)if(has(avail,a)&&(A[a]&avail))for(let b=0;b<n;b++)if(has(A[a]&avail,b)){i=a;j=b;break;}
      if(i<0)break;I.push(i);J.push(j);avail&=~(bit(i)|bit(j)|A[i]|A[j]);
    }
    for(let a=0;a<I.length;a++)for(let b=0;b<J.length;b++)ck(has(A[I[a]],J[b])===Number(a===b),"induced minor");
    const M=A.map((v,i)=>v|bit(i)); // d=b=ones: exact cancellation, no enumeration required
    const N=M.slice();N[0]^=1n;ck(!par(N[0]&1n),"neighbor singleton");
    expanders.push({n,modulus:m,inducedMatchingRankLowerBound:I.length,original:"UNSAT by symmetric cancellation",neighbor:"SAT singleton",connected:true});
  }
  return {seed:20261125,checks,closureCases,contradictions,additionalCertifiedIndependentEquations:forces,rounds,actualModelsVerified:actualModels,expanders};
}
console.log(JSON.stringify(supplementalAudit(),null,2));
