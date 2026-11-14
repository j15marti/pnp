'use strict';
function parityCode(i){let p=0,n=i;while(n){p^=n&1;n=Math.floor(n/2);}return 2*i+p;}

function makePrism(r){const edges=[],adj=Array.from({length:2*r},()=>[]);for(let i=0;i<r;i++){edges.push([i,(i+1)%r],[r+i,r+(i+1)%r],[i,r+i]);}edges.forEach(([a,b],e)=>{adj[a].push([b,e]);adj[b].push([a,e]);});if(!adj.every(a=>a.length===3))throw Error("not cubic");return {edges,adj};}

function makeSource(r,charged){
 const {edges,adj}=makePrism(r),t=edges.length,w=Math.ceil(Math.log2(2*t+2)),N=2**w-1;
 const charge=Array(2*r).fill(0);charge[charged]=1;
 const main=[];
 for(let v=0;v<adj.length;v++)for(let k=0;k<8;k++){const b=[k&1,(k>>1)&1,(k>>2)&1];if((b[0]^b[1]^b[2])===charge[v])continue;main.push({v,tuple:b,clause:adj[v].map((x,j)=>[parityCode(x[1]+1),b[j],x[1]])});}
 const used=new Set(Array.from({length:t},(_,i)=>parityCode(i+1))),missing=[];
 for(let j=1;j<=N;j++)if(!used.has(j))missing.push(j);
 const filler=[];for(let i=0;i+3<=missing.length;i+=3)filler.push(missing.slice(i,i+3).map(x=>[x,0,null]));
 const left=missing.length%3;if(left)filler.push([...missing.slice(-left),...missing.slice(0,3-left)].map(x=>[x,0,null]));
 const clauses=[...main.map(x=>x.clause),...filler],M=clauses.length;
 const all=new Set(clauses.flatMap(c=>c.map(x=>x[0])));if(all.size!==N)throw Error("missing used ID");
 let source="1".repeat(N)+"0"+"1".repeat(M)+"0";const positions=[];
 clauses.forEach((c,ci)=>c.forEach(([id,sign],li)=>{
   const field=String(sign)+id.toString(2).padStart(w,"0");
   for(let q=0;q<field.length;q++)if(ci<main.length)positions.push({pos:source.length+q,ci,li,sign:q===0});
   source+=field;
 }));
 if(source.length!==N+M+2+3*M*(w+1))throw Error("bad length");
 return {r,charged,t,w,N,M,edges,adj,charge,main,filler,missing,source,positions};
}

function parseStrict(s){
 let i=0;while(i<s.length&&s[i]==="1")i++;let N=i;if(i>=s.length||s[i]!=="0"||N<3)return null;i++;let j=i;while(i<s.length&&s[i]==="1")i++;const M=i-j;if(M<1||i>=s.length||s[i]!=="0")return null;i++;
 const w=Math.ceil(Math.log2(N+1)),width=3*(w+1);if(i+M*width!==s.length)return null;
 const clauses=[],occur=new Set();
 for(let c=0;c<M;c++){const cl=[],inClause=new Set();for(let q=0;q<3;q++){
   const neg=Number(s[i++]),id=parseInt(s.slice(i,i+w),2);i+=w;
   if(!Number.isInteger(id)||id<1||id>N||inClause.has(id))return null;
   cl.push([id,neg]);inClause.add(id);occur.add(id);
 }clauses.push(cl);}
 return occur.size===N?clauses:null;
}

function satisfies(clauses,assignment){
 return clauses.every(c=>c.some(([id,neg])=> ((assignment.get(id)??0)^neg)===1));
}

function deletionAssignment(src,ci){
 const target=src.main[ci],v=target.v;
 const vals=new Map(src.adj[v].map(([z,e],j)=>[e,target.tuple[j]]));
 const parent=new Map(),parentEdge=new Map(),order=[],root=v===0?1:0;
 parent.set(root,-1);order.push(root);
 for(let ii=0;ii<order.length;ii++){const u=order[ii];for(const [z,e] of src.adj[u])if(z!==v&&!parent.has(z)){parent.set(z,u);parentEdge.set(z,e);order.push(z);}}
 if(order.length!==src.adj.length-1)throw Error("vertex deletion disconnected");
 for(let ii=order.length-1;ii>=1;ii--){const u=order[ii],pe=parentEdge.get(u);
   let xor=src.charge[u];for(const [z,e] of src.adj[u])if(e!==pe)xor^=vals.get(e)??0;
   vals.set(pe,xor);
 }
 for(let u=0;u<src.adj.length;u++){if(u===v)continue;let xor=0;for(const [z,e] of src.adj[u])xor^=vals.get(e)??0;
   if(xor!==src.charge[u])throw Error("bad incidence witness");}
 const assignment=new Map();
 for(let e=0;e<src.t;e++)assignment.set(parityCode(e+1),vals.get(e)??0);
 for(const id of src.missing)assignment.set(id,1);
 return assignment;
}

function audit(){
 const data={schema:"TMR5-NO-UNUSED-ID-PADDING-006",status:"COMPUTATIONAL",cases:0,deleted_clauses_witnessed:0,sign_flips:0,id_flips:0,all_single_bit_neighbors:0,unused_rejections:0,universal_id_coverage_checks:0,brute_unsat_checks:0,failures:0,maxL:0,minRatio:1,maxRatio:0,by_case:[]};
 for(const r of [3,4,6,8,12,24])for(const charged of [0,r]){
  const src=makeSource(r,charged),clauses=parseStrict(src.source);
  if(!clauses)throw Error("source invalid");
  data.universal_id_coverage_checks++;
  const Q=src.positions.length,L=src.source.length;
  for(let ci=0;ci<src.main.length;ci++){
   const a=deletionAssignment(src,ci),falseClauses=[];
   clauses.forEach((cl,j)=>{if(!cl.some(([id,neg])=>((a.get(id)??0)^neg)===1))falseClauses.push(j);});
   if(falseClauses.length!==1||falseClauses[0]!==ci)throw Error("deletion failed");
   data.deleted_clauses_witnessed++;
   const lo=ci*3*(src.w+1),hi=lo+3*(src.w+1);
   for(let q=lo;q<hi;q++){
    const pos=src.positions[q],flip=src.source[pos.pos]==="1"?"0":"1";
    const ss=src.source.slice(0,pos.pos)+flip+src.source.slice(pos.pos+1);
    const parsed=parseStrict(ss);if(!parsed||ss.length!==L)throw Error("invalid mutated source");
    const b=new Map(a);
    if(!pos.sign){
      const old=clauses[ci][pos.li][0],nid=parsed[ci][pos.li][0];
      if(nid===old||!src.missing.includes(nid)||parityCode(nid)===0)throw Error("bad identifier mutation");
      b.set(nid,1^parsed[ci][pos.li][1]);data.id_flips++;
    }else data.sign_flips++;
    if(!satisfies(parsed,b))throw Error("not satisfiable neighbor");
    data.all_single_bit_neighbors++;
   }
  }
  // Source with a triple of otherwise unused IDs omitted is rejected by no-unused grammar.
  const begin=src.N+src.M+2,recordLen=3*(src.w+1),idx=src.main.length+1;
  const payload=src.source.slice(begin,begin+idx*recordLen)+src.source.slice(begin+(idx+1)*recordLen);
  const malformed="1".repeat(src.N)+"0"+"1".repeat(src.M-1)+"0"+payload;
  if(parseStrict(malformed)!==null)throw Error("unused-id negative accepted");
  data.unused_rejections++;
  if(r===3&&charged===0){for(let mask=0;mask<2**src.t;mask++){
    const a=new Map(src.missing.map(id=>[id,1]));for(let e=0;e<src.t;e++)a.set(parityCode(e+1),(mask>>e)&1);
    if(satisfies(clauses,a))throw Error("original SAT");data.brute_unsat_checks++;
  }}
  data.cases++;data.maxL=Math.max(data.maxL,L);
  const ratio=Q/L;data.minRatio=Math.min(data.minRatio,ratio);data.maxRatio=Math.max(data.maxRatio,ratio);
  data.by_case.push({r,charged,N:src.N,w:src.w,M0:src.main.length,Mfill:src.filler.length,L,Q,ratio:Number(ratio.toFixed(6))});
 }
 return data;
}
console.log(JSON.stringify(audit(), null, 2));
