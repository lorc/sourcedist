typedef int mytype;

int g_v1 = 44;


int f1(void)
{
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

int loopfunc(int param)
{
    int res;
    int x;
    for( x = 0;x<param;x++)
    {
        switch(x%4)
        {
        case 0:
            res+=3;
        case 2:
            res*=2;
            break;
        case 3:
            res--;
        case 1:
            res/=2;
            break;
        }
        if(res%2)
            res/=2;
    }
}

int main(void)
{
	f2();
	f1();
    loopfunc();
}
