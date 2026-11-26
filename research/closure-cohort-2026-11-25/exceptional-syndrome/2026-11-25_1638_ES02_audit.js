/* ES02 exact reproducible audit. Node.js 18+: node 2026-11-25_1638_ES02_audit.js */
function run(){
  const out={seed:0x5e520026,exhaustive_tournaments:0,random_tournaments:0,span_comparisons:0,feasible_supports_checked:0,local_generators_checked:0,forced_zero_checks:0,dominating_demand_decisions:0,dominating_sat:0,dominating_unsat:0,syndrome_comparisons:0,syndrome_sat:0,syndrome_unsat:0,strict_rank_checks:0,large_controls:[],assertions:0};
  let state=out.seed>>>0;
  const rng=()=>{state^=state<<13;state^=state>>>17;state^=state<<5;return state>>>0};
  const ok=(x,msg)=>{out.assertions++;if(!x)throw Error(msg)};
  const B=i=>1n<<BigInt(i),mask=n=>B(n)-1n;
  const parity=x=>{let r=0;while(x){x&=x-1n;r^=1}return r};
  const wt=x=>{let r=0;while(x){x&=x-1n;r++}return r};
  const ids=x=>{let a=[];while(x){let v=x&-x;a.push(v.toString(2).length-1);x^=v}return a};
  const rank=vs=>{let base=new Map();for(let x of vs){while(x){let k=x.toString(2).length-1;if(base.has(k))x^=base.get(k);else{base.set(k,x);break}}}return base.size};
  const xor=vs=>vs.reduce((a,b)=>a^b,0n);
  const feasible=(M,p)=>{for(const i of ids(p))if(parity(M[i]&p))return false;return true};
  const tournament=M=>M.every((r,i)=>M.every((s,j)=>i===j||Boolean(r&B(j))!==Boolean(s&B(i))));
  const strong=M=>{for(let i=0;i<M.length;i++){let s=B(i);while(true){let t=s;for(let j of ids(s))t|=M[j];if(t===s)break;s=t}if(s!==mask(M.length))return false}return true};
  const dominating=(M,b)=>{let s=b;for(const i of ids(b))s|=M[i];return s===mask(M.length)};
  function forced(M){let a=mask(M.length);while(true){let old=a;for(let i of ids(a))if((M[i]&a)===B(i))a^=B(i);if(a===old)return a}}
  function local(M,b=null,check=false){
    let a=forced(M),vs=ids(a),incoming=M.map((_,i)=>xor(vs.filter(j=>j!==i&&(M[j]&B(i))!==0n).map(B))),gens=[];
    for(let ii=0;ii<vs.length;ii++)for(let jj=ii+1;jj<vs.length;jj++)for(let kk=jj+1;kk<vs.length;kk++){
      let i=vs[ii],j=vs[jj],k=vs[kk],t=B(i)|B(j)|B(k);
      if(!feasible(M,t))continue;
      let dom=incoming[i]&incoming[j]&incoming[k];
      if(b!==null){if(parity(t&b))return t;if(dom&b)return t|((dom&b)&-(dom&b))}
      else{
        gens.push(t);if(check){ok(feasible(M,t),"triangle");out.local_generators_checked++}
        for(let v of ids(dom)){gens.push(t|B(v));if(check){ok(feasible(M,t|B(v)),"dominator");out.local_generators_checked++}}
      }
    }
    return b===null?gens:null;
  }
  function solve(M,b){
    if(!b)return null;
    if(!tournament(M))throw Error("unsupported non-tournament");
    let a=forced(M); if(!(b&a))return null;
    for(let i=0;i<M.length;i++)if(!(M[i]&B(i))){
      if(b&B(i))return B(i);
      for(let j of ids(b))if(M[j]&B(i)){if(!(M[j]&B(j)))return B(j);return B(j)|B(i)}
    }
    if(!M.every((r,i)=>r&B(i)))throw Error("mixed diagonal without dominating promise");
    return local(M,b);
  }
  function brute(M){let f=[];for(let p=0n;p<B(M.length);p++){out.feasible_supports_checked++;if(feasible(M,p))f.push(p)}return f}
  function makeT(n,word=null){let M=Array.from({length:n},(_,i)=>B(i)),k=0;for(let i=0;i<n;i++)for(let j=i+1;j<n;j++){if(word===null?(rng()&1):((word>>>k)&1))M[i]|=B(j);else M[j]|=B(i);k++}return M}
  function checkT(M){
    let f=brute(M),a=forced(M),g=local(M,null,true);
    for(let p of f){ok(!(p&~a),"forced zero unsound");out.forced_zero_checks++}
    ok(rank(f)===rank(g),"span mismatch");out.span_comparisons++;
    let b=BigInt(rng())&mask(M.length),p=solve(M,b),want=f.some(x=>parity(x&b));
    ok((p!==null)===want,"single demand");if(p!==null)ok(feasible(M,p)&&parity(p&b),"actual witness");
  }
  for(let n=1;n<=6;n++)for(let t=0;t<2**(n*(n-1)/2);t++){checkT(makeT(n,t));out.exhaustive_tournaments++}
  for(let n=7;n<=11;n++)for(let j=0;j<60;j++){checkT(makeT(n));out.random_tournaments++}
  function checkDominating(M,b,f){
    if(!dominating(M,b)||!b)return;
    let p=solve(M,b),want=f.some(x=>parity(x&b));
    ok((p!==null)===want,"mixed dominating decision");
    if(p!==null){ok(feasible(M,p)&&parity(p&b),"mixed actual witness");out.dominating_sat++}else out.dominating_unsat++;
    out.dominating_demand_decisions++;
  }
  for(let t=0;t<64;t++){let T=makeT(4,t);for(let d=0;d<16;d++){let M=T.map((r,i)=>(r&~B(i))|(BigInt(d)&B(i))),f=brute(M);for(let b=1n;b<16n;b++)checkDominating(M,b,f)}}
  for(let j=0;j<300;j++){let n=5+rng()%5,T=makeT(n),b=(BigInt(rng())&mask(n))||1n,d=BigInt(rng())&mask(n),M=T.map((r,i)=>(r&~B(i))|(d&B(i)));if(dominating(M,b))checkDominating(M,b,brute(M))}
  function chart(M,b){let n=M.length,e=M.map((_,i)=>B(i)),w=B(n),f=M.map((_,j)=>xor(M.map((r,i)=>(((r&B(j))!==0n)!==(i===j))?B(i):0n))|((b&B(j))?w:0n));return {e,f,w,t:w^xor(f)}}
  function lift(M,b,p){let {e,f,w,t}=chart(M,b),q=xor(M.map((r,i)=>parity(r&p)?B(i):0n));let y=f.map((v,i)=>(p&B(i))?e[i]:v^((q&B(i))?e[i]:0n));ok(y.every((v,i)=>v!==0n&&(v===e[i]||v===f[i]||v===(e[i]^f[i])))&&xor(y)===t,"source lift");return y}
  function support(P){let s=new Set([0n]);for(let u of P){let t=new Set();for(let x of s)for(let y of u)t.add(x^y);s=t}return s}
  function strict(P){let n=P.length;ok(rank(P.flat())===n+1,"full rank");for(let S=1n;S<=mask(n);S++){ok(rank(ids(S).flatMap(i=>P[i]))>=wt(S)+1,"strict Hall");out.strict_rank_checks++}}
  for(let trial=0;trial<40;trial++){
    let n=3+rng()%4,M=makeT(n),b=(BigInt(rng())&mask(n))||1n;
    if(!strong(M)||!dominating(M,b))continue;
    let {e,f,w,t}=chart(M,b),P=e.map((v,i)=>[v,f[i],v^f[i]]),s=support(P);strict(P);
    for(let target=0n;target<B(n+1);target++){
      let diff=target^t,got;
      if(diff&w){let q=target^xor(f),y=f.map((v,i)=>v^((q&B(i))?e[i]:0n));ok(xor(y)===target,"hyperplane direct lift");got=true}
      else{let M2=M.map((r,i)=>r^(diff&B(i))),p=solve(M2,b);got=p!==null;if(got){lift(M2,b,p);ok(chart(M2,b).t===target,"target transport")}}
      ok(got===s.has(target),"exact syndrome");out.syndrome_comparisons++;if(got)out.syndrome_sat++;else out.syndrome_unsat++;
    }
  }
  const atom=[[15n,32n,47n],[13n,17n,28n],[14n,36n,42n],[11n,53n,62n],[10n,39n,45n]];
  strict(atom);let as=support(atom),missing=[];for(let t=0n;t<64n;t++)if(!as.has(t))missing.push(Number(t));ok(JSON.stringify(missing)==="[29]","atom missing");
  let chartCount=0,tourCount=0,oneCount=0;
  function atomChart(es,fs,coord){
    let w=29n^xor(fs);if(coord.has(w))return;
    let all=new Map(coord);for(let [x,v] of coord)all.set(x^w,v|32n);
    let cols=fs.map(f=>all.get(f)),M=es.map((_,i)=>xor(cols.map((x,j)=>Boolean(x&B(i))!==(i===j)?B(j):0n)));
    chartCount++;if(tournament(M)){tourCount++;if(M.every((r,i)=>r&B(i)))oneCount++}
  }
  function chooseF(es,fs,coord){if(fs.length===5){atomChart(es,fs,coord);return}let i=fs.length;for(let f of atom[i])if(f!==es[i])chooseF(es,[...fs,f],coord)}
  function chooseE(es,coord){if(es.length===5){chooseF(es,[],coord);return}let i=es.length;for(let e of atom[i]){if(coord.has(e))continue;let next=new Map(coord);for(let [x,v] of coord)next.set(x^e,v|B(i));chooseE([...es,e],next)}}
  chooseE([],new Map([[0n,0n]]));ok(chartCount===5568&&tourCount===0,"atom chart check");
  out.five_plane={missing,charts:chartCount,tournament_charts:tourCount,all_one_tournament_charts:oneCount};
  const groups=[[[0,1],[2,3]],[[0,2],[1,4]],[[0,3],[2,4]],[[0,4],[1,3]],[[1,2],[3,4]]],edges=groups.flat(),rows=edges.map(([i,j])=>B(i)^B(j));
  for(let S=1;S<31;S++){let r=[];for(let i=0;i<5;i++)if(S>>i&1)r.push(rows[2*i],rows[2*i+1]);ok(rank(r)>=wt(BigInt(S)),"K5 proper rank")}
  ok(rank(rows)===4,"K5 total rank");
  const k5Sat=(sig)=>{for(let x=0n;x<32n;x++)if(groups.every((_,i)=>parity(x&rows[2*i])===((sig>>(2*i))&1)||parity(x&rows[2*i+1])===((sig>>(2*i+1))&1)))return true;return false};
  ok(!k5Sat(1023),"K5 all inequality");for(let j=0;j<10;j++)ok(k5Sat(1023^(1<<j)),"K5 sign neighbor");
  out.K5={all_inequality:"UNSAT",single_sign_neighbors_sat:10};
  const bad=[52n,3n,22n,15n,26n,62n],bBad=20n,fBad=brute(bad);ok(tournament(bad)&&strong(bad),"mixed counterexample strict chart");strict(chart(bad,bBad).e.map((e,i)=>[e,chart(bad,bBad).f[i],e^chart(bad,bBad).f[i]]));
  let odd=fBad.filter(p=>parity(p&bBad));ok(odd.length===1&&odd[0]===47n&&wt(odd[0])===5,"mixed counterexample");
  // Verify this is the shortest-path diagonal candidate, not merely a noncandidate.
  let reached=bBad,layer=bBad,dStar=bBad,dist=0;while(reached!==mask(6)){let nxt=0n;for(let i of ids(layer))nxt|=bad[i];nxt&=~reached;ok(nxt!==0n,"BFS progress");dist++;if(dist%2)dStar|=nxt;reached|=nxt;layer=nxt}
  ok(dStar===xor(bad.map((r,i)=>r&B(i))),"mixed actual candidate");lift(bad,bBad,47n);out.mixed_candidate_counterexample={rows:bad.map(Number),demand:Number(bBad),only_odd_repair:47,min_support:5};
  for(let l of [2,4,8,16,32,64,128]){
    let n=2*l+1,M=Array.from({length:n},(_,i)=>B(i));
    for(let i=0;i<=l;i++)for(let j=i+1;j<=l;j++)M[i]|=B(j);
    for(let i=1;i<=l;i++)for(let j=i+1;j<=l;j++)M[l+i]|=B(l+j);
    for(let i=0;i<=l;i++)for(let j=1;j<=l;j++){if(j<=l-i)M[l+j]|=B(i);else M[i]|=B(l+j)}
    let b=mask(l+1),bp=b|B(l+1);
    ok(tournament(M)&&strong(M)&&dominating(M,b)&&dominating(M,bp),"family admission");
    ok(rank(M.slice(l+1).map(r=>r&b))===l,"prescribed lower block rank");
    let p=solve(M,b),pp=solve(M,bp);
    ok(p===null&&pp!==null,"family labels");ok(feasible(M,pp)&&parity(pp&bp),"family witness");lift(M,bp,pp);
    let {f,w,t}=chart(M,b);ok(xor(f)===(t^w),"same-geometry neighbor");
    out.large_controls.push({n,fixed_order_feedback_rank_lower_bound:l,alternating_rank_lower_bound:2*l,exception_candidate:"UNSAT",changed_demand_candidate:"SAT",same_geometry_neighbor:"SAT",witness_support:wt(pp)});
  }
  return out;
}
console.log(JSON.stringify(run(), null, 2));
