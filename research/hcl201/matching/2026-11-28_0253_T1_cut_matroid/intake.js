
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
 function rec(p){if(++W.nodes>10000||pre+learnChecks+W.visits>cap)return {s:"UNKNOWN"};let r=up(C,p,W,cap-pre-learnChecks);if(r.status==="UNSAT")return {s:"UNSAT",t:0};if(r.status==="UNKNOWN")return {s:"UNKNOWN"};if(r.status==="SAT")return {s:"SAT",a:[...r.a]};let occ=new Map();for(let c of C)if(!c.some(l=>r.a.get(Math.abs(l))===Number(l>0)))for(let l of c)if(!r.a.has(Math.abs(l)))occ.set(Math.abs(l),(occ.get(Math.abs(l))||0)+1);let v=[...occ].sort((a,b)=>b[1]-a[1]||a[0]-b[0])[0]?.[0];if(v===undefined)return {s:"UNKNOWN"};let b=a[v],x=rec([...r.a,[v,b]]);if(x.s!=="UNSAT")return x;let y=rec([...r.a,[v,1-b]]);return y.s==="UNSAT"?{s:"UNSAT",t:b?[v,y.t,x.t]:[v,x.t,y.t]}:y}
 let R=rec([]),V=R.s==="UNSAT"?check(C,R.t):null;if(R.s==="SAT"){let z=new Map(R.a);if(!F.every(c=>c.some(l=>z.get(Math.abs(l))===Number(l>0))))throw Error("source witness")}
 return {mode,width,start,status:R.s,proof:R.t??null,witness:R.a??null,pre,learnChecks,pairs,learned,flips,ties,initial,search:W,replay:V,logicalLiteralRecords:C.reduce((s,c)=>s+c.length,0),ms:Date.now()-t,cap,chargedNamed:pre+learnChecks+W.visits+(V?.visits||0)}
}
function feedback(corpus,registry){let S=[];for(let name of ["JOINT-24","RANDOM-3CNF-40"]){let s=corpus.instances.find(x=>x.id===name),r=registry.instances.find(x=>x.alias==="EB-"+name).source_cnf;if(sha(s.dimacs)!==r.sha256||s.dimacs.length*8!==r.N_bits)throw Error("auth");S.push({name,n:s.nvars,dimacs:s.dimacs,instance_id:r.instance_id,N:r.N_bits})}
 let lines=[[1,2,3],[1,4,5],[1,6,7],[2,4,6],[2,5,7],[3,4,7],[3,5,6]],F=lines.flatMap(c=>[c,c.map(x=>-x)]),d="p cnf 7 14\n"+F.map(c=>c.join(" ")+" 0").join("\n")+"\n";S.push({name:"FANO-NAE",n:7,dimacs:d,instance_id:"DIMACS-CNF-v1:sha256:"+sha(d),N:d.length*8});
 for(let s of S){let F=s.dimacs.trimEnd().split("\n").slice(1).map(l=>l.trim().split(/\s+/).map(Number).slice(0,-1));s.arms=[];for(let width of [2,4])for(let start of [0,1])for(let mode of ["baseline","flips","deductions","table","residue"])s.arms.push(feedbackArm(F,s.n,mode,width,start))}return S
}

// Load after pinned T1 check.js; call feedback(corpus,registry).
