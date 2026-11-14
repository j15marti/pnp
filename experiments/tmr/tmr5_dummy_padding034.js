function runAudit(){
  const st={assertions:0,functions:0,dnf_checks:0,padded_bit_checks:0,exact_min_checks:0,threshold_checks:0,failures:0};
  function ck(ok,msg){st.assertions++;if(!ok){st.failures++;throw Error(msg)}}
  function bit(f,i){return (BigInt(f)>>BigInt(i))&1n}
  function rep(f,n,r){let out=0n,N=1<<n;for(let i=0;i<(1<<(n+r));i++)out|=bit(f,i%N)<<BigInt(i);return out}
  function makeDNF(f,n){
    const gates=[],neg={},emit=(op,a,b)=>{gates.push([op,a,b]);return n+2+gates.length-1};
    const N=1<<n,full=(1n<<BigInt(N))-1n;if(f===0n)return {gates,out:n};if(f===full)return {gates,out:n+1};
    const terms=[];
    for(let x=0;x<N;x++)if(bit(f,x)){
      let root=null;
      for(let j=0;j<n;j++){
        let lit=j;
        if(!((x>>j)&1)){if(neg[j]===undefined)neg[j]=emit("NOT",j,0);lit=neg[j]}
        root=root===null?lit:emit("AND",root,lit);
      }
      terms.push(root);
    }
    let out=terms[0];for(let j=1;j<terms.length;j++)out=emit("OR",out,terms[j]);
    return {gates,out}
  }
  function evalDNF(p,n,x){let a=Array.from({length:n},(_,j)=>(x>>j)&1).concat([0,1]);for(const [op,i,j] of p.gates)a.push(op==="NOT"?1-a[i]:op==="AND"?(a[i]&a[j]):(a[i]|a[j]));return a[p.out]}
  function minSets(n){
    const N=1<<n,full=(1n<<BigInt(N))-1n;
    const base=[0n,full,...Array.from({length:n},(_,j)=>{let x=0n;for(let i=0;i<N;i++)x|=BigInt((i>>j)&1)<<BigInt(i);return x})];
    const L=[new Set(base),new Set(base),new Set(base)];
    function *next(sig){for(let a of sig)yield a^full;for(let a of sig)for(let b of sig){yield a&b;yield a|b;}}
    for(let a of next(base)){L[1].add(a);L[2].add(a);for(let b of next(base.concat([a])))L[2].add(b)}
    return L;
  }
  for(let n=1;n<=3;n++)for(let f=0;f<(1<<(1<<n));f++){
    const ff=BigInt(f),c=makeDNF(ff,n),N=1<<n;ck(c.gates.length<=n*N+n+2,"dnf count");
    for(let x=0;x<N;x++){ck(BigInt(evalDNF(c,n,x))===bit(ff,x),"dnf");st.dnf_checks++}
    for(let r=1;r<=2;r++){let P=rep(ff,n,r);for(let x=0;x<(1<<(n+r));x++){ck(((P>>BigInt(x))&1n)===bit(ff,x%N),"padding");st.padded_bit_checks++}}
    st.functions++;
  }
  for(let n=1;n<=2;n++){const base=minSets(n);for(let r=1;r<=2;r++){const larger=minSets(n+r);for(let f=0;f<(1<<(1<<n));f++){const x=BigInt(f),y=rep(x,n,r);for(let s=0;s<=2;s++){ck(base[s].has(x)===larger[s].has(y),"minimum gate invariant");st.exact_min_checks++}}}}
  function clg(x){let k=0,p=1;while(p<x){p*=2;k++}return k}
  for(const [p,q] of [[1,2],[1,3],[1,10],[2,5]])for(let n=1;n<=32;n++){
    const nprime=Math.max(n,Math.ceil(q*(n+clg(n+2)+2)/p));
    const B=BigInt(n)*(1n<<BigInt(n))+BigInt(n)+2n;
    ck((1n<<BigInt(p*nprime))>=B**BigInt(q),"power threshold");
    ck(nprime>=n,"arity");st.threshold_checks++;
  }
  return {status:"COMPUTATIONAL",execution:"hosted V8, exact standalone source; not a physical TM",stats:st,gate_basis:"AND/OR/NOT; free input and constants, unrestricted fan-out",inputs:"all n<=3 Boolean functions; padded arities +1,+2; exact circuit budgets 0..2 at n<=2; rational powers 1/2 1/3 1/10 2/5 n<=32",scope:"semantic checks and arithmetic only; asymptotic proof separate"};
}

const result = runAudit();
if (typeof process !== 'undefined') process.stdout.write(JSON.stringify(result, null, 2) + '\n');
