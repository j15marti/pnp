function cnfSolve(I,cap=10000000){
 const F=I.dimacs.trim().split("\n").slice(1).map(l=>l.trim().split(/\s+/).map(Number).slice(0,-1)),n=I.nvars;let ticks=0,nodes=0,units=0;
 function walk(A){nodes++;for(;;){let forced=0,score=new Int32Array(n+1),unresolved=false;for(let c of F){let open=0,last=0,sat=false;for(let l of c){if(++ticks>cap)throw Error("cap");let v=A[Math.abs(l)];if(v<0){open++;last=l}else if(Boolean(v)===(l>0)){sat=true;break}}if(sat)continue;unresolved=true;if(!open)return false;if(open===1){forced=last;break}for(let l of c)if(A[Math.abs(l)]<0)score[Math.abs(l)]++}if(!unresolved)return true;if(forced){A[Math.abs(forced)]=Number(forced>0);units++;continue}let v=1;for(let j=2;j<=n;j++)if(score[j]>score[v])v=j;if(!score[v])throw Error("bad split");let x=A.slice();x[v]=0;if(walk(x))return true;x=A.slice();x[v]=1;return walk(x)}}
 try{return{status:walk(new Int8Array(n+1).fill(-1))?"SAT":"UNSAT",nodes,units,literalScans:ticks}}catch(e){return{status:"UNKNOWN",nodes,units,literalScans:ticks,error:String(e)}}
}
module.exports={cnfSolve};
if(require.main===module){const f=require('fs');const I=JSON.parse(f.readFileSync(process.argv[2],'utf8')).instances.find(x=>x.id===process.argv[3]);console.log(cnfSolve(I))}
