'use strict';
// LSPV-1 356 strict canonical signed-DIMACS source-input controls.
// Independent of the RES+VARDEF proof producer.
function parse(s){
 if(typeof s!=='string'||!s.endsWith('\n'))throw Error('unterminated');
 const l=s.slice(0,-1).split('\n'),h=/^p cnf (0|[1-9]\d*) (0|[1-9]\d*)$/.exec(l[0]);
 if(!h)throw Error('header');
 const n=Number(h[1]),m=Number(h[2]);
 if(n>1e6||m>1e6||l.length!==m+1)throw Error('count');
 const clauses=[];
 for(const line of l.slice(1)){
   if(!/^(-?[1-9]\d*( -?[1-9]\d*)* )?0$/.test(line))throw Error('clause grammar');
   const a=line.split(' ').map(Number),C=a.slice(0,-1),seen=new Set();
   for(const v of C){
     if(!Number.isSafeInteger(v)||Math.abs(v)>n||seen.has(v)||seen.has(-v))throw Error('invalid literal');
     seen.add(v);
   }clauses.push(C);
 }
 return {n,m,clauses};
}
const good=['p cnf 2 3\n1 2 0\n-1 0\n-2 0\n','p cnf 2 2\n1 2 0\n-1 0\n','p cnf 2 0\n','p cnf 0 1\n0\n'];
const bad=['','p cnf 2 3\n1 2 0\n-1 0\n','p cnf 2 1\n1 2\n',
 'p cnf 2 1\n3 0\n','p cnf 2 1\n1 0 2 0\n','p cnf 2 1\n1 1 0\n',
 'p cnf 2 1\n1 -1 0\n','p cnf 2 1\nx 0\n','p cnf 2 0\nTRAILER\n',
 'p cnf 2 1\n1 -0 0\n','p cnf 2 1\n1 0','p cnf -2 1\n1 0\n',
 'p cnf 2 -1\n1 0\n','p cnf 2 1\n0\n0\n','p cnf 2 1\n01 0\n',
 'p cnf 2 1\n+1 0\n'];
for(const v of good)parse(v);
let rejected=0;for(const v of bad)try{parse(v)}catch(e){rejected++}
if(rejected!==bad.length)throw Error('malformed source accepted');
console.log(JSON.stringify({valid:good.length,malformed_rejected:rejected,status:'PASS'}));
