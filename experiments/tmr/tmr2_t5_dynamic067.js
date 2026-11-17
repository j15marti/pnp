"use strict";
// TMR-2/067 source-authenticated five-symbol CSP audits. No external packages.
// Run: node tmr2_t5_dynamic067.js
function audit(){
  const SEED=202611171212, K=5, ALL=31;
  const R=(a,b)=>[1,3].includes((b-a+5)%5);
  const OUT=Array.from({length:5},(_,a)=>Array.from({length:5},(_,b)=>R(a,b)?1<<b:0).reduce((p,q)=>p|q,0));
  const IN=Array.from({length:5},(_,b)=>Array.from({length:5},(_,a)=>R(a,b)?1<<a:0).reduce((p,q)=>p|q,0));
  const out=m=>OUT.reduce((v,o,i)=>m>>i&1?v|o:v,0);
  const inc=m=>IN.reduce((v,o,i)=>m>>i&1?v|o:v,0);
  const pop=m=>m.toString(2).replace(/0/g,"").length;
  const fail=(cond,why)=>{if(!cond)throw Error(why)};
  const domainTable=Array.from({length:32},(_,m)=>({mask:m,pop:pop(m),out:out(m),in:inc(m)}));
  const actualMasks=new Set([ALL,0,...OUT,...IN,...Array.from({length:5},(_,i)=>1<<i)]);
  fail(actualMasks.size===12,"12-mask alphabet");
  for(let a=0;a<5;a++)fail(IN[a]===OUT[(a+1)%5],"in/out rotation");
  const hist={};for(const z of domainTable){const k=`${z.pop}->${pop(z.out)}`;hist[k]=(hist[k]||0)+1}
  const mat=Array.from({length:5},(_,a)=>Array.from({length:5},(_,b)=>R(a,b)?1:0));
  // Exact 5x5 determinant by permutations, no floating point.
  function det(a){if(a.length===1)return a[0][0];let v=0;for(let j=0;j<a.length;j++){const b=a.slice(1).map(row=>row.filter((_,k)=>j!==k));v+=(j%2?-1:1)*a[0][j]*det(b)}return v}
  const determinant=det(mat);fail(determinant===2,"det");
  function rank2(m){m=m.map(x=>x.slice());let rank=0;for(let j=0;j<5;j++){let pivot=rank;while(pivot<5&&!m[pivot][j])pivot++;if(pivot===5)continue;[m[pivot],m[rank]]=[m[rank],m[pivot]];for(let i=0;i<5;i++)if(i!==rank&&m[i][j])for(let c=j;c<5;c++)m[i][c]^=m[rank][c];rank++}return rank}
  const rankF2=rank2(mat);fail(rankF2===4,"rankF2");
  let endomorphisms=0,translations=0;
  for(let code=0;code<3125;code++){let x=code;const f=[];for(let i=0;i<5;i++){f.push(x%5);x=Math.floor(x/5)}let ok=true;for(let i=0;i<5&&ok;i++)for(let j=0;j<5;j++)if(R(i,j)&&!R(f[i],f[j])){ok=false;break}if(ok){endomorphisms++;if(f.every((v,i)=>v===(i+f[0])%5))translations++}}
  fail(endomorphisms===5&&translations===5,"template core automorphisms");
  const edgeSet=e=>new Set(e.map(([u,v])=>`${u},${v}`));
  function dp(n,edges){
    const es=edgeSet(edges);if(edges.some(([a,b])=>a===b))return {count:0,states:[1,...Array(n).fill(0)],transitions:0};
    let states=new Map([[Array(n).fill(ALL).join(","),1]]), widths=[1],transitions=0;
    for(let v=0;v<n;v++){
      const next=new Map();
      for(const [key,weight] of states){
        const z=key.split(",").map(Number);
        for(let a=0;a<5;a++)if((z[v]>>a)&1){
          const q=z.slice();q[v]=0;
          let valid=true;
          for(let j=v+1;j<n;j++){
            if(es.has(`${v},${j}`))q[j]&=OUT[a];
            if(es.has(`${j},${v}`))q[j]&=IN[a];
            if(q[j]===0){valid=false;break}
          }
          transitions++;
          if(valid){
            for(let j=v+1;j<n;j++)fail(actualMasks.has(q[j]),"mask closed");
            const k=q.join(",");next.set(k,(next.get(k)||0)+weight)
          }
        }
      }
      states=next;widths.push(states.size)
    }
    return {count:[...states.values()].reduce((x,y)=>x+y,0),states:widths,transitions}
  }
  function brute(n,edges){
    let count=0;const es=edgeSet(edges),all=5**n;
    for(let code=0;code<all;code++){
      let t=code;const x=[];for(let i=0;i<n;i++){x.push(t%5);t=Math.floor(t/5)}
      if(edges.every(([i,j])=>R(x[i],x[j])))count++
    }
    return count
  }
  function pc(n,edges){
    const es=edgeSet(edges), C=[];
    for(let i=0;i<n;i++){C.push([]);for(let j=0;j<n;j++){C[i].push([]);for(let a=0;a<5;a++){let mask=0;for(let b=0;b<5;b++)if((i!==j||a===b)&&(!es.has(`${i},${j}`)||R(a,b))&&(!es.has(`${j},${i}`)||R(b,a)))mask|=1<<b;C[i][j].push(mask)}}}
    let changes=0,rounds=0;
    while(true){let updated=false;rounds++;
      for(let i=0;i<n;i++)for(let j=0;j<n;j++)for(let h=0;h<n;h++)for(let a=0;a<5;a++){
        let m=0;for(let b=0;b<5;b++)if(C[i][h][a]>>b&1)m|=C[h][j][b];
        m&=C[i][j][a];
        if(m!==C[i][j][a]){changes+=pop(C[i][j][a]^m);updated=true;C[i][j][a]=m}
      }
      if(!updated)break;
      fail(rounds<30,"PC did not terminate")
    }
    return {nonempty:C.every(row=>row.every(cols=>cols.some(Boolean))),rounds,removedTuples:changes}
  }
  function width(n,edges){
    const truth=new Uint8Array(5**n);
    for(let code=0;code<truth.length;code++){
      let t=code;const a=[];for(let i=0;i<n;i++){a.push(t%5);t=Math.floor(t/5)}
      truth[code]=edges.every(([i,j])=>R(a[i],a[j]))?1:0;
    }
    // First t variables in little-endian order are fixed; suffix cofactor
    // indices are code=prefix+5^t*suffix (interleaved, not contiguous).
    const v=[];
    for(let t=0;t<=n;t++){
      const prefixN=5**t,suffixN=5**(n-t),seen=new Set();
      for(let p=0;p<prefixN;p++){
        let s="";for(let q=0;q<suffixN;q++)s+=truth[p+prefixN*q];
        seen.add(s);
      }
      v.push(seen.size);
    }
    return v
  }
  const t5=[];for(let i=0;i<5;i++)for(let j=0;j<5;j++)if(R(i,j))t5.push([i,j]);
  const cycle=n=>Array.from({length:n},(_,i)=>[i,(i+1)%n]);
  const path=n=>Array.from({length:n-1},(_,i)=>[i,i+1]);
  const trans=n=>Array.from({length:n},(_,i)=>Array.from({length:n-i-1},(_,k)=>[i,i+k+1])).flat();
  const cases={
    arc:[2,[[0,1]]],two_cycle:[2,[[0,1],[1,0]]],
    loop:[1,[[0,0]]],T5:[5,t5],
    T5_plus_one:[6,[...t5,...Array.from({length:5},(_,i)=>i%2?[5,i]:[i,5])]],
    transitive_T5:[5,trans(5)],transitive_T6:[6,trans(6)],
    two_triangles:[6,[...cycle(3),...cycle(3).map(([a,b])=>[a+3,b+3])]],
    K3_3_forward:[6,Array.from({length:3},(_,i)=>Array.from({length:3},(_,j)=>[i,j+3])).flat()]
  };
  for(let n=3;n<=8;n++)cases[`cycle_${n}`]=[n,cycle(n)];
  for(let n=2;n<=8;n++)cases[`path_${n}`]=[n,path(n)];
  const control={};
  for(const [name,[n,e]] of Object.entries(cases)){
    const d=dp(n,e),b=brute(n,e);fail(d.count===b,`count ${name}`);
    control[name]={n,m:e.length,count:d.count,dpStates:d.states,dpTransitions:d.transitions,pc:pc(n,e),cofactorWidths:n<=7?width(n,e):null};
  }
  fail(control.T5.count===5&&control.T5_plus_one.count===0,"T5 and K6");
  fail(control.K3_3_forward.count===70,"K3_3");
  fail(control.cycle_3.count===15&&control.cycle_5.count===10,"cycle counts");
  // Fixed-seed random graph controls include absent, forward, reverse, and bidirected edges.
  let rng=(SEED>>>0);const rand=()=>{rng^=(rng<<13);rng^=(rng>>>17);rng^=(rng<<5);return rng>>>0};
  let random=0,randomSat=0,maxStates=0;
  for(let n=1;n<=7;n++)for(let rep=0;rep<60;rep++){
    const e=[];
    for(let i=0;i<n;i++)for(let j=i+1;j<n;j++){
      const z=rand()%5;if(z===0)e.push([i,j]);if(z===1)e.push([j,i]);if(z===2)e.push([i,j],[j,i]);
    }
    const d=dp(n,e),b=brute(n,e);
    fail(d.count===b,`random ${n},${rep}`);
    random++;if(b)randomSat++;maxStates=Math.max(maxStates,...d.states);
  }
  return {revision:"tmr2-t5-dynamic067.v1",seed:SEED,strict:"Computational checks, no proof of unrestricted lower bounds",R:mat,OUT,IN,domainTable,domainOutSizeHistogram:hist,possibleResidualMasks:[...actualMasks].sort((a,b)=>a-b),determinant,rankF2,endomorphisms,translations,controls:control,random:{count:random,satisfiable:randomSat,maxStates,failures:0},failures:0};
}
console.log(JSON.stringify(audit(),null,2));
