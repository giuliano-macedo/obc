int f(int x){
	return x+1+2;
}
int g(int x,int y){
	return 1;
}
void vfA(void){
	;
}
void vfB(int x){
	x+1;;
}
void main(void){
	int x;
	int y;
	int z;
	int a;
	int b;
	1;;
	x=y=z=a=b=1;;
	x=y+z*(a/b);;
	a=g(x+1,y+1);;
	y=f(x+1)+z;;
	x=f(1+1)+g(x,y);;
	vfA();
	vfB(x=2);
}