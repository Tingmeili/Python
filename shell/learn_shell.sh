# 参考网址：http://man.linuxde.net
# 一：#!/bin/sh
       #!/bin/sh是指此脚本使用/bin/sh来解释执行，#!是特殊的表示符，其后面根的是此解释此脚本的shell的路径。

       #其实第一句的#!是对脚本的解释器程序路径，脚本的内容是由解释器解释的，我们可以用各种各样的解释器来写对应的脚本。

       #比如说/bin/csh脚本，/bin/perl脚本，/bin/awk脚本，/bin/sed脚本，甚至/bin/echo等等。#!/bin/bash同理

       #ls -l /bin/sh /bin/dash 可以看到你本机的情况
       #Ubuntu中可以认为/bin/sh就是/bin/dash
       #bin/sh与/bin/bash虽然大体上没什么区别，但仍存在不同的标准。标记为#!/bin/sh的脚本不应使用任何POSIX没有规定的特性 (如let等命令, 但#!/bin/bash可以)  


      #其中：
          # expect命令
          #可以用来处理交互，实现自动化。需要安装expect : pip install expect，执行的命令和shell不同，而是expect xxx.sh。
          #   sh脚本的第一行就是：
              #!/usr/bin/expect -f   
              #set timeout 2 
              #set username [lindex $argv 0] 
              #set password [lindex $argv 1] 
              #set hostname [lindex $argv 2] 
              #spawn /usr/bin/ssh $username@$hostname
              #expect {
                #"yes/no"
                #{send "yes\r"; exp_continue;}
                #"Password:"{send "$password\r";}
               #}
               #expect eof




# 二 ：
       #echo "\$#:"$#
       #echo "\$0:$0"
       #echo "\$1:$1"
       #echo "\$2:$2"
       #echo "\$@:$@"
       #echo "\$*:$*"

#   $# 传给脚本的参数个数
#   $0 脚本本身的名字
#     $1 传递给该shell脚本的第1个参数
#    $2 传递给该shell脚本的第2个参数
#     $@ 传给脚本的所有参数的列表
#     $* 以一个单字符串显示所有向脚本传递的参数，与位置变量不同，参数可超过9个
#      $$ 脚本运行的当前进程ID号
#    $? 命令执行结果反馈，0表示执行成功，其余数字表示执行不成功。



# 例： if [ $# != 4 ]
#      then
#        echo "cmd rtvpath cameraParam:[65|127] countryName:[us|de|uk|jp] CES:version"
#        exit
       #else
       #rtvDir=$1
       #cameraParam=$2
       #countryName=$3
       #version=$4
       #fi





#三：管道符 ：  
    #‘|’：前面的输出作为后面的输入
   
        #ls -l * | grep "^-"| wc -l   查看某文件夹下文件的个数，包括子文件夹里的。

        #ls -l
        #长列表输出该目录下文件信息(注意这里的文件，不同于一般的文件，可能是目录、链接、设备文件等)

       #grep "^-"

       #这里将长列表输出信息过滤一部分，只保留一般文件，如果只保留目录就是 ^d

       #wc -l
       #统计输出信息的行数,文件的个数.
  

   #xargs：
        
     # find . -name *.db | xargs -i cp {} .
     # find ~ -name ‘*.log' -print0 | xargs -0 rm -f
     
        #-i 选项告诉 xargs 用每项的名称替换 {}。
        #-print0和-0，是避免前面的输出有空格以后，后面测
        #例：xargs 默认是以空白字符 (空格, TAB, 换行符) 来分割记录的, 因此如果文件名是 ./file 1.log，就会被解释成了两个记录 ./file 和 1.log,为了避免这个问题
           #让 find 在打印出一个文件名之后接着输出一个 NULL 字符 ('\0') 而不是换行符, 然后再告诉 xargs 也用 NULL 字符来作为记录的分隔符. 这就是 find 的 -print0 和 xargs 的 -0 的来历
     
     #删除数量比较多的文件
     #ls | xargs -n 20 rm -fr
    
         # -n 将前面的输入进行分批处理
     
     #查找所有的jpg 文件，并且压缩它
        #find / -name *.jpg -type f -print | xargs tar -cvzf images.tar.gz
        #-print 在每一个输出后会添加一个回车换行符，而-print0则不会。

     #pgrep mysql | xargs kill -9　　#直接杀掉mysql的进程
 
      
              



    #区别：
      #管道是实现“将前面的标准输出作为后面的标准输入”
      #xargs是实现“将标准输入作为命令的参数”



#四：find
   
     # -name:  查找时文件名大小写敏感。
     #-iname:  查找时文件名大小写不敏感
     #-atime  -n[+n]: 找出文件访问时间在n日之内[之外]的文件。
     #-ctime  -n[+n]: 找出文件更改时间在n日之内[之外]的文件。
     #-mtime -n[+n]:  找出修改数据时间在n日之内[之外]的文件。
     #-amin   -n[+n]: 找出文件访问时间在n分钟之内[之外]的文件。
     #-cmin   -n[+n]: 找出文件更改时间在n分钟之内[之外]的文件。
     #-mmin  -n[+n]: 找出修改数据时间在n分钟之内[之外]的文件。

      #例：
         #find -cmin -2  找出修改状态时间在2分钟之内的文件。

    #  find . -ctime -2 -exec ls -l {} \;
    #  find . -name "*.dat" -mtime -1 -ok rm -f {} \;
       # -exec: 对匹配的文件执行该参数所给出的shell命令。相应命令的形式为'command' {} \;，注意{}和\；之间的空格，同时两个{}之间没有空格
       # -ok:   其主要功能和语法格式与-exec完全相同，唯一的差别是在于该选项更加安全，因为它会在每次执行shell命令之前均予以提示，只有在回答为y的时候， 其后的shell命令才会被继续执行。需要说明的是，该选项不适用于自动化脚本，因为该提供可能会挂起整个自动化流程

    # find . -user root           #搜索owner是root的文件 
    # find . ！-user root          #搜索owner不是root的文件

    # -type：后面指定文件的类型。
         #b - 块设备文件。
         #d - 目录。
         #c - 字符设备文件。
         #p - 管道文件。
         #l  - 符号链接文件。
         #f  - 普通文件


    #例：
       # find . -type d
       # find . ! -type d  这是找出当前的路径下面不为目录的其他的文件

    #find . -size +4k -exec ls -l {} \;  #查找文件大小大于4k的文件，同时打印出找到文件的明细
    #find . -size -4k -exec ls -l {} \;  #查找文件大小小于4k的文件。

    # find . -size 183c -exec ls -l {} \; #查找文件大小等于183字节的文件。
    #  find . -empty  -type f -exec ls -l {} \; 查找空的文件




#五：常用shell命令
     #nohup command > myout.file 2>&1 &  后台运行command，并将输出的结果重定向到myout.file里面
    # cp，mv，mkdir，touch，rm ，tar zcvf，tar -xzvf，sed，cat，expect命令
      
      #cat ~/.ssh/id_rsa.pub | ssh username@IP "cat >> ~/.ssh/authorized_keys"  将自己的key追加到server上
      
     #5.1  mkdir 
        # mkdir -p $signs_path $xml_path
        # 命令选项

　　         #-m=mode  #为目录指定访问权限，与chmod类似。

　　         #-p　　如果目录已经存在，则不会有错误提示。若父目录不存在，将会创建父目录。该选项常用于创建级联目录。

　　         #-v　　为每个目录显示提示信息

    #5.2 grep
        #fn=`grep "ImgsNum" ${dir_name}"/"cmd.log 
        # 输出的结果为：[2017-06-17 14:57:29.819][VEHICLE_SIGN][debug][7720] Traffic Sign Processing, ImgsNum = 1787, frmStartIdx:0, frmEndIdx:1786      (TSAlgorithmB.cpp:534)

       #fn=`grep "ImgsNum" ${dir_name}"/"cmd.log | awk -F ' ' '{print $8}' `
       # 输出的结果为:1787,

       #fn=`grep "ImgsNum" ${dir_name}"/"cmd.log | awk -F ' ' '{print $8}' | awk -F ',' '{print $1}'`
       # 输出的结果为:1787
    
      #example:
       #echo a,b,c|awk -F","  '{print $1}'
       #将以","分隔字段，因此$1为a



   #5.3 mv

     #mv $xml_name TSRlog.txt cmd.log $dir_name
    #移动前面三个文件到指定目录下面
     #mv
      #1.重命名文件或目录
         #$ mv demo1.txt demo2.txt
         #$ ls
          #  demo2.txt

       #2.mv -i:覆盖文件
          #$ ls
             #demo2.txt  demo.txt
          #$ mv demo2.txt -i demo.txt 
              #mv：是否覆盖"demo.txt"？ y


      #3.mv 不具备写权限的文件名:
           #$ ls -l
            #总用量 0
               #-rw-r--r-- 1 root root 0  1月  8 13:31 cc
                #-rw-r--r-- 1 siu  siu  0  1月  8 13:24 dd
           #$ mv dd cc
              #mv：是否覆盖"cc"，而不理会权限模式0644 (rw-r--r--)？ y
              #$ ls
              #cc
          #如果是mv dd -f cc,则不会提示是否覆盖，强制覆盖

    #4.mv 移动目录
        #$ ls
          #abc  cde
        #$ mv cde abc
        #$ ls
          #abc
        #$ cd abc/
        #$ ls
         #cde

      
    #5.mv -u
       #确认修改时间再判断是否覆盖，此处time2.txt的修改时间比time1.txt的修改时间新，所以覆盖失败
    #6. mv -v
       #列出移动或覆盖时的信息

    #7. mv -b
      #$ mv -b aa.txt bb.txt
      #$ ls
         #bb.txt  bb.txt~

      #覆盖时进行备份，所备份的文件尾部有个～



 
  #5.4 sed
   # sed -i:
   
    #sed -i "s/VERSION/ver2.0/g" $old_pwd/tools/conti/TSR_Evaluation_Tool/TSRConfig.py
      #格式：sed 's/要替换的字符串/新的字符串/g'   （要替换的字符串可以用正则表达式）


  #sed [-nefri] ‘command’ 输入文本 
     #常用选项：
        #-n∶使用安静(silent)模式。在一般 sed 的用法中，所有来自 STDIN的资料一般都会被列出到萤幕上。但如果加上 -n 参数后，则只有经过sed 特殊处理的那一行(或者动作)才会被列出来。
        #-e∶直接在指令列模式上进行 sed 的动作编辑；
        #-f∶直接将 sed 的动作写在一个档案内， -f filename 则可以执行 filename 内的sed 动作；
        #-r∶sed 的动作支援的是延伸型正规表示法的语法。(预设是基础正规表示法语法)
        #-i∶直接修改读取的档案内容，而不是由萤幕输出。



    #常用命令：
        #a   ∶新增， a 的后面可以接字串，而这些字串会在新的一行出现(目前的下一行)～
        #c   ∶取代， c 的后面可以接字串，这些字串可以取代 n1,n2 之间的行！
        #d   ∶删除，因为是删除啊，所以 d 后面通常不接任何咚咚；
         #i   ∶插入， i 的后面可以接字串，而这些字串会在新的一行出现(目前的上一行)；
        # p  ∶列印，亦即将某个选择的资料印出。通常 p 会与参数 sed -n 一起运作～ 


     
   #删除某行
     #[root@localhost ruby] # sed '1d' ab              #删除第一行 
     #[root@localhost ruby] # sed '$d' ab              #删除最后一行
     #[root@localhost ruby] # sed '1,2d' ab           #删除第一行到第二行
     #[root@localhost ruby] # sed '2,$d' ab           #删除第二行到最后一行


   #显示某行
.    #[root@localhost ruby] # sed -n '1p' ab           #显示第一行 
     #[root@localhost ruby] # sed -n '$p' ab           #显示最后一行
     #[root@localhost ruby] # sed -n '1,2p' ab        #显示第一行到第二行
     #[root@localhost ruby] # sed -n '2,$p' ab        #显示第二行到最后一行

    # sed '1a drink tea' ab  #第一行后增加字符串"drink tea"

    #在每行的头添加字符，比如"HEAD"，命令如下：
    #sed 's/^/HEAD&/g' test.file

    #在每行的行尾添加字符，比如“TAIL”，命令如下：

    #sed 's/$/&TAIL/g' test.file



 
      

       
       
       


   

 #将命令执行结果存入变量 ：` `与$( )  
     #LINE_CNT=`wc -l test.txt`

     #LINE_CNT=$(wc -l test.txt)

    # 以上命令均可把wc -l test.txt的结果存入LINE_CNT变量中










#六：echo使用：

    # echo "\"It is a test\"" 输出为："It is a test"

    #  name="OK" 设置一个变量   echo "$name It is a test"  输出 ： OK It is a test
    #  显示换行：echo "OK!\n"
    
    #echo "It is a test" > myfile 输出到一个定向的文件

    # echo '$name\"' 输出$name\"   即：原样输出字符串，不进行转义或取变量(用单引号)



     


#七：shell 里面的变量：
    #例：
    #定义变量：
        # rtvDir=$1
        results_path=`pwd`/test  （`pwd` 代表我脚本的运行的当前的路径）
     
    #使用该变量： 
      #rtvpath=${rtvDir}或则是 $rtvDir  
      #如果变量与其它字符相连的话，需要使用大括号（{ }）例 m=8  echo "${mouth}-1-2009"



    # 6.1整数：
       #整数加减乘除
         #例：
            #a=1 b=2

           # echo `expr $a + $b`
           # echo $(( (1+2)*3/4 ))  # 表达式中可以带括号

   
    #6.2 字符串
      # ${string/old/new} 	string中第一个old替换为new
      # ${string//old/new} 	string中所有old替换为new
        #例：s="i hate hate you"  echo ${s//hate/love} 输出：i love love you


      # ${string:n} 	string从下标n到结尾的子串
      # ${string:n:m} 	string从下标n开始长度为m的子串
      # ${string::m} 	string从下标0开始长度为m的子串


     #通配删除
       #${string#pattern} 	string从左到右删除pattern的最小通配
       #${string##pattern} 	string从左到右删除pattern的最大通配
       #${string%pattern} 	string从右到左删除pattern的最小通配
       #${string%%pattern} 	string从右到左删除pattern的最大通配
       


       #最小通配和最大通配的区别：
         #最小通配：符合通配的最小子串
         #最大通配：符合通配的最大子串
         #例如string值为/00/01/02/dir，对于通配/*/，其最小通配为/00/，而最大通配/00/01/02/



       #使用技巧：
          #获取文件名：${path##*/} (相当于basename命令的功能)

          #获取目录名：${path%/*} (相当于dirname命令的功能)

          #获取后缀名：${path##*.}

            #例： s="/root/test/dir/subdir/abc.txt"
                  # echo ${s##*/}
                  #abc.txt
                  # echo ${s%/*}
                  #/root/test/dir/subdir
                  # echo ${s##*.}
                  #txt


         #例:
             # file=/dir1/dir2/dir3/my.file.txt
             # 可以用${ }分别替换得到不同的值：
             # ${file#*/}：删掉第一个 / 及其左边的字符串：dir1/dir2/dir3/my.file.txt
             # ${file##*/}：删掉最后一个 /  及其左边的字符串：my.file.txt
             # ${file#*.}：删掉第一个 .  及其左边的字符串：file.txt
             # ${file##*.}：删掉最后一个 .  及其左边的字符串：txt
             # ${file%/*}：删掉最后一个  /  及其右边的字符串：/dir1/dir2/dir3
             # ${file%%/*}：删掉第一个 /  及其右边的字符串：(空值)
             # ${file%.*}：删掉最后一个  .  及其右边的字符串：/dir1/dir2/dir3/my.file
             # ${file%%.*}：删掉第一个  .   及其右边的字符串：/dir1/dir2/dir3/my

       
    
     #6.3  数组
         #a=()         # 空数组
         #a=(1 2 3)    # 元素为1,2,3的数组
         #echo ${#a[*]}  # 数组长度
         #echo ${a[2]}   # 下标为2的元素值（下标从0开始）
         #a[1]=0         # 给下标为1的元素赋值

       # 遍历数组
        #for i in ${a[*]}
        #do
        #echo ${i}
        #done

        #unset a        # 清空数组
   


#八：if
     if false
     then
        echo "Hello World"
     elif true
     then
        echo "Bug"
     else
       echo "Bee"
     fi


   # 例：
    if [ $1 -eq 0 ];then
      SUFFIX="Inter"
    elif [ $1 -eq 1 ];then 
    SUFFIX="Exter"
    else
    SUFFIX="Sdor"
    fi

   #注意：if与[之间，以及[ ]与值之间，以及值与运算符之间均有空格


   # 7.1
     #整数比较 

     #等于： if [ “$a” –eq “$b” ] 或者 if(( “$a” == “$b” ))

     #其他的以此类推

     #不等于 ： -ne   

    # 大于： -gt       

     #大于等于:  -ge  

     #小于:      -lt     

     #小于等于:    -le     


  # 文件测试
    # -e filename 	如果 filename 存在，则为真 	[ -e /var/log/syslog ]
    # -d filename 	如果 filename 为目录，则为真 	[ -d /tmp/mydir ]
    # -f filename 	如果 filename 为常规文件，则为真 	[ -f /usr/bin/grep ]
    # -L filename 	如果 filename 为符号链接，则为真 	[ -L /usr/bin/grep ]
    # -r filename 	如果 filename 可读，则为真 	[ -r /var/log/syslog ]
    # -w filename 	如果 filename 可写，则为真 	[ -w /var/mytmp.txt ]
    # -x filename 	如果 filename 可执行，则为真 	[ -x /usr/bin/grep ]
    # filename1 -nt filename2 	如果 filename1 比 filename2 新，则为真 	[ /tmp/install/etc/services -nt /etc/services ]
    # filename1 -ot filename2 	如果 filename1 比 filename2 旧，则为真



 # 字符串测试
   #-z string 	如果 string 长度为零，则为真 	[ -z "${myvar}" ]
   # -n string 	如果 string 长度非零，则为真 	[ -n "${myvar}" ]
   #string1 = string2 	如果 string1 与 string2 相同，则为真 	[ "${myvar}" = "abc" ]
  # string1 != string2 	如果 string1 与 string2 不同，则为真 	[ "${myvar}" != "abc" ]
   #string1 < string 	如果 string1 小于 string2，则为真 	[ "${myvar}" \< "abc" ]<br/>[[ "${myvar}" < "abc" ]]
   #string1 > string 	如果 string1 大于 string2，则为真 	[ "${myvar}" \> "abc" ]<br/>[[ "${myvar}" > "abc" ]]

     
  

    #注意：

        #在字符串两边加上""防止出错

       # <和>是字符串比较，不要错用成整数比较

        #如果是在[ ]中使用<和>，需要将它们写成\<和\>

   
     



#九：循环

   for each_file in `ls -l -R $rtvpath | grep rtv | awk -F ' ' '{print $9}'`
   do
      rtv_path=`find $rtvpath -name $each_file`  #find 会输出查找文件的完整的路径，所以rtv_path=/home/wbo/worksapcethe/Ts/uk/2017-02-21_T_16-36-25.009_GMT/2017-02-21_T_16-36-25.009_GMT.rtv
      rtv_name=`basename $rtv_path`    ##2017-02-21_T_16-36-25.009_GMT.rtv

   done

       # $ basename /tmp/test/file.txt
       #输出file.txt
       # $ basename /tmp/test/file.txt .txt
       # 输出file

      sign_oripath=`dirname $rtv_path`  
      # dirname取指定路径的目录部分




#十：函数

    ###### 函数定义 ######
    echo "函数定义";

   # 注意：所有函数在使用前必须定义。这意味着必须将函数放在脚本开始部分，直至shell解释器首次发现它时，才可以使用。调用函数仅使用其函数名即可。
function hello() {
    echo "Hello!";
}

function hello_param() {
    echo "Hello $1 !";
}
###### 函数调用 ######
# 函数调用
echo "函数调用";
hello;

###### 参数传递 ######
echo "函数传参调用";
hello_param ben;

###### 函数文件 ######
echo "函数文件调用";
# 调用函数文件，点和demo_call之间有个空格
. demo_call.sh;
# 调用函数
callFunction ben;



###### 参数读取 ######
echo "参数读取";

# 参数读取的方式和终端读取参数的方式一样
funWithParam(){
    echo "The value of the first parameter is $1 !"
    echo "The value of the second parameter is $2 !"
    echo "The value of the tenth parameter is $10 !"
    echo "The value of the tenth parameter is ${10} !"
    echo "The value of the eleventh parameter is ${11} !"
    echo "The amount of the parameters is $# !"
    echo "The string of the parameters is $* !"
}
funWithParam 1 2 3 4 5 6 7 8 9 34 73

###### 函数return ######
echo "函数return";

funWithReturn(){
    echo "The function is to get the sum of two numbers..."
    echo -n "Input first number: "
    read aNum
    echo -n "Input another number: "
    read anotherNum
    echo "The two numbers are $aNum and $anotherNum !"
    return $(($aNum+$anotherNum))
}
funWithReturn
# 函数返回值在调用该函数后通过 $? 来获得
echo "The sum of two numbers is $? !"
    






#十一：
   #重定向标准输出流(stdout)


    #标准输入流 	stdin 	程序读取的用户输入 	键盘输入 	/dev/stdin 	0
    #标准输出流 	stdout 	程序的打印的正常信息 	终端(terminal), 即显示器 	/dev/stdin 	1
    #标准错误流 	stderr 	程序的错误信息 	终端(terminal)，, 即显示器 	/dev/stderr 	2


    #cmd > file 	把 stdout 重定向到 file
    #cmd >> file 	把 stdout 追加到 file
    #cmd 2> file 	把 stderr 重定向到 file
    #cmd 2>> file 	把 stderr 追加到 file
    #cmd &> file 	把 stdout 和 stderr 重定向到 file
    #cmd > file 2>&1 	把 stdout 和 stderr 重定向到 file
    #cmd >> file 2>&1 	把 stdout 和 stderr 追加到 file
    #cmd <file >file2 cmd 	cmd 以 file 作为 stdin，以 file2 作为 stdout
    #cat <>file 	以读写的方式打开 file
    #cmd < file cmd 	cmd 命令以 file 文件作为 stdin


    #例：
      # 以下两种方式都会将`Hello World`写入到hello.txt(若不存在则创建)
        #echo "Hello World" > hello.txt   # hello.txt原有的将被覆盖
        #echo "Hello World" >> hello.txt  # hello.txt原有内容后追加`Hello World`



       
     # ${ts_cmd} --ivid $device_id --ivg $rtv_path --ic $camera_config --ip $ts_config --d $dir_name --ol ${dir_name}/log.out --of ${dir_name}/tf.out > cmd.log 2>&1


     #命令的结果可以通过“%>”的形式来定向输出，%表示文件描述符：1为标准输出stdout、2为标准错误stderr。系统默认%值是1，也就是“1>”，而1>可以简写为>，也就是默认为>

     #可以使用重定向操作符将命令输入和输出数据流从默认位置重定向到其他位置。输入或输出数据流的位置称为句柄。


     #重定向操作符 & 可以将输出或输入从一个指定句柄复制到另一个指定的句柄。例如，要将 dir 输出发送到 File.txt 并将错误输出发送到 File.txt，请键入：

     #dir>c:\file.txt 2>&1 




#十二：
     #--of ${T1_OUTPUT}${file%.*}.json   ：变量与字符串的拼接

    
  
     


    

   

   
  
     





 整数比较 

[]与值之间，以及值与运算符之间均有空格
等于	表达式：[ “$a” –eq “$b” ] 或者 if(( “$a” == “$b” ))
不等于	表达式：[ “$a” –ne “$b” ] 或者 if(( “$a” != “$b” ))
大于	表达式：[ “$a” –gt “$b” ] 或者 if(( “$a” > “$b” ))
大于等于	表达式：[ “$a” –ge “$b” ] 或者 if(( “$a” >= “$b” ))
小于	表达式：[ “$a” –lt “$b” ] 或者 if(( “$a” < “$b” ))
小于等于	表达式：[ “$a” –le “$b” ] 或者 if(( “$a” <= “$b” ))
数字加减乘除
a=1, b=2
+	expr $a + $b
-	expr $a - $b
*	expr $a * $b
/	expr $a / $b
小数	echo "scale=2;$a/$b"|bc
let	let a+=20；；或者let b = c*3
字符串比较 

大小的比较时按照ASCII顺序执行的
text1=nihao, text2=nihao2
=	[ "$text1" = "$text2" ] 或者  [[ "$text1" == "$text2" ]]
>	[ "$text1" > "$text2" ] 或者  [[ "$text1" > "$text2" ]]
<	[ "$text1" < "$text2" ] 或者  [[ "$text1" < "$text2" ]]
!=	[ "$text1" != "$text2" ]
empty	 -z $text1；；表示字符串长度为0
non-empty	-n $text1；；表示字符串长度为非0
正则表达式	[[ $text1 = n* ]]；表示text1是否是n开头的
[[ $text2 = "n*2" ]]：表示text1是否是n*2
同时读取多个文件

一般情况下，可以允许重定向数十个文件；当读取完行数最少的文件后，循环停止

exec 3<file1
exec 4<file2 
while read var1 <&3 && read var2 <&4
do
  echo $var1 $var2
done

set命令

用来修改命令行参数，注意：即使只是针对某一个参数进行修改，但是在使用该命令时，仍然要写完所有的参数，比如：

if [ ! "$1" = */ ];then
  set -- "$1""/" "$2"
fi
 
含义：如果"$1"不是以"/"结尾，则添加"/"，同时保持"$2"不变；如果不添加最后的"$2"，则命令行参数个数由2降为1，使得传入的"$2"无效

find命令

功能：主要是查找特定的文件/文件夹；与复合命令组合能快速的达到目标；比如：

find ./ -wholename '*dist/arm/lib/*' -exec cp {} ./arm-resources/arm-lib/ \;        将./下面所有以dist结尾的文件夹下面的/arm/lib/* 复制到 arm-resources/arm-lib里面 
find ./ -name targetfile -print0| xargs -0 mv -t targetdir       查找并移动目标文件到targetdir
find ./ -type f -name filename      只查找特定名字的文件；；-type d  查找特定的文件夹
find ./ -name filename1 -o -name filename2    查找filename1或者filename2
find ./ -maxdepth n 设置最大的查找层级为n    该参数紧跟在find之后，必须位于其他参数之前

sed命令

功能：流处理命令，可查找、替换、打印关注的内容；或者修改文件内容

sed -i "2c sedid=$ID" filename      修改第二行中sedid为指定值
sed 's:.*/\(.*\).jar$:\1:'          .*贪婪匹配到最后一个/前面；括号就是把里面匹配的内容获取到；最后那个\1就是把匹配到的内容替换当前行
sed 's/\(.*_cut[0-9]\).*/\1/g'      从符合条件的内容中截取()中的部分并替换原内容
sed 's/^/HEAD&/g' test.file         在每行的头添加字符，比如"HEAD"
sed 's/$/&TAIL/g' test.file         在每行的行尾添加字符，比如“TAIL”
sed 's/abc//g'                      将每行中的abc替换成空串
 
 
注意：一般情况下，sed使用"/"作为分隔符，但是如果使用的值中带有"/"时，sed命令会报错：unknown option to s；；此时只需要将sed中的分隔符改成其他字符就行，比如"|"

awk命令

 功能：流处理命令，主要用来打印关注的信息

ls -a | awk '/.*/&&$1 != "."&&$1 != ".."' | xargs rm -rf {}      删除除.和..之外的所有文件/文件夹
awk -F '[A|B]'   设置分隔符为A或者B；；如果需要指定的分隔符为[]，写法：-F '[][]'
awk -F "," '{print $3;if(NR>1){c=($3-a);print c;a=$3}}' test.txt     打印test.txt的第三个字段，并且打印它们之间的差值
awk '{print gensub(".rtv", "", $0)}'        将$0中的".rtv"替换成空串，并打印
awk '{print substr($0, 0, 20)}'             打印将$0中的前20个字符

SSH命令

cat ~/.ssh/id_rsa.pub | ssh username@IP "cat >> ~/.ssh/authorized_keys"  将自己的key（id_rsa.pub）追加到server上的authorized_keys中
ssh test@10.69.141.4 "sed -i \"s/xx/yy/g\" ~/test.txt"   修改server路径~/test.txt中的内容，将xx替换成yy
echo `ssh test@IP1 "cat ~/test.txt"` | ssh test@IP2 "cat >> ~/test.txt"    可以将IP1路径~/test.txt中的内容追加到1P2路径~/test.txt中；前提：需要将本机的key提前添加到IP1和IP2
ssh test@10.69.141.4 'for var in `cat test.txt`;do echo $var;done'         ssh中使用循环的简单示例
ssh -o "StrictHostKeyChecking no" roaddb@ip -p 22    连接主机时不进行秘钥确认，也就是默认秘钥被认证了

sort命令

 功能：对数据排序，支持：数字、字符等各种形式

echo $a | sed 's/PRE //g' | sed 's/\///g'| tr ' ' '\n' | sort -t. -nk 3 | grep -E "^[0-9][0-9][0-9][0-9].*"   将a值中的PRE 和/删除，然后将空格替换成\n(为了后续的sort命令）然后再排序，过滤
cat test.txt | grep -E "^[0-9][0-9.]*[0-9]$" | sort -t. -k 1nr,1 -k 2nr,2 -k 3nr,3 -k 4nr,4   先过滤test.txt中的文本并分段；先将第一个字段按照数字倒序排列，再按照第二个字段倒序排列，依次类推
sort -k 2               表示使用第二个字段开始的字符与行尾之间的字符来排序
sort -k 2,2             表示只以第二个字段来排序
sort -k 2,2 -k 3,3      表示先以第二个字段排序，再以第三个字段排序

EOF命令

形式

command <<EOF
  subcommand
EOF

功能：将subcommand以标准输入的形式输入到交互式程序中，也可以用于在远程环境上执行命令；；复合命令中经常使用；比如：

value=`cat test.txt`
ssh test@10.69.141.4 <<eof
  echo "$value" > nihao.txt
eof


将本地test.txt的内容写入远端的nihao.txt中

注意：

   1）在EOF里不能touch文件，但可以创建文件夹。

   2）在EOF里不能定义变量，只能使用已定义的变量。

   3）在EOF里不能使用for循环
grep命令

grep -s -rn -I "WRONG TSR RETURN"  *   可以查找相关路径下面的log里面哪些log出现了你需要找的错误的信息
grep -E "^[0-9][0-9][0-9][0-9].*" filename   打印filename中符合正则表达式的行
grep context filename            打印filename中包含的context行
grep -vwf file1 file2            统计file1中没有，file2中有的行

expect命令

功能：可以用来处理交互，实现自动化。需要安装expect : pip install expect，执行的命令和shell不同，而是expect xxx.sh。

示例：（用来本地远程登录22主机，执行文件夹中py脚本对aws主机进行关机开机操作，免输入密码一键执行）

xxxx.sh
 
#!/usr/bin/expect -f   
set timeout 20
set host "10.69.130.22"
set username "user"    #设置用户名
set password "xxx"      #设置密码
set operation [lindex $argv 0]    #可以读取多个输入参数

spawn ssh $username@$host
expect "password"     
send "$password\n"
expect "*roaddb@*"
send "cd /home/roaddb/merge_tmp_html_yingtan/aws\r"
expect "*aws"
send "python operation_instance_id.py XXXXX $operation\r"
#interact    如果需要命令操作完成后停留在远端主机，可以加上这个命令
expect eof


>>> expect xxx.sh start    

   
       
    
    










  



























           

















# sign_num=`awk '{print NR}' ${sign_file_dir}/*.signs | tail -n1 ` 计算文档的行数

