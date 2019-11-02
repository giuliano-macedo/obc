int test[50];
int f(int a[],int b,int c){
	return a[0]+b+c;
}
void main(void){
	int x[1];
	x[0]=1;
	f(x,2/3,3);
}