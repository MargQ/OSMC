#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <locale.h>

int Correlations(int a[], int b[]){
    int correl = 0 ;

    for (int i=0; i < 8; i++){
        correl+= a[i]*b[i] ;   
    }
    
    return correl;
}

float Norm_Correlat(int a[], int b[]){
    int sum_a=0, sum_b = 0, cor_a_b=0;

    for (int i = 0; i < 8; i++ ){
        sum_a+=a[i]*a[i];
        sum_b+=b[i]*b[i];
        //printf(" %d ", sum_a);
    }

    cor_a_b = Correlations(a,b);
    
    float res =(cor_a_b/sqrt(sum_a*sum_b));
    
    return res;
}


int main(){

    setlocale(LC_ALL, "Russian");
    int a[] = {2, 3, 6, -1, -4, -2, 2, 5};  
    int b[] = {4, 6, 8, -2, -6, -4, 2, 7};
    int c[] = {-3, -1, 3, -7, 2, -8, 5, -1};
    
    int corr_a_b = Correlations(a,b);
    int corr_a_c = Correlations(a,c);
    int corr_b_c = Correlations(b,c);
    //printf("\n%d", corr_a_b);
    //printf("\n%d", corr_a_c);
    //printf("\n%d", corr_b_c);
    printf("Корреляция\n");
    printf("--------------------------\n");
    printf("| / |  A  |   B  |   C  |\n");
    printf("--------------------------\n");
    printf("|  A |     |  %d |   %d |\n",corr_a_b,corr_a_c);
    printf("--------------------------\n");
    printf("|  B | %d |      |  %d  |\n",corr_a_b,corr_b_c);
    printf("--------------------------\n");
    printf("|  C |  %d |  %d  |      |\n",corr_a_c,corr_b_c);
    printf("--------------------------\n\n\n");

    float norm_corr_a_b = Norm_Correlat(a,b);
    float norm_corr_a_c = Norm_Correlat(a,c);
    float norm_corr_b_c = Norm_Correlat(b,c);
    
    // printf("\n%.3f", norm_corr_a_b);
    // printf("\n%f", norm_corr_a_c);
    //printf("\n%f", norm_corr_b_c);
    printf("Нормализованная корреляция\n");
    printf("--------------------------\n");
    printf("|  / |  A  |   B  |   C  |\n");
    printf("--------------------------\n");
    printf("|  A |     |%.3f | %.3f|\n",norm_corr_a_b,norm_corr_a_c);
    printf("--------------------------\n");
    printf("|  B |%.3f|      | %.3f|\n",norm_corr_a_b,norm_corr_b_c);
    printf("--------------------------\n");
    printf("|  C |%.3f|%.3f |      |\n",norm_corr_a_c,norm_corr_b_c);
    printf("--------------------------\n");

    

}