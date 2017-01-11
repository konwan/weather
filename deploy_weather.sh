#!/bin/sh

now=$(pwd)
user=weacrawler
prj=weather
img=${prj}_img
con=${prj}_con
dt=$(date +'%Y-%m-%d-%H:%M:%S')

# [step1] get code from git
#sudo rm -r ${now}/${prj}
#git clone git@bitbucket.org:goming/${prj}.git

# [step2] copy code to weacrawler
#sudo cp -R ${prj} /home/${user}
#sudo chown -R ${user}:${user} /home/${user}/${prj}

cleardocker(){
    t=$1
    c=$2
    if [ ${t} -eq 1 ]; then
        failimg=$(sudo docker images -f "dangling=true" -q)
        failcon=$(sudo docker ps -a -q)
        sudo docker rm ${failcon}
        sudo docker rmi ${failimg}
    fi

    sudo docker rm -f ${con}
    sudo rm phantomjs
    sudo mv log log_${dt}

    if [ ${c} -eq 1 ]; then
        sudo docker rmi -f ${img}
    fi
}

# [step1] - new docker img
cleardocker 0 0
sudo docker build -t ${img}  .
ret=$?
if [ ${ret} -eq 0 ]; then
    echo "[Deploy-Success] - New Docker Image Successfully"
    sudo docker run -tid  --name ${con} -v ${now}:/opt/${prj} ${img} /bin/bash -c "ln -s /opt/docker/phantomjs-2.1.1-linux-x86_64 /opt/weather/phantomjs && mkdir /opt/weather/log && crontab /opt/weather/getdata.cron && service cron start && service cron reload && service cron status && tail -f /dev/null"
    #ret=$?
    #if [ ${ret} -eq 0 ]; then
    #    sudo docker exec ${con} /bin/bash -c "cat getdata.cron >> /var/spool/cron/crontabs/root && service cron status"
    #fi
else
    echo "[Deploy-Fail] - New Docker Image Fail"
    cleardocker 1 1
    exit 1
fi
