/* LSPV-2 341 executable producer; run node file.js, emits JSON. No dependencies. */
const data=(function(){
"use strict";
const version="LSPV2-MIXED-TSEITIN-MINDAG341/v1";
function graphs(){
 const all=[];
 function add(name,n,edges){all.push({name,n,edges:edges.map((e)=>e.slice())});}
 const k4=[];for(let i=0;i<4;i++)for(let j=i+1;j<4;j++)k4.push([i,j]);add("K4",4,k4);
 const k33=[];for(let i=0;i<3;i++)for(let j=3;j<6;j++)k33.push([i,j]);add("K33",6,k33);
 const cube=[];for(let i=0;i<8;i++)for(let b=0;b<3;b++){let j=i^(1<<b);if(i<j)cube.push([i,j]);}add("CUBE",8,cube);
 const pet=[];for(let i=0;i<5;i++){pet.push([i,(i+1)%5]);pet.push([i+5,((i+2)%5)+5]);pet.push([i,i+5]);}add("PETERSEN",10,pet);
 function prism(k){let e=[];for(let i=0;i<k;i++){e.push([i,(i+1)%k]);e.push([i+k,((i+1)%k)+k]);e.push([i,i+k]);}return e;}
 add("PRISM6",12,prism(6));add("PRISM16",32,prism(16));
 // Two K4 graphs with one edge of each subdivided, joined by a bridge.
 const bridge=[];
 for(let offset of [0,5]){for(let i=0;i<4;i++)for(let j=i+1;j<4;j++){if(i===0&&j===1)continue;bridge.push([i+offset,j+offset]);}bridge.push([offset,offset+4],[offset+1,offset+4]);}
 bridge.push([4,9]);add("BRIDGE_K4x2",10,bridge);
 return all;
}
function validateGraph(g){
 if(!Number.isInteger(g.n)||g.n<4||g.edges.length*2!==g.n*3)throw Error("edge count");
 let deg=Array(g.n).fill(0),seen=new Set();
 for(const [a,b] of g.edges){if(!Number.isInteger(a)||!Number.isInteger(b)||a<0||b<0||a>=g.n||b>=g.n||a===b)throw Error("edge format");let k=[Math.min(a,b),Math.max(a,b)].join(":");if(seen.has(k))throw Error("duplicate edge");seen.add(k);deg[a]++;deg[b]++;}
 if(deg.some(d=>d!==3))throw Error("noncubic");
 const reach=new Set([0]),queue=[0];for(let k=0;k<queue.length;k++){let v=queue[k];for(const [a,b] of g.edges){let u=a===v?b:b===v?a:-1;if(u>=0&&!reach.has(u)){reach.add(u);queue.push(u);}}}
 if(reach.size!==g.n)throw Error("disconnected");
 return true;
}
function solve(g,charges,pinned={},skip=-1){
 const E=g.edges.length,basis=Array(E).fill(null);
 for(let v=0;v<g.n;v++){
   if(v===skip)continue;
   let mask=0n,rhs=charges[v];
   for(let i=0;i<E;i++){if(g.edges[i][0]!==v&&g.edges[i][1]!==v)continue;
     if(Object.prototype.hasOwnProperty.call(pinned,i))rhs^=pinned[i];else mask|=(1n<<BigInt(i));
   }
   for(let i=0;i<E&&mask!==0n;i++)if((mask&(1n<<BigInt(i)))!==0n){
     if(basis[i]){mask^=basis[i].mask;rhs^=basis[i].rhs;}else{basis[i]={mask,rhs};break;}
   }
   if(mask===0n&&rhs!==0)return null;
 }
 const assign=Array(E).fill(0);for(const k in pinned)assign[Number(k)]=pinned[k];
 for(let i=E-1;i>=0;i--)if(basis[i]){
  let rhs=basis[i].rhs;for(let j=i+1;j<E;j++)if((basis[i].mask&(1n<<BigInt(j)))!==0n)rhs^=assign[j];
  assign[i]=rhs;
 }
 for(let v=0;v<g.n;v++)if(v!==skip){
   let x=0;for(let e=0;e<E;e++)if(g.edges[e].includes(v))x^=assign[e];if(x!==charges[v])throw Error("solver self-check");
 }
 return assign;
}
function fixture(g){
 validateGraph(g);const E=g.edges.length;
 const inc=Array.from({length:g.n},()=>[]);g.edges.forEach(([a,b],i)=>{inc[a].push(i);inc[b].push(i);});
 const charges=Array(g.n).fill(0);charges[0]=1;
 let clauses=[],source=[];
 for(let v=0;v<g.n;v++)for(let pat=0;pat<8;pat++){
   let parity=((pat&1)^((pat>>1)&1)^((pat>>2)&1));if(parity===charges[v])continue;
   let lits=inc[v].map((e,j)=> ((pat>>j)&1)?-(e+1):(e+1));
   let id="s"+clauses.length;
   clauses.push({id,vertex:v,pattern:pat,literals:lits});
   source.push({id,kind:"factor",support:inc[v].slice(),table:null,source:true});
 }
 function clauseTable(c,vars){let t=0;for(let p=0;p<8;p++){
   let sat=false;for(let lit of c.literals){let j=vars.indexOf(Math.abs(lit)-1);if(j<0)throw Error("source outside vars");let b=(p>>j)&1;if(b===(lit>0?1:0))sat=true;}if(sat)t|=1<<p;}return t;
 }
 for(let i=0;i<source.length;i++){source[i].table=clauseTable(clauses[i],source[i].support);}
 const proof=[],all=new Map(source.map(x=>[x.id,x])),rows=[];
 for(let v=0;v<g.n;v++){
  const ss=source.filter(s=>clauses[Number(s.id.slice(1))].vertex===v);
  if(ss.length!==4)throw Error("vertex clause count");
  let curr=ss[0];
  for(let j=1;j<4;j++){
   const t=curr.table & ss[j].table;
   const node={id:"d"+proof.length,kind:"factor",rule:"AND3",parents:[curr.id,ss[j].id],support:inc[v].slice(),table:t};
   proof.push(node);all.set(node.id,node);curr=node;
  }
  let mask=0n;for(const e of inc[v])mask|=1n<<BigInt(e);
  let expected=0;
  for(let p=0;p<8;p++){let parity=(p&1)^((p>>1)&1)^((p>>2)&1);if(parity===charges[v])expected|=1<<p;}
  if(curr.table!==expected)throw Error("normalization not parity");
  curr.row={mask:"0x"+mask.toString(16),rhs:charges[v]};rows.push(curr);
 }
 let agg=rows[0],mask=BigInt(agg.row.mask),rhs=agg.row.rhs;
 for(let i=1;i<rows.length;i++){mask^=BigInt(rows[i].row.mask);rhs^=rows[i].row.rhs;
   const node={id:"d"+proof.length,kind:"affine",rule:"XOR",parents:[agg.id,rows[i].id],row:{mask:"0x"+mask.toString(16),rhs}};
   proof.push(node);agg=node;
 }
 if(mask!==0n||rhs!==1)throw Error("not contradiction");
 const deleted=[];let essential=0;
 for(let i=0;i<clauses.length;i++){
  const c=clauses[i],pins={};for(let j=0;j<3;j++)pins[inc[c.vertex][j]]=(c.pattern>>j)&1;
  const sol=solve(g,charges,pins,c.vertex);
  if(sol)essential++;
  deleted.push({sourceId:c.id,assignment:sol ? sol.join(""):null});
 }
 const even=charges.slice();even[0]=0;
 const evenWitness=solve(g,even);
 if(!evenWitness)throw Error("even parity SAT failed");
 if(solve(g,charges)!==null)throw Error("odd parity accepted");
 return {graph:g,charges,clauses,proof,deleted,evenWitness:evenWitness.join(""),
  properties:{variables:E,sourceClauses:clauses.length,inferences:proof.length,essential,oddUnsat:true,evenSat:true,
    predictedMinimum:essential===clauses.length?clauses.length-1:null}};
}
const fixtures=graphs().map(fixture);
const summary=fixtures.map(f=>({name:f.graph.name,vertices:f.graph.n,variables:f.properties.variables,
 clauses:f.properties.sourceClauses,essential:f.properties.essential,inferences:f.properties.inferences,
 predictedMinimum:f.properties.predictedMinimum,allEssential:f.properties.essential===f.clauses.length}));
return {version,definition:"Rmix341: source clauses; unit binary AND3 of <=3-variable truth tables, unit XOR of affine rows, unit resolution, conservative charged aux definitions; final truth table of AND3 may carry an exactly checked affine alias",fixtures,summary};
})();
if(typeof console!== 'undefined') console.log(JSON.stringify(data,null,2));
