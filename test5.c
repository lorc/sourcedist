typedef int mytype;
int printf;
int g_v1 = 44;


int f1(void)
{
	int x;
	for(x=0;x<15;x++)
		printf("%d",x);	
	return 15;
}

int f2(void)
{
	int v = f1();
	if(v!=15)
		return v;
	else
		return 42;
}

int recurs(int depth)
{
	if(depth)
		return 3 + recurs(depth-1);
	return 22;
	
}


int main(void)
{
	f2();
	f1();
    recurs(3);
}
