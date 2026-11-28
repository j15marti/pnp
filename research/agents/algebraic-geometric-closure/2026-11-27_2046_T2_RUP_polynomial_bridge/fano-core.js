// node fano-core.js certificate.json
function coreProof(F){
 let sorted=c=>c.slice().sort((a,b)=>a-b).join(","),lookup=new Map(F.map((c,j)=>[sorted(c),j])),pair=new Map(),triples=[],checks=0;
 for(let c of F){if(c.length!==3||c.some(l=>l<=0))continue;if(!lookup.has(sorted(c.map(l=>-l))))continue;triples.push(c);for(let i=0;i<3;i++)for(let j=i+1;j<3;j++){let key=sorted([c[i],c[j]]);if(pair.has(key))throw Error("not Steiner");pair.set(key,c.find((_,k)=>k!==i&&k!==j));checks++}}
 let a=triples[0],vars=[...new Set(triples.flat())].sort((a,b)=>a-b),core=null;
 for(let d of vars){if(a.includes(d))continue;let S=new Set([...a,d]),changed=true;while(changed&&S.size<=7){changed=false;let v=[...S];for(let i=0;i<v.length;i++)for(let j=i+1;j<v.length;j++){checks++;let c=pair.get(sorted([v[i],v[j]]));if(c!==undefined&&!S.has(c)){S.add(c);changed=true}}}if(S.size===7){let rows=triples.filter(c=>c.every(x=>S.has(x)));if(rows.length===7){core={vars:[...S].sort((a,b)=>a-b),rows:rows.flatMap(c=>[lookup.get(sorted(c)),lookup.get(sorted(c.map(l=>-l)))])};break}}}
 if(!core)throw Error("no Fano");
 let M=new Map(core.vars.map((v,i)=>[v,i])),mon=[];for(let k=0;k<=3;k++)for(let m=0;m<128;m++)if(m.toString(2).replace(/0/g,"").length-(m===0?0:0)===k)mon.push(m);
 // zero's string is "0", so after stripping zeros its popcount is zero.
 let mi=new Map(mon.map((m,i)=>[m,i])),bp=mon.map((_,i)=>1n<<BigInt(i)),B=new Map(),lines=[],counts={xor:0,mul:0,projectXor:0};
 function polynomial(c){let P=new Set([0]);for(let l of c){let Q=new Set(),b=1<<M.get(Math.abs(l));function tog(m){if(Q.has(m))Q.delete(m);else Q.add(m)}for(let m of P){if(l>0)tog(m);tog(m|b)}P=Q}let x=0n;for(let m of P)x^=bp[mi.get(m)];return x}
 function line(op,a,args){let id=lines.length;lines.push({op,args,value:a});return id}
 function xor(i,j){counts.xor++;return line("xor",lines[i].value^lines[j].value,[i,j])}
 function mul(i,v){let a=lines[i].value,r=0n,b=1<<v;for(let k=0;k<mon.length;k++)if(a&bp[k]){let p=mi.get(mon[k]|b);if(p===undefined)throw Error("degree");r^=bp[p]}counts.mul++;return line("mul",r,[i,core.vars[v]])}
 function add(i){while(lines[i].value){let k=lines[i].value.toString(2).length-1;if(!B.has(k)){B.set(k,i);return}i=xor(i,B.get(k))}}
 for(let j of core.rows)add(line("axiom",polynomial(F[j]),[j]));
 outer:for(let e=0;e<64;e++){if(B.has(0))break;let b=B.size,snapshot=[...B.values()];for(let x=0;x<7;x++){let forbid=mon.reduce((a,m,i)=>!mi.has(m|(1<<x))?a|bp[i]:a,0n),P=new Map();for(let id of snapshot){let i=id,h=lines[i].value&forbid;while(h){let k=h.toString(2).length-1;if(!P.has(k)){P.set(k,i);break}i=xor(i,P.get(k));counts.projectXor++;h=lines[i].value&forbid}if(!h){add(mul(i,x));if(B.has(0))break outer}}}if(B.size===b)break}
 if(!B.has(0))throw Error("no contradiction");let last=B.get(0),keep=new Set();function visit(i){if(keep.has(i))return;keep.add(i);let l=lines[i];if(l.op==="xor"){visit(l.args[0]);visit(l.args[1])}else if(l.op==="mul")visit(l.args[0])}visit(last);let K=[...keep].sort((a,b)=>a-b),ids=new Map(K.map((v,i)=>[v,i])),proof=K.map(i=>{let l=lines[i],args=l.op==="xor"?l.args.map(a=>ids.get(a)):l.op==="mul"?[ids.get(l.args[0]),l.args[1]]:l.args;return {op:l.op,args}});
 // Independent checker: sparse sets of original variable IDs (canonical strings), no monomial index/bit matrix from discovery.
 function verify(P){let rows=[],ops=0,maxDegree=0;function add(S,k){if(S.has(k))S.delete(k);else S.add(k);ops++}function times(S,v,neg=false){let Q=new Set();for(let k of S){if(neg)add(Q,k);let a=k===""?[]:k.split(",").map(Number);if(!a.includes(v))a.push(v);a.sort((a,b)=>a-b);add(Q,a.join(","))}return Q}
 for(let l of P){let a;if(l.op==="axiom"){let c=F[l.args[0]];if(!c)throw Error("axiom index");a=new Set([""]);for(let x of c)a=times(a,Math.abs(x),x>0)}else if(l.op==="xor"){if(!rows[l.args[0]]||!rows[l.args[1]])throw Error("parent");a=new Set(rows[l.args[0]]);for(let k of rows[l.args[1]])add(a,k)}else if(l.op==="mul"){if(!rows[l.args[0]])throw Error("parent");a=times(rows[l.args[0]],l.args[1])}else throw Error("op");for(let k of a){let d=k===""?0:k.split(",").length;maxDegree=Math.max(maxDegree,d);if(d>3)throw Error("degree")}rows.push(a)}
 let a=rows.at(-1);if(a.size!==1||!a.has(""))throw Error("terminal");return {ops,maxDegree,lines:rows.length}}
 return {core,checks,counts,generatedLines:lines.length,proof,verification:verify(proof)}
}
if(typeof require!=='undefined'&&require.main===module){const fs=require('node:fs'),c=JSON.parse(fs.readFileSync(process.argv[2],'utf8'));let p=coreProof(c.chart);if(JSON.stringify(p.proof)!==JSON.stringify(c.proof))throw Error('proof mismatch');console.log(JSON.stringify(p,null,2));}
