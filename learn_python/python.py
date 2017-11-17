

python基础学习笔记（一）


交互式python解释器可以当强大的计算器使用
  

>>> 1-2 
-1 
>>> 1+2 
3 
>>> 32784*13 
426192 
>>> 1/2 
0
   什么情况？1除2 不是应该等于0.5么？怎么是0呢？ “/” 用于取整，不够整除，肯定就是0了，试试浮点数

>>> 7/2 
3
>>> 1.0/2.0 
0.5

试试“%” 取余


>>> 6 % 3 
0 
>>> 6 / 3 
2 
>>> 6 % 3 
0 
>>> 7 / 3 
2 
>>> 7 % 3 
1 
>>> 13 % 9 
4
>>> 0.75 % 0.5 
0.25

下面再试试“ ** ” 幂运算（乘方）符


>>> 2*2*2 
8 
>>> 2**3 
8 
>>> 2**6 
64 
>>> -3**2 
-9 
>>> (-3)**2 


   2的3次方可以用乘方符（**）表示，这样就相当方便。

   乘方符比取反（一元减运算符）的优先级高，所以-3**2 等同于-（3**2），如果想计算（-3）**2 ，就需要显式说明。

长整数


python可以处理非常大的数

>>> 100000000000000000000000 
100000000000000000000000L 

>>> 100000000000000000000000L 
100000000000000000000000L

普通整数在2 147 483 647 至 -2 147 483 647 之间，超出可以用长整形表示（L） ，我们也可以自己把整数转换成长整型（输入时在末尾加“L”）



语句


实际上最开始我们已经讲了语句 print 就是打印输出语句。

>>> 2*2 
4 

>>> print 2*2 
4

虽然结果一样，上面的是表达式，下面的是语句。






获取用户的输入：
  






变量：
   










python代码规范：https://confluence.ygomi.com:8443/display/RRT/Code+specification+of+Python







使用技巧：


输出：
    1.1 使用逗号

    >>> print 'age:',25
        age: 25

        如果想要同时输出文本和变量值，却又不希望使用字符串格式化的话，那这个特性就非常有用了：

    >>> name = 'chongshi'
    >>> salutation = 'Mr'
    >>> greeting = 'Hello.'
    >>> print greeting,salutation,name
        Hello. Mr chongshi


   1.2 使用字符串格式化：
    >>> print 'age: %d' %25
        age: 25



模块导入函数:
    从模块导入函数的时候，可以使用

    import somemodule

    或者

    form somemodule immport  somefunction

    或者

    from somemodule import somefunction.anotherfunction.yetanotherfunction

    或者

    from somemodule import *  

    只有确定自己想要从给定的模块导入所有功能进。

    import math as foobar   #为整个模块提供别名

    from math import sqrt as foobar  #为函数提供别名







    
    



