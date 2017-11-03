#!/bin/bash

if [[ $# < 1 ]]; then
        echo -e "Usage: $0 \033[33m mode\033[0m \033[36m[all]\033[0m"
	echo "Mode 0: internal"
        echo "Mode 1: external"
        echo "Mode 2: sdor"
	echo "when \"all\" is set (to any value) this script will backup more files"
        exit 1
fi

if [ $1 -eq 0 ];then
    SUFFIX="Inter"
elif [ $1 -eq 1 ];then 
    SUFFIX="Exter"
else
    SUFFIX="Sdor"
fi

if [[ $# > 1 ]]
then
    BAK_MORE_FLAG=1
    SUFFIX=${SUFFIX}_VERBOSE
fi

echo "SUFFIX of backup folder is "${SUFFIX}
DATE=`date +%Y-%m-%d-%H-%M-%S`
IP_ADDRESS=`ifconfig | grep "10.69" | awk -F '[: ]' '{print $13}'`
DATE_AND_TIME=${DATE}@${IP_ADDRESS}_${SUFFIX}
DBFILE_DIR=/opt/ygomi/roadDB/file_storage/WorkflowManager
mkdir $DATE_AND_TIME

echo -e "\033[32mstart to backup server results\033[0m"

cp -rf ${DBFILE_DIR}/backendDB/ $DATE_AND_TIME
cp -rf ${DBFILE_DIR}/vehicleDB/ $DATE_AND_TIME
cp -rf ${DBFILE_DIR}/logicDB/ $DATE_AND_TIME
cp -rf ${DBFILE_DIR}/mergeDB/ $DATE_AND_TIME
cp -rf ${DBFILE_DIR}/../log $DATE_AND_TIME

#make another copy of backenddb and then delete some tables from it
cp -rf ${DBFILE_DIR}/backendDB/ $DATE_AND_TIME/backendDB_after_delete
backendDBList=`find $DATE_AND_TIME/backendDB_after_delete -name *.db`

for dbfile in ${backendDBList}
do
    BASE_DB_NAME=`basename $dbfile`
    SEG_ID=`echo ${BASE_DB_NAME} | awk -F"[_.]" '{print $2}'`
    #echo "Found DB: "${BASE_DB_NAME}
    sqlite3 $dbfile "delete from Reference_${SEG_ID};"
    TBL_EXIST=`sqlite3 $dbfile "SELECT count(*) FROM sqlite_master WHERE type='table' AND name='RoadGeometry_${SEG_ID}'"`
    if [[ ${TBL_EXIST} == 1 ]];then
        sqlite3 $dbfile "delete from RoadGeometry_${SEG_ID};"
    fi
    sqlite3 $dbfile "update DBVersion set VERSION = 106;"
done


if [ -n "${BAK_MORE_FLAG}" ];then
    echo -e "\033[32mBackup uploads and all input files\033[0m"
    cp -rf ${DBFILE_DIR}/../events/uploads $DATE_AND_TIME
    cp -rf ${DBFILE_DIR}/../../work_path/WorkflowManager $DATE_AND_TIME
fi

echo -e "\033[32mstart to backup mysql data\033[0m"
mysqldump -udba -pmysql history processing_files processing_reports references > ${DATE_AND_TIME}/history_backup.sql

#echo -e "\033[32mstart to backup vehicleUpload files\033[0m"
#mkdir -p ${DATE_AND_TIME}/vehicleUpload
#find ${DBFILE_DIR}/../events/uploads  -regex ".*[kf|sp|sdor]\.out.*"  -exec cp {} ${DATE_AND_TIME}/snippets \;
#cp -rf ${DBFILE_DIR}/../events/uploads ${DATE_AND_TIME}/vehicleUpload
#tar zcvf ${DATE_AND_TIME}/vehicleUpload.tar.gz ${DATE_AND_TIME}/vehicleUpload
#rm -rf ${DATE_AND_TIME}/vehicleUpload
echo -e "\033[32msend data to backup server\033[0m"

tar zcvf pack_${DATE_AND_TIME}.tar.gz $DATE_AND_TIME
#scp -P 22 pack_${DATE_AND_TIME}.tar.gz roaddb@10.69.141.184:/media/psf/Untitled/systemTestReport
#scp -P 22 -r ${DATE_AND_TIME} roaddb@10.69.141.184:/media/psf/Untitled/systemTestReport

if [[ $? -eq 0 ]]; then
	echo -e "\033[32mfile transfer over\033[0m"
        rm -rf $DATE_AND_TIME
        #rm -rf pack_${DATE_AND_TIME}.tar.gz
        touch ${DATE_AND_TIME}/${DATE}.log
else 
	echo "delete the tmp file!!!"
fi


