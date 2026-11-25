function checkDA13(){
  const stats={assertions:0,rank_calls:0,closure_scans:0,forced_rows:0,guard_branches:0,reference_words:0,labeled_graphs:0,cut_checks:0,extra_guard_checks:0,independent_cases:0,parallel_controls:0};
  function ok(x){stats.assertions++;if(!x)throw Error("assertion "+stats.assertions)}
  function rank(rows){stats.rank_calls++;const b=[];let r=0;for(let x of rows){while(x){let i=31-Math.clz32(x);if(b[i])x^=b[i];else{b[i]=x;r++;break}}}return r}
  function parity(x){let p=0;while(x){p^=1;x&=x-1}return p}
  function sym(x,y,n){const m=(1<<n)-1;return parity((x&m)&(y>>n))^parity((y&m)&(x>>n))}
  function defect(H,n){return rank(H.map(x=>H.reduce((a,y,j)=>a|(sym(x,y,n)<<j),0)))}
  function d(e){return (1<<e[0])^(1<<e[1])}
  function row(e,l,n){return ((l&1)?d(e):0)^((l&2)?d(e)<<n:0)}
  function full(E,n){return E.flatMap(e=>[row(e,1,n),row(e,2,n)])}
  function cut(A,B){return rank(A)+rank(B)-rank(A.concat(B))}
  function qcut(A,B,H){return rank(A.concat(H))+rank(B.concat(H))-rank(A.concat(B,H))-rank(H)}
  function basisRows(rows){const b=[];for(const x of rows)if(rank(b.concat(x))>b.length)b.push(x);return b}
  function comps(n,E){let a=Array.from({length:n},(_,i)=>i);function f(x){while(a[x]!==x)x=a[x];return x}for(const [u,v] of E)a[f(u)]=f(v);let m={};for(let i=0;i<n;i++)m[f(i)]=(m[f(i)]||0)+1;return Object.values(m)}
  const K4=[];for(let i=0;i<4;i++)for(let j=i+1;j<4;j++)K4.push([i,j]);
  for(let z=0;z<4096;z++){
    let E=[],H=[],ls=[];for(let i=0;i<6;i++){let l=(z>>(2*i))&3;if(l){E.push(K4[i]);H.push(row(K4[i],l,4));ls.push(l)}}
    const R=rank(H),r=rank(E.map(d)),rho=defect(H,4),t=comps(4,E).filter(x=>x%2===0).length,delta=Math.max(0,...Array.from({length:4},(_,v)=>E.filter(e=>e.includes(v)).length)),maxRow=Math.max(0,2*(delta-1));
    ok(rho%2===0);ok(rho>=2*(R-r-t));ok(R-r<=maxRow*rho);
    if(rho===0){ok(R===r);for(let i=0;i<E.length;i++)for(let j=i+1;j<E.length;j++)if(E[i].some(v=>E[j].includes(v)))ok(ls[i]===ls[j])}
    if(R===E.length){stats.independent_cases++;ok(E.length-r<=maxRow*rho);if(rho===0)ok(E.length===r)}
    for(let mask=0;mask<(1<<E.length);mask++){
      let X=[],Y=[],HX=[],HY=[];for(let i=0;i<E.length;i++)if(mask>>i&1){X.push(E[i]);HX.push(H[i])}else{Y.push(E[i]);HY.push(H[i])}
      let lam=cut(X.map(d),Y.map(d)),sel=cut(HX,HY),w=qcut(full(X,4),full(Y,4),H);
      ok(sel>=lam-maxRow*rho);ok(w>=lam-(R-r));if(rho===0)ok(w===lam&&sel===lam);
      stats.cut_checks++;
      if(mask===Math.floor((1<<E.length)/3)){
        let G=basisRows(H);G=basisRows(G.concat(((z*73+17)&255)));let h=G.length;
        ok(qcut(full(X,4),full(Y,4),G)>=lam-(h-r));stats.extra_guard_checks++;
      }
    }stats.labeled_graphs++;
  }
  // Parallel edges show that zero symplectic defect need not imply a uniform direction.
  let E=[[0,1],[0,1]],H=[row(E[0],1,2),row(E[1],2,2)];
  ok(defect(H,2)===0&&rank(H)===2&&rank(E.map(d))===1);stats.parallel_controls++;
  // Affine chart: equations represented as row | (rhs<<n); local acceptance hull via all four observed words.
  function solve(n,P){
    const mask=(1<<n)-1;
    function good(G){return rank(G)===rank(G.map(x=>x&mask))}
    function closure(G){
      G=G.slice();
      if(!good(G))return null;
      while(true){
        stats.closure_scans++;let added=false;
        for(const [a,b,s] of P){
          let words=[];
          for(let v=0;v<4;v++)if(v!==s&&good(G.concat(a|((v&1)<<n),b|(((v>>1)&1)<<n))))words.push(v);
          if(!words.length)return null;
          for(let l=1;l<=3;l++){
            let p=parity(l&words[0]);if(words.every(v=>parity(l&v)===p)){
              let r=((l&1)?a:0)^((l&2)?b:0);
              if(!good(G.concat(r|(p<<n))))throw Error("bad closure");
              if(rank(G.map(x=>x&mask).concat(r))>rank(G.map(x=>x&mask))){
                G.push(r|(p<<n));stats.forced_rows++;added=true;break;
              }
            }
          }
          if(added)break;
        }
        if(!added)return G;
      }
    }
    function rec(G){
      G=closure(G);if(G===null)return 0;
      let rows=G.map(x=>x&mask),r=rank(rows);
      // All-hit or not: if a forbidden word is impossible then owner is tautological; otherwise rank-two owner branches.
      let choice=0;
      for(const [a,b,s] of P)if(good(G.concat(a|((s&1)<<n),b|(((s>>1)&1)<<n)))){
        if(rank(rows.concat(a,b))-r===2){choice=a;break}
        // A rank <= 1 active blocker must have been removed or made impossible by closure.
        throw Error("stagnation");
      }
      if(!choice)return 2**(n-r);
      stats.guard_branches++;return rec(G.concat(choice))+rec(G.concat(choice|(1<<n)));
    }
    let count=rec([]),ref=0;for(let x=0;x<(1<<n);x++){stats.reference_words++;if(P.every(([a,b,s])=> (parity(a&x)+2*parity(b&x))!==s))ref++}
    ok(count===ref);return count;
  }
  const K5=[];for(let i=0;i<5;i++)for(let j=i+1;j<5;j++)K5.push([i,j]);let p=K5.map(e=>[row(e,1,5),row(e,2,5),0]);
  const k5={root:solve(10,p),deletions:[],signs:[]};for(let i=0;i<p.length;i++){k5.deletions.push(solve(10,p.filter((_,j)=>j!==i)));k5.signs.push(solve(10,p.map((a,j)=>j===i?[a[0],a[1],1]:a)))}
  const triples=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]];
  const f=triples.map(([a,b,c])=>[(1<<a)^(1<<b),(1<<a)^(1<<c),0]);
  const fano={root:solve(7,f),signs:[]};for(let i=0;i<7;i++)for(let s=1;s<=3;s++)fano.signs.push(solve(7,f.map((a,j)=>j===i?[a[0],a[1],s]:a)));
  return {stats,k5,fano};
}
console.log(JSON.stringify(checkDA13(),null,2));
