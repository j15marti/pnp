function audit(){
 let state=1729;function rand(n){state=(Math.imul(1664525,state)+1013904223)>>>0;return state%n;}
 let maskchecks=0,dbmchecks=0,atomchecks=0;
 const rows=[];for(let H=-2;H<=2;H++)for(let a=H;a<=H+1;a++)for(let b=H;b<=H+1;b++)for(let c=Math.max(a,b);c<=H+1;c++){let mode=c===H?0:1+2*(a-H)+(b-H);rows.push({H,a,b,c,mode});}
 for(let subset=0;subset<32;subset++)for(const {H,a,b,c,mode} of rows){const allowed=(i)=>Boolean(subset&(1<<i));const pass=(allowed(0)||c===H+1)&&(allowed(1)||c<=Math.max(a,b))&&(allowed(2)||b<=a)&&(allowed(3)||a<=b)&&(allowed(4)||H>=Math.min(a,b));if(pass!==allowed(mode))throw Error("mask");maskchecks++;}
 const n=4,B=2,words=[];for(let a=-B;a<=B;a++)for(let b=-B;b<=B;b++)for(let c=-B;c<=B;c++)words.push([0,a,b,c]);
 const sat=(x,C)=>C.every(([u,v,k])=>x[v]-x[u]<=k);
 const hull=(S)=>Array.from({length:n},(_,u)=>Array.from({length:n},(_,v)=>Math.max(...S.map(x=>x[v]-x[u]))));
 for(let t=0;t<400;t++){let C=Array.from({length:5},()=>[rand(n),rand(n),rand(5)-2]);let S=words.filter(x=>sat(x,C));if(!S.length)continue;let modes=Array.from({length:3},()=>Array.from({length:2},()=>[rand(n),rand(n),rand(5)-2]));let sets=modes.map(A=>S.filter(x=>sat(x,A))).filter(A=>A.length);if(!sets.length)continue;let H=hull(sets.flat()),Ds=sets.map(hull);for(let i=0;i<n;i++)for(let j=0;j<n;j++){if(H[i][j]!==Math.max(...Ds.map(D=>D[i][j])))throw Error("hull");for(let k=0;k<n;k++)if(H[i][j]>H[i][k]+H[k][j])throw Error("triangle");}dbmchecks++;}
 for(let t=0;t<500;t++){let atoms=Array.from({length:7},()=>[rand(n),rand(n),rand(n),rand(5)-2]);let C=Array.from({length:4},()=>[rand(n),rand(n),rand(5)-2]);let expected=words.some(x=>sat(x,C)&&atoms.every(([v,a,b,k])=>x[v]<=Math.max(x[a],x[b])+k));let x=[0,B,B,B],ok=true,changed=true;while(changed&&ok){changed=false;for(const [v,r] of [...C.map(([u,v,k])=>[v,x[u]+k]),...atoms.map(([v,a,b,k])=>[v,Math.max(x[a],x[b])+k])]){if(x[v]>r){x[v]=r;changed=true;if(x[v]<(v===0?0:-B)){ok=false;break;}}}}if(ok!==expected)throw Error("atom");atomchecks++;}
 return {maskchecks,dbmchecks,atomchecks,seed:1729};
}
console.log(JSON.stringify(audit()));
