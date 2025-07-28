# !/bin/sh
servername=`hostname`.local

f_getport()
{
    perl - <<'EOT'
    use IO::Socket::INET;
    my $port_no = do {
        my $l = IO::Socket::INET->new(
            Listen => 5,
            LocalHost => '127.0.0.1',
            LocalPort => 0,
            Proto => 'tcp',
            ReuseAddr => 1,
        ) or die $!;
        print $l->sockport;
    };
EOT
}

cmd=$1
if [ "x$cmd" = "x" ];then
    echo "Usage: `basename $0` start|stop" >&2
    exit 1
fi


ret=9
if [ "x$cmd" = "xstart" ];then

    l_port=`f_getport`

    git instaweb --stop
    sleep 1

    git instaweb  --httpd=webrick --port=$l_port --browser='none'

    echo "\n"
    echo "-----"
    printf "Access URL -->   http://%s:%s/\n" "$servername" "$l_port"
    echo "-----"
    ret=0

elif [ "x$cmd" = "xstop" ];then

    git instaweb  --stop
    ret=0
fi

exit $ret

