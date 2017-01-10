#!/bin/sh

now=$(pwd)
user=weacrawler
prj=weather
img=${prj}_img
con=${prj}_con

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
    if [ ${c} -eq 1 ]; then
        sudo docker rmi -f ${img}
    fi
}




# [step1] - new docker img
cleardocker 0 0
# sudo docker build -t ${img}  .
ret=$?
if [ ${ret} -eq 0 ]; then
    echo "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Successfully"
    sudo docker run -tid  --name ${con} -v ${now}:/opt/${prj} ${img} /bin/bash -c "ln -s /opt/docker/phantomjs-2.1.1-linux-x86_64 /opt/weather/phantomjs && mkdir /opt/weather/log && cat /opt/weather/getdata.cron >> /var/spool/cron/crontabs/root && service cron start && service cron status && tail -f /dev/null"
    #ret=$?
    #if [ ${ret} -eq 0 ]; then
    #    sudo docker exec ${con} /bin/bash -c "cat getdata.cron >> /var/spool/cron/crontabs/root && service cron status"
    #fi
else
    echo "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Fail"
    cleardocker 1 1
    exit 1
fi

# [step2] - new docker container
#echo "docker run --name crawler -p 3306:3306 -v /Users/data/Desktop/cindy/gomi/docker/my:/mikudb -v /Users/data/Desktop/cindy/gomi/docker/my.conf:/etc/mysql/my.cnf  -e MYSQL_ROOT_PASSWORD=0000 -d mariadb:10.1"

# sudo docker rm -f ${con}
# sudo docker run -t --name ${con} -v ${now}:/opt/${prj} ${img}
# sudo docker run --rm -it --name crawler2 -v /home/cindy/weather:/opt/weather weather_img bash

# sudo docker ps -a


# service cron stop
# service cron start
# service cron status
# cat '' >> /var/spool/cron/crontabs/root


