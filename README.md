<h1 align="center">NET-MONITOR
<h3 align="center">Linux daemon for monitoring network hosts availability</h3>
<br>
<p><b>install:</b></p>
<p>install make and git package:</p>
<p><code>apt install make git</code></p>
<p>clone this git repo:</p>
<p><code>cd ~</code></p>
<p><code>git clone https://github.com/Ivashkka/net-monitor.git</code></p>
<p><code>cd net-monitor</code></p>
<p>start make install from root:</p>
<p><code>sudo make install; cd ~</code></p>
<p>wait until installation finishes</p>
<p>after the installation is finished, configure conf.yaml:</p>
<p><code>vim /etc/net-monitor/conf.yaml</code></p>
<p>also write scripts that will react to changes in the states of network groups (see conf.yaml)</p>
<p>start net-monitor:</p>
<p><code>systemctl start net-monitor</code></p>
<p><code>systemctl status net-monitor</code></p>
<p>and enable if needed:</p>
<p><code>systemctl enable net-monitor</code></p>
<br>
<p><b>settings:</b></p>
<p>all net-monitor settings located in <code>/etc/net-monitor/conf.yaml</code></p>
<pre>
monitor:
  hosts: # actual hosts
    - name: ISP1
      addr: 172.16.1.1
      type: icmp # currently only icmp and command are supported
    - name: ISP2
      addr: 172.16.2.1
      type: icmp
    - name: ISP3
      addr: 172.16.3.1
      type: command
      exec: bash /usr/local/bin/check-isp3-availability.sh # exit 1 or 0 # exec param is ignored when type != command
  groups: # availability groups of hosts
    - name: HA-ISP
      hosts: [ ISP1, ISP2, ISP3 ]
      interval: 5 # seconds
      exec: /usr/local/bin/ha-isp.sh # the script is called when the availability state changes
      #with arguments indicating which hosts remain available
      #this exec param is not the same as one in hosts directive. Here you can only pass path to script
    - name: SINGLE-ISP3
      hosts: [ ISP3 ]
      interval: 10 # seconds
      exec: /usr/local/bin/isp3.sh
      #### optional group settings: ####
      args: #default arguments: ALL, <HOST>, NONE
        - default: ALL # redefinition of default 'ALL' argument to 'up' argument
          redefine: up
        - default: NONE # redefinition of default 'NONE' argument to 'down' argument
          redefine: down
</pre>
<p><code>hosts</code> - list of network hosts and info about it. Use icmp or command types.</p>
<p><code>groups</code> - actual monitoring units. Group can contain one or more hosts. When availability ststus changes,</p>
<p>net-monitor calls specified in exec field script with arguments indicating which hosts remain available.</p>
<p>net-monitor daemon works in bg and monitors specified groups.</p>
<p>example of /usr/local/bin/ha-isp.sh script:</p>
<pre>
case $1 in
    ALL)
        ip route replace default \
            nexthop via 172.16.1.1 dev enp0s3 weight 1 \
            nexthop via 172.16.2.1 dev enp0s8 weight 1
    ;;
    ISP1)
        ip route replace default via 172.16.1.1 dev enp0s3
    ;;
    ISP2)
        ip route replace default via 172.16.2.1 dev enp0s8
    ;;
esac
</pre>
<p>where ALL, HOST, NONE - arguments passed from net-monitor on script call</p>
<p>you can redefine default arguments whith your own in conf.yaml</p>
<p>net-monitor demonstration:</p>
<img src="./demonstration.svg">
<br>
<p><b>uninstall:</b></p>
<p>stop net-monitor:</p>
<p><code>systemctl stop net-monitor</code></p>
<p>disable autorun if needed:</p>
<p><code>systemctl disable net-monitor</code></p>
<p>move inside net-monitor git repo directory(where you cloned net-monitor.git):</p>
<p><code>cd ~/net-monitor</code></p>
<p>start uninstall process:</p>
<p><code>make clean</code></p>
<br>
