typedef int mytype;

int g_v1 = 44;


int rename_f1(void)
{
	return 15;
}

int rename_f2(void)
{
	int v = rename_f1();
	if(v!=15)
		return v;
	else
		return 42;
}

int rename_recurs(int depth)
{
	if(depth)
		return 3 + rename_recurs(depth-1);
	return 22;
	
}

int rename_loopfunc(int param)
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
        case 5:
            res/=2;
            break;
        }
        if(res%2)
            res/=2;
	res+=rename_recurs(res);
	res+=rename_recurs(res);
    }
}


int main(void)
{
	rename_f2();
	rename_f1();
    rename_loopfunc();
}
