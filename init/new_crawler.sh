#!/bin/sh
##################################
# sh new_crawler.sh
##################################

now=$(pwd)
prj=spiderman
user=weacrawler
host=$(hostname)
dt=$(date +'%Y-%m-%d-%H:%M:%S')

showinfo(){
    msg=$1
    echo "${dt} $msg"
}

setenv(){
    showinfo "Add new spider"
    sudo adduser ${user}
    sudo adduser ${user} sudo

    showinfo "Setup ssh channel"
    sudo cp ~/.ssh/id_rsa.pub  /home/${user}/.ssh/authorized_keys
    sudo chmod 600 /home/${user}/.ssh/authorized_keys
    sudo chown ${user}:${user} /home/${user}/.ssh/authorized_keys
}

getcode(){
    showinfo "Get latest spider code"
    mkdir code
    cd ${now}/code
    git clone git@bitbucket.org:goming/${prj}.git
    sudo cp -R ${prj} /home/${user}
    sudo chown -R ${user}:${user} /home/${user}/${prj}
    cd ..
    sudo rm -rf code
}

startspider(){
    showinfo "Deploy spider env"
    ssh -t ${user}@${host} "whoami; cd ${prj}; sh deploy_weather.sh; crontab -l;"
    sed -i "s|/opt/upbq.sh|${now}/upbq.sh|g" upbq.cron
    crontab upbq.cron
}

setenv
getcode
startspider
