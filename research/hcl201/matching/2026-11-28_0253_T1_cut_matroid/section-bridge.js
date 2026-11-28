
function parseCNF(s){return s.trimEnd().split("\n").slice(1).map(l=>l.trim().split(/\s+/).map(Number).slice(0,-1))}
function section(F){
 let seen=new Set(),demands=[],work=0,interior=new Set(),block=new Map(),exterior=[],parent=[];
 for(let i=0;i<F.length;i++){let c=F[i];work+=c.length;if(c.length&&c.every(l=>l>0)){if(c.some(v=>seen.has(v))||new Set(c).size!==c.length)return {status:"REFUSE",why:"overlapping positive demands",work};c.forEach(v=>seen.add(v));demands.push({row:i,c});}}
 if(!demands.length)return {status:"REFUSE",why:"no demand",work};interior=new Set(seen);
 for(let i=0;i<F.length;i++){let c=F[i],I=c.filter(l=>interior.has(Math.abs(l)));work+=c.length;if(c.length&&c.every(l=>l>0))continue;if(!I.length){exterior.push(c);continue}if(I.length!==1||I[0]>0||block.has(-I[0]))return {status:"REFUSE",why:"non-shell or multiple blocker",work};block.set(-I[0],{row:i,P:c.filter(l=>l!==I[0]).map(l=>-l)})}
 let bins=sort([...interior]),ix=new Map(bins.map((v,i)=>[v,i])),H=demands.map(d=>d.c.map(v=>ix.get(v))),q=bins.length,A=alternating(H,q);if(A.status!=="EXACT-PAIR-QUOTIENT")return {status:"REFUSE",why:"not rank-one partition",work};
 if(bins.some(v=>!block.has(v)))return {status:"REFUSE",why:"missing blocker predicate",work};
 function emit(B){let rows=B.map(i=>block.get(bins[i])),C=sort(rows.flatMap(r=>r.P).map(l=>-l));work+=C.length;if(!C.some(l=>C.includes(-l))){exterior.push(C);parent.push({clause:C,blockers:rows.map(r=>r.row+1),bins:B.map(i=>bins[i])})}}
 for(let i of A.loops)emit([i]);for(let C of A.classes)for(let i=0;i<C.length;i++)for(let j=i+1;j<C.length;j++)emit([C[i],C[j]]);
 return {status:"EXACT",work,flowScans:A.flow.scans,reachScans:A.scans,retired:bins,demands:demands.map(d=>d.row+1),blockers:[...block],quotient:exterior,parent,alternating:A}
}
function gf2ClauseGroups(F){let M=new Map();for(let c of F){let s=sort(c.map(Math.abs)),k=s.join(","),v=M.get(k)||{s,m:full(s.length)};if(s.length>8)return {status:"REFUSE-WIDTH"};let r=mask(s.length,w=>c.some(l=>((w>>s.indexOf(Math.abs(l)))&1)===Number(l>0)));v.m&=r;M.set(k,v)}let fs=[...M.values()];return {rank:gf2(fs.map(f=>({...f,o:[]}))),groups:fs.map(x=>[x.s,x.m.toString(16)])}}
function bridge(seam,corpus,registry){let out=[];for(let name of ["JOINT-24","RANDOM-3CNF-40"]){let s=corpus.instances.find(x=>x.id===name),r=registry.instances.find(x=>x.alias==="EB-"+name).source_cnf;assert(sha(s.dimacs)===r.sha256&&s.dimacs.length*8===r.N_bits,"auth");out.push({name,id:r.instance_id,N:r.N_bits,section:section(parseCNF(s.dimacs))})}
 for(let x of seam.controls){let F=parseCNF(x.cnf.dimacs),A=section(F);assert(A.status==="EXACT","source recognition");let supports=[],rows=[];for(let [a,b] of x.cnf.regions){let R=section(F.slice(a,b));assert(R.status==="EXACT","local section");let Z=gf2ClauseGroups(R.quotient);assert(Z.rank.rank===1&&!Z.rank.bad,"parity row");let s=Z.groups[0][0],m=BigInt("0x"+Z.groups[0][1]),w=[];for(let u=0;u<8;u++)if(bit(m,u))w.push(u);supports.push(w);rows.push({region:[a+1,b],clauseProof:R.parent,rank:Z.rank,groups:Z.groups})}
 let full=gf2ClauseGroups(A.quotient);assert(full.rank.bad===(x.label==="UNSAT"),"GE result");
 for(let w=0;w<8;w++){let valid=A.quotient.every(c=>c.some(l=>sat(l,w)));assert(valid===x.joint.includes(w),"exact joint");if(valid){let a=new Map([1,2,3].map((v,i)=>[v,(w>>i)&1]));let B=A.blockers,bs=new Map(B);for(let v of A.retired)a.set(v,0);for(let id of A.demands){let d=F[id-1],v=d.find(v=>!bs.get(v).P.every(l=>sat(l,w)));assert(v!==undefined,"section lift");a.set(v,1)}assert(F.every(c=>c.some(l=>a.get(Math.abs(l))===Number(l>0))),"lift whole source")}}
 out.push({name:x.cnf.short,id:x.cnf.id,N:x.cnf.N,section:A,rows,supports,full,label:x.label})}
 return out}

// Load after pinned check.js, cut-matroid.js and alternating.js; call bridge(seam,corpus,registry).
