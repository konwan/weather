#!/bin/sh
##################################
# sh new_crawler.sh
##################################


prj=spiderman
depuser=$(whoami)
now=/opt/dev_${prj}
user=weacrawler
host=$(hostname)
dt=$(date +'%Y-%m-%d-%H:%M:%S')

showinfo(){
    msg=$1
    echo "${dt} $msg"
}

setenv(){
    id ${user}
    res=$?

    if [ ${res} -ne 0 ];then
        showinfo "Add new spider"
        sudo adduser ${user}
        sudo adduser ${user} sudo

        showinfo "Setup ssh channel"
        sudo mkdir /home/${user}/.ssh && sudo chown ${user}:${user} /home/${user}/.ssh && sudo chmod 600 /home/${user}/.ssh
        sudo cp ~/.ssh/id_rsa.pub  /home/${user}/.ssh/authorized_keys
        sudo chmod 600 /home/${user}/.ssh/authorized_keys
        sudo chown ${user}:${user} /home/${user}/.ssh/authorized_keys
    else
        showinfo "${user} already exist"
    fi
}

getcode(){
    if [ ! -d "${now}" ]; then
        sudo mkdir ${now}
        sudo chown ${devuser}:${devuser} ${now}
    fi
    cd ${now}
    sudo rm -rf ${prj}
    showinfo "Get latest spider code"
    git clone -b weather git@bitbucket.org:goming/${prj}.git
    sudo cp -R ${prj} /home/${user}
    sudo chown -R ${user}:${user} /home/${user}/${prj}
}

startspider(){
    showinfo "Deploy spider env"
    ssh -t ${user}@${host} "whoami; cd ${prj}; sh deploy_weather.sh; crontab -l;"
    sed -i "s|/opt/upbq.sh|${now}/${prj}/init/upbq.sh|g" ${now}/${prj}/init/upbq.cron
    crontab ${now}/${prj}/init/upbq.cron
}

clearuser(){
    sudo rm /var/spool/cron/crontabs/${depuser}
    sudo deluser ${user}
    sudo rm -rf /home/${user}
    sudo rm -rf ${now}/${prj}
}

clearuser
setenv
getcode
startspider
