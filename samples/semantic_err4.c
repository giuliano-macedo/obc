void f(int x[]){
	return;
}
void main(void){
	int x;
	int vec[10];
	f(x);
	f(vec);
	f(x,vec);
}