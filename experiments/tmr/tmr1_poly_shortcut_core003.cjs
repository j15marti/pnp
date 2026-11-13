function gadget(z,u,v,polarity) {
  const a=[];
  for (const su of [-1,1]) for(const sv of [-1,1]) a.push([polarity*z,su*u,sv*v]);
  return a;
}

function family(n) {
  if(n<3) throw Error("n>=3");
  const clauses=[];
  for(let i=1;i<=n;i++)for(let j=i+1;j<=n;j++)for(let k=j+1;k<=n;k++) clauses.push([i,j,k]);
  clauses.push(...gadget(1,n+1,n+2,1),...gadget(1,n+3,n+4,-1));
  return {N:n+4,clauses};
}

function enc(N,clauses) {
  const w=Math.max(1,Math.ceil(Math.log2(N)));
  let s="1".repeat(N)+"0"+"1".repeat(clauses.length)+"0";
  for(const clause of clauses) for(const lit of clause)
    s+=(lit<0?"1":"0")+(Math.abs(lit)-1).toString(2).padStart(w,"0");
  return s;
}

function parse(s) {
  if(!/^[01]*$/.test(s))return null;
  const q=s.indexOf("0");if(q<1)return null;
  const N=q,p=s.indexOf("0",q+1);if(p<q+2)return null;
  const M=p-q-1,w=Math.max(1,Math.ceil(Math.log2(N)));
  if(s.length!==p+1+3*M*(w+1))return null;
  let at=p+1;const clauses=[];
  for(let j=0;j<M;j++){
    const c=[];const seen=new Set();
    for(let k=0;k<3;k++){
      const sign=s[at++]==="1"?-1:1;
      const v=parseInt(s.slice(at,at+w),2)+1;at+=w;
      if(v>N || seen.has(v))return null;
      c.push(sign*v);seen.add(v);
    }
    clauses.push(c);
  }
  return {N,clauses};
}

function isCore(N,clauses) {
  const key=c=>c.slice().sort((a,b)=>a-b).join(",");
  const set=new Set(clauses.map(key));
  const full=(z,sg,u,v)=>{
    for(const su of [-1,1])for(const sv of [-1,1])
      if(!set.has(key([sg*z,su*u,sv*v])))return false;
    return true;
  };
  for(let z=1;z<=N;z++){
    let pos=false,neg=false;
    for(let u=1;u<=N;u++) if(u!==z)
      for(let v=u+1;v<=N;v++) if(v!==z){
        if(!pos)pos=full(z,1,u,v);
        if(!neg)neg=full(z,-1,u,v);
        if(pos&&neg)return true;
      }
  }
  return false;
}

function satBF(N,clauses) {
  if(N>14)throw Error("bounded audit only");
  for(let a=0;a<(1<<N);a++){
    let valid=true;
    for(const c of clauses){
      let ok=false;
      for(const lit of c){
        const v=(a>>(Math.abs(lit)-1))&1;
        if((lit>0&&v===1)||(lit<0&&v===0)){ok=true;break;}
      }
      if(!ok){valid=false;break;}
    }
    if(valid)return true;
  }
  return false;
}

function permute(N,clauses,seed){
  let state=seed>>>0;
  const rnd=()=>{state=(Math.imul(1664525,state)+1013904223)>>>0;return state;};
  let index=Array.from({length:N},(_,i)=>i+1);
  for(let i=N-1;i>0;i--){const j=rnd()%(i+1);[index[i],index[j]]=[index[j],index[i]];}
  let flips=Array.from({length:N},()=>rnd()&1?1:-1);
  let cs=clauses.map(c=>c.map(lit=>Math.sign(lit)*flips[Math.abs(lit)-1]*index[Math.abs(lit)-1]));
  for(const c of cs)for(let i=2;i>0;i--){const j=rnd()%(i+1);[c[i],c[j]]=[c[j],c[i]];}
  for(let i=cs.length-1;i>0;i--){const j=rnd()%(i+1);[cs[i],cs[j]]=[cs[j],cs[i]];}
  return cs;
}

function run(){
  const d={date_pst:"2026-11-13 15:00 PST",status:"COMPUTATIONAL_ONLY",assertions:0,failed:0,small_n:[],large_n:[],permuted_unsat_cases:0,deleted_single_clause_sat_cases:0,strict_source_cases:0,encoded_bit_lengths:[]};
  const check=(x,msg)=>{d.assertions++;if(!x){d.failed++;throw Error(msg);}};
  for(let n=3;n<=8;n++){
    const {N,clauses}=family(n),s=enc(N,clauses),p=parse(s);
    check(p!==null,"parse original "+n);
    check(isCore(N,p.clauses),"core missing "+n);
    check(!satBF(N,p.clauses),"core SAT "+n);
    d.encoded_bit_lengths.push({n,N,M:clauses.length,L:s.length});
    for(let i=0;i<8;i++){
      const reduced=clauses.filter((_,j)=>j!==clauses.length-8+i),q=parse(enc(N,reduced));
      check(q!==null,"deleted invalid "+n+" "+i);
      check(!isCore(N,q.clauses),"unexpected residual core "+n+" "+i);
      check(satBF(N,q.clauses),"deleting clause still UNSAT "+n+" "+i);
      d.deleted_single_clause_sat_cases++;
    }
    for(let seed=1;seed<=5;seed++){
      const shuffled=permute(N,clauses,seed*673+n),e=enc(N,shuffled),q=parse(e);
      check(q!==null,"bad permute "+n+" "+seed);
      check(isCore(N,q.clauses),"not invariant "+n+" "+seed);
      check(!satBF(N,q.clauses),"SAT permute "+n+" "+seed);
      d.permuted_unsat_cases++;
    }
    // original x_1 ... x_n induce a clique, despite constant-size contradictory core.
    const edge=new Set();
    for(const c of clauses.slice(0,clauses.length-8)){
      for(let i=0;i<3;i++)for(let j=i+1;j<3;j++){
        const a=Math.min(c[i],c[j]),b=Math.max(c[i],c[j]);
        edge.add(a+","+b);
      }
    }
    check(edge.size===n*(n-1)/2,"missing clique edge "+n);
    d.small_n.push(n);d.strict_source_cases+=1+8+5;
  }
  for(const n of [12,20,35,50]){
    const {N,clauses}=family(n),s=enc(N,clauses),p=parse(s);
    check(p!==null,"large source parse "+n);
    check(isCore(N,p.clauses),"large core lost "+n);
    check(clauses.length===n*(n-1)*(n-2)/6+8,"large count "+n);
    d.large_n.push({n,N,M:clauses.length,L:s.length,primal_treewidth_lower_bound:n-1});
    d.strict_source_cases++;
  }
  // Minimal positive/negative gadget controls without high-width surround.
  const n=3,{N,clauses}=family(n);
  check(parse("1110")===null,"invalid header");
  check(parse(enc(N,clauses).slice(0,-1))===null,"truncation accepted");
  check(parse(enc(N,clauses)+"0")===null,"overlong accepted");
  return d;
}

const stats=run();
if(typeof console!=='undefined')console.log(JSON.stringify(stats,null,2));
