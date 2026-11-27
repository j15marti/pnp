function defectPairs(C,H,width,limit=10000,maxLearn=128){
 let X=new Map(H.assignment),bad=H.fields.map((r,i)=>r[0]===0?i:-1).filter(i=>i>=0),breaks=new Map(),tests=0,litWork=0,duplicates=0,tooWide=0,trace=[],keys=new Set(C.map(c=>c.join(","))),breakCounts=new Map();
 for(let j=0;j<C.length;j++){if(H.fields[j][0]!==1)continue;let l=C[j].find(l=>X.get(Math.abs(l))===Number(l>0));litWork+=C[j].length;if(!breaks.has(-l))breaks.set(-l,[]);breaks.get(-l).push(j)}
 let covered=0,totalPivots=0;
 outer:for(let i of bad)for(let p of C[i]){totalPivots++;if(!breaks.get(p)?.length)throw Error("strict plateau lacks break partner");covered++;for(let j of breaks.get(p)){if(tests>=limit||trace.length>=maxLearn)break outer;tests++;let c=[...new Set(C[i].filter(l=>l!==p).concat(C[j].filter(l=>l!==-p)))].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b);litWork+=C[i].length+C[j].length+c.length*c.length;if(c.some(l=>X.get(Math.abs(l))===Number(l>0))||c.some(l=>c.includes(-l)))throw Error("not false resolvent");if(c.length>width){tooWide++;continue}let k=c.join(",");if(keys.has(k)){duplicates++;continue}keys.add(k);trace.push({i,j,p,c})}}
 return {trace,tests,litWork,duplicates,tooWide,totalPivots,covered,defects:bad.length};
}
module.exports={defectPairs};
