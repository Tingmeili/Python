#!/usr/bin/env python
# encoding: utf-8
'''
Configration file for E2E Test tool

Created on Nov 6, 2017
@author: Hongping Wang
@change: Nov 6, 2017 Hongping Wang: initialization
'''
#===============================================================================
# User Settings
#===============================================================================
# set every server IP address
SERVER_IP_ADDRESS = ['10.72.22.176']
CLOUD_IP_ADDRESS = ['10.72.22.118', ]
VEHICLE_IP_ADDRESS = ['10.72.20.136', '10.72.20.150']

# set traffic sign nation abbreviate. if value equal None or '', use SignConfig.json, otherwise use SignConfig_xx.json
# support 'de','de_v1','de_v2','jp','jp_v1','jp_v2','uk','uk_v1','uk_v2','us','us_v1','us_v2'
SIGN_NATION_ABBREVIATE = 'us_v2'

# set the directories which save RTV & IMU & GPD files
# those files will be distributed to all vehicle for run SLAM test
# if not found the GPS or IMU matching RTV, the tool will create a empty file
ORG_SERVER_RTV_DIR = '/home/roaddb/largeScaleTest/rtv'
ORG_SERVER_GPS_DIR = '/home/roaddb/largeScaleTest/rtv'
ORG_SERVER_IMU_DIR = '/home/roaddb/largeScaleTest/rtv'

# set the tag which is mean run or not run SLAM test. True: stop, False: not stop
RUN_SLAM_TEST = True

# set the tag which is mean run or not run Alignment test. True: stop, False: not stop
RUN_ALIGNMENT_TEST = True
ALIGNMENT_ROUND_NUMBER = 2  # how many rounds of running Alignment
# Increment RTV files in each Alignment round. example: ['/home/roaddb/dengshuang/rtv_128', '/home/roaddb/dengshuang/rtv_128']
# if no increment, set to []
INCR_RTV_DIR = []
INCR_GPS_DIR = []  # Increment GPS files in each Alignment round. if no increment, set to []
INCR_IMU_DIR = []  # Increment IMU files in each Alignment round. if no increment, set to []

# set the tag which is mean run or not run Sdor test. True: stop, False: not stop
RUN_SDOR_TEST = True

# if the gps or imu file not exist, whether create a empty one
CREATE_EMPTY_IMU = False
CREATE_EMPTY_GPS = True

# set the directory which save other external tools deb package, e.g. DB2KML
OTHERS_TOOL_DIR = '/home/roaddb/road_deployment'

# skeleton file path. not support now
# java -jar target/offline-tool-backendDB-import.jar  --skeleton-dir <skeleton dir>
IMPORT_SKELETON = False
SKELETON_FOLDER = 'http://10.69.130.22/public/debug_section_db/VW_debug_sectionDB_026.zip'  # http url or folder
IM_SKELETON_TOOL = '/opt/ygomi/roadDB/jar/cmd/offline-tool-backendDB-import.jar'

#===============================================================================
# Advance Settings, not recommend to change
#===============================================================================
# set the directories which save RTV & IMU & GPD files in vehicle.
# this folder cannot in ('', '/', '/bin', '/usr', '/sbin', '~')
DIVICE_MEDIA_DIR = '/home/roaddb/test_media'

# set the directories which will be clean when execute clean operation.
# this folder cannot in ('', '/', '/bin', '/usr', '/sbin', '~')
INIT_CLEAN_SERVER_DIR = ['/opt/ygomi/roadDB/file_storage/events/uploads',
                         '/opt/ygomi/roadDB/file_storage/log',
                         '/opt/ygomi/roadDB/file_storage/WorkflowManager/vehicleDB',
                         '/opt/ygomi/roadDB/file_storage/WorkflowManager/unzip',
                         '/opt/ygomi/roadDB/file_storage/WorkflowManager/reference',
                         '/opt/ygomi/roadDB/file_storage/WorkflowManager/logicDB']
INIT_CLEAN_VEHICLE_CMD = ['sudo service road_probe stop',
                          'sudo rm -rf /opt/ygomi/roadDB/etc/loc_seg_db_dir_0/*',
                          'sudo rm -rf /opt/ygomi/roadDB/etc/loc_seg_db_dir_1/*',
                          'sudo sqlite3 /opt/ygomi/roadDB/etc/settings.db "delete from download_tasks_status"',
                          'sudo rm -rf /opt/ygomi/roadDB/etc/ver_db.db',
                          'sudo service road_probe start']
INIT_INSTALL_SERVER_DB_PKGS = ['{0}/roles/common/files/mysqlbridge/rdb-db-*.deb'.format(OTHERS_TOOL_DIR)]

# RTV distribute type. 1: order average, 2: reverse order average (not support)
RTV_DISTRIBUTE_TYPE = 1

# Vehicle process timeout, unit is second
VEHICLE_PROCESS_TIMEOUT = 3600 * 20

# Server process timeout, unit is second
SERVER_PROCESS_TIMEOUT = 3600 * 2

# set the tag which is mean stop or not stop Workflowmanager. True: stop, False: not stop
STOP_WORKFLOWMANAGER_TAG = True

# set the directory which save other external tools, e.g. DB2KML
TOOLS_PATH = '/opt/ygomi/roadDB/tool'

# all database and output files save into this directory. it is must be absolute path
BASE_DIR = '/home/roaddb/e2etest_result'

# set MySQL server informatin
MYSQL_IP_ADDRESS = 'localhost'
MYSQL_PORT = 3306  # must integer
MYSQL_USERNAME = 'dba'
MYSQL_PASSWORD = 'mysql'

VEHICLE_VEHICLE_DB_DIR = '/opt/ygomi/roadDB/etc'
SERVER_VEHICLE_DB_DIR = '/opt/ygomi/roadDB/file_storage/WorkflowManager/vehicleDB'
VEHICLE_DB_TOOL = '/opt/ygomi/roadDB/jar/cmd/rdb-server-vehicleDBGenerate-cmd.jar'
SEGMENT_CONFIG = '/usr/local/ygomi/roadDB/algo_res/SegmentConfig.json'
MODE_FILE = '/opt/ygomi/roadDB/etc/config/rdb-server-workflow-manager.yml'
SERVER_MODE = {'full':0,  # 0  normal,run all
                'iteration':1,  # 1(internal_optimization)  only run T2.0,T2.1,T2.2;
                'section':2,  # 2(external_optimization)  only run T2.15,T2.2;
                'sdor':3,  # 3(sdor)  only run T2.0',T3;
                }

STOP_SERVER_OS_AFTER_TEST = True
STOP_CLOUD_OS_AFTER_TEST = True
STOP_DEVICE_OS_AFTER_TEST = True

STOP_OS_DELAY_TIME = 15  # unit is minute
WAIT_T2_2_TIME = 10  # unit is minute
WAIT_VEHICLE_DOWNLOAD_TIME = 600  # unit is second

MAX_SEND_FILE_THREAD = 5  # send rtv files with thread
MAX_SEND_FILE_TIME = 600  # unit is second

if __name__ == '__main__':
    pass
