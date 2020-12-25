#!/bin/sh
run()
{
    chmod +x $1
    $1 $2 $3 $4 $5
}

compute_score()
{
    : '
        Compute score as per predicted values and write to given file
        $1 python_file
        $2 targets
        $3 predicted
        $4 outfile
    '
    python3 $1 $2 $3 $4 $5
}


main()
{
    : '
        $1: data_dir
        $2: sandbox_dir
        $3: entry_number
        $4: submissions_dir
        $5: qid
    '
    main_dir=`pwd`
    qid=$5
    if [ -f "${4}/${3}.zip" ]; then
        echo -e "Zip file found!"
        if [ -d "${2}/${3}" ]; then
            echo -e "Unzipped dir found!"
        else
            echo -e "Unzipping!"
            mkdir -p "${2}/${3}"
            unzip "${4}/${3}.zip" -d "${2}/${3}"
        fi
    fi

    status="FAIL"
    stud_dir_path="${main_dir}/${2}/${3}/${3}"
    stud_bdir_path="${main_dir}/${2}/${3}"
    stud_bfname="${stud_bdir_path}/run.sh"
    stud_fname="${stud_dir_path}/run.sh"
    data_dir_path="${main_dir}/${1}"
    compute_accuracy="${main_dir}/compute_accuracy.py"

    if [ -d "${stud_dir_path}" ]; then
        if [ -f ${stud_fname} ]; then
            sed -i 's/\r$//' ${stud_fname} # Handle windows file endings
            status="OK"
        else
            echo -e "run.sh not found!"
        fi
    else
        echo -e "Bad directory structure!"
        if [ -f ${stud_bfname} ]; then
            status="OK"
            sed -i 's/\r$//' ${stud_bfname} # Handle windows file endings
            stud_fname="${stud_bfname}"
            stud_dir_path="${stud_bdir_path}"
        else
            echo -e "run.sh not found!"
        fi
    fi

    if [ $status == "OK" ]; then
        echo -e "Running.."
        cd "$stud_dir_path"
        time run "${stud_fname}" ${qid} "${data_dir_path}/${TRAIN}" "${data_dir_path}/${TEST}" "${stud_dir_path}/predictions_q${qid}"
        compute_score "${compute_accuracy}" "${data_dir_path}/${TEST_GT}" "${stud_dir_path}/predictions_q${qid}" "${stud_dir_path}/result_q${qid}" 
        if [ -f "${stud_dir_path}/result_q${qid}" ]; then
            cp "${stud_dir_path}/result_q${qid}" "${stud_bdir_path}/result_q${qid}"
        fi
        cd $main_dir
    fi    
}


# change these filenames as per your requirement
# label file should be a text file with an ground truth class in each line
# Use dummy labels in dtest; if possible
if [ "$5" -eq 1 ] || [ "$5" -eq 3 ]; then
    TRAIN="yelp.dtrain.json"
    TEST="yelp.dtest.json"
    TEST_GT="yelp.dtest.labels.txt"
else
    TRAIN="fmnist.dtrain.csv"
    TEST="fmnist.dtest.csv"
    TEST_GT="fmnist.dtest.labels.txt"
fi

main $1 $2 $3 $4 $5
