#!/usr/bin/env node
'use strict';
// TMR-2/050 reproducible exact Q and GF(2) rank checks, no dependencies.
const runBench=function runBench(){
  const assert=(x,msg)=>{if(!x)throw Error(msg)};
  const pin=(z,a,b)=>{const C=[];for(let v=1;v<8;v++){C.push([0,1,2].map((j)=>((v>>j)&1)?-[z,a,b][j]:[z,a,b][j]))}return C};
  const create=(type,k,edges=[])=>{
    const n=type==="GRAPH"?k:2*k,z=n+1,a=n+2,b=n+3,base=pin(z,a,b),eq=[],pins=[];
    if(type==="EQ"){for(let i=1;i<=k;i++){eq.push([-i,k+i,z],[i,-(k+i),z]);pins.push([-i,a,b])}}
    if(type==="DISJ"){for(let i=1;i<=k;i++)eq.push([-i,-(k+i),z])}
    if(type==="GRAPH"){for(const [u,v] of edges)eq.push([-u,-v,z])}
    const all=base.concat(eq,pins), dimacs=`p cnf ${n+3} ${all.length}\n`+all.map(c=>c.join(" ")+" 0\n").join("");
    assert(all.every(c=>c.length===3&&new Set(c.map(Math.abs)).size===3),"proper ternary");
    assert(new Set(all.map(c=>c.join(","))).size===all.length,"duplicate clauses");
    assert(evaluate(all,Array(n+4).fill(0)),"all-zero witness");
    return {type,k,n,z,a,b,base,eq,pins,all,meta:{vars:n+3,clauses:all.length,literal_occurrences:3*all.length,dimacs_utf8_bytes:dimacs.length}}
  };
  function evaluate(clauses,v){return clauses.every(c=>c.some(l=>v[Math.abs(l)]===(l>0?1:0)))}
  function gf2(M){let a=M.map(row=>row.reduce((s,v,j)=>v?(s|(1n<<BigInt(j))):s,0n)),r=0,xors=0,nc=M[0].length;
    for(let j=0;j<nc;j++){let p=-1;for(let i=r;i<a.length;i++)if((a[i]>>BigInt(j))&1n){p=i;break}
      if(p<0)continue;[a[r],a[p]]=[a[p],a[r]];
      for(let i=r+1;i<a.length;i++)if((a[i]>>BigInt(j))&1n){a[i]^=a[r];xors++}
      r++;if(r===a.length)break
    }return {rank:r,row_xors:xors}
  }
  const ab=x=>x<0n?-x:x,gcd=(a,b)=>{a=ab(a);b=ab(b);while(b){const r=a%b;a=b;b=r}return a||1n};
  const F=(n,d=1n)=>{n=BigInt(n);d=BigInt(d);assert(d!==0n,"denominator");if(d<0n){n=-n;d=-d}if(n===0n)return [0n,1n];const g=gcd(n,d);return [n/g,d/g]};
  const plus=(a,b)=>F(a[0]*b[1]+b[0]*a[1],a[1]*b[1]);
  const neg=a=>[-a[0],a[1]], sub=(a,b)=>plus(a,neg(b)),mul=(a,b)=>F(a[0]*b[0],a[1]*b[1]),div=(a,b)=>F(a[0]*b[1],a[1]*b[0]);
  function qrank(M){const a=M.map(row=>row.map(v=>F(v))),cols=M[0].length;let r=0,ops=0,maxNum=1,maxDen=1;
    for(let j=0;j<cols;j++){let p=-1;for(let i=r;i<a.length;i++)if(a[i][j][0]!==0n){p=i;break}
      if(p<0)continue;[a[r],a[p]]=[a[p],a[r]];const pivot=a[r][j];
      for(let i=r+1;i<a.length;i++){if(a[i][j][0]===0n)continue;
        const ratio=div(a[i][j],pivot);ops++;
        for(let c=j+1;c<cols;c++){a[i][c]=sub(a[i][c],mul(ratio,a[r][c]));ops+=2;
          maxNum=Math.max(maxNum,ab(a[i][c][0]).toString(2).length);
          maxDen=Math.max(maxDen,a[i][c][1].toString(2).length);
        }a[i][j]=F(0)
      }r++;if(r===a.length)break
    }return {rank:r,exact_field_operations_upper:ops,max_numerator_bits:maxNum,max_denominator_bits:maxDen}
  }
  function matrixXY(k,clauses){const M=[];for(let x=0;x<(1<<k);x++){const row=[];
      for(let y=0;y<(1<<k);y++){const v=Array(2*k+4).fill(0);
        for(let j=0;j<k;j++){v[j+1]=(x>>j)&1;v[k+j+1]=(y>>j)&1}
        row.push(evaluate(clauses,v)?1:0)
      }M.push(row)
    }return M
  }
  function graphMatrix(n,edges,part,clauses){const A=part,B=[];for(let i=1;i<=n;i++)if(!A.includes(i))B.push(i);const M=[];
    for(let x=0;x<(1<<A.length);x++){const row=[];
      for(let y=0;y<(1<<B.length);y++){const v=Array(n+4).fill(0);
        A.forEach((id,j)=>v[id]=(x>>j)&1);B.forEach((id,j)=>v[id]=(y>>j)&1);
        row.push(evaluate(clauses,v)?1:0)
      }M.push(row)
    }return M
  }
  const eq=[],disj=[];
  for(let k=1;k<=5;k++){
    let f=create("EQ",k), orders={};
    for(const [name,seq] of [["good",f.pins.concat(f.eq)],["bad",f.eq.concat(f.pins)]]){
      const ranks=[];let xors=0;
      for(let j=0;j<=seq.length;j++){let z=gf2(matrixXY(k,f.base.concat(seq.slice(0,j))));ranks.push(z.rank);xors+=z.row_xors}
      orders[name]={prefix_ranks_GF2:ranks,peak_rank_GF2:Math.max(...ranks),total_GF2_row_xors:xors}
    }
    assert(orders.good.peak_rank_GF2===1&&orders.bad.peak_rank_GF2===(1<<k),"prefix rank gap");
    const bad=qrank(matrixXY(k,f.base.concat(f.eq))),end=qrank(matrixXY(k,f.all));
    assert(bad.rank===(1<<k)&&end.rank===1,"exact Q equality rank");
    let count=0;for(let x=0;x<(1<<(2*k+3));x++){const v=Array(2*k+4).fill(0);for(let i=0;i<2*k+3;i++)v[i+1]=(x>>i)&1;if(evaluate(f.all,v))count++}
    assert(count===1,"unique full solution");
    eq.push({k,cnf:f.meta,full_satisfying_assignments:count,intermediate_rank_Q:bad.rank,final_rank_Q:end.rank,arithmetic_bad:bad,arithmetic_final:end,orders});
    f=create("DISJ",k);
    const M=matrixXY(k,f.all),r=gf2(M),q=qrank(M),solutions=M.flat().reduce((a,b)=>a+b,0);
    assert(r.rank===q.rank&&q.rank===(1<<k)&&solutions===3**k,"DISJ ranks and counts");
    disj.push({k,cnf:f.meta,rank_Q:q.rank,rank_GF2:r.rank,number_solutions:solutions,arithmetic:q});
  }
  const cube=[];for(let u=0;u<8;u++)for(let b=0;b<3;b++){let v=u^(1<<b);if(u<v)cube.push([u+1,v+1])}
  const ps=new Set();const add=(x,y)=>ps.add([Math.min(x,y),Math.max(x,y)].join(","));
  for(let i=0;i<5;i++){add(i+1,((i+1)%5)+1);add(i+6,((i+2)%5)+6);add(i+1,i+6)}
  const petersen=[...ps].map(s=>s.split(",").map(Number));
  const graphs=[];
  for(const [name,n,edges,cuts] of [
      ["cube_Q3",8,cube,[[1,2,3,4],[1,3,5,7],[1,3,4,6]]],
      ["petersen",10,petersen,[[1,2,3,4,5],[1,3,5,7,9],[3,4,7,9,10]]]]){
    let f=create("GRAPH",n,edges);
    const cr=cuts.map(A=>{const M=graphMatrix(n,edges,A,f.all),r=gf2(M),q=qrank(M);assert(r.rank===q.rank,"graph exact Q/GF2 match");return {cut_A:A,rank_GF2:r.rank,rank_Q:q.rank,arithmetic:q}});
    graphs.push({name,n,edges:edges.length,cnf:f.meta,cuts:cr,all_zero_witness:true});
  }
  const H=[[1,1],[1,-1]],D=[[1,1],[1,0]];
  const HDH=H.map((row,i)=>H.map((_,j)=>row.reduce((sum,_,u)=>sum+H[i][u]*D[u][0]*H[j][0]+H[i][u]*D[u][1]*H[j][1],0)));
  assert(JSON.stringify(HDH)==="[[3,1],[1,-1]]","Walsh multiplication");
  assert(qrank(D).rank===2&&qrank(HDH).rank===2&&gf2(D).rank===2&&gf2(HDH).rank===1,"Walsh characteristic");
  return {code:"tmr2_dynamic_prefix_rank050.js",revision:"v1.0.0",timestamp_PST:"2026-11-15 11:19 PST",seed:"none (fixed graph cuts)",matrices:"fixed-formula assignment evaluation, not SAT decision on encodings",exact_arithmetic:"BigInt fractions (Q), independent BigInt bit-row GF2",eq,disj,graphs,walsh:{D,H,HDH,rank_Q:[2,2],rank_GF2:[2,1]},errors:0};
};
const result=runBench();
console.log(JSON.stringify(result,null,2));
