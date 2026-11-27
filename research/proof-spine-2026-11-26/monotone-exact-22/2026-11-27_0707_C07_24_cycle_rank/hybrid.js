const fs=require('fs');
const run=function(raw){
return raw.map(({r,adapter,source})=>{
 let clauses=adapter.map(a=>a.clause),m=4*r, checks=0,imports=[];
 for(let j=0;j<r;j++){
 let i=4*j,has=(a,b,f,g)=>clauses.some(c=>{checks++;return c[0]===a&&c[1]===b&&c[2]===f&&c[3]===g;});
 if(!has(i+1,i+2,0,0)||!has(i+1,i+2,1,1))throw Error("missing premises");
 // from internal xor 1 and geometric cycle xor 0, spoke xor 1.
 imports.push([i,i+3,0,0],[i,i+3,1,1]);
 }
 const satCheck=cs=>{
 let n=2*m,R=Array.from({length:n},(_,i)=>Array.from({length:n},(_,j)=>i===j));let edges=0,scans=0;
 for(const [i,j,f,g] of cs){R[2*i+f][2*j+(1-g)]=true;R[2*j+g][2*i+(1-f)]=true;edges+=2;}
 for(let k=0;k<n;k++)for(let i=0;i<n;i++)if(R[i][k])for(let j=0;j<n;j++){scans++;if(R[k][j])R[i][j]=true;}
 const conflicts=Array.from({length:m},(_,i)=>i).filter(i=>R[2*i][2*i+1]&&R[2*i+1][2*i]);
 return {edges,scans,conflicts,no:conflicts.length>0};
 };
 const before=satCheck(clauses), trace=[];
 for(let i=0;i<imports.length;i+=2){clauses.push(...imports.slice(i,i+2));const z=satCheck(clauses);trace.push(z);if(z.no)break;}
 if(before.no||!trace.at(-1).no)throw Error("wrong");
 return {r,checks,imports,base:before,trace};
});
};
console.log(JSON.stringify(run(JSON.parse(fs.readFileSync(__dirname+'/raw.json','utf8'))),null,2));
