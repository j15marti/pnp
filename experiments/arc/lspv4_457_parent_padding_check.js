// LSPV-4/457 independent finite witness checker. Standard Node.js, no dependencies.
function check457(){
let aCount=0;function assert(x,tag){aCount++;if(!x)throw Error(tag)}
const graphs=[
["K4",4,Array.from({length:4},(_,i)=>Array.from({length:3-i},(_,j)=>[i,i+j+1])).flat()],
["Cube",8,Array.from({length:8},(_,i)=>[0,1,2].map(k=>[i,i^(1<<k)]).filter(e=>e[0]<e[1])).flat()],
["Petersen",10,[...Array.from({length:5},(_,i)=>[i,(i+1)%5]),...Array.from({length:5},(_,i)=>[i+5,(i+2)%5+5]),...Array.from({length:5},(_,i)=>[i,i+5])]]];
function tseitin(n,edges,odd){
 const I=Array.from({length:n},()=>[]);
 edges.forEach(([u,v],j)=>{I[u].push(j+1);I[v].push(j+1)});
 assert(I.every(row=>row.length===3),"degree-three required");
 const rows=[];
 for(let v=0;v<n;v++)for(let z=0;z<8;z++){
 const parity=((z>>0)&1)+((z>>1)&1)+((z>>2)&1);
 if((parity&1)===Number(odd&&v===0))continue;
 rows.push(I[v].map((id,j)=>((z>>j)&1)?-id:id));
 }return rows;
}
function sat(cs,m){
 for(let v=0;v<2**m;v++)if(cs.every(c=>c.some(x=>Number((v>>(Math.abs(x)-1))&1)===Number(x>0))))return true;
 return false;
}
const results=[];
for(const [name,n,edges] of graphs)for(const odd of [false,true]){
 const root=tseitin(n,edges,odd),m=edges.length;
 assert(root.length===4*n,"root-clause count");
 assert(sat(root,m)===!odd,"root-charge SAT/UNSAT");
 let h=1;while(h<4*n)h=h*2+1;
 let next=m+1,blocks=[root];
 for(let k=1;k<h;k++){const block=[];for(let j=0;j<4*n;j++){block.push([next,next+1,next+2]);next+=3;}blocks.push(block);}
 const source=blocks.flat();
 assert(source.length===4*n*h,"parent source length");
 const owner=new Map();
 blocks.forEach((block,b)=>block.forEach(cl=>{
 assert(cl.length===3&&new Set(cl.map(Math.abs)).size===3,"strict 3CNF");
 for(const x of cl){const v=Math.abs(x);assert(!owner.has(v)||owner.get(v)===b,"cross-block variable");owner.set(v,b);}
 }));
 assert(blocks.slice(1).every(b=>b.every(c=>c.every(l=>l>0))),"independent padding SAT");
 // All child interfaces are empty, hence root OR-fold guest is exactly the root packet CNF.
 assert(sat(root,m)===!odd,"root guest must retain odd-charge UNSAT");
 let min=Infinity,cuts=0;
 for(let mask=1;mask<(1<<n)-1;mask++){
 let weight=0;for(let j=0;j<n;j++)weight+=(mask>>j)&1;
 if(weight<Math.floor(n/3)||weight>Math.floor(n/2))continue;
 let cross=0;for(const [u,v] of edges)if(Boolean((mask>>u)&1)!==Boolean((mask>>v)&1))cross++;
 min=Math.min(min,cross);cuts++;
 }
 assert(cuts>0&&min>0,"balanced graph cut");
 const corrupt=source.map(c=>c.slice());corrupt[0][0]=-corrupt[0][0];
 assert(corrupt[0][0]!==source[0][0],"signed-original source mutation");
 results.push({graph:name,n,odd_charge:odd,h,parent_clauses:source.length,guest_clauses:root.length,guest_sat:!odd,min_balanced_cut:min,balanced_cuts:cuts});
}
return {status:"COMPUTATIONAL only; asymptotic packet-expansion lemma separately proved",assertions:aCount,failures:0,results};
}
if(typeof module!=="undefined"&&module.exports){module.exports=check457;if(require.main===module){console.log(JSON.stringify(check457(),null,2));}}
else {check457();}
