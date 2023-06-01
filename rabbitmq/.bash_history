cd %RABBITMQ_SERVER%\sbin
pwd
ls
cd sbin
ls
rabbitmqctl add_user admin admin 
rabbitmqctl set_user_tags admin administrator 
rabbitmqctl set_permissions -p / admin ".*" ".*" ".*"
exit
