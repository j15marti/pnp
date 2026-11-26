function audit(){
const E=[[2,3],[2,7],[3,4],[3,8],[4,9],[5,7],[5,8],[6,8],[6,9],[7,9]],P=[4,5,2,6],best={},counts={};let valid=0;
function check(c,msg){if(!c)throw Error(msg)}
for(let k=0;k<4**10;k++){let d=Array(10).fill(0),z=0,x=k;for(const [u,v] of E){let c=x%4;x=Math.floor(x/4);d[u]^=c;d[v]^=c;z+=c===0?1:0}if([3,7,8,9].some(v=>d[v]))continue;let b=P.map(v=>d[v]);if(b.includes(0))continue;let s=b.join("");best[s]=Math.min(best[s]??99,z);counts[s]=(counts[s]??0)+1;valid++}
let words=0;for(let p=1;p<=3;p++)for(let q=1;q<=3;q++)for(let r=1;r<=3;r++)for(let s=1;s<=3;s++){let z=best[""+p+q+r+s]??99;check((z===0)===(p===q&&r===s),"proper relation");if(p===r&&q===s)check(z===Number(p!==q),"crossed relation");words++}
for(const [b,f] of [["1111",[2,3,3,1,2,2,3,2,3,1]],["1122",[1,3,3,2,2,2,3,1,3,1]],["1212",[0,1,2,2,3,3,1,3,1,2]]]){let d=Array(10).fill(0);E.forEach(([u,v],i)=>{d[u]^=f[i];d[v]^=f[i]});check(P.map(v=>d[v]).join("")===b&&[3,7,8,9].every(v=>!d[v]),"witness");check(f.filter(c=>!c).length===Number(b==="1212"),"zero count")}
const diffs=[];for(const d of [0,1,3])for(const e of [0,1,3])if(d!==e)diffs.push((d-e+7)%7);check(new Set(diffs).size===6,"Heawood girth");
const PE=[[5,6],[6,7],[7,8],[8,9],[5,8],[6,9]];for(const [path,selected] of [[[5,8,9,6,7],[[5,8],[8,9],[6,9],[6,7]]],[[9,6,5,8,7],[[6,9],[5,6],[5,8],[7,8]]]]){const key=([u,v])=>[Math.min(u,v),Math.max(u,v)].join(",");check(path.length===5,"parity");check(path.slice(1).every((v,i)=>selected.some(e=>key(e)===key([path[i],v]))),"C04 path");check(selected.every(e=>PE.some(p=>key(p)===key(e))),"C04 edges")}
return {internalAssignments:4**10,nonzeroBoundaryAssignments:valid,words,feasibleBoundaryWords:Object.keys(best).length,best,counts,heawoodDifferences:diffs,peerPathsChecked:2};
}
console.log(JSON.stringify(audit(),null,2));
