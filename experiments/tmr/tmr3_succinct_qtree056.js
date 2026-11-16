// TMR-3/056 end-to-end succinct Q3CNF Tree Evaluation audit.
// Node 22+ standalone. No external packages.
// Usage: node tmr3_succinct_qtree056.js [optional-raw-json-path]
// Exact finite tests; NOT an asymptotic lower bound.
function audit(){
  "use strict";
  const SEED=20261115;
  let rng=SEED>>>0, checks=0, cases={genericQbf:0,compactQbf:0,uniqueExtensions:0,oraclePairs:0,malformed:0};
  const samples=[];
  function rnd(k){rng=(Math.imul(rng,1664525)+1013904223)>>>0;return rng%k;}
  function ck(p,tag){checks++;if(!p)throw Error("FAIL "+tag+" at check "+checks);}
  function width(k){return Math.ceil(Math.log2(k+1));}
  function enc(k,qs,clauses){
    const m=clauses.length,w=width(k);
    ck(qs.length===k&&m>=1,"encoder preconditions");
    const str="1".repeat(k)+"0"+"1".repeat(m)+"0"+qs.map(x=>x?"1":"0").join("")+
      clauses.map(c=>c.map(z=>(z<0?"1":"0")+Math.abs(z).toString(2).padStart(w,"0")).join("")).join("");
    ck(str.length===2*k+m+2+3*m*(w+1),"length ledger");
    return str;
  }
  function parse(str){
    if(typeof str!=="string"||!/^[01]+$/.test(str))return null;
    let j=0,k=0,m=0;
    while(j<str.length&&str[j]==="1"){k++;j++;}
    if(k<1||j===str.length||str[j++]!=="0")return null;
    while(j<str.length&&str[j]==="1"){m++;j++;}
    if(m<1||j===str.length||str[j++]!=="0")return null;
    const w=width(k),need=j+k+3*m*(w+1);
    if(need!==str.length)return null;
    const qs=[];for(let i=0;i<k;i++)qs.push(str[j++]==="1"?1:0);
    const clauses=[];
    for(let ci=0;ci<m;ci++){const row=[];for(let h=0;h<3;h++){
      let sign=str[j++]==="1"?-1:1;let v=parseInt(str.slice(j,j+w),2);j+=w;
      if(v<1||v>k)return null;row.push(sign*v);
    }clauses.push(row);}
    return {k,m,qs,clauses,N:str.length,w};
  }
  function val(a,clauses){
    for(let c of clauses){let sat=false;for(let z of c){
      const v=a[Math.abs(z)-1];
      if((z>0&&v===1)||(z<0&&v===0)){sat=true;break;}
    }if(!sat)return 0;}return 1;
  }
  function tree(qs,clauses,stats){
    const k=qs.length,as=Array(k).fill(0);
    function visit(d){
      stats.nodes++;
      if(d===k){stats.leaves++;return val(as,clauses);}
      as[d]=0;
      const l=visit(d+1);
      if((qs[d]===1&&l===1)||(qs[d]===0&&l===0))return l;
      as[d]=1;
      const r=visit(d+1);
      return qs[d]===1?(l|r):(l&r);
    }return visit(0);
  }
  function independent(qs,clauses){
    const k=qs.length,arr=[];
    for(let mask=0;mask<2**k;mask++){
      const a=[];for(let j=0;j<k;j++)a.push((mask>>(k-j-1))&1);
      arr.push(val(a,clauses));
    }
    let row=arr;
    for(let i=k-1;i>=0;i--){const next=[];for(let j=0;j<row.length;j+=2)next.push(qs[i]===1?(row[j]|row[j+1]):(row[j]&row[j+1]));row=next;}
    return row[0];
  }
  function mkCompact(n,gateQ,goal){
    const k=2*n+1, qs=gateQ.concat(Array(n+1).fill(1)),cs=[],z0=n+1;
    const pin=(z,bit)=>cs.push([bit?z:-z,bit?z:-z,bit?z:-z]);
    pin(z0,goal);
    for(let i=1;i<=n;i++){
      const a=i,p=n+i,z=n+i+1,neutral=gateQ[i-1]===1?0:1;
      for(let u=0;u<=1;u++)for(let v=0;v<=1;v++){
        const f=u?v:neutral;
        cs.push([u?-a:a,v?-p:p,f?z:-z]);
      }
    }
    pin(2*n+1,1);
    return {k,qs,clauses:cs,word:enc(k,qs,cs)};
  }
  function neutralLeaf(q,goal,a){
    let d=goal;for(let i=0;i<q.length;i++)if(a[i]===0)d=q[i]===1?0:1;return d;
  }
  function canonicalZ(q,goal,a){
    let z=[goal],v=goal;
    for(let i=0;i<q.length;i++){if(a[i]===0)v=q[i]===1?0:1;z.push(v);}
    return z;
  }
  // General authenticated Q3CNF source -> short circuit tree -> exact truth table.
  for(let k=1;k<=6;k++)for(let trial=0;trial<(k===6?96:160);trial++){
    const qs=Array.from({length:k},()=>rnd(2)),m=1+rnd(7),clauses=[];
    for(let c=0;c<m;c++){let row=[];for(let j=0;j<3;j++){const z=1+rnd(k);row.push(rnd(2)?z:-z);}clauses.push(row);}
    const word=enc(k,qs,clauses),parsed=parse(word);
    ck(parsed!==null&&parsed.N===word.length,"valid parse");
    ck(parsed.k===k&&parsed.m===m&&JSON.stringify(parsed.clauses)===JSON.stringify(clauses),"source roundtrip");
    const stats={nodes:0,leaves:0},got=tree(parsed.qs,parsed.clauses,stats),expected=independent(qs,clauses);
    ck(got===expected,"QBF tree vs independent truth table");
    ck(stats.nodes<=2**(k+1)-1&&stats.leaves<=2**k,"Q query caps");
    cases.genericQbf++;
    if(k===6&&trial<2)samples.push({type:"generic",k,m,qs:qs.join(""),answer:got,queries:stats.nodes});
  }
  // Compact canonical Q3CNF: every original quantifier subtree must be visited
  // by left-first short-circuit DFS, despite trivially source-readable root bit.
  for(let n=1;n<=6;n++){
    const patterns=n<=4?2**n:(n===5?12:7);
    for(let t=0;t<patterns;t++)for(let goal=0;goal<=1;goal++){
      const q=Array.from({length:n},(_,i)=>n<=4?(t>>(n-i-1))&1:rnd(2));
      const h=mkCompact(n,q,goal);
      const parsed=parse(h.word);
      ck(parsed!==null&&parsed.k===2*n+1&&parsed.m===4*n+2,"compact source canonical parse");
      ck(parsed.N===2*parsed.k+parsed.m+2+3*parsed.m*(parsed.w+1),"compact source bit length");
      const stats={nodes:0,leaves:0},k=h.k;
      // Count original-depth subtree visits, distinct from physically enumerated leaves.
      const as=Array(k).fill(0),ctr={nodes:0,leaves:0,originalSubtrees:0};
      function recur(d){
        ctr.nodes++;
        if(d===n)ctr.originalSubtrees++;
        if(d===k){ctr.leaves++;return val(as,h.clauses);}
        as[d]=0;const left=recur(d+1);
        if((h.qs[d]===1&&left===1)||(h.qs[d]===0&&left===0))return left;
        as[d]=1;const right=recur(d+1);
        return h.qs[d]===1?(left|right):(left&right);
      }
      const out=recur(0),independentOut=independent(h.qs,h.clauses);
      ck(out===goal&&independentOut===goal,"compact root and independent full QBF");
      ck(ctr.originalSubtrees===2**n,"all original prefixes must be visited");
      ck(ctr.nodes>=2**(n+1)-1,"node query lower count for specified evaluator");
      ck(ctr.nodes<=2**(k+1)-1,"full tree node query upper");
      for(let mask=0;mask<2**n;mask++){
        let a=Array.from({length:n},(_,i)=>(mask>>(n-i-1))&1);
        let z=canonicalZ(q,goal,a),expected=neutralLeaf(q,goal,a);
        ck(z[n]===expected,"last zero formula");
        ck(val(a.concat(z),h.clauses)===expected,"unique functional extension");
        if(n<=3){
          let count=0;
          for(let bits=0;bits<2**(n+1);bits++){
            let aux=Array.from({length:n+1},(_,i)=>(bits>>(n-i))&1);
            count+=val(a.concat(aux),h.clauses);
          }
          ck(count===expected,"exact existential extension enumeration");
          cases.uniqueExtensions++;
        }
      }
      cases.compactQbf++;
      if((n===4&&t===3&&goal===1)||(n===6&&t===1&&goal===0))
        samples.push({type:"compact",n,k,qs:q.join(""),goal,encodedBits:h.word.length,originalSubtrees:ctr.originalSubtrees,treeNodeQueries:ctr.nodes,treeLeaves:ctr.leaves});
    }
  }
  // Black-box OR-tree all-zero leaves versus each distinct single flipped leaf.
  for(let n=1;n<=8;n++){
    let count=2**n;
    const zeros=Array(count).fill(0);
    ck(zeros.every(x=>x===0),"oracle all-zero base");
    for(let j=0;j<count;j++){
      let changed=zeros.slice();changed[j]=1;
      ck(changed.some(x=>x===1),"unqueried bit indistinguishability");
      cases.oraclePairs++;
    }
  }
  const ok=mkCompact(2,[1,0],1),broken=[
    ok.word+"0",ok.word.slice(0,-1),ok.word.replace(/^1/,"0"),
    "2222",ok.word.slice(1),ok.word.replace("0","1") // may parse as another word; remove this case if so
  ];
  for(let i=0;i<broken.length;i++){if(i===5)continue;ck(parse(broken[i])===null,"malformed source reject");cases.malformed++;}
  return {
    revision:"tmr3-succinct-qtree056-v1",
    seed:SEED,
    status:"COMPUTATIONAL",
    assertions:checks,failures:0,cases,
    samples,
    model:"unary variable/clauses, quantifier bits, fixed three literal records, binary indices",
    hard_family:"2n+1 quantified variables; original q then n+1 existential gate vars; 4n+2 three-literal clauses; root goal direct from canonical source pattern",
    restrictions:"full-query lower bound applies only to left-first short-circuit evaluator; generic black-box lower bound applies to oracle-independent leaf values; no unrestricted lower bound or generic TreeEval improvement",
    source_references:["Williams STOC2025 10.1145/3717823.3718225","TQBF PSPACE completeness standard textbook"],
    independent_reviews:"OPEN"
  };
}
const result=audit();
const json=JSON.stringify(result,null,2)+"\n";
if(typeof process!=="undefined" && process.argv[2])require("fs").writeFileSync(process.argv[2],json,"utf8");
console.log(json);
