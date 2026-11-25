function controls(){
const F=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]];
const P=[];for(let i=0;i<3;i++){P.push([0,1,2].map(j=>3*i+j));P.push([0,1,2].map(j=>3*j+i));P.push([0,1,2].map(j=>3*j+(i+j)%3));P.push([0,1,2].map(j=>3*j+(i+2*j)%3))}
function count(O,n,pin=-1){let count=0;for(let w=0;w<(1<<n);w++){if(pin>=0&&(w&1)!==pin)continue;if(O.every(o=>{let t=o.t.reduce((s,j,k)=>s+(((w>>j)&1)<<k),0);return !o.bad.includes(t)}))count++}return count}
let f=F.map(t=>({t,bad:[0,7]})),p=P.map(t=>({t,bad:[0,7]})),roots=[-1,0,1].map(pin=>({pin,Fano:count(f,7,pin),plane:count(p,9,pin)}));
let neighbors=[];for(let i=0;i<f.length;i++)for(let mask of [1,2,4,0,7]){let r=f.map((o,j)=>j!==i?o:{t:o.t,bad:mask===0||mask===7?[mask]:[mask,7^mask]});neighbors.push({i,mask,models:count(r,7)})}
if(roots.some(r=>r.Fano||r.plane)||neighbors.some(r=>r.models!==([0,7].includes(r.mask)?5:10)))throw Error("control mismatch");
return {roots,neighbors}}
console.log(JSON.stringify(controls(),null,2));
