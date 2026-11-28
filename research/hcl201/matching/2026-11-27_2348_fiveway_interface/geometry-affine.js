
function sep(F){
 let V=sort(F.flatMap(f=>f.s)),K=Math.max(1,Math.floor(V.length/3)),inc=new Map(V.map(v=>[v,F.map((f,i)=>f.s.includes(v)?i:-1).filter(i=>i>=0)])),best=null,scans=0;
 function split(I){let A=new Set();for(let v of I)for(let j of inc.get(v))A.add(j);let L=F.filter((f,j)=>A.has(j)),R=F.filter((f,j)=>!A.has(j)),lv=sort(L.flatMap(f=>f.s)),rv=new Set(R.flatMap(f=>f.s)),b=lv.filter(v=>rv.has(v)),ls=lv.length-b.length,rs=rv.size-b.length;scans+=F.length;return {L,R,b,ls,rs,I:[...I],score:[b.length,-Math.min(ls,rs),Math.abs(L.length-R.length)]}}
 function better(a,b){return !b||a.score.some((x,i)=>x<b.score[i]&&a.score.slice(0,i).every((v,j)=>v===b.score[j]))}
 for(let v of V){let I=new Set([v]);for(let k=1;k<K;k++){let next=null;for(let u of V)if(!I.has(u)){let q=split(new Set([...I,u]));if(better(q,next))next=q}I=new Set(next.I)}let q=split(I);if(q.ls>=K&&q.rs>=K&&better(q,best))best=q;}
 if(!best){for(let v of V){let q=split(new Set([v]));if(q.ls&&q.rs&&better(q,best))best=q}}
 return best?{...best,scans}:null
}
function projectedAffine(F,B){let V=sort(F.flatMap(f=>f.s)),I=V.filter(v=>!B.includes(v)),O=[...B,...I],ix=new Map(O.map((v,i)=>[v,i])),D=new Map(),checks=0,updates=0;let par=x=>{let z=0;for(;x;x&=x-1)z^=1;return z};
 for(let f of F){let ws=[];for(let x=0;x<2**f.s.length;x++)if(bit(f.m,x))ws.push(x);if(!ws.length)return {bad:true,eqs:[],checks,updates};for(let q=1;q<2**f.s.length;q++){let r=par(q&ws[0]);if(ws.every(w=>{checks++;return par(q&w)===r})){let b=0n;for(let j=0;j<f.s.length;j++)if(q>>j&1)b|=1n<<BigInt(ix.get(f.s[j]));while(b){let k=b.toString(2).length-1;if(!D.has(k)){D.set(k,[b,r]);break}let [c,s]=D.get(k);b^=c;r^=s;updates++}if(!b&&r)return {bad:true,eqs:[],checks,updates}}}}
 let eqs=[...D].filter(([k])=>k<B.length).map(([k,[b,r]])=>[Number(b),r]);return {bad:false,eqs,rank:eqs.length,checks,updates}
}
function allowed(eq,w){let par=x=>{let z=0;for(;x;x&=x-1)z^=1;return z};return eq.every(([b,r])=>par(b&w)===r)}
function main(compile,corpus,reg){let out=[];for(let name of ["JOINT-24","RANDOM-3CNF-40"]){let s=corpus.instances.find(x=>x.id===name),r=reg.instances.find(x=>x.alias==="EB-"+name),G=compile(s),h={native:sha(J(G.network)),map:sha(J(G.source_map)),cnf:sha(s.dimacs)};if(h.native!==r.sha256||h.map!==r.source_map_sha256||h.cnf!==r.source_cnf.sha256||J(G.network).length*8!==r.N_bits||s.dimacs.length*8!==r.source_cnf.N_bits)throw Error("auth");let n=native(G.network),cases=[];for(let kind of ["native","cnf"]){let st=Date.now(),F=kind==="native"?n.F:cnfFactors(s),E=early(F),C=compress(E.F,"cache",6),V=replay(E.F,C),Q=sep(C.F);if(!Q){cases.push({kind,status:"NO-SPLIT"});continue}let A=projectedAffine(Q.L,Q.b),B=projectedAffine(Q.R,Q.b),all=projectedAffine(C.F,Q.b),data={kind,original:kind==="native"?r:r.source_cnf,auth:h,roots:kind==="native"?n.roots:s.nvars,early:E.stats,projection:C.stats,projectionCheck:V,boundary:Q.b,leftInterior:Q.ls,rightInterior:Q.rs,regionCounts:[Q.L.length,Q.R.length],geometryScans:Q.scans,affine:{left:A,right:B,global:all},residual:J(serial(C.F)),reverseMap:C.compressed,left:serial(Q.L),right:serial(Q.R),ms:Date.now()-st};cases.push(data)}out.push({name,h,cases})}return out}

// Evaluate with pinned check.js in scope; call main(compile,corpus,registry).
