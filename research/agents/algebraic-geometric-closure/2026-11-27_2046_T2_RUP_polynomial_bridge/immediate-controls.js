function controls(F,proof,limit){
 let vars=[...new Set(F.flat().map(Math.abs))],upVisits=0,impVisits=0,firstUP=null,firstSCC=null,upWitness=null,sccWitness=null,db=F.slice();
 function up(){let A=new Set();for(;;){let change=false;for(let j=0;j<db.length;j++){let free=[],sat=false;for(let l of db[j]){upVisits++;if(A.has(l)){sat=true;break}if(!A.has(-l))free.push(l)}if(sat)continue;if(!free.length)return {row:j,assigned:[...A]};if(free.length===1){A.add(free[0]);change=true}}if(!change)return null}}
 function scc(){let adj=new Map(vars.flatMap(x=>[[x,[]],[-x,[]]]));for(let j=0;j<db.length;j++){let c=db[j];impVisits++;if(!c.length)return {empty:j};if(c.length===1)adj.get(-c[0]).push([c[0],j]);else if(c.length===2){adj.get(-c[0]).push([c[1],j]);adj.get(-c[1]).push([c[0],j])}}
 function path(a,b){let Q=[a],par=new Map([[a,null]]);for(let i=0;i<Q.length;i++){let x=Q[i];if(x===b){let P=[];while(par.get(x)){let [y,j]=par.get(x);P.push([y,x,j]);x=y}return P.reverse()}for(let [y,j] of adj.get(x)){impVisits++;if(!par.has(y)){par.set(y,[x,j]);Q.push(y)}}}return null}
 for(let v of vars){let p=path(v,-v);if(!p)continue;let q=path(-v,v);if(q)return {v,paths:[p,q]}}return null}
 for(let i=0;i<=limit;i++){if(i)db.push(proof[i-1]);if(firstUP===null){let z=up();if(z){firstUP=i;upWitness=z}}if(firstSCC===null){let z=scc();if(z){firstSCC=i;sccWitness=z}}}
 return {firstUP,firstSCC,upVisits,impVisits,upWitness,sccWitness,terminalPrefixRows:proof.slice(Math.max(0,limit-4),limit)}
}
if(typeof require!=='undefined'&&require.main===module){const fs=require('node:fs'),a=JSON.parse(fs.readFileSync(process.argv[2],'utf8'));console.log(JSON.stringify(a.map(q=>({name:q.name,native:controls(q.chart,q.native.proof,q.native.firstPCConstantBeforeEmpty)})),null,2));}
