'use strict';

function sorted(a){return [...new Set(a)].sort((x,y)=>Math.abs(x)-Math.abs(y)||x-y)};

function mk(h){
 if(!Number.isInteger(h)||h<1)throw Error("bad h");
 const A=j=>2*j+1,B=j=>2*j+2,source={P0:[A(0)]};
 for(let j=1;j<h;j++)source["P"+j]=[B(j-1),A(j)];
 source["P"+h]=[B(h-1)];
 for(let j=0;j<h;j++)source["H"+j]=[-A(j),-B(j)];
 const witness={};
 for(let i=0;i<=h;i++){const on=[];for(let j=0;j<i;j++)on.push(A(j));for(let j=i;j<h;j++)on.push(B(j));witness["P"+i]=on}
 for(let i=0;i<h;i++){const on=[];for(let j=0;j<=i;j++)on.push(A(j));for(let j=i;j<h;j++)on.push(B(j));witness["H"+i]=on}
 let previous="P0";const proof=[],nodes={...source};
 for(let j=0;j<h;j++){
    let id="R"+proof.length,cl=resolution(nodes[previous],nodes["H"+j],A(j));
    proof.push({id,left:previous,right:"H"+j,pivot:A(j),clause:cl});nodes[id]=cl;previous=id;
    id="R"+proof.length;cl=resolution(nodes[previous],nodes["P"+(j+1)],B(j));
    proof.push({id,left:previous,right:"P"+(j+1),pivot:B(j),clause:cl});nodes[id]=cl;previous=id;
 }
 return {h,source,witness,proof}
};

function resolution(a,b,p){
 const L=new Set(a),R=new Set(b),ok=(L.has(p)&&R.has(-p))||(R.has(p)&&L.has(-p));
 if(!ok)throw Error("missing opposing pivot");
 const o=sorted([...L,...R].filter(z=>Math.abs(z)!==p));
 if(o.some(z=>o.includes(-z)))throw Error("tautology");
 return o;
};

function sat(cl,on){return cl.some(z=>z>0?on.has(z):!on.has(-z))};

function verifySets(data){
 const {h,source,witness,proof}=data,expected=mk(h).source;
 if(Object.keys(source).length!==2*h+1||Object.keys(expected).some(k=>JSON.stringify(source[k])!==JSON.stringify(expected[k])))throw Error("source mismatch");
 let checks=1,nodes={...source},depth={};
 for(let id of Object.keys(source))depth[id]=0;
 for(const e of proof){
  if(!(e.left in nodes)||!(e.right in nodes)||e.id in nodes)throw Error("bad node");
  if(JSON.stringify(resolution(nodes[e.left],nodes[e.right],e.pivot))!==JSON.stringify(e.clause))throw Error("false resolvent");
  nodes[e.id]=e.clause;depth[e.id]=1+Math.max(depth[e.left],depth[e.right]);checks++;
 }
 if(proof.length!==2*h||JSON.stringify(proof[proof.length-1].clause)!=="[]")throw Error("wrong proof size or root");
 if(depth[proof[proof.length-1].id]!==2*h)throw Error("span");
 checks++;
 for(const [id,cl] of Object.entries(source)){
   if(!(id in witness))throw Error("witness missing");
   const set=new Set(witness[id]);
   if(Object.entries(source).some(([other,cl2])=>other!==id&&!sat(cl2,set))||sat(cl,set))throw Error("wrong deletion witness");
   checks++;
 }
 return checks
};

function verifyMasks(data){
 const {h,source,witness,proof}=data;
 const encode=(cl)=>{let P=0n,N=0n;for(const z of cl){if(z===0||Math.abs(z)>2*h)throw Error("out of bound");const bit=1n<<BigInt(Math.abs(z)-1);if(z>0)P|=bit;else N|=bit}return {P,N}};
 let checks=0,nodes=new Map;
 for(const [id,cl]of Object.entries(source))nodes.set(id,encode(cl));
 for(const s of proof){
   const l=nodes.get(s.left),r=nodes.get(s.right);
   if(!l||!r)throw Error("bad premise");
   const bit=1n<<BigInt(s.pivot-1);
   if(!((l.P&bit)&&(r.N&bit))&&!((r.P&bit)&&(l.N&bit)))throw Error("bad pivot");
   const P=(l.P|r.P)&~bit,N=(l.N|r.N)&~bit;
   if((P&N)!==0n)throw Error("tautology from proof");
   const e=encode(s.clause);if(e.P!==P||e.N!==N)throw Error("bitmask resolvent differs");
   nodes.set(s.id,e);checks++;
 }
 if(proof.length!==2*h||nodes.get(proof[proof.length-1].id).P!==0n||nodes.get(proof[proof.length-1].id).N!==0n)throw Error("not refutation");
 checks++;
 for(const [id,cl]of Object.entries(source)){
   const on=new Set(witness[id]);
   for(const [other,c]of Object.entries(source)){
     const has=c.some(z=>z>0?on.has(z):!on.has(-z));
     if(has===(other===id))throw Error("invalid deletion truth table");
     checks++;
   }
 }
 return checks
};

function restriction(h){
 const rows=[],pcode=(p,j)=>(p===j?2*j+1:2*j+2);
 for(let p=0;p<h+1;p++){let c=[];for(let j=0;j<h;j++)if(p===j||p===j+1)c.push(pcode(p,j));rows.push(sorted(c))}
 for(let j=0;j<h;j++)for(let p=0;p<h+1;p++)for(let q=p+1;q<h+1;q++)
    if((p===j||p===j+1)&&(q===j||q===j+1))rows.push(sorted([-pcode(p,j),-pcode(q,j)]));
 return rows
};

function audit(){
 let checks=0,neg=0,brute=0,examples={},rows=[];
 for(let h=1;h<=64;h++){
    const x=mk(h),count=verifySets(x)+verifyMasks(x);checks+=count;
    const k1=Object.values(x.source).map(x=>JSON.stringify(sorted(x))).sort().join("|");
    const k2=restriction(h).map(x=>JSON.stringify(sorted(x))).sort().join("|");
    if(k1!==k2)throw Error("complete PHP restriction is not graphPHP");
    checks++;
    if(h<=7){
       for(let mask=0;mask<2**(2*h);mask++){
          const on=new Set;for(let i=0;i<2*h;i++)if((mask>>i)&1)on.add(i+1);
          if(Object.values(x.source).every(c=>sat(c,on)))throw Error("SAT source");
          brute++
       }
    }
    if([1,2,4,7,12].includes(h))examples[h]=x;
    rows.push({h,vars:2*h,source_clauses:2*h+1,paid_RES_minimum:2*h,exhibited_span:2*h,checks:count+1});
 }
 for(let h of [1,2,3,4,6,8]){
  let x=mk(h);
  let corrupt=JSON.parse(JSON.stringify(x));corrupt.proof[0].pivot=0;
  try{verifySets(corrupt);throw Error("BAD mutation accepted")}catch(e){if(e.message==="BAD mutation accepted")throw e;neg++}
  corrupt=JSON.parse(JSON.stringify(x));corrupt.witness.P0=[];
  try{verifyMasks(corrupt);throw Error("BAD witness accepted")}catch(e){if(e.message==="BAD witness accepted")throw e;neg++}
  corrupt=JSON.parse(JSON.stringify(x));corrupt.source.P0=[-1];
  try{verifySets(corrupt);throw Error("BAD source accepted")}catch(e){if(e.message==="BAD source accepted")throw e;neg++}
  corrupt=JSON.parse(JSON.stringify(x));corrupt.proof.pop();
  try{verifyMasks(corrupt);throw Error("BAD AND branch accepted")}catch(e){if(e.message==="BAD AND branch accepted")throw e;neg++}
 }
 return {schema:"LSPV3_GRAPH_PHP_PATH431_v1",status:"PROVED/EXACT within RES fragment; COMPUTATIONAL finite verification",family:"path graph-PHP restriction of complete PHP",ranged_h:[1,64],rows,examples,checks,brute_unsat_assignments:brute,negative_rejections:neg,qualified_hardness:"Haken lower bound for complete graph ordinary Resolution; restriction has linear minimum"}
};
if (typeof require !== 'undefined' && require.main === module) console.log(JSON.stringify(audit(),null,2));
