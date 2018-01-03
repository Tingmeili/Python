#!/usr/bin/env python
# encoding: utf-8
'''
fix server,device and domin
@author: Chao Wang
'''

import re
from multiprocessing import Pool
from tools.common import ssh_exec_command
import videomap.videocenter_log as logging
from tools import common
import time

def _read_host(file_path):
    '''
    @summary: read source file content
    @param file_path:absoluted file path
    @return: return string content of file
    '''
    content = "NULL"
    with open(file_path, 'r') as fopen:
        content = fopen.read()
    logging.info("Read source content of host.ini")
    return content

def _fix_server_host(source_content, server, host, dns=""):
    '''
    @summary: fix server's host in content
    @param source_content:source string content that will be fixed
    @param server:server in content that will be replaced with new value
    @param host:new value will be given to server
    @return: fixed content
    '''
    if str(server) == "cloud-server":
        pattern_new_version = str(server) + r"\s*ansible_host\s*=\s*\d*\.\d*\.\d*\.\d*\s*domin=\".*\""
        pattern_old_version = str(server) + r"\s*ansible_host\s*=\s*\d*\.\d*\.\d*\.\d*"

        if re.search(pattern_new_version, source_content):
            latest_value = "{0} ansible_host={1} domin=\"{2}\"".format(str(server), str(host), str(dns))
            pattern = pattern_new_version

        elif re.search(pattern_old_version, source_content):
            latest_value = "{0} ansible_host={1}".format(str(server), str(host))
            pattern = pattern_old_version
            source_content = _fix_var_value(source_content, 'MQTT_HOST', str(dns))

    elif str(server) == "backend-server":
        pattern = str(server) + r"\s*ansible_host\s*=\s*\d*\.\d*\.\d*\.\d*"
        latest_value = "{0} ansible_host={1}".format(str(server), str(host))
    logging.info("set {0} is {1}".format(server, latest_value))

    return re.sub(pattern, latest_value, source_content)

def _fix_var_value(source_content, var, value):
    '''
    @summary: fix var's value in content
    @param source_content:source string content that will be fixed
    @param var:var in content that will be replaced with new value
    @param value:new value will be given to var
    @return: fixed content
    '''
    pattern = str(var) + r"\s*=\s*.*\n*?"
    latest_value = "{0}=\"{1}\"".format(str(var), str(value))
    logging.info("set {0} is {1}".format(var, value))

    return re.sub(pattern, latest_value, source_content)

def _set_all_device(source_content, device_domain, ansible_host, ansible_user="roaddb"):
    '''
    @summary: set all device information in source content
    @param device_domain:list of device domain
    @param ansible_host:list of device ip
    @param ansible_user:string of ansible user
    @return: fixed content
    '''
    if len(device_domain) == len(ansible_host):

        all_device = '[device]\n'
        for i in range(len(device_domain)):
            each_device = "{0} ansible_host={1} ansible_connection=local ansible_user={2} ansible_ssh_port=22 \n".format("device_" + str(device_domain[i]), ansible_host[i], ansible_user)
            all_device = all_device + each_device
        all_device = all_device + "\n[all:vars]\n"

        pattern_device = re.compile(r"\[device\].*\[all\:vars\]", flags=re.DOTALL)
        pattern_no_device = re.compile(r"\[all\:vars\]", flags=re.DOTALL)

        pattern = (pattern_device if re.search(pattern_device, source_content) else pattern_no_device)
        logging.info("set device is {0}".format(all_device))

        return pattern.sub(all_device, source_content)

    else:
        logging.error("Device information is not completed,please set again")

    logging.info("set device information is {1}".format())

def create_divid_envir(envir):
    '''
    @summary: create divided envir list by divid_num
    @param envir:dict of envirment information like {'cloud_ip':[],'backend_ip':[],'device_ip':[]}
    @return: the list of the envir
    '''
    need_keys = ['cloud_ip', 'backend_ip', 'device_ip', 'cloud_domin']
    if set(envir.keys()) == set(need_keys):
        device_list = envir['device_ip']
        divid_num = 6
        divid_device_list = _divid_devices(device_list, divid_num)
        envir_list = []
        for device in divid_device_list:
            new_envir = {}
            new_envir['cloud_domin'] = envir['cloud_domin']
            new_envir['cloud_ip'] = envir['cloud_ip']
            new_envir['backend_ip'] = envir['backend_ip']
            new_envir['device_ip'] = device
            envir_list.append(new_envir)
        return envir_list
    else:
        logging.error("Environment is error,please given like {0}".format(need_keys))

def _divid_devices(device_list, divid_num):
    '''
    @summary: divid the devices by divid number
    @param device_list:the list of the device
    @param divid_num:the divid number
    @return: the list of divided devices like [[],[]]
    '''
    return [device_list[i:i + divid_num] for i in range(len(device_list)) if i % divid_num == 0]

def fix_host_all(envir, host_path, goal_path, suffix):
    '''
    @summary: set deploy environment information in source content
    @param host_path:absoluted path of host.ini
    @param goal_path:last location of latest host.ini
    @param envir:dict of envirment information like {'cloud_domin':[],'backend_domin':[],'device_domin':[]}
    @param suffix:the suffix of the host.ini
    @return: fixed content
    '''
    need_keys = ['cloud_domin', 'cloud_ip', 'backend_ip', 'device_ip']

    if set(envir.keys()) == set(need_keys):
        source_content = _read_host(host_path.rstrip("/") + '/hosts.ini')

        after_cloud = _fix_server_host(source_content, 'cloud-server', envir['cloud_ip'][0], dns=envir['cloud_domin'][0])

        after_backend = _fix_server_host(after_cloud, 'backend-server', envir['backend_ip'][0])

        after_set_device = _set_all_device(after_backend, envir['device_ip'], envir['device_ip'])

        after_set_device = after_set_device.replace("ansible_connection=local", "")
        with open(goal_path.rstrip("/") + '/hosts_{0}.ini'.format(suffix), "w") as fopen:
            fopen.write(after_set_device)
    else:
        logging.error("Environment is error,please given like {0}".format(need_keys))

def tranfer_hostini(locate_machine, remote_path, local_path, envir, index):
    '''
    @summary: update hosts.ini
    @param locate_machine:backend server ip
    @param remote_path:backend server's host.ini absoluted path
    @param local_path:local absoluted path to locate hosts.ini
    @param envir:detailed environment information
    '''
    remote_path = remote_path.rstrip("/")
    local_path = local_path.rstrip("/")

    fix_host_all(envir, local_path, local_path, index)

def start_ansible(request, locate_machine, host_path, yml_path, envir_list):
    '''
    @summary: start to deploy packages
    @param locate_machine:the machine which will execute cmd
    @param host_path:absoluted path of hosts.ini
    @param yml_path:absoluted path of *.yml
    @param envir_list:the list of detailed environment information
    @return: the status of the ansible
    '''
    host_path = host_path.rstrip("/")
    yml_path = yml_path.rstrip("/")

    # create deploy backend process
    common.logging_and_send_websocket(request, "Start to deploy backend")
    backend_status = _deploy_backend(host_path, yml_path, locate_machine)
    common.logging_and_send_websocket(request, "Backend Deploy Status {0}".format(('success' if backend_status == 0 else 'fail')))

    # create deploy cloud process
    common.logging_and_send_websocket(request, "Start to deploy cloud")
    cloud_status = _deploy_cloud(host_path, yml_path, locate_machine)
    common.logging_and_send_websocket(request, "Cloud Deploy Status {0}".format(('success' if cloud_status == 0 else 'fail')))

    # create deploy device process pool
    device_status = deploy_device(request, locate_machine, host_path, yml_path, envir_list)

    return backend_status, cloud_status, device_status

def deploy_device(request, locate_machine, host_path, yml_path, envir_list):
    '''
    @summary: start to deploy device
    @param locate_machine:the machine which will execute cmd
    @param host_path:absoluted path of hosts.ini
    @param yml_path:absoluted path of *.yml
    @param envir_list:the list of detailed environment information
    @return: the status of the ansible
    '''
    device_status = 0
    results = []
    pool = Pool(processes=len(envir_list))
    # deploy by mutiple process
    for index, item in enumerate(envir_list):
        results.append(pool.apply_async(_deploy_device, (host_path, yml_path, len(item), index, locate_machine,)))
    pool.close()
    common.logging_and_send_websocket(request, "Start to deploy device")
    pool.join()
    # get deploy status of result
    for result in results:
        logging.debug("result.get() : {0}".format(result.get()))
        device_status += result.get()
    common.logging_and_send_websocket(request, "Device Deploy Status {0}".format(('success' if device_status == 0 else 'fail')))

    return device_status

def _deploy_backend(host_path, yml_path, locate_machine):
    '''
    @summary: start to deploy device
    @param locate_machine:the machine which will execute cmd
    @param host_path:absoluted path of hosts.ini
    @param yml_path:absoluted path of *.yml
    @return: the status of the ansible
    '''
    deploy_backend = "ansible-playbook -i {0}/hosts_0.ini {1}/deploy_backend.yml {1}/deploy_rdb_tool.yml".format(host_path, yml_path)
    _, outtext = ssh_exec_command(locate_machine, deploy_backend)
    backend_status = check_deploy_status(outtext, "backend-server")

    logging.debug("backend check_deploy_status : {0}".format(backend_status))

    return backend_status

def _deploy_cloud(host_path, yml_path, locate_machine):
    '''
    @summary: start to deploy device
    @param locate_machine:the machine which will execute cmd
    @param host_path:absoluted path of hosts.ini
    @param yml_path:absoluted path of *.yml
    @return: the status of the ansible
    '''
    deploy_cloud = "ansible-playbook -i {0}/hosts_0.ini {1}/deploy_cloud.yml".format(host_path, yml_path)
    _, outtext = ssh_exec_command(locate_machine, deploy_cloud)
    cloud_status = check_deploy_status(outtext, "cloud-server")
    logging.debug("cloud check_deploy_status : {0}".format(cloud_status))

    return cloud_status

def _deploy_device(host_path, yml_path, devive_count, index, locate_machine):
    '''
    @summary: the process function to deploy devices
    @param host_path:absoluted path of hosts.ini
    @param yml_path:absoluted path of *.yml
    @param devive_count:the count of the devices
    @param index:the index of the envir list
    @param locate_machine:the machine which will execute cmd
    '''

    deploy_device = "ansible-playbook -i {0}/hosts_{3}.ini {1}/deploy_device_ygo_deb.yml -f {2}".format(host_path, yml_path, devive_count, index)
    time.sleep(int(index))
    _, outtext = ssh_exec_command(locate_machine, deploy_device)

    return check_deploy_status(outtext, "device")

def skip_ansible_confirm(local, remote):
    '''
    @summary: skip ansible confirm
    @param local:backend machine
    @param remote:remote machine
    '''
    for item in remote:
        # remove the device host name from backend known_hosts
        cmd = "ssh-keygen -f /home/roaddb/.ssh/known_hosts -R {0};ssh -o StrictHostKeychecking=no roaddb@{0} pwd".format(item)
        ssh_exec_command(local, cmd)

def check_deploy_status(outtext, type):
    '''
    @summary: check deploy status
    @param outtext:string of ansible command
    @return: 0 success,1 fail
    '''
    all_status = []
    if type == "cloud-server":
        cloud = re.search("cloud-server.*unreachable\s*=\s*0.*failed\s*=\s*0", outtext)
        all_status.append((True if cloud else False))
    elif type == "backend-server":
        backend = re.search("backend-server.*unreachable\s*=\s*0.*failed\s*=|s*0", outtext)
        all_status.append((True if backend else False))
    elif type == "device":
        device_false = re.search("device.*unreachable\s*=\s*1 | .*failed\s*=\s*[1-9]\d*", outtext)
        device_true = re.search("device.*unreachable\s*=\s*0.*failed\s*=\s*0", outtext)
        all_status.append((True if (not device_false and device_true) else False))

    if len(all_status) != 0 and (False not in all_status):
        logging.debug("{0} deployment success".format(type))
        return 0
    else:
        logging.error("{0} deployment fail".format(type))
        return 1

if __name__ == '__main__':
    pass

