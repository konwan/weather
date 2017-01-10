#!/bin/sh
##################################
# bash ./tmp.sh -t forecast
##################################

now=/opt/weather
user=weacrawler
prj=weather
prefix=wc
img=${prj}_img
con=${prj}_con
time=$(date +'%Y-%m-%d %H:%M:%S')
type=daily

while getopts "t:" opt; do
  case $opt in
    t)
      type=$OPTARG
      ;;
  esac
done

cd ${now}

historydata(){
    echo ${time} >> ${now}/log/${type}.log
    #python -c "import os; print(os.path.dirname(os.path.realpath('__file__')))" >> ${now}/log/${type}.log
    /usr/local/bin/python ${now}/src/history.py >> ${now}/log/${type}.log
}

forecastdata(){
    echo ${time} >> ${now}/log/${type}.log
    #pwd >> ${now}/log/${type}.log
    /usr/local/bin/python ${now}/src/forecast.py  >> ${now}/log/${type}.log
}

dailydata(){
    echo ${time} >> ${now}/log/${type}.log
    /usr/local/bin/python ${now}/tmp.py >> ${now}/log/${type}.log
    /usr/local/bin/python ${now}/src/daily.py  >> ${now}/log/${type}.log
}

if [ "${type}" == 'forecast' ]; then
    forecastdata
elif [ "${type}" == 'daily' ];then
    dailydata
else
    historydata
fi
~



