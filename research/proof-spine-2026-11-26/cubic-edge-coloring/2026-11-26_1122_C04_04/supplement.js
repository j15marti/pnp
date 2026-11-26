function supplement(){
 const E=[[0,5],[0,7],[0,9],[1,8],[1,9],[2,7],[2,8],[3,5],[3,6],[4,6],[4,7]],ports=[2,3,1,4,5,8,6,9];
 function pms(D=[]){let used=new Set(D),M=[],out=[];function rec(){let u=Array.from({length:10},(_,i)=>i).find(i=>!used.has(i));if(u===undefined){out.push([...M].sort((a,b)=>a-b));return}used.add(u);E.forEach(([x,y],i)=>{let v=x===u?y:y===u?x:-1;if(v<0||used.has(v))return;used.add(v);M.push(i);rec();M.pop();used.delete(v)});used.delete(u)}rec();return out}
 const A=pms(),words=[[1,1,2,2,1,1,2,2],[1,1,2,2,1,2,1,2]],rows=words.map(w=>{let B=pms(ports.filter((_,i)=>w[i]===1)),C=pms(ports.filter((_,i)=>w[i]===2)),P=[];for(const b of B)for(const c of C)if(!b.some(i=>c.includes(i)))P.push({b,c,a:E.flatMap((_,i)=>!b.includes(i)&&!c.includes(i)?[i]:[])});return {w,B,C,P}});
 if(A.length!==3||new Set(A.flat()).size!==11||rows[0].P.length||rows[1].P.length!==1||rows[0].B.length!==1||rows[0].C.length!==1)throw Error("BIP8");
 const G=[[0,6],[0,17],[0,19],[1,4],[1,7],[1,14],[2,6],[2,8],[2,10],[3,8],[3,12],[3,13],[4,10],[4,13],[5,9],[5,13],[5,17],[6,16],[7,11],[7,15],[8,14],[9,14],[9,15],[10,15],[11,16],[11,19],[12,18],[12,19],[16,18],[17,18]];
 let cutCounts=[],first=null;for(let k=1;k<=4;k++){let count=0,cyclic=0,S=[];function rec(i){if(S.length===k){count++;let bad=new Set(S),a=Array.from({length:20},()=>[]);G.forEach(([u,v],j)=>{if(!bad.has(j)){a[u].push(v);a[v].push(u)}});let vis=new Set(),C=[];for(let u=0;u<20;u++)if(!vis.has(u)){let q=[u],d=0;vis.add(u);for(let j=0;j<q.length;j++){d+=a[q[j]].length;for(let v of a[q[j]])if(!vis.has(v)){vis.add(v);q.push(v)}}C.push([q,d/2])}if(C.length>=2&&C.filter(([vs,m])=>m>=vs.length).length>=2){cyclic++;if(first===null)first=[...S]}return}for(let j=i;j<=G.length-(k-S.length);j++){S.push(j);rec(j+1);S.pop()}}rec(0);cutCounts.push({k,count,cyclic})}
 if(cutCounts.slice(0,3).some(x=>x.cyclic)||!cutCounts[3].cyclic)throw Error("cyclic connectivity");
 return {bip8:{E,ports,A,rows},cutCounts,first}
}
console.log(JSON.stringify(supplement(),null,2));
