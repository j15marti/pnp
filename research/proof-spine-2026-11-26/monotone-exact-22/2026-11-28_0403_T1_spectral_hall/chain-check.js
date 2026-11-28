function recognize(F,mode,N){
 let ops=0, pos=new Map(), all=new Map();for(let i=0;i<F.length;i++)for(let l of F[i]){ops++;if(!all.has(Math.abs(l)))all.set(Math.abs(l),[]);all.get(Math.abs(l)).push(i);if(l>0){if(!pos.has(l))pos.set(l,[]);pos.get(l).push(i)}}
 let eligible=F.map((c,i)=>({c,i})).filter(({c,i})=>c.length&&c.every(v=>v>0&&pos.get(v).length===1&&all.get(v).every(j=>{ops++;return j===i||(F[j].length===2&&F[j].includes(-v))})));
 const es=eligible.map(x=>x.i),vo=new Map();eligible.forEach(({c,i})=>c.forEach(v=>vo.set(v,i)));let adj=new Map(es.map(i=>[i,new Set()]));for(let c of F){ops++;if(c.length===2&&c.every(l=>l<0)&&vo.has(-c[0])&&vo.has(-c[1])){let a=vo.get(-c[0]),b=vo.get(-c[1]);if(a!==b){adj.get(a).add(b);adj.get(b).add(a)}}}
 let parts=[],seen=new Set();for(let i of es)if(!seen.has(i)){let Q=[i];seen.add(i);for(let u of Q)for(let v of adj.get(u)){ops++;if(!seen.has(v)){seen.add(v);Q.push(v)}}parts.push(Q.sort((a,b)=>a-b))}
 const candidates=[],dedup=new Set();function add(a){let s=a.slice().sort((a,b)=>a-b),k=s.join(",");if(s.length&&!dedup.has(k)){dedup.add(k);candidates.push(s)}}
 for(let P of parts){add(P);if(mode!=="spectral")for(let v of P)add([v]);if(mode!=="exact"&&P.length>1){let D=Math.max(1,...P.map(v=>adj.get(v).size));let z=new Map(P.map((v,i)=>[v,BigInt(i*2-P.length+1)]));for(let t=0;t<8;t++){let y=new Map();for(let v of P){let a=BigInt(2*D-adj.get(v).size)*z.get(v);for(let u of adj.get(v)){a+=z.get(u);ops++}y.set(v,a)}z=y}let order=P.slice().sort((a,b)=>z.get(a)<z.get(b)?-1:z.get(a)>z.get(b)?1:a-b);for(let j=1;j<P.length;j++){add(order.slice(0,j));add(order.slice(j))}}}
 let failures={},accepted=[],tests=0,matchingScans=0;
 function inspect(rows){let S=new Set(rows),I=rows.flatMap(i=>F[i]),IS=new Set(I),C=new Map(I.map(v=>[v,new Set()])),B=new Map(I.map(v=>[v,new Set()])),removed=new Set(rows);for(let i of rows)for(let v of F[i])for(let j of all.get(v)){ops++;if(j===i)continue;let c=F[j],l=c.find(l=>l!==-v);if(l===undefined)return {why:"malformed binary"};removed.add(j);if(IS.has(Math.abs(l))){if(l>0)return {why:"positive interior"};if(vo.get(v)!==vo.get(-l))C.get(v).add(-l)}else B.get(v).add(-l)}
 let bins=[],bin=new Map();for(let v of I)if(!bin.has(v)){let Q=[v],j=bins.length;bin.set(v,j);for(let u of Q)for(let w of C.get(u)){ops++;if(!bin.has(w)){bin.set(w,j);Q.push(w)}}bins.push(Q)}
 let triggers=[];for(let Q of bins){let b=[...B.get(Q[0])].sort((a,b)=>a-b).join(",");for(let u of Q){if([...B.get(u)].sort((a,b)=>a-b).join(",")!==b)return {why:"nonuniform blockers"};for(let v of Q){ops++;if(vo.get(u)!==vo.get(v)&&!C.get(u).has(v))return {why:"nonclique bin"}}}triggers.push([...B.get(Q[0])].sort((a,b)=>a-b))}
 let A=rows.map(i=>[...new Set(F[i].map(v=>bin.get(v)))]),q=bins.length,k=q-rows.length;if(k<0)return {why:"negative slack"};if(k>Math.floor(Math.log2(N)))return {why:"above logarithmic slack"};
 function match(a){let own=Array(q).fill(-1);function aug(i,s){for(let j of a[i]){matchingScans++;if(s.has(j))continue;s.add(j);if(own[j]<0||aug(own[j],s)){own[j]=i;return true}}return false}for(let i=0;i<a.length;i++)if(!aug(i,new Set()))return null;return own}
 let flows=[];for(let i=0;i<rows.length;i++){let ext=A.concat(Array.from({length:k},()=>A[i])),m=match(ext);if(!m)return {why:"robust Hall refusal"};let used=new Set();for(let j=0;j<q;j++)if(m[j]>=0){ops++;if(used.has(m[j])||!ext[m[j]].includes(j))throw Error("matching check");used.add(m[j])}if(used.size!==ext.length)throw Error("matching incomplete");flows.push(m)}
 let hard=[];if(k<=1){for(let a=0;a<q;a++)for(let l of triggers[a])if(k===0)hard.push([-l]);else for(let b=a+1;b<q;b++)for(let t of triggers[b]){ops++;if(l!==-t)hard.push(l===t?[-l]:[-l,-t])}}
 return {rows,bins,triggers,removed:[...removed].sort((a,b)=>a-b),slack:k,flows,hard,interior:I,exterior:F.filter((c,i)=>!removed.has(i)),A}}
 for(let a of candidates){tests++;let r=inspect(a);if(r.why)failures[r.why]=(failures[r.why]||0)+1;else accepted.push(r)}
 return {eligible:es,parts,candidates:tests,failures,accepted,ops,matchingScans,mode}
}

function tests(recognize,sha){
 function source(name,A,remove){let F=[],vars=[],q=0;for(let i=0;i<A.length;i++){vars.push(A[i].map(j=>({bin:j,v:++q})));F.push(vars[i].map(o=>o.v))}
 for(let i=0;i<vars.length;i++)for(let j=i+1;j<vars.length;j++)for(let a of vars[i])for(let b of vars[j])if(a.bin===b.bin)F.push([-a.v,-b.v]);
 if(remove!==null)F.splice(remove,1);let dimacs="p cnf "+q+" "+F.length+"\n"+F.map(c=>c.join(" ")+" 0\n").join("");
 let meta={name,model:"DIMACS-CNF-v1",instance_id:"DIMACS-CNF-v1:sha256:"+sha(dimacs),N:8*dimacs.length,guard:"EMPTY",residual:"ROOT",original_ids:{variables:[1,q],clauses:[1,F.length]},dimacs};
 let arms=["exact","spectral","hybrid"].map(m=>recognize(F,m,meta.N));
 let exact=[];let checks=0;for(let w=0;w<2**q;w++)if(F.every(c=>{checks++;return c.some(l=>((w>>(Math.abs(l)-1))&1)===Number(l>0))}))exact.push(w);
 // Verify every accepted response on all exterior words, independently of the matching implementation.
 let replay=[];for(let a of arms)for(let R of a.accepted){let B=[...new Set(R.triggers.flat().map(Math.abs))],I=R.interior,words=0,rows=0;
 for(let b=0;b<2**B.length;b++){let bit=v=>((b>>B.indexOf(Math.abs(v)))&1)===Number(v>0);let off=R.triggers.filter(t=>t.some(bit)).length;let hit=false;
 for(let u=0;u<2**I.length;u++){words++;let sat=l=>I.includes(Math.abs(l))?((u>>I.indexOf(Math.abs(l)))&1)===Number(l>0):bit(l);if(R.removed.every(j=>{rows++;return F[j].some(sat)})){hit=true;break}}
 if(hit!==(off<=R.slack))throw Error("bad exact projection "+name)
 if(R.slack<=1&&R.hard.every(c=>c.some(bit))!==hit)throw Error("bad binary export")}
 replay.push({mode:a.mode,rows:R.rows,boundary:B,words,rowsChecked:rows})}
 return {...meta,arms,exactCount:exact.length,witness:exact[0]??null,checks,replay}}
 let A=[[0,1],[0,1],[1,2],[1,2]],X=source("CHAIN-HALL-NO",A,null),Y=source("CHAIN-HALL-YES",[[0,1,3],[0,1],[1,2],[1,2]],null),D=source("CHAIN-HALL-DELETE",A,0);
 if(X.exactCount!==0||!Y.exactCount||!D.exactCount)throw Error("control");
 return [X,Y,D]
}

const fs=require("node:fs"),h=fs.readFileSync(process.argv[2],"utf8");const sha=new Function(h.slice(h.indexOf("function sha("),h.indexOf("if(require.main"))+";return sha")();console.log(JSON.stringify(tests(recognize,sha))+"\n");
