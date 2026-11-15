"use strict";
// TMR-4/052, revision multicut-frontier-052.v1
// Deterministic exhaustive exact GF(2), modular-prime and all-order/all-partition audit.
// Standalone: node experiments/tmr/tmr4_multicut_frontier052.js
function permutations(a) {
  const out=[];
  function go(p,r){if(!r.length){out.push(p);return;}for(let i=0;i<r.length;i++)go(p.concat(r[i]),r.slice(0,i).concat(r.slice(i+1)));}
  go([],a);return out;
}
function embed(vars, bits){let s=0;for(let i=0;i<vars.length;i++)if((bits>>i)&1)s|=1<<vars[i];return s;}
function disj(s,k){for(let i=0;i<k;i++)if(((s>>i)&1)&&((s>>(k+i))&1))return 0;return 1;}
function inner(s,k){let z=0;for(let i=0;i<k;i++)z^=((s>>i)&1)&((s>>(k+i))&1);return z;}
function eq(s,k){for(let i=0;i<k;i++)if(((s>>i)&1)!==((s>>(k+i))&1))return 0;return 1;}
function horn(s,n){for(let i=0;i<n;i++)if(((s>>i)&1)&&((s>>((i+1)%n))&1))return 0;return 1;}
function rank2(rows){
  const piv=new Map();let rank=0;
  for(let v of rows){while(v){const p=v.toString(2).length-1;if(piv.has(p))v^=piv.get(p);else{piv.set(p,v);rank++;break;}}}
  return rank;
}
function inverse(a,p){let v=1,t=p-2,b=a;while(t){if(t&1)v=v*b%p;b=b*b%p;t=Math.floor(t/2);}return v;}
function rankMod(rows,p){
  const a=rows.map(row=>row.slice());let r=0;
  for(let col=0;col<a[0].length&&r<a.length;col++){
    let i=r;while(i<a.length&&a[i][col]===0)i++;
    if(i===a.length)continue;
    [a[i],a[r]]=[a[r],a[i]];
    const inv=inverse(a[r][col],p);
    for(let j=col;j<a[r].length;j++)a[r][j]=a[r][j]*inv%p;
    for(let ii=r+1;ii<a.length;ii++){const c=a[ii][col];if(!c)continue;
      for(let j=col;j<a[ii].length;j++)a[ii][j]=(a[ii][j]-c*a[r][j]%p+p)%p;
    }
    r++;
  }
  return r;
}
function matrix(f,X,Y){
  const rows=[],modRows=[];
  for(let a=0;a<(1<<X.length);a++){let v=0n,row=[];
    for(let b=0;b<(1<<Y.length);b++){let x=f(embed(X,a)|embed(Y,b));if(x)v|=1n<<BigInt(b);row.push(x);}
    rows.push(v);modRows.push(row);
  }
  return {gf2:rank2(rows),modRows};
}
function frontierSizes(f,order){
  const n=order.length,F=[];
  for(let p=0;p<=n;p++){
    const pre=order.slice(0,p),suf=order.slice(p),seen=new Set();
    for(let a=0;a<(1<<p);a++){let v=0n;
      for(let b=0;b<(1<<(n-p));b++)if(f(embed(pre,a)|embed(suf,b)))v|=1n<<BigInt(b);
      seen.add(v.toString());
    }F.push(seen.size);
  }
  return F;
}
function checks(f,order,mask,F){
  const X=order.filter(v=>(mask>>v)&1),Y=order.filter(v=>!((mask>>v)&1));
  const switches=[];for(let i=1;i<order.length;i++)if(((mask>>order[i-1])&1)!==((mask>>order[i])&1))switches.push(i);
  let bound=1;for(const i of switches)bound*=F[i];
  const rank=matrix(f,X,Y).gf2;
  if(rank>bound)throw Error("MULTICUT_TARIFF_FAIL:"+JSON.stringify({order,mask,rank,bound,F,switches}));
  return {rank,bound,switches:switches.length};
}
function runAudit(){
  const n=6,k=3,orders=permutations([0,1,2,3,4,5]);
  const families=[
    ["DISJ3",s=>disj(s,k)],["IP3",s=>inner(s,k)],
    ["EQ3",s=>eq(s,k)],["HORN_C6",s=>horn(s,n)],
    ["SINGLETON6",s=>s===0?1:0]
  ];
  const result={revision:"multicut-frontier-052.v1",date_pst:"2026-11-15 12:35 PST",
    scope:"6 Boolean inputs; all 720 orders; 62 nontrivial bipartitions per family",
    seed:null,field:"GF(2) exact BigInt",modulus:65521,
    families:[],assertions:0,failures:0};
  const A=(condition,msg)=>{result.assertions++;if(!condition)throw Error(msg);};
  for(const [name,f] of families){
    let partitions=0, tight=0, maxRank=0,maxFrontier=0,rankOverMaxFrontier=0;
    let badNaive=0,maxBound=0,orderMinMaxFrontier=Number.POSITIVE_INFINITY;
    for(const order of orders){
      const F=frontierSizes(f,order);
      const w=Math.max(...F);maxFrontier=Math.max(maxFrontier,w);
      orderMinMaxFrontier=Math.min(orderMinMaxFrontier,w);
      for(let mask=1;mask<(1<<n)-1;mask++){
        const x=checks(f,order,mask,F);
        partitions++;
        A(x.rank<=x.bound,name+" invalid multicut");
        if(x.rank===x.bound)tight++;
        if(x.rank>w)badNaive++;
        maxRank=Math.max(maxRank,x.rank);
        maxBound=Math.max(maxBound,x.bound);
        rankOverMaxFrontier=Math.max(rankOverMaxFrontier,x.rank/w);
        if(name==="DISJ3"){
          let crossing=0;
          for(let i=0;i<k;i++)if(((mask>>i)&1)!==((mask>>(k+i))&1))crossing++;
          A(x.rank===(1<<crossing),"DISJ tensor rank control");
        }
      }
    }
    A(partitions===720*62,"partition tally");
    result.families.push({name,orders:orders.length,partitions,tight,maxRank,maxFrontier,
      minPeakFrontier:orderMinMaxFrontier,badNaive,maxRankToPeakFrontierRatio:rankOverMaxFrontier,maxBound});
  }
  const grouped=[0,1,2,3,4,5],interleaved=[0,3,1,4,2,5],X=[0,1,2],Y=[3,4,5];
  const Dg=matrix(s=>disj(s,k),X,Y),Ig=matrix(s=>inner(s,k),X,Y);
  const Dint=frontierSizes(s=>disj(s,k),interleaved);
  const Dgroup=frontierSizes(s=>disj(s,k),grouped);
  const Iint=frontierSizes(s=>inner(s,k),interleaved);
  const Igroup=frontierSizes(s=>inner(s,k),grouped);
  A(Dg.gf2===8,"DISJ grouped rank");
  A(Ig.gf2===3,"IP grouped GF2 rank");
  A(rankMod(Ig.modRows,65521)===7,"IP grouped odd-prime rank");
  A(rankMod(Dg.modRows,65521)===8,"DISJ grouped odd-prime rank");
  A(Math.max(...Dint)<=3,"DISJ interleaved peak frontier");
  A(Math.max(...Iint)<=4,"IP interleaved peak frontier");
  A(Dg.gf2>Math.max(...Dint),"naive non-prefix transfer falsified");
  result.witness={DISJ3:{groupedRankGF2:Dg.gf2,groupedRankPrime:rankMod(Dg.modRows,65521),
    groupedFrontiers:Dgroup,interleavedFrontiers:Dint,naiveSingleFrontierFalse:true},
    IP3:{groupedRankGF2:Ig.gf2,groupedRankPrime:rankMod(Ig.modRows,65521),
      groupedFrontiers:Igroup,interleavedFrontiers:Iint}};
  return result;
}
if(typeof module!=="undefined"&&module&&module.exports)module.exports={runAudit};
if(typeof require!=="undefined"&&typeof module!=="undefined"&&require.main===module)console.log(JSON.stringify(runAudit(),null,2));
