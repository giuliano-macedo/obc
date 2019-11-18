int fib(int n){
	if(n<=1){
		return 1;
	}
	return n+fib(n-1);
}
void main(void){
	int i;
	int u;

	u=getint();
	i=0;
	while(i<u){
		putint(fib(i));
		i=i+1;
	}
}