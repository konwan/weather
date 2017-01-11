#!/bin/sh
##################################
# bash ./tmp.sh -t forecast |daily |history
##################################

now=$(pwd)
user=weacrawler

prj=gomi-dev
ds=cindy_test
tb=''
bqtb=''
gettype=daily
upload_data=${now}/data
prefix=wc

today=$(date +'%Y%m%d')
thismonth=$(date +'%Y%m')
lastmonth=$(date -d "${today} -1 month" +"%Y%m")
time=$(date +'%Y-%m-%d %H:%M:%S')

while getopts "t:" opt; do
  case $opt in
    t)
      gettype=$OPTARG
      ;;
  esac
done


upload_dir=${now}/up/${gettype}
filename=''
schema=''

getschema(){
    file_cols=$(cat ${filename} |head -n 1|awk -F ',' '{print NF}')
    #sudo dpkg-reconfigure dash
    for (( i=1; i<=${file_cols}; i=i+1 ));
    do
        if [ "${i}" == ${file_cols} ]; then
            schema+="col${i}:string"
        else
            schema+="col${i}:string,"
        fi
    done
    #echo ${schema}
}

bqlisttb(){
    # list project
    # bq --format=json ls -p
    # bq mk [DATASET_ID]
    # bq ls gomi-dev:
    # list dataset
    # bq --format=json ls -d

    # list prj:ds
    # bq ls ${prj}:${ds}
    #        tableId             Type
    # ------------------------ ----------
    #  nb_store_list            EXTERNAL
    #  weather                  TABLE
    #  weather201612            TABLE
    #  weather_cities_all       VIEW

    bq show ${bqtb}
    #   Last modified           Schema          Total Rows   Total Bytes   Expiration
    # ----------------- ---------------------- ------------ ------------- ------------
    #  28 Dec 15:10:14   |- date: string        5689379      339870630
    #                    |- hightemp: string
    #                    |- lowtemp: string
    #                    |- status: string
    #                    |- winddir: string
    #                    |- windpower: string
    #                    |- city: string

    bq head -n 4 ${bqtb}

    # echo ${time} >> ${now}/log/${type}.log
    # python -c "import os; print(os.path.dirname(os.path.realpath('__file__')))" >> ${now}/log/${type}.log
    # /usr/local/bin/python ${now}/src/history.py >> ${now}/log/${type}.log
}


getfile(){
    if [ ! -d ${upload_dir} ]; then
        mkdir -p ${upload_dir}
    fi
    filename=${upload_dir}/${gettype}_${today}.csv
    if [ "${gettype}" == 'forecast' ]; then
        find ${upload_data}/7days -name "*_${today}.csv" -exec cat {} \; | grep -v '日期' > ${filename}
    elif [ "${gettype}" == 'daily' ];then
        find ${upload_data}/daily -name "*_${thismonth}.csv" -exec cat {} \; | grep -v '日期' > ${filename}
    else
        find ${upload_data}/weather -name "*_${lastmonth}.csv" -exec cat {} \; | grep -v '日期' > ${filename}
    fi
}



uploadfiletobq(){
    tb=${gettype}_${today}
    bqtb=${prj}:${ds}.${tb}
    getschema

    bq rm -f ${bqtb}
    bq load --source_format=CSV --field_delimiter=',' --encoding=UTF-8 \
                  --max_bad_records=3 --skip_leading_rows=0 ${bqtb} ${filename} ${schema}

    res=$(bq query "select count(*) from ${ds}.${tb}")
    upload_cnt=$(echo ${res} | awk -F '+-----+' '{print $3}'|sed -e "s/+//g; s/|//g; s/ //g")
    file_cnt=$(wc -l ${filename} |awk '{print $1}')

    if [ "${upload_cnt}" == ${file_cnt} ]; then
        echo "[fiinished - ${file_cnt}] upload ${filename} to ${ds}.${tb} \n\n"
        bqlisttb
    else
        echo "[fail - ${file_cnt}] upload count ${upload_cnt}"
    fi
}


#bq cp dataset.mytable dataset2.mynewtable
#bq query "SELECT name,count FROM mydataset.babynames WHERE gender = 'M' ORDER BY count DESC LIMIT 6"
#bq --nosync query --batch "SELECT name,count FROM mydataset.babynames WHERE gender = 'M' ORDER BY count DESC LIMIT 6"

getfile
echo "start to handle ${filename}"
uploadfiletobq

# ls -al ${upload_dir}
# wc -l ${upload_dir}/*
