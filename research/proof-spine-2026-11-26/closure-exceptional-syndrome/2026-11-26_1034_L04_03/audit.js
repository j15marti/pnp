function audit(){
  let checks=0;
  function ck(x,msg){if(!x)throw Error(msg+" @"+checks);checks++}
  const frame=s=>"1".repeat(s.length)+"0"+s, bin=n=>n.toString(2);
  const rules=[[0,1,0,0,1,0,1,2],[0,2,0,2,2,0,1,2],[2,1,0,0,1,0,1,2],[2,2,0,2,2,0,1,2],[2,0,0,1,0,0,2,2]];
  const code=rules.flat().map(n=>frame(bin(n))).join("");
  function source(x,t){return frame(code)+frame(x)+frame(bin(t))}
  function parse(w){let p=0;function get(){let a=p;while(w[p]==="1")p++;let n=p-a;ck(w[p++]==="0"&&p+n<=w.length,"frame");let s=w.slice(p,p+n);p+=n;return s}let c=get(),x=get(),t=Number("0b"+get());ck(c===code&&/^0*$/.test(w.slice(p))&&BigInt(t)<=BigInt(w.length)**2n,"source");return {x,t}}
  function simulate(x,t){let s=0,p=0;for(let j=0;j<t;j++){let a=p<x.length?Number(x[p])+1:0;let r=rules.find(r=>r[0]===s&&r[1]===a&&r[2]===0);if(!r)return false;s=r[3];if(s===1)return true;if(r[6]===1)p++}return false}
  function norm(c){let a=[...new Set(c)].sort((a,b)=>a-b);return a.some(x=>a.includes(-x))?null:a}
  function runs(a){let r=[];for(const x of a){let t=r[r.length-1];if(t&&t[1]+1===x)t[1]=x;else r.push([x,x])}return r}
  function compile(Q,n){
    const q=Q.length,b=Math.max(1,Math.ceil(Math.log2(Math.max(1,q)))),dict=new Map();
    for(let j=0;j<q;j++){let seen=new Set();for(let c of Q[j]){c=norm(c);if(c===null)continue;let key=JSON.stringify(c);if(seen.has(key))continue;seen.add(key);if(!dict.has(key))dict.set(key,{c,ids:[]});dict.get(key).ids.push(j)}}
    let rows=[...dict.values()].map(({c,ids})=>({c,r:runs(ids)})), next=n+b, clauses=[], gates=[];
    const fresh=()=>++next, neg=x=>typeof x==="boolean"?!x:-x;
    function add(c){let t=norm(c);if(t===null)return;if(t.length===3){clauses.push(t);return}ck(t.length<=3,"width");let pad=Array.from({length:3-t.length},fresh);for(let mask=0;mask<2**pad.length;mask++)clauses.push(t.concat(pad.map((x,i)=>(mask>>i)&1?x:-x)))}
    function and(x,y){if(x===false||y===false)return false;if(x===true)return y;if(y===true)return x;if(x===y)return x;if(x===-y)return false;let z=fresh();gates.push([z,x,y]);add([-z,x]);add([-z,y]);add([z,-x,-y]);return z}
    const or=(x,y)=>neg(and(neg(x),neg(y)));
    const fold=(a,f,z)=>a.reduce(f,z);
    function le(c){if(c<0)return false;if(c>=2**b-1)return true;let z=true;for(let k=0;k<b;k++){let x=n+b-k;if((c>>k)&1)z=or(neg(x),z);else z=and(neg(x),z)}return z}
    const inrun=(l,r)=>and(neg(le(l-1)),le(r));
    let root=le(q-1);
    for(const row of rows){let active=fold(row.r.map(([l,r])=>inrun(l,r)),or,false), value=fold(row.c,or,false);root=and(root,or(neg(active),value))}
    if(root===false)add([]);else if(root!==true)add([root]);
    function evaluate(x,j){let v=Array(next+1).fill(false);for(let i=1;i<=n;i++)v[i]=!!x[i-1];for(let k=0;k<b;k++)v[n+b-k]=!!((j>>k)&1);const lit=l=>typeof l==="boolean"?l:l>0?v[l]:!v[-l];for(let [z,a,b] of gates)v[z]=lit(a)&&lit(b);let ok=lit(root),cnf=clauses.every(c=>c.some(lit));ck(ok===cnf,"Tseitin extension");return ok}
    function sweep(x){let diff=new Int32Array(q+1);for(let {c,r} of rows)if(!c.some(l=>l>0?x[l-1]:!x[-l-1]))for(let [a,b]of r){diff[a]++;diff[b+1]--}let z=0,ret=[];for(let i=0;i<q;i++){z+=diff[i];if(z===0)ret.push(i)}return ret}
    for(let c of clauses)ck(c.length===3&&new Set(c.map(Math.abs)).size===3,"proper 3CNF");
    return {q,b,rows,gates,clauses,evaluate,sweep,variables:next,intervals:rows.reduce((s,r)=>s+r.r.length,0)}
  }
  function truth(F,x){return F.every(c=>c.some(l=>l>0?x[l-1]:!x[-l-1]))}
  let seed=654321;function rnd(n){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n}
  let small=0,projections=0;
  for(let t=0;t<180;t++){let n=1+rnd(6),q=rnd(8),Q=Array.from({length:q},()=>Array.from({length:rnd(7)},()=>Array.from({length:rnd(4)},()=> (rnd(2)?1:-1)*(1+rnd(n)))));let C=compile(Q,n);for(let m=0;m<2**n;m++){let x=Array.from({length:n},(_,i)=>!!(m>>i&1));let actual=Q.flatMap((F,j)=>truth(F,x)?[j]:[]);ck(JSON.stringify(actual)===JSON.stringify(C.sweep(x)),"sweep");for(let j=0;j<2**C.b;j++){ck(C.evaluate(x,j)===(j<q&&truth(Q[j],x)),"projection");projections++}}small++}
  // Explicit proper 3-CNF input query lists: shared dummy pair makes each unit equivalent to its four clauses.
  const unit=(l,u,v)=>[[l,u,v],[l,u,-v],[l,-u,v],[l,-u,-v]];
  let scales=[];
  for(let m of [8,16,32,64,128,256,512]){
    for(let last of [0,1]){
      let w=source("0".repeat(m-1)+last,m+1),s=parse(w);ck(simulate(s.x,s.t)===!!last,"clocked label");
      let n=m+2,base=Array.from(s.x,(x,i)=>unit(x==="1"?i+1:-(i+1),m+1,m+2)).flat();
      let Q=Array.from({length:m},(_,i)=>base.concat(unit(i+1,m+1,m+2))),C=compile(Q,n);
      let assignment=Array.from(s.x,x=>x==="1").concat([false,false]);
      let found=C.sweep(assignment);ck(found.length===last&&(!last||found[0]===m-1),"source sweep");
      for(let j=0;j<m;j++){ck(C.evaluate(assignment,j)===(last===1&&j===m-1),"source projection")}
      scales.push({m,N:w.length,label:last,inputClauses:Q.reduce((s,F)=>s+F.length,0),dictionary:C.rows.length,intervals:C.intervals,gates:C.gates.length,outputClauses:C.clauses.length,outputVariables:C.variables});
    }
  }
  // Contrasting no-sharing list and a syntactic counterexample to intersecting negative queries.
  let anti=compile([[[1]],[[-1]]],1);ck(anti.sweep([false]).join()==="1"&&anti.sweep([true]).join()==="0","OR not AND");
  let distinct=Array.from({length:128},(_,i)=>[[i+1]]),D=compile(distinct,128);
  return {checks,small,projections,scales,disjoint:{queries:128,dict:D.rows.length,intervals:D.intervals,outputClauses:D.clauses.length},limitations:"Finite exhaustive original-variable/selector projections, gate clauses verified on canonical extension; no general SAT solver, no two-tape benchmark, no hierarchy-hard controller acquired. Source controls are actual last-bit clocked U_2 words, not evidence of asymptotic hardness."};
}
console.log(JSON.stringify(audit(),null,2));
