#!/bin/sh


#针对tsdver1.0的检测log
#ver1.0和2.0代表是要对比的两套不一样的代码，不是traffic sign检测的版本
# 统计ver1.0的时候运行：./TS_statistic_1.0.sh /home/test/Documents/TS_code/core/test_uk_1.0 /home/test/Documents/traffisign/workspace/TS_sta_1.csv
# 统计ver2.0的时候运行：./TS_statistic_1.0.sh /home/test/Documents/SDOR/workspace/test_06_22/log/test  /home/test/Documents/SDOR/workspace/TS_sta_2.csv
#test就是我们批量跑traffic sign生成的test文件
#将.py文件跟该文件放在一个目录
#结果生成在demo.xlsx


if [[ $# != 2 ]]
then
	echo "cmd logfilepath statisticfilepath"
	exit
else
	log_file_path=$1
	statistic_file_path=$2
fi


echo "RTV_name,ROI_num,Track_num,recognized_num,recognized_track_ID,recognized_types,sign_num,classifyRoi_Totaltime,classifyRoi_Called,classifyRoi_Avgtime,detectSingleFrame_Totaltime,detectSingleFrame_Called,detectSingleFrame_Avgtime,trackSegTS_Totaltime,trackSegTS_Called,trackSegTS_Avgtime,Total_Time(ms)" >> ${statistic_file_path}
Track_num=0
sign_num=0
xml_name="xml_result"
sign_name="signs_result"
for each_folder in `ls ${log_file_path}`
do
	#echo "xml_name:" $xml_name
	#echo "each_folder:" $each_folder
	if [[ ${each_folder} != ${xml_name} ]] && [[ ${each_folder} != ${sign_name} ]]
	then
		log_path=$log_file_path/$each_folder
		#echo "log_path:" $log_path
		rtv_name=`grep "Input Params" ${log_path}"/"log.* | awk -F ',' '{print $2}' | awk -F '/' '{print $(NF)}'`
		echo "rtv_name:" $rtv_name

		#ROI_num=`grep "begin to track" ${log_path}"/"log.* | awk -F ',' '{print $2}' | awk -F ':' '{print $2}' | awk -F ' ' '{print $1}'`
		#echo "ROI_num:" $ROI_num

		#Track_fail_num=`grep -o 'recognize failed' ${log_path}"/"log.* | wc -l`
		#echo "Track_fail_num:" $Track_fail_num


		Track_num=`grep -o 'push new TrackID' ${log_path}"/"log.* | wc -l`
		#echo "Track_success_num:" $Track_success_num

		#Track_num=`expr $Track_fail_num + $Track_success_num`
		echo "Track_num:" $Track_num

		recognized_num=`grep -o 'snippet' ${log_path}"/"log.* | wc -l`
		recognized_num=`expr $recognized_num - 1`
		echo "recognized_num:" $recognized_num


		
		Total_Time=`grep "Module TS" ${log_path}"/"log.* | awk -F ':' '{print $2}'`
		#Total_Time=`sed ':a;N;$!ba;s/\n/ /g' ${Total_Time}`
		echo "Total_Time:" $Total_Time
		
		classifyRoi_Totaltime=`grep "classifyRoi" ${log_path}"/"log.* | awk -F ' ' '{print $2}' `
		classifyRoi_Called=`grep "classifyRoi" ${log_path}"/"log.* | awk -F ' ' '{print $3}' `
		classifyRoi_Avgtime=`grep "classifyRoi" ${log_path}"/"log.* | awk -F ' ' '{print $4}' `

		detectSingleFrame_Totaltime=`grep "detectTS:" ${log_path}"/"log.* | awk -F ' ' '{print $2}' `
		detectSingleFrame_Called=`grep "detectTS:" ${log_path}"/"log.* | awk -F ' ' '{print $3}' `
		detectSingleFrame_Avgtime=`grep "detectTS:" ${log_path}"/"log.* | awk -F ' ' '{print $4}' `


		trackSegTS_Totaltime=`grep "assignToTracks" ${log_path}"/"log.* | awk -F ' ' '{print $2}' `
		trackSegTS_Called=`grep "assignToTracks" ${log_path}"/"log.* | awk -F ' ' '{print $3}' `
		trackSegTS_Avgtime=`grep "assignToTracks" ${log_path}"/"log.* | awk -F ' ' '{print $4}' `


	
		
		
	fi
	sign_dir=$log_file_path/${sign_name}
	#echo "sign_dir:"${sign_dir}
	for sign_file in `ls ${sign_dir} `
	do
		if [[ ${sign_file} == ${each_folder} ]]
		then
			sign_file_dir=${sign_dir}/${sign_file}
			#echo "sign_file_dir:"${sign_file_dir}
			chmod +x ${sign_file_dir}/*
			sign_num=`awk '{print NR}' ${sign_file_dir}/*.signs | tail -n1 `
			#sign_num='"'${sign_num}'"' 
			echo "sign_num:" ${sign_num}
		
		fi


	done
	#$ROI_num=0
	#$recognized_track_ID=0
	#$recognized_types=0
    if [[ ${each_folder} != ${xml_name} ]] && [[ ${each_folder} != ${sign_name} ]]
    then
	    echo  "$rtv_name,$ROI_num,$Track_num,$recognized_num,$recognized_track_ID,$recognized_types,${sign_num},$classifyRoi_Totaltime,$classifyRoi_Called,$classifyRoi_Avgtime,$detectSingleFrame_Totaltime,$detectSingleFrame_Called,$detectSingleFrame_Avgtime,$trackSegTS_Totaltime,$trackSegTS_Called,$trackSegTS_Avgtime,$Total_Time" >> ${statistic_file_path}
    fi
    Total_sign_num=`expr $Total_sign_num + $sign_num`
    #cho "tatal:"$Total_sign_num
    Total_recognized_num=`expr $Total_recognized_num + $recognized_num`    
	sign_num=0
done
echo "Total_sign_num:"$Total_sign_num
echo "Total_recognized_num:"$Total_recognized_num
chmod +x ./TS_sta_1.csv
csv_name=`basename ${statistic_file_path}`
if [ $csv_name == 'TS_sta_1.csv' ]
then
	python ./python_excel.py 1 TS_sta_1.csv
else
	python ./python_excel.py 2 TS_sta_2.csv

fi 













