void f(void){}
void main(void){
	int x;
	x=1+f();
	x=f();
	f()+1;
	f();
}