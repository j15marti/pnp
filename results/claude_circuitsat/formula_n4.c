// Exact B2 formula size (leaves) for all 2^(2^n) functions, n<=4, level by level. Negation free; leaves x_i, constants cost 0.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
int main(int argc,char**argv){
  int n=atoi(argv[1]); int NF=1<<(1<<n); unsigned M=NF-1;
  static signed char L[65536]; memset(L,-1,sizeof L);
  static int lev[40][65536]; int cnt[40]={0};
  L[0]=0;L[M]=0; // constants
  for(int i=0;i<n;i++){unsigned t=0;for(int a=0;a<(1<<n);a++)if((a>>i)&1)t|=1u<<a;
    L[t]=1;L[M^t]=1;}
  for(int f=0;f<NF;f++) if(L[f]==1) lev[1][cnt[1]++]=f;
  for(int s=2;s<40;s++){
    for(int sa=1;2*sa<=s;sa++){int sb=s-sa;
      for(int i=0;i<cnt[sa];i++){unsigned a=lev[sa][i];
        for(int j=0;j<cnt[sb];j++){unsigned b=lev[sb][j];
          unsigned r[5]={a&b,a&(M^b),(M^a)&b,(M^a)&(M^b),a^b};
          for(int k=0;k<5;k++){unsigned x=r[k];
            if(L[x]<0){L[x]=s;lev[s][cnt[s]++]=x;}
            if(L[M^x]<0){L[M^x]=s;lev[s][cnt[s]++]=M^x;}}}}}
    printf("leaves %d: %d\n",s,cnt[s]);fflush(stdout);
    if(cnt[s]==0&&s>3)break;
  }
  FILE*o=fopen(argv[2],"wb");fwrite(L,1,NF,o);fclose(o);
}
