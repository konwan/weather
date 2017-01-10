#!/bin/sh
##################################
# bash ./tmp.sh -t forecast
##################################

now=$(pwd)
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

historydata(){
    echo ${time} >> ${now}/log/${type}.log
    #python ${now}/src/history.py
}

forecastdata(){
    echo ${time} >> ${now}/log/${type}.log
    #python ${now}/src/forecast.py
}

dailydata(){
    echo ${time} >> ${now}/log/${type}.log
    #python ${now}/src/daily.py
}

if [ "${type}" == 'forecast' ]; then
    forecastdata
elif [ "${type}" == 'daily' ];then
    dailydata
else
    historydata
fi

