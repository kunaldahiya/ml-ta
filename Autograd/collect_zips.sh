#!/bin/bash
# RUN: ./collect_zips.sh ./moodle_submissions ./submissions ./users.txt ./log_collect_zip.txt
indir=$1
outdir=$2
outfile=$3
logfile=$4
lookupfile=$5
echo -e "Collecting zips...." > $logfile
for dir in ${indir}/*; do
    if [ -d "$dir" ]; then
        for file in "${dir}"/*.zip; do
            fname=$(basename -- "$file")
            fname="${fname%.*}"
            if ! grep -q "${fname}" "${lookupfile}"; then
                echo "${fname} found!" >> $logfile
                echo "${fname}" >> $outfile
            fi
            cp "${file}" "${outdir}"
        done
    fi
done