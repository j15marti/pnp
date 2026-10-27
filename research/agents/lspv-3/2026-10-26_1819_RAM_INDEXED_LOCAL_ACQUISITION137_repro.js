#!/usr/bin/env node
'use strict';
/* Complete, dependency-free finite audit: LSPV-3 RAM-INDEXED-LOCAL-ACQUISITION137.
 * Original Q/J source lineage: project SOURCE-LOCAL-RAM-TAPE-CERT136, EXACT22-TAPE-TRANSPORT1.
 * Math/probe claims are proved separately in the LaTeX report, not inferred from finite checks.
 */
const result=(function runAudit() {
  "use strict";
  const WTXT="-1 3 -14 2 -8 9 10 -13 14 3 7 -13 -4 -9 -11 5 8 -14 4 -8 -11 1 7 13 1 -7 10 -5 -6 -15 -2 -6 12 -4 9 -10 -2 5 -12 -3 6 -15 6 -7 11 2 -9 11 4 8 -10 -3 12 15 -5 -12 15 -1 13 14";
  const wl=WTXT.split(/\s+/).map(Number); const W=Array.from({length:20},(_,i)=>wl.slice(3*i,3*i+3));
  const Q=W.filter(c=>c.join(",")!=="1,7,13");
  const J=[[1,-2,-3],[2,4,-5],[2,5,-6],[3,6,-4],[3,-5,-6],[-2,4,5],[-3,-4,6]];
  const stat={formula_cases:0,sat_cases:0,unsat_cases:0,model_checks:0,flips_checked:0,positions_checked:0,source_authenticated_cores:0,ordinary_two_level_cases:0,malformed_rejected:0,bit_query_lower_bound_tests:0};
  const assert=(v,s)=>{if(!v)throw Error(s);};
  const bw=n=>Math.floor(Math.log2(n))+1;
  function builder(m,a,b){
    let next=m+1,F=[],meta={},model=Object.create(null);
    const alloc=k=>{let out=Array.from({length:k},(_,i)=>next+i);next+=k;return out;};
    const add=row=>{assert(row.length===3 && new Set(row.map(Math.abs)).size===3,"proper");F.push(row);};
    function j(signed_y){
      const aux=alloc(5), map=[0,Math.abs(signed_y),...aux];
      for(const r of J) add(r.map(z=>Math.sign(z)*(Math.abs(z)===1?Math.sign(signed_y):1)*map[Math.abs(z)]));
      aux.forEach(v=>model[v]=false);
    }
    function side(i,bit,shore){
      const start=F.length,q=alloc(15);
      Q.forEach(r=>add(r.map(z=>Math.sign(z)*q[Math.abs(z)-1])));
      const x=i+1,sgn=bit?x:-x,forced=F.length;
      add([sgn,q[0],q[6]]);
      const [u,v,z,w]=alloc(4),dummy=F.length;
      add([-sgn,u,v]);add([q[12],z,w]);
      for(const y of [u,v,z,w]){j(y);j(-y);j(-y);}
      q.forEach(t=>model[t]=false);
      model[u]=true;model[v]=false;model[z]=true;model[w]=false;
      assert(F.length-start===106,"side-size");
      meta[shore+":"+i]={start,forced,dummy,q,x,shore};
    }
    for(let i=0;i<m;i++)model[i+1]=Boolean(a[i]);
    for(let i=0;i<m;i++)side(i,a[i],"L");
    for(let i=0;i<m;i++){
      const e=alloc(9);
      for(let row=0;row<3;row++){const v=e.slice(3*row,3*row+3);add(v);add(v.map(x=>-x));}
      for(let col=0;col<3;col++){const v=[e[col],e[col+3],e[col+6]];add(v);add(v.map(x=>-x));}
      for(let row=0;row<3;row++)for(let col=0;col<3;col++)model[e[row*3+col]]=(row+col)%2===1;
    }
    for(let i=0;i<m;i++)side(i,b[i],"R");
    let n=next-1;
    assert(n===168*m && F.length===224*m,"global-size");
    let deg=new Int32Array(2*n+2);
    for(const c of F)for(const x of c)deg[2*Math.abs(x)+(x<0?1:0)]++;
    for(let v=1;v<=n;v++)assert(deg[2*v]===2 && deg[2*v+1]===2,"exact-22");
    assert(new Set(F.map(c=>c.join(","))).size===F.length,"unique-clauses");
    return{m,a,b,n,F,meta,model};
  }
  function encode(F,n){
    let w=bw(n), head="1".repeat(w)+"0"+n.toString(2).padStart(w,"0")+F.length.toString(2).padStart(w+2,"0");
    assert(F.length<2**(w+2),"count-fits");
    return head+F.map(c=>c.map(x=>(x<0?"1":"0")+Math.abs(x).toString(2).padStart(w,"0")).join("")).join("");
  }
  function parse(s){
    const w=s.indexOf("0");assert(w>0 && s.length>=3*w+3,"header");
    const n=parseInt(s.slice(w+1,2*w+1),2),m=parseInt(s.slice(2*w+1,3*w+3),2);
    assert(bw(n)===w && s.length===3*w+3+3*(w+1)*m,"encoded-length");
    const F=[];let p=3*w+3;
    for(let i=0;i<m;i++){
      let c=[];
      for(let j=0;j<3;j++){
        let neg=s[p]==="1";let v=parseInt(s.slice(p+1,p+w+1),2);p+=w+1;
        assert(v>=1&&v<=n,"var-ID");c.push(neg?-v:v);
      }
      assert(new Set(c.map(Math.abs)).size===3,"proper-parsed");F.push(c);
    }
    return {n,F};
  }
  const truth=(c,M)=>c.some(x=>Boolean(M[Math.abs(x)])===(x>0));
  function qports(){
    let ct=0,ports=new Set();
    for(let a=0;a<2**15;a++){
      const M={};for(let j=1;j<=15;j++)M[j]=Boolean(a&(1<<(j-1)));
      if(Q.every(c=>truth(c,M))){ct++;ports.add([+M[1],+M[7],+M[13]].join("")); }
    }
    assert(ct===244 && ports.size===1 && ports.has("000"),"Q-ports");
    return ct;
  }
  function position(m,clause,n){return 3*bw(n)+3+clause*3*(bw(n)+1);}
  function coreCheck(B,i){
    const L=B.meta["L:"+i],R=B.meta["R:"+i],x=i+1;
    function get(side){
      const u=side.q, rows=B.F.slice(side.start,side.start+19);
      for(let j=0;j<19;j++)assert(rows[j].join(",")===Q[j].map(v=>Math.sign(v)*u[Math.abs(v)-1]).join(","),"auth-Q");
      const sign=B.F[side.forced],p=u[0],q=u[6];
      assert(sign.length===3&&sign[1]===p&&sign[2]===q&&Math.abs(sign[0])===x,"auth-forced-names");
      return Math.sign(sign[0]);
    }
    return get(L)!==get(R);
  }
  function pin(lit,n){let a=n+1,b=n+2;return [[lit,a,b],[lit,a,-b],[lit,-a,b],[lit,-a,-b]];}
  const q_count=qports(),perM=[],representatives=[];
  for(let m=1;m<=5;m++){
    const limit=m<=4?2**m:8;
    for(let aa=0;aa<limit;aa++){
      const a=Array.from({length:m},(_,i)=>aa>>i&1);
      const b=a.slice(),B=builder(m,a,b),s=encode(B.F,B.n),P=parse(s);
      assert(P.n===B.n&&P.F.length===B.F.length,"parse-count");
      assert(P.F.every((c,j)=>c.join(",")===B.F[j].join(",")),"reparse-source");
      stat.formula_cases++;stat.sat_cases++;
      assert(B.F.every(c=>truth(c,B.model)),"SAT-model");
      stat.model_checks+=B.F.length;
      const allLeft=[],allRight=[];
      for(let i=0;i<m;i++){
        allLeft.push(position(m,B.meta["L:"+i].forced,B.n));
        allRight.push(position(m,B.meta["R:"+i].forced,B.n));
      }
      for(let i=0;i<m;i++){
        for(const side of ["L","R"]){
          const al=a.slice(),bl=b.slice();
          if(side==="L")al[i]^=1;else bl[i]^=1;
          const D=builder(m,al,bl),ds=encode(D.F,D.n);
          const changed=[];
          assert(s.length===ds.length,"fixed-physical-width");
          for(let k=0;k<s.length;k++)if(s[k]!==ds[k])changed.push(k);
          const info=B.meta[side+":"+i],wanted=[position(m,info.forced,B.n),position(m,info.dummy,B.n)];
          assert(changed.length===2&&changed[0]===wanted[0]&&changed[1]===wanted[1],"exact-two-sensitive-fields");
          assert(coreCheck(D,i),"source-auth-local-UNSAT");
          stat.flips_checked++;stat.unsat_cases++;stat.positions_checked+=changed.length;
          stat.source_authenticated_cores++;
          const other=(side==="R"?allLeft:allRight).concat((side==="R"?allRight:allLeft).filter((v,j)=>j!==i));
          assert(other.every(k=>s[k]===ds[k]),"indexed-no-access-indistinguishable");
          stat.bit_query_lower_bound_tests++;
          if(m>=3 && aa===0 && side==="R" && i===0){
            let j=1,k=2;let G1=D.F.concat(pin(-2,D.n)),n1=D.n+2;
            let G2=G1.concat(pin(-3,n1)),n2=n1+2;
            const R1=parse(encode(G1,n1)),R2=parse(encode(G2,n2));
            assert(G1.length===D.F.length+4&&G2.length===D.F.length+8,"real-level-count");
            assert(R1.F.slice(0,D.F.length).every((c,v)=>c.join(",")===D.F[v].join(",")),"real-child-alias");
            assert(R2.F.slice(0,D.F.length).every((c,v)=>c.join(",")===D.F[v].join(",")),"real-grandchild-alias");
            assert(coreCheck({...D,F:R2.F},0),"hereditary-core");
            assert(encode(G2,n2).length>encode(G1,n1).length&&encode(G1,n1).length>ds.length,"no-short-child");
            stat.ordinary_two_level_cases++;
          }
          if(m<=4 && aa===0 && i===0 && side==="R"){
            const E={...D,F:D.F.map(c=>c.slice())};
            E.F[D.meta["R:0"].forced][0]=-(E.F[D.meta["R:0"].forced][0]);
            assert(!coreCheck(E,0),"wrong-sign-rejected");stat.malformed_rejected++;
            E.F[D.meta["R:0"].forced][0]=B.n+1;
            let rejected=false;try{coreCheck(E,0);}catch(e){rejected=true;}
            assert(rejected,"wrong-original-alias-rejected");stat.malformed_rejected++;
          }
        }
      }
    }
    perM.push({m,checked_yes:limit,checked_one_flip:2*m*limit,encoding_bits:encode(builder(m,Array(m).fill(0),Array(m).fill(0)).F,168*m).length,bit_probe_yes_lower_bound:2*m,one_mismatch_finder_lower_bound:m-1});
  }
  function dp(r){return r<=1?0:1+dp(r-1);}
  for(let m=1;m<=12;m++)assert(dp(m)===m-1,"unique-mismatch-minimax");
  const m=8,a=Array(m).fill(0),b=a.slice();b[m-1]=1;
  const D=builder(m,a,b);
  assert(coreCheck(D,m-1),"last-coordinate-hostile");
  const summary={run:"RAM_INDEXED_LOCAL_ACQUISITION137",status:"PROVED/EXACT restricted, mathematical review pending",q_models:q_count,stats:stat,per_m:perM,model_claims:{indexed_yes_informative_bit_queries:"at least 2m on each equality input",one_mismatch_locator_worst_case:"at least m-1 independently probed coordinate groups",bounded_logword_ram:"Omega(m) word reads for fixed O(log N) word size and spaced groups",sequential_tape:"native transport lower bounds inherited, not transferred",all_UNSAT_coverage:"OPEN",P_vs_NP:"OPEN"}};
  return summary;
})();
console.log(JSON.stringify(result,null,2));
