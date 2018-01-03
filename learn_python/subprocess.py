import subprocess



def execute_command_in_local(self, cmd, shell=True, no_return=False):
        '''
        @summary: execute command in local host, and return the execution result
        @param cmd: string of the command
        @param shell: whether run the command in shell mode
        '''
        logging.info("Start to execute cmd: {0}".format(cmd))
        if no_return:
            return os.system(cmd), ''
        command_pipe = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=shell)
        logging.debug("has send cmd: {0}".format(cmd))
        command_pipe.wait()
        #1. Popen对象创建后，主程序不会自动等待子进程完成。
         #  我们必须调用对象的wait()方法，父进程才会等待 (也就是阻塞block)
        logging.debug("finished cmd: {0}".format(cmd))
        command_return = command_pipe.stdout.read()
        command_return_code = command_pipe.returncode
        logging.info("end execution, cmd: {0}. return code: {1}".format(cmd, command_pipe.returncode))
        logging.debug("return: {0}".format(command_return))

        return command_return_code, command_return


python中subprocess:
        subprocess的popen函数：

        subprocess包含了所有的跟进程有关的操作，subprocess.Popen用来创建新的进程。
        
        subprocess.Popen(args, bufsize=0, executable=None, stdin=None,
        stdout=None, stderr=None, preexec_fn=None, close_fds=False,
        shell=False, cwd=None, env=None, universal_newlines=False,
        startupinfo=None, creationflags=0
        )      
     
       
     参数说明： 
         1. shell参数：

         当shell=True时，表示在系统默认的shell环境中执行新的进程，此shell在windows表示为cmd.exe，在linux为/bin/sh。 
         
         2.executable参数：

          当指定shell=True时，executable用来修改默认的shell环境，比如executable='/bin/bash' 
          
        3.  stdin，stdout，stderr参数：

默认地stdin，stdout，stderr均为None，此时表示此新进程的stdin，stdout，stderr均为默认，从keyboard获得输入，将输出和错误输出到display。如果stdin设置为PIPE，此时的stdin其实是个file对象，用来提供输入到新创建的子进程；如果stdout设置为PIPE，此时stdout其实是个file对象，用来保存新创建的子进程的输出；如果stderr设置为PIPE，此时的stderr其实是个file对象，用来保存新创建的子进程的错误输出。         
     


         
