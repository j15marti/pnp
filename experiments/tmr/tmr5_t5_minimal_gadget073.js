// Standalone Node.js 18+ executable. No dependencies, no seed.
const verify = function verify(){
 const R=(a,b)=>((b-a+5)%5===1)||((b-a+5)%5===3);
 const C=(a,b)=>{const d=(b-a+5)%5;return d===1||d===4};
 let checks=0;const assert=(x,m)=>{checks++;if(!x)throw Error(m||"assertion")};
 function multiplicity(E,k,d){
  let sum=0,limit=5**k;
  for(let i=0;i<limit;i++){
   let q=i,x=[0,d];for(let j=0;j<k;j++){x.push(q%5);q=Math.floor(q/5)}
   if(E.every(([u,v])=>R(x[u],x[v])))sum++;
  }return sum;
 }
 function prof(E,k){return Array.from({length:5},(_,d)=>multiplicity(E,k,d))}
 const target=[0,1,0,0,1];let one=0,short=0,graphs=0;
 let uniqueProfiles=new Set(),byAux={};
 for(let k=0;k<=3;k++){
  let options=[];for(let u=0;u<k+2;u++)for(let v=0;v<k+2;v++)if(u!==v)options.push([u,v]);
  let count=0;
  for(let a=-1;a<options.length;a++){
   for(let b=a+1;b<options.length;b++){
    for(let c=b+1;c<options.length;c++){
     let E=[a,b,c].filter(x=>x>=0).map(x=>options[x]);
     let p=prof(E,k); count++;
     assert(p.some((x,d)=>(x>0)!==(target[d]>0)),"short support");
    }
   }
  }
  // k=0..3: missing empty/one/two variants for options[last] handled here
  for(let a=-1;a<options.length;a++){
   for(let b=a+1;b<options.length;b++){
    let E=[a,b].filter(x=>x>=0).map(x=>options[x]);
    let p=prof(E,k);count++;
    assert(p.some((x,d)=>(x>0)!==(target[d]>0)),"short support 2");
   }
  }
  // Counting above intentionally overlapping; strict symbolic checks independent.
  byAux[k]=count;short+=count;
 }
 let arc3=[];for(let i=0;i<3;i++)for(let j=0;j<3;j++)if(i!==j)arc3.push([i,j]);
 for(let mask=0;mask<64;mask++){
  let E=arc3.filter((_,i)=>(mask>>i)&1),p=prof(E,1);
  uniqueProfiles.add(p.join(","));one++;
  assert(p.some((v,d)=>(v>0)!==(target[d]>0)),"one auxiliary");
 }
 let gE=[[0,2],[0,3],[3,2],[3,1]];
 let oldE=[[0,2],[2,1],[1,3],[3,0]];
 assert(JSON.stringify(prof(gE,2))===JSON.stringify(target),"new vector");
 assert(JSON.stringify(prof(oldE,2))===JSON.stringify([0,2,0,0,2]),"old vector");
 for(let a=0;a<5;a++)for(let b=0;b<5;b++){
   let completions=[];
   for(let z=0;z<5;z++)for(let w=0;w<5;w++)
    if(R(a,z)&&R(a,w)&&R(w,z)&&R(w,b))completions.push([z,w]);
   let correct=C(a,b)?[[(a+1)%5,(a+3)%5]]:[];
   assert(JSON.stringify(completions)===JSON.stringify(correct),"25 endpoints");
 }
 let totalColorings=0;
 for(let n=0;n<=4;n++){
  let allEdges=[];for(let i=0;i<n;i++)for(let j=i+1;j<n;j++)allEdges.push([i,j]);
  for(let mask=0;mask<2**allEdges.length;mask++){
   let E=allEdges.filter((_,j)=>(mask>>j)&1),source=0,via=0;
   for(let t=0;t<5**n;t++){
    let q=t,col=[];for(let j=0;j<n;j++){col.push(q%5);q=Math.floor(q/5)}
    let accepted=E.every(([u,v])=>C(col[u],col[v]));
    source+=+accepted;
    let ways=1;for(let [u,v] of E){
      ways*=multiplicity(gE,2,(col[v]-col[u]+5)%5);
    }via+=ways;
   }
   assert(source===via,"full H counts");graphs++;totalColorings+=source;
  }
 }
 return {revision:"tmr5-gadget-minimality073-node-v1",seed:null,one_aux_all_arc_subsets:one,one_aux_distinct_count_profiles:uniqueProfiles.size,short_arc_tests:short,short_tests_by_aux:byAux,short_false_positive_count:0,endpoint_pairs:25,graphs_n_at_most_4:graphs,original_solution_sum:totalColorings,assertions:checks,failures:0,scope:"exhaustive finite; no mathematical claim from tests alone"};
};
console.log(JSON.stringify(verify(),null,2));
