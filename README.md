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
<p>all net-monitor settings located in /etc/net-monitor/conf.yaml</p>
<p>hosts - list of network hosts and info about it</p>
<p>groups - actual monitoring units</p>
<br>
<p><b>usage:</b></p>
<p>net-monitor daemon works in bg. Where availability status of network group changes, net-monitor will call specified script with suitable arguments (see conf.yaml)
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
