// Independent verifier for LSPV-1 Result 375. No imports, no shared producer helpers.
// Run: node experiments/arc/lspv1_375_independent_verify.js
function expect(ok, msg){if(!ok)throw new Error(msg);}
function dot(mask, vector, width){let r=0;for(let i=0;i<width;i++)if((mask&(1<<i))&&(vector&(1<<i)))r=1-r;return r;}
function verify(){
 let identity=0,maskPairs=0,bad=0;
 for(let width=1;width<=7;width++){
  const total=2**width;
  for(let left=0;left<total;left++)for(let right=0;right<total;right++){
   maskPairs++;
   for(let input=0;input<total;input++){
    let out=dot(left,input,width)+dot(right,input,width);
    out%=2;
    expect(out===dot(left^right,input,width),'invalid affine sum');
    identity++;
   }
  }
 }
 for(let width=1;width<=6;width++){
  const total=2**width;
  for(let a=0;a<total;a++)for(let b=0;b<total;b++)for(let j=0;j<width;j++){
    const corrupt=(a^b)^(2**j);
    const opposite=(1<<j);
    expect((dot(a,opposite,width)^dot(b,opposite,width))!==dot(corrupt,opposite,width),
      'corrupt assertion accepted');
    bad++;
  }
 }
 // Gaussian rank of K4 incidence matrix, then compare enumeration with each charge.
 const edges=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]];
 const rows=[0,0,0,0];for(let i=0;i<edges.length;i++)for(const v of edges[i]) rows[v]^=1<<i;
 const rankRows=rows.slice();let rank=0;
 for(let col=0;col<6;col++){let pick=-1;for(let r=rank;r<4;r++)if(rankRows[r]&(1<<col)){pick=r;break;}
 if(pick<0)continue;
 [rankRows[rank],rankRows[pick]]=[rankRows[pick],rankRows[rank]];
 for(let r=0;r<4;r++)if(r!==rank&&(rankRows[r]&(1<<col)))rankRows[r]^=rankRows[rank];
 rank++;
 }
 expect(rank===3,'rank must equal |V|-1');
 function counts(ch){let c=0;for(let x=0;x<64;x++){let good=true;for(let v=0;v<4;v++){
 let z=0;for(let e=0;e<6;e++)if(rows[v]&(1<<e))z^=(x>>e)&1;
 if(z!==ch[v]){good=false;break;}}if(good)c++;}return c;}
 const odd=counts([1,0,0,0]),even=counts([0,0,0,0]);
 expect(odd===0&&even===8,'K4 labels');
 return {report:'AFFINE_ROW_ER2_SIMULATION375',independent:true,
  identity_assignments:identity,mask_pairs:maskPairs,corrupted_masks_rejected:bad,
  k4_incidence_rank:rank,odd_k4_models:odd,even_k4_models:even,random_seed:null,
  qualification:'tests affine semantics only, not a native signed ER2 verifier'};
}
const result=verify();
if(typeof module!=='undefined'&&module.exports)module.exports={verify};
if(typeof console!=='undefined')console.log(JSON.stringify(result,null,2));