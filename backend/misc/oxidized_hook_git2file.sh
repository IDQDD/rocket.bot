#!/usr/bin/env bash
# oxidized hook script to refresh bf_snapshots when network devices config changes
# the script should be put under the ~oxidized/.config/oxidized directory
#
# then create a hook like that in the oxidized config
# hooks:
#   git_to_file:
#     type: exec
#     events: [post_store]
#     cmd: '/bin/bash /home/oxidized/.config/oxidized/oxidozed_hook_git2file.sh $OX_NODE_NAME && echo "git2file for $OX_NODE_NAME has been performed" >> /tmp/oxid.script.res'
#     async: true
#     timeout: 40

OXIDIZED_HOME="/home/oxidized/.config/oxidized"
BF_CONFIGS_PATH="/home/nryzhkov/rocket/rocket.bot/backend/bf_snapshots/networks/bf1/configs"

case $1 in 
        "n7k1" | "n7k2" )
                echo "get config from git for nexus"
                git --git-dir $OXIDIZED_HOME/cisco.git show master:$1 > $BF_CONFIGS_PATH/$1.cfg
                ;; 

        "ex4600-dci-1" | "ex4600-dci-2" )
                echo "get config from git for juniper"
                git --git-dir $OXIDIZED_HOME/juniper.git show master:$1 > $BF_CONFIGS_PATH/$1.cfg
                ;; 

        *) 
                ;; 
esac