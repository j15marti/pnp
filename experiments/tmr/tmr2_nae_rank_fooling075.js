const run = function run(){
  "use strict";
  let assertions=0;
  const check=(cond,msg)=>{assertions++;if(!cond)throw new Error("FAIL: "+msg);};
  const bit=(n,i)=>(n>>i)&1;
  const count=(a)=>a.reduce((s,x)=>s+x,0);
  const nae=(a,b,c)=>!(a===b&&b===c);
  function construct(k){
    const E=[];for(let i=0;i<k;i++)for(let j=i+1;j<k;j++)E.push([i,j]);
    const n=3*k+E.length, clauses=[];
    const add=(a,b,c)=>{clauses.push([a+1,b+1,c+1]);clauses.push([-a-1,-b-1,-c-1]);};
    for(let i=0;i<k;i++)add(i,k+i,2*k+i);
    for(let h=0;h<E.length;h++)add(E[h][0],E[h][1],3*k+h);
    return {k,n,edges:E,clauses};
  }
  function satisfies(clauses,values){
    return clauses.every(cl=>cl.some(l=>l>0?values[l-1]===1:values[-l-1]===0));
  }
  function assignment(o,x,y,w,z){
    const v=Array(o.n).fill(0);
    for(let i=0;i<o.k;i++){v[i]=bit(x,i);v[o.k+i]=bit(y,i);v[2*o.k+i]=bit(w,i);}
    for(let j=0;j<o.edges.length;j++)v[3*o.k+j]=bit(z,j);
    return v;
  }
  function f(o,x,y,w,z){return satisfies(o.clauses,assignment(o,x,y,w,z))?1:0;}
  function zChoice(o,x){
    let z=0;
    for(let h=0;h<o.edges.length;h++){const [i,j]=o.edges[h];if(bit(x,i)===bit(x,j)&&bit(x,i)===0)z|=(1<<h);}
    return z;
  }
  function degreeWitness(clauses,n){
    const seen=new Set(),occ=Array(n).fill(0);
    for(const raw of clauses){
      const cl=[...raw].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b),key=cl.join(",");
      if(seen.has(key))continue;seen.add(key);
      for(const l of cl)occ[Math.abs(l)-1]++;
    }
    return occ.map(x=>x>2?0:1);
  }
  function rankExact(input){
    const M=input.map(row=>row.map(BigInt));const n=M.length,m=M[0].length;
    const abs=a=>a<0n?-a:a;
    const gcd=(a,b)=>{a=abs(a);b=abs(b);while(b!==0n){const r=a%b;a=b;b=r;}return a;};
    let r=0;
    for(let c=0;c<m&&r<n;c++){
      let p=r;while(p<n&&M[p][c]===0n)p++;
      if(p===n)continue;
      [M[r],M[p]]=[M[p],M[r]];
      for(let i=r+1;i<n;i++)if(M[i][c]!==0n){
        const a=M[r][c],b=M[i][c];
        for(let j=c;j<m;j++)M[i][j]=a*M[i][j]-b*M[r][j];
        let g=0n;for(let j=c;j<m;j++)g=gcd(g,M[i][j]);
        if(g>1n)for(let j=c;j<m;j++)M[i][j]/=g;
      }
      r++;
    }
    return r;
  }
  const cases=[];
  for(let k=2;k<=7;k++){
    const o=construct(k),m=o.edges.length,lim=1<<k;
    check(o.clauses.length===2*(k+m),"clause count "+k);
    check(o.n===3*k+m,"variable count "+k);
    const seen=new Set(o.clauses.map(cl=>cl.join(",")));
    check(seen.size===o.clauses.length,"duplicate source "+k);
    const deg=Array(o.n).fill(0),plus=Array(o.n).fill(0),minus=Array(o.n).fill(0);
    for(const c of o.clauses)for(const l of c){const i=Math.abs(l)-1;deg[i]++;(l>0?plus:minus)[i]++;}
    for(let i=0;i<o.n;i++){
      check(plus[i]>0&&minus[i]>0,"nonpure "+k+"/"+i);
      check(deg[i]===(i<k?2*k:2),"degree "+k+"/"+i);
    }
    const witness=degreeWitness(o.clauses,o.n);
    check(satisfies(o.clauses,witness),"degree witness "+k);
    check(!satisfies(o.clauses,Array(o.n).fill(0)),"allzero fails "+k);
    check(!satisfies(o.clauses,Array(o.n).fill(1)),"allone fails "+k);
    const reordered=o.clauses.slice().reverse().map(c=>c.slice().reverse());
    check(satisfies(reordered,degreeWitness(reordered,o.n)),"reordered "+k);
    const renamed=o.clauses.slice().reverse().map(c=>c.map(l=>Math.sign(l)*(o.n+1-Math.abs(l))));
    check(satisfies(renamed,degreeWitness(renamed,o.n)),"renamed "+k);
    const dupl=o.clauses.concat(o.clauses.slice(0,Math.min(5,o.clauses.length)));
    check(satisfies(dupl,degreeWitness(dupl,o.n)),"dedup "+k);
    const qnae=[[0,0,1],[0,1,0],[0,1,1],[1,0,0],[1,0,1],[1,1,0]];
    for(const [u,v,w] of qnae){
      const x=Array(k).fill(0),y=Array(k).fill(1),ww=Array(k).fill(0),zz=Array(m).fill(0);
      x[0]=u;y[0]=v;ww[0]=w;
      for(let h=0;h<m;h++){
        const [i,j]=o.edges[h];zz[h]=x[i]===x[j]?1-x[i]:0;
      }
      const vals=Array(o.n).fill(0);
      for(let i=0;i<k;i++){vals[i]=x[i];vals[k+i]=y[i];vals[2*k+i]=ww[i];}
      for(let h=0;h<m;h++)vals[3*k+h]=zz[h];
      check(satisfies(o.clauses,vals),"NAE existential projection "+k+"/"+[u,v,w]);
    }
    let fool=0;
    for(let a=0;a<lim;a++){
      const ca={y:(lim-1)^a,w:0,z:zChoice(o,a)};
      check(f(o,a,ca.y,ca.w,ca.z)===1,"fooling diagonal "+k+"/"+a);
      for(let b=a+1;b<lim;b++){
        const cb={y:(lim-1)^b,w:0,z:zChoice(o,b)};
        check(f(o,a,cb.y,cb.w,cb.z)===0||f(o,b,ca.y,ca.w,ca.z)===0,"fooling cross "+k+"/"+a+","+b);
        fool++;
      }
    }
    let exactRank=null;
    if(k<=4){
      const K=[];
      for(let a=0;a<lim;a++){
        const row=[];const t=count(Array.from({length:k},(_,i)=>bit(a,i))),c=2**(t*(k-t));
        for(let b=0;b<lim;b++){
          let value=0;
          for(let z=0;z<(1<<m);z++)value+=f(o,a,b,0,z);
          const product=Array.from({length:k},(_,i)=>bit(a,i)||bit(b,i)).every(Boolean)?1:0;
          check(value===c*product,"row-sum "+k+"/"+a+","+b);
          row.push(value);
        }
        K.push(row);
      }
      exactRank=rankExact(K);
      check(exactRank===lim,"rank full "+k);
    }
    cases.push({k,variables:o.n,nae_blocks:k+m,clauses:o.clauses.length,primal_clique:k,rank_over_Q:"2^"+k,rectangle_cover:"2^"+k,exact_row_sum_rank_checked:exactRank,fooling_pairs:fool,degree_witness:true,permutation_renaming_duplicate_controls:true});
  }
  return {name:"TMR2_NAE_RANK_FOOLING075",timestamp_PST:"2026-11-15 01:13 PST",status:"COMPUTATIONAL (finite V8) plus separately proved symbolic family",assertions,failed:0,arithmetic:"BigInt exact rank elimination and integer row sums; no floating point rank",cases,limitations:["No physical Turing-machine executable compiled","No inference of SAT superpolynomial lower bound","Independent mathematical peer review OPEN"]};
};
console.log(JSON.stringify(run(),null,2));
