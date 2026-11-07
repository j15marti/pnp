"use strict";
function assert(x,msg){if(!x)throw Error(msg);}
function bit(mask,i){return (mask>>>i)&1;}
function cnf(mask){let out=[];for(let a=0;a<8;a++)if(!bit(mask,a))out.push(a);return out;}
function evalCnf(blockers,a){return blockers.every(b=>b!==a);}
function affine(mask,rhs,a){let s=0;for(let i=0;i<3;i++)if(bit(mask,i))s^=bit(a,i);return s===rhs;}
function clauseEval(c,a){return c.some(([i,pos])=>bit(a,i)===(pos?1:0));}
function makeClauses(){let a=[];for(let k=0;k<27;k++){let r=k,c=[];for(let j=0;j<3;j++){let q=r%3;r=Math.floor(r/3);if(q)c.push([j,q===1]);}a.push(c);}return a;}
function main(){
let checks=0,implications=0,affineTests=0,resPairs=0,wideTests=0;
for(let f=0;f<256;f++){let F=cnf(f);for(let a=0;a<8;a++){assert(evalCnf(F,a)===!!bit(f,a),"canonical mismatch");checks++;}
for(let g=0;g<256;g++){let G=cnf(g),and=f&g;for(let a=0;a<8;a++){assert(evalCnf(cnf(and),a)===(!!bit(f,a)&&!!bit(g,a)),"AND mismatch");checks++;}let implies=(f&(~g&255))===0;if(implies){implications++;for(let blocker of G){assert(F.includes(blocker),"missing falsifier source blocker");checks++;}}}
for(let row=0;row<8;row++)for(let rhs=0;rhs<2;rhs++){let rmask=0;for(let a=0;a<8;a++)if(affine(row,rhs,a))rmask|=1<<a;let implies=(f&(~rmask&255))===0;if(implies){affineTests++;for(let a=0;a<8;a++)if(bit(f,a))assert(affine(row,rhs,a),"invalid row");checks++;}}
}
let cls=makeClauses();
for(let A of cls)for(let B of cls)for(let v=0;v<3;v++){
let pa=A.some(([i,p])=>i===v&&p),na=A.some(([i,p])=>i===v&&!p),pb=B.some(([i,p])=>i===v&&p),nb=B.some(([i,p])=>i===v&&!p);
if(!((pa&&nb)||(na&&pb)))continue;
let R=[...A.filter(([i,p])=>i!==v),...B.filter(([i,p])=>i!==v)];resPairs++;
for(let a=0;a<8;a++){assert(!(clauseEval(A,a)&&clauseEval(B,a))||clauseEval(R,a),"RES unsound");checks++;}
}
for(let rowMask=0;rowMask<64;rowMask++){if(rowMask.toString(2).replace(/0/g,"").length<4)continue;for(let rhs=0;rhs<2;rhs++){for(let x=0;x<6;x++)for(let y=x+1;y<6;y++)for(let z=y+1;z<6;z++){let s=[x,y,z];if(s.every(v=>bit(rowMask,v)))continue;
for(let a=0;a<8;a++){let found=false;for(let b=0;b<64;b++){if(s.some((v,j)=>bit(b,v)!==bit(a,j)))continue;let parity=0;for(let v=0;v<6;v++)if(bit(rowMask,v))parity^=bit(b,v);if(parity===rhs){found=true;break;}}
assert(found,"wide row implies local nontrivial");checks++;wideTests++;
}}}}
assert(!evalCnf([0],0),"corrupted canonical blocker not rejected");
assert(!affine(1,0,1),"corrupted affine polarity not rejected");
assert(!clauseEval([[0,true]],0),"corrupted literal polarity not rejected");
return {status:"PASS", checks, factorPairs:65536, implications, affineTests, resolutionPairs:resPairs, wideProjectionTests:wideTests, corruptControls:3, scopes:"all 3-var relations, all 3-var clauses, 6-var wide row projection", originalSourceControl:"symbolic clauses; no SAT oracle", caveat:"not an historical R_mix341 checker or Pang proof reproduction"};
}
if(typeof module!=="undefined"&&require.main===module)console.log(JSON.stringify(main()));
