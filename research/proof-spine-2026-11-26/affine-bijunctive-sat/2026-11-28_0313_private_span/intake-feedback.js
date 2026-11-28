function sha(s){const p=[],h=[],k=[];for(let i=2;k.length<64;i++){if(p.some(q=>i%q===0))continue;p.push(i);if(h.length<8)h.push((Math.sqrt(i)%1*4294967296)|0);k.push((Math.cbrt(i)%1*4294967296)|0)}const a=Array.from(s,c=>c.charCodeAt(0));if(a.some(x=>x>127))throw Error("ASCII");const l=a.length*8;a.push(128);while(a.length%64!==56)a.push(0);for(let j=7;j>=0;j--)a.push(Math.floor(l/2**(8*j))%256);const R=(x,n)=>(x>>>n)|(x<<(32-n));for(let i=0;i<a.length;i+=64){let w=[];for(let j=0;j<16;j++)w.push((a[i+4*j]<<24)|(a[i+4*j+1]<<16)|(a[i+4*j+2]<<8)|a[i+4*j+3]);for(let j=16;j<64;j++){let x=w[j-15],y=w[j-2];w[j]=(w[j-16]+(R(x,7)^R(x,18)^(x>>>3))+w[j-7]+(R(y,17)^R(y,19)^(y>>>10)))|0}let [A,B,C,D,E,F,G,H]=h;for(let j=0;j<64;j++){let t=(H+(R(E,6)^R(E,11)^R(E,25))+((E&F)^(~E&G))+k[j]+w[j])|0,u=((R(A,2)^R(A,13)^R(A,22))+((A&B)^(A&C)^(B&C)))|0;[A,B,C,D,E,F,G,H]=[(t+u)|0,A,B,C,(D+t)|0,E,F,G]}[A,B,C,D,E,F,G,H].forEach((v,j)=>h[j]=(h[j]+v)|0)}return h.map(x=>(x>>>0).toString(16).padStart(8,"0")).join("")}


function up(C,p,W,cap){
 let a=new Map(p);for(;;){let changed=false,all=true;for(const row of C){let sat=false,free=[];for(const l of row){if(++W.visits>cap)return {status:"UNKNOWN"};if(!a.has(Math.abs(l)))free.push(l);else if(a.get(Math.abs(l))===Number(l>0)){sat=true;break}}if(sat)continue;all=false;if(!free.length)return {status:"UNSAT",a};if(free.length===1){a.set(Math.abs(free[0]),Number(free[0]>0));W.pins++;changed=true}}if(all)return {status:"SAT",a};if(!changed)return {status:"OPEN",a}}
}
function check(C,t){
 // Independent reverse-order scan, no call to solver's up.
 let visits=0,nodes=0,leaves=0;function walk(node,p){nodes++;const a=new Map(p);for(;;){let next=false;for(let k=C.length-1;k>=0;k--){let row=C[k],hit=false,last=0,num=0;for(let j=row.length-1;j>=0;j--){visits++;let l=row[j],v=a.get(Math.abs(l));if(v===undefined){num++;last=l}else if(v===Number(l>0)){hit=true;break}}if(hit)continue;if(!num){leaves++;return true}if(num===1){a.set(Math.abs(last),Number(last>0));next=true}}if(!next)break}
 if(node===0)return false;let [v,l,r]=node;if(a.has(v))return walk(a.get(v)?r:l,[...a]);return walk(l,[...a,[v,0]])&&walk(r,[...a,[v,1]])}
 if(!walk(t,[]))throw Error("proof replay failed");return {visits,nodes,leaves,verified:true};
}
const sort=a=>[...new Set(a)].sort((a,b)=>a-b),J=x=>JSON.stringify(x);

function feedbackArm(F,n,mode,width,start){
 let t=Date.now(),C=F.map(c=>c.slice()),W={visits:0,nodes:0,pins:0},pre=0,learnChecks=0,flips=[],ties=0,pairs=0,learned=[],a=Array(n+1).fill(start),cap=500000;
 function signed(c,z){let k=0,s=0;for(let l of c){pre++;if(z[Math.abs(l)]===Number(l>0)){k++;s+=Math.sign(l)}}return [k,k%3,(s%3+3)%3]}
 function table(z){return C.map(c=>signed(c,z))}
 function score(T){return [T.filter(r=>r[0]===0).length,T.filter(r=>r[0]>0&&r[2]===0).length]}
 let initial=mode==="baseline"?null:{zero:table(Array(n+1).fill(0)),one:table(Array(n+1).fill(1))};
 function flip(){let T=table(a),now=score(T);for(let step=0;step<8&&now[0]>0&&pre<120000;step++){let best=now[0],id=0,tieid=0,rs=Infinity;for(let i=1;i<=n;i++){a[i]^=1;let v=score(table(a));a[i]^=1;if(v[0]<best){best=v[0];id=i;tieid=i;rs=v[1]}else if(v[0]===best&&id&&v[1]<rs){tieid=i;rs=v[1]}}if(!id)break;let j=mode==="residue"?tieid:id;if(j!==id)ties++;a[j]^=1;T=table(a);now=score(T);flips.push({j,unsat:now[0],zeroSignedResidue:now[1]})}}
 function resolution(c,d,l){let x=sort(c.filter(z=>z!==l).concat(d.filter(z=>z!==-l)));return x.some(z=>x.includes(-z))?null:x}
 function learn(){let keys=new Set(C.map(c=>sort(c).join(","))),initialN=C.length;for(let i=0;i<initialN&&learned.length<64&&pre<230000;i++)for(let j=i+1;j<initialN&&learned.length<64&&pre<230000;j++){pairs++;pre+=C[i].length+C[j].length;for(let l of C[i])if(C[j].includes(-l)){let c=resolution(C[i],C[j],l);if(!c||c.length>width||keys.has(c.join(",")))continue;let replay=resolution(C[i],C[j],l);learnChecks+=C[i].length+C[j].length+c.length;if(J(c)!==J(replay))throw Error("resolution");keys.add(c.join(","));learned.push({parents:[i+1,j+1],pivot:l,c});C.push(c)}}}
 if(["flips","table","residue"].includes(mode))flip();if(["deductions","table","residue"].includes(mode))learn();if(["table","residue"].includes(mode))flip();
 function rec(p){if(++W.nodes>10000||pre+learnChecks+W.visits>cap)return {s:"UNKNOWN"};let r=up(C,p,W,cap-pre-learnChecks);if(r.status==="UNSAT")return {s:"UNSAT",t:0};if(r.status==="UNKNOWN")return {s:"UNKNOWN"};if(r.status==="SAT")return {s:"SAT",a:[...r.a]};let occ=new Map();for(let c of C){W.visits+=2*c.length;if(!c.some(l=>r.a.get(Math.abs(l))===Number(l>0)))for(let l of c)if(!r.a.has(Math.abs(l)))occ.set(Math.abs(l),(occ.get(Math.abs(l))||0)+1);}let v=[...occ].sort((a,b)=>b[1]-a[1]||a[0]-b[0])[0]?.[0];if(v===undefined)return {s:"UNKNOWN"};let b=a[v],x=rec([...r.a,[v,b]]);if(x.s!=="UNSAT")return x;let y=rec([...r.a,[v,1-b]]);return y.s==="UNSAT"?{s:"UNSAT",t:b?[v,y.t,x.t]:[v,x.t,y.t]}:y}
 for(let i=0;i<learned.length;i++){let p=learned[i],a=C[p.parents[0]-1],b=C[p.parents[1]-1];if(!a.includes(p.pivot)||!b.includes(-p.pivot))throw Error("pivot replay");let set=new Set();for(let l of a)if(l!==p.pivot)set.add(l);for(let l of b)if(l!==-p.pivot)set.add(l);if(set.size!==p.c.length||p.c.some(l=>!set.has(l)||set.has(-l)))throw Error("independent resolution replay");learnChecks+=a.length+b.length+p.c.length}
 let R=rec([]),V=R.s==="UNSAT"?check(C,R.t):null;if(R.s==="SAT"){let z=new Map(R.a);if(!F.every(c=>c.some(l=>z.get(Math.abs(l))===Number(l>0))))throw Error("source witness")}
 return {mode,width,start,status:R.s,proof:R.t??null,witness:R.a??null,pre,learnChecks,pairs,learned,flips,ties,initial,search:W,replay:V,logicalLiteralRecords:C.reduce((s,c)=>s+c.length,0),ms:Date.now()-t,cap,chargedNamed:pre+learnChecks+W.visits+(V?.visits||0)}
}
function feedback(corpus,registry){let S=[];for(let name of ["JOINT-24","RANDOM-3CNF-40"]){let s=corpus.instances.find(x=>x.id===name),r=registry.instances.find(x=>x.alias==="EB-"+name).source_cnf;if(sha(s.dimacs)!==r.sha256||s.dimacs.length*8!==r.N_bits)throw Error("auth");S.push({name,n:s.nvars,dimacs:s.dimacs,instance_id:r.instance_id,N:r.N_bits})}
 let lines=[[1,2,3],[1,4,5],[1,6,7],[2,4,6],[2,5,7],[3,4,7],[3,5,6]],F=lines.flatMap(c=>[c,c.map(x=>-x)]),d="p cnf 7 14\n"+F.map(c=>c.join(" ")+" 0").join("\n")+"\n";S.push({name:"FANO-NAE",n:7,dimacs:d,instance_id:"DIMACS-CNF-v1:sha256:"+sha(d),N:d.length*8});
 for(let s of S){let F=s.dimacs.trimEnd().split("\n").slice(1).map(l=>l.trim().split(/\s+/).map(Number).slice(0,-1));s.arms=[];for(let width of [2,4])for(let start of [0,1])for(let mode of ["baseline","flips","deductions","table","residue"])s.arms.push(feedbackArm(F,s.n,mode,width,start))}return S
}

// Load after pinned T1 check.js; call feedback(corpus,registry).

const fs=require('node:fs');console.log(JSON.stringify(feedback(JSON.parse(fs.readFileSync(process.argv[2],'utf8')),JSON.parse(fs.readFileSync(process.argv[3],'utf8'))),null,2));
