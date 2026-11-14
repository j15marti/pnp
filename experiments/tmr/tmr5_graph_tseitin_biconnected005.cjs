"use strict";
// Independent TMR-5 graph-Tseitin source-level GF(2) audit. No physical TM claims.
function fixture(name){
 if(name==="K33"){let e=[];for(let u=0;u<3;u++)for(let v=3;v<6;v++)e.push([u,v]);return [6,e]}
 if(name[0]==="K"){let n=Number(name.slice(1)),e=[];for(let u=0;u<n;u++)for(let v=u+1;v<n;v++)e.push([u,v]);return [n,e]}
 if(name==="prism")return [6,[[0,1],[1,2],[0,2],[3,4],[4,5],[3,5],[0,3],[1,4],[2,5]]];
 if(name==="cube"){let e=[];for(let u=0;u<8;u++)for(let v=u+1;v<8;v++)if(((u^v).toString(2).match(/1/g)||[]).length===1)e.push([u,v]);return [8,e]}
 if(name==="petersen"){let e=[];for(let i=0;i<5;i++){e.push([i,(i+1)%5],[i,i+5],[i+5,((i+2)%5)+5])}return [10,e]}
 throw Error(name)
}

function build(n,edges,b){
 let arr=edges.map(([u,v])=>[Math.min(u,v),Math.max(u,v)]).sort((a,b)=>a[0]-b[0]||a[1]-b[1]), at=Array.from({length:n},()=>[]);arr.forEach(([u,v],i)=>{at[u].push(i+1);at[v].push(i+1)});
 let next=arr.length+1, rows=[],clauses=[],owners=[];
 for(let v=0;v<n;v++){let inc=at[v],d=inc.length;if(d<3)throw Error("degree");
 let y=Array.from({length:d-3},()=>next++), gates=[];
 if(d===3)gates.push([inc,b[v]]);
 else{gates.push([[inc[0],inc[1],y[0]],0]);for(let j=1;j<d-3;j++)gates.push([[y[j-1],inc[j+1],y[j]],0]);gates.push([[y[y.length-1],inc[d-2],inc[d-1]],b[v]])}
 for(let [ids,z] of gates){let r=rows.length;rows.push([ids,z]);for(let t=0;t<8;t++){let bs=[t>>2&1,t>>1&1,t&1];if((bs[0]^bs[1]^bs[2])!==z){clauses.push(ids.map((id,k)=>bs[k]?-id:id));owners.push(r)}}}
 }
 return {vars:next-1,rows,clauses,owners}
}

function solve(n,rows,freeze=[]){
 let piv=new Map(), all=rows.concat(freeze.map(([x,b])=>[[x],b]));
 for(let [ids,bb] of all){let mask=0n,z=bb;for(let id of ids)mask^=1n<<BigInt(id-1);
 while(mask){let p=mask.toString(2).length-1, prev=piv.get(p);if(!prev){piv.set(p,[mask,z]);break}mask^=prev[0];z^=prev[1]}
 if(mask===0n&&z)return null;
 }
 let vals=Array(n+1).fill(0);
 for(let p of [...piv.keys()].sort((a,b)=>a-b)){let [mask,z0]=piv.get(p),z=z0,low=mask^(1n<<BigInt(p));while(low){let q=(low&-low).toString(2).length-1;z^=vals[q+1];low&=low-1n}vals[p+1]=z}
 return vals
}

function encode(n,clauses){
 let w=Math.max(1,Math.ceil(Math.log2(n))),s="1".repeat(n)+"0"+"1".repeat(clauses.length)+"0",offsets=[];
 for(let c of clauses)for(let lit of c){offsets.push(s.length);s+=(lit<0?"1":"0")+Math.abs(lit).toString(2).padStart(w,"0")}
 return {source:s,offsets}
}

function parse(s){
 let i=0,N=0,M=0;while(s[i]==="1"){N++;i++}if(!N||s[i++]!=="0")return null;while(s[i]==="1"){M++;i++}if(!M||s[i++]!=="0")return null;
 let w=Math.max(1,Math.ceil(Math.log2(N))),cls=[];
 if(s.length!==i+3*M*(1+w))return null;
 for(let j=0;j<M;j++){let c=[];for(let k=0;k<3;k++){let sign=s[i++],bits=s.slice(i,i+w);i+=w;if(!/^[01]+$/.test(bits)||(sign!=="0"&&sign!=="1"))return null;let id=parseInt(bits,2);if(id<1||id>N)return null;c.push(sign==="1"?-id:id)}if(new Set(c.map(Math.abs)).size!==3)return null;cls.push(c)}
 return cls
}

function audit(){
 let o={id:"TMR5-GRAPH-TSEITIN-GENERALIZATION005",status:"COMPUTATIONAL",cases:[],deleted_clause_witnesses:0,single_sign_source_neighbors:0,source_parser_roundtrips:0,negative_disconnected_component_checks:0,failures:0,notes:"independent V8 GF(2) construction; not a physical Turing machine"};
 for(let name of ["K4","prism","K33","cube","petersen","K5","K6","K7"]){
 let [n,e]=fixture(name),degree=Array(n).fill(0);for(let [u,v] of e){degree[u]++;degree[v]++}if(degree.some(x=>x<3))throw Error("degree "+name);
 for(let pattern of [0,1]){let b=Array(n).fill(0);(pattern===0?[0]:[0,1,2]).forEach(v=>b[v]=1);let F=build(n,e,b);if(solve(F.vars,F.rows)!==null)throw Error("odd SAT");
 let {source,offsets}=encode(F.vars,F.clauses);if(!parse(source)||offsets.length!==F.clauses.length*3)throw Error("source parse");o.source_parser_roundtrips++;
 for(let j=0;j<F.clauses.length;j++){
 let cl=F.clauses[j],frozen=cl.map(l=>[Math.abs(l),+(l<0)]),rem=F.rows.filter((_,k)=>k!==F.owners[j]),a=solve(F.vars,rem,frozen);if(!a)throw Error("no deleted witness "+name+" "+j);
 for(let k=0;k<F.clauses.length;k++){let yes=F.clauses[k].some(l=>a[Math.abs(l)]==+(l>0));if(yes===(k===j))throw Error("not unique clause "+name+" "+j)}
 o.deleted_clause_witnesses++;
 for(let l=0;l<3;l++){let pos=offsets[3*j+l],mut=source.slice(0,pos)+(source[pos]==="1"?"0":"1")+source.slice(pos+1),parsed=parse(mut);if(!parsed||parsed.length!==F.clauses.length)throw Error("mut invalid");
 if(parsed[j][l]!==-cl[l])throw Error("not flipped");if(!parsed[j].some(x=>a[Math.abs(x)]===+(x>0)))throw Error("flip witness");o.single_sign_source_neighbors++}
 }
 let w=Math.max(1,Math.ceil(Math.log2(F.vars)));o.cases.push({graph:name,pattern,n,edges:e.length,variables:F.vars,clauses:F.clauses.length,input_bits:source.length,sensitive_source_sign_bits:3*F.clauses.length,bitwidth:w})
 }
 }
 let a=build(4,fixture("K4")[1],[1,0,0,0]),b=build(4,fixture("K4")[1],[1,0,0,0]);let shift=a.vars;let rows=a.rows.concat(b.rows.map(([ids,z])=>[ids.map(x=>x+shift),z]));let clauses=a.clauses.concat(b.clauses.map(c=>c.map(x=>x>0?x+shift:x-shift)));
 if(solve(a.vars+b.vars,rows)!==null)throw Error("disjoint odd oddly SAT");
 for(let j of [0,3,15,16,31]){let rem=rows.filter((_,k)=>k!==(j<16?a.owners[j]:a.rows.length+b.owners[j-16]));if(solve(a.vars+b.vars,rem)!==null)throw Error("disconnected deletion unexpectedly SAT");o.negative_disconnected_component_checks++}
 return o
}
if(typeof require!=="undefined"&&require.main===module)console.log(JSON.stringify(audit(),null,2));
if(typeof module!=="undefined")module.exports={fixture,build,solve,encode,parse,audit};
