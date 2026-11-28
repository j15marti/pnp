// Source-only width-two RUP escape for AND-SEAM NO. No extension variables.
// node narrow-rup.js case.cert.json
const crypto=require("node:crypto"),sha=s=>crypto.createHash("sha256").update(s).digest("hex");
function narrow(dimacs){
 const lines=dimacs.trimEnd().split("\n"),h=lines.shift().split(" "),F=lines.map(s=>s.split(" ").map(Number).slice(0,-1)),n=+h[2];if(F.length!==+h[3])throw Error("header");
 let sourceRows=F.length,vis=0,occ=new Map(),neg=[],pairs=new Map(),key=(a,b)=>a<b?a+","+b:b+","+a;
 for(let i=0;i<F.length;i++){let c=F[i];if(c.every(l=>l<0)){let idx=neg.length;neg.push({row:i+1,vs:c.map(l=>-l)});for(let v of neg.at(-1).vs){vis++;if(!occ.has(v))occ.set(v,[]);occ.get(v).push(idx)}}else if(c.length===2&&c.every(l=>l>0)){pairs.set(key(...c),i+1);vis+=2}else throw Error("not a recognized seam")}
 let groupMap=new Map();for(let [v,e] of occ){let z=e.join(",");if(!groupMap.has(z))groupMap.set(z,[]);groupMap.get(z).push(v)}
 let B=[...groupMap.values()],m=B.length,k=B[0].length;if(m<5||!(m%2)||k<2||B.some(b=>b.length!==k)||m*k!==n||occ.size!==n)throw Error("shape");
 let id=new Map(),adj=B.map(()=>[]),edge=new Map();B.forEach((b,i)=>b.forEach(v=>id.set(v,i)));
 for(let {row,vs} of neg){let u=[...new Set(vs.map(v=>id.get(v)))];if(u.length!==2||vs.length!==2*k)throw Error("bad negative seam");let [i,j]=u;adj[i].push(j);adj[j].push(i);edge.set(key(i,j),row);for(let a of B[i])for(let b of B[j]){vis++;if(!pairs.has(key(a,b)))throw Error("missing positive seam")}}
 if(adj.some(a=>a.length!==2)||neg.length!==m||F.length!==m*(k*k+1))throw Error("source not exact cycle");
 let order=[0];while(order.length<m){let t=adj[order.at(-1)].find(v=>v!==order.at(-2)&&!order.includes(v));if(t===undefined)throw Error("disconnected");order.push(t)}if(!edge.has(key(order.at(-1),order[0])))throw Error("cycle not closed");
 let proof=[],units=[];
 function admit(clause,reasons){F.push(clause);proof.push({clause,reasons});return F.length}
 function pair(a,b){vis++;let r=pairs.get(key(a,b));if(!r)throw Error("missing earlier pair");return r}
 for(let start of [0,1])for(let a of B[order[start]]){
  let at=t=>order[(start+t)%m];
  for(let l=3;l<m;l+=2){let left=B[at(l-2)],right=B[at(l-1)],dest=B[at(l)],close=edge.get(key(at(l-2),at(l-1)));
   for(let d of dest){let reasons=[...left.map(x=>pair(a,x)),...right.map(x=>pair(d,x)),close];let r=admit([a,d],reasons);pairs.set(key(a,d),r)}
  }
  let left=B[at(m-2)],right=B[at(m-1)],close=edge.get(key(at(m-2),at(m-1)));
  let reasons=[...left.map(x=>pair(a,x)),...right.map(x=>pair(a,x)),close];units.push(admit([a],reasons));
 }
 admit([],[...units,edge.get(key(order[0],order[1]))]);
 return {m,k,n,sourceRows,order,B,proof,discoveryEvents:vis};
}
function replay(dimacs,proof){
 let F=dimacs.trimEnd().split("\n").slice(1).map(s=>s.split(" ").map(Number).slice(0,-1)),vis=0,reasonCount=0,maxLive=0;
 for(let {clause,reasons} of proof){let A=new Set(clause.map(l=>-l)),conflict=false;for(let i=0;i<reasons.length;i++){let r=reasons[i];if(!Number.isInteger(r)||r<1||r>F.length)throw Error("bad reason");let C=F[r-1],u=[];reasonCount++;
 for(let l of C){vis++;if(A.has(l))throw Error("reason satisfied");if(!A.has(-l))u.push(l)}
 if(!u.length){if(i!==reasons.length-1)throw Error("early conflict");conflict=true;break}if(u.length!==1)throw Error("not unit");A.add(u[0]);maxLive=Math.max(maxLive,A.size)}
 if(!conflict)throw Error("RUP failure");F.push(clause)}
 if(F.at(-1).length!==0)throw Error("no terminal");return {literalVisits:vis,reasonCount,maxLive,rows:F.length}
}
function run(dimacs){let x=narrow(dimacs),y=replay(dimacs,x.proof),bytes=JSON.stringify(x.proof)+"\n";return {m:x.m,k:x.k,sourceRows:x.sourceRows,proofRows:x.proof.length,proofBytes:bytes.length,proofSHA256:sha(bytes),discoveryEvents:x.discoveryEvents,replay:y,maxWidth:Math.max(...x.proof.map(x=>x.clause.length)),proof:x.proof}}
if(require.main===module){let c=JSON.parse(require("node:fs").readFileSync(process.argv[2],"utf8")),x=run(c.dimacs);console.log(JSON.stringify(x))}
module.exports={narrow,replay,run};
