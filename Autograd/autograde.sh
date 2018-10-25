#!/bin/bash
# RUN: ./autograde.sh users.txt log.txt scores.txt ./data ./sandbox ./submissions
infile=$1
logfile=$2
scorefile=$3
data_dir=$4
sandbox_dir=$5
submissions_dir=$6
echo -e "ENTRY_NUM,Score,TIME,PEN_ZIP,PEN_FILENAME" > $scorefile
echo -e "Autograding...." > $logfile
while read entry_num; do 
    #Check if user submitted the correct file
    echo -e "Evaluating: ${entry_num}"
    user_score=""
    echo -e "Evaluating: ${entry_num}" >> $logfile
    if [ -f  "${submissions_dir}/${entry_num}.zip" ] || [ -f  "${submissions_dir}/${entry_num}.rar" ]; then
        echo "File found" >> $logfile
        #If correct zip file exist
        #Run for allowed time
        time_start=$(date +%s)
        timeout -k 1500s 1500s ./evaluate.sh $data_dir $sandbox_dir $entry_num $submissions_dir >> $logfile
        status=$?
        time_end=$(date +%s)
        user_time=$(( time_end - time_start ))
        if [ $status == 124 ]; then
            echo -e "Status: Timed out!" >> $logfile
        else
            echo -e "Status: OK, Time taken: ${user_time}" >> $logfile
        fi
        if [ -f  "${sandbox_dir}/${entry_num}/result_cnn" ]; then
            user_score=`cat "${sandbox_dir}/${entry_num}/result_cnn"`
        else
            user_score="0.0"
        fi
        penalty=`cat "${sandbox_dir}/${entry_num}/penalty"`
        echo -e "Scores: ${user_score:1}" >> $logfile
        user_score+=","
        user_score+=${user_time}
        user_score+=","
        user_score+=${penalty}
    else
        #If the correct zip file doesn't exist
        echo -e "FILE NOT FOUND!" >> $logfile
        user_score=",NA,NA,YES,NO"
    fi
    echo -e "\n--------------------\n" >> $logfile
    echo -e "${entry_num}${user_score}" >> $scorefile
    #rm -r $5/*.py
    #rm -r $5/*.r
    #rm -rf $5/__MACOSX
    #rm -r $5/cnn
    #rm -r $5/cnn.sh
done < $infile 
