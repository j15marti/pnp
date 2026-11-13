/* TMR-5 independent oracle for observation potential and strict E(a,b) gadget. Node: node tmr5_observation_independent.cjs */
const auditTMR5 = function auditTMR5(){
  const stats={status:"COMPUTATIONAL",date_pst:"2026-11-13 13:48 PST",families:0,states:0,edge_inequalities:0,optimality:0,strict_equality_formulas:0,sat_assignments_tested:0,opposite_label_flips:0,scoped_falsifiers:[],errors:[]};
  const bits=x=>{let b=0;for(;x;x&=x-1)b++;return b};
  const tau=(L,ds,U)=>{if(U===0)return 0;let best=L+1;for(let j=0;j<(1<<L);j++){let ok=true;for(let i=0;i<ds.length;i++)if((U&(1<<i))&&(j&ds[i])===0){ok=false;break}if(ok)best=Math.min(best,bits(j))}return best};
  for(let L=1;L<=5;L++){
    const masks=Array.from({length:(1<<L)-1},(_,i)=>i+1);
    for(let r=1;r<=3;r++){
      function explore(ds,start){
        if(ds.length<r){for(let i=start;i<masks.length;i++)explore([...ds,masks[i]],i);return}
        stats.families++;
        const memo={0:0};
        function shortest(U){
          if(U===0)return 0;
          if(memo[U]!==undefined)return memo[U];
          let best=1e6;
          for(let j=0;j<L;j++){let V=U;for(let i=0;i<r;i++)if(ds[i]&(1<<j))V &=~(1<<i);if(V!==U)best=Math.min(best,1+shortest(V))}
          memo[U]=best;return best;
        }
        for(let U=0;U<(1<<r);U++){
          stats.states++;const t=tau(L,ds,U),d=shortest(U);
          if(t!==d)throw Error(`shortest mismatch ${L} ${ds} ${U} ${t} ${d}`);
          if(t>L)throw Error("linear ceiling");
          stats.optimality++;
          for(let j=0;j<L;j++){
            let V=U;for(let i=0;i<r;i++)if(ds[i]&(1<<j))V&=~(1<<i);
            const cost=V===U?0:1;
            if(t>cost+tau(L,ds,V))throw Error(`potential inequality ${L} ${ds} ${U} ${j}`);
            stats.edge_inequalities++;
          }
        }
      }
      explore([],0);
    }
  }
  function addGadget(clauses,core,aux1,aux2,forced){
    const sign=forced===1?0:1;
    for(let u=0;u<=1;u++)for(let v=0;v<=1;v++)
      clauses.push([[core,sign],[aux1,u],[aux2,v]]);
  }
  function build(n,a,b){
    const clauses=[];
    for(let i=0;i<n;i++)addGadget(clauses,i,n+i,2*n+i,(a>>i)&1);
    for(let i=0;i<n;i++)addGadget(clauses,i,3*n+i,4*n+i,(b>>i)&1);
    return clauses;
  }
  function count(n,clauses){
    let found=0;
    for(let x=0;x<(1<<(5*n));x++){
      stats.sat_assignments_tested++;
      if(clauses.every(c=>c.some(([v,s])=>(((x>>v)&1)^s)===1)))found++;
    }
    return found;
  }
  for(let n=1;n<=2;n++)for(let a=0;a<(1<<n);a++)for(let b=0;b<(1<<n);b++){
    const c=build(n,a,b);
    if(c.length!==8*n||c.some(row=>new Set(row.map(z=>z[0])).size!==3))throw Error("encoding not proper");
    const models=count(n,c);
    if((models>0)!==(a===b))throw Error(`incorrect equality ${n},${a},${b},${models}`);
    stats.strict_equality_formulas++;
    if(a===b){
      for(let i=0;i<2*n;i++){
        const changed=c.map(row=>row.map(z=>z.slice()));
        for(let j=4*i;j<4*i+4;j++)changed[j][0][1]^=1;
        if(count(n,changed)!==0)throw Error(`sensitive block invalid ${n},${a},${i}`);
        stats.opposite_label_flips++;
      }
    }
  }
  if(tau(3,[0b011,0b110],3)!==1)throw Error("overlap control");
  stats.scoped_falsifiers.push("overlap {0,1},{1,2} has optimal charge 1, not 2");
  if(tau(5,[1,2,4,8,16],31)!==5)throw Error("singleton control");
  stats.scoped_falsifiers.push("five singleton differences attain observation ceiling L=5");
  if(!(tau(3,[1,2],3)>0))throw Error("zero cost control");
  stats.scoped_falsifiers.push("any zero-cost edge from nonempty U to goal violates positive potential inequality");
  return stats;
};
const result=auditTMR5();
process.stdout.write(JSON.stringify(result,null,2)+'\n');
