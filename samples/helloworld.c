void main(void){
	int str[13] ;/* "hello world\n\0" */

	str[0]=104; 	/* h */
	str[1]=101; 	/* e */
	str[2]=108; 	/* l */
	str[3]=108; 	/* l */
	str[4]=111; 	/* o */
	str[5]=32; 		/*   */
	str[6]=119; 	/* w */
	str[7]=111; 	/* o */
	str[8]=114; 	/* r */
	str[9]=108; 	/* l */
	str[10]=100;	/* d */
	str[11]=10; 	/* \n */
	str[12]=0;		/* \0 */

	putstr(str);
}