#!/bin/sh
run()
{
    chmod +x $1
    ./$1 $2 $3 $4
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
    '
    main_dir=`pwd`
    if [ -f "${4}/${3}.zip" ]; then
        echo -e "Zip file found!"
        unzip $4/$3.zip -d $2
        zip_penalty="NO"
    elif [ -f "${4}/${3}.rar" ]; then
        echo -e "RAR file found!"
        unrar x "$4/$3.rar" $2
        zip_penalty="YES"
    fi
    
    stud_folder_path="${main_dir}/${2}/${3}"
    data_folder_path="${main_dir}/${1}"
    compute_accuracy="${main_dir}/compute_accuracy.py"
    cd "$stud_folder_path"

    status="OK"
    if [ -f "cnn" ]; then
        fname="cnn" 
        bash_fname_penalty="NO"
        dos2unix cnn
    elif [ -f "cnn.sh" ]; then
        echo -e "Using cnn.sh; Follow submission instructions."
        fname="cnn.sh"
        bash_fname_penalty="YES"
        dos2unix cnn.sh
    else
        status="NA"
        echo -e "ERROR; cnn or cnn.sh not found!"
        bash_fname_penalty="YES"
    fi

    echo -e "Zip Penalty: ${zip_penalty}\nBash_File_Name_Penalty: ${bash_fname_penalty}"
    echo -e "${zip_penalty},${bash_fname_penalty}" > penalty


    if [ $status == "OK" ]; then
        time run "${fname}" "${data_folder_path}/devnagri_train.csv" "${data_folder_path}/devnagri_test.csv" "${stud_folder_path}/predictions_cnn"
        compute_score "${compute_accuracy}" "${data_folder_path}/devnagri_target_labels.txt" "${stud_folder_path}/predictions_cnn" "${stud_folder_path}/result_cnn" 
    fi
    cd $main_dir
}

main data sandbox $1 submissions
