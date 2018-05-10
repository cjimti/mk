---
published: true
layout: post
title: Production Hobby Cluster
tags: kubernetes kubectl cli
featured: kubernetes cli
mast: cluster
---

Setting up a production-grade Kubernetes cluster can be done on a hobby budget, and if this is true why mess around with 
a lesser grade. If you are investing time to learn distributed cloud computing or microservices, is the distance between 
$0 and **15 dollars a month** worth the time in translating best practices? Kubernetes is designed to host production 
applications. My personal web applications may only be hobbies, but they might as well be production grade hobbies. 

I have read my thousandth tutorial on how to do things the wrong way; well, the not-good-for-production-way, you know 
for "learning." The following are my notes as I unlearn the "not for production" tutorial way and re-apply my production 
notes to a 15 dollar-a-month production grade hobby way.

In this article, I'll be using three $5 servers from [vultr.com](https://www.vultr.com/?ref=7418713) (referral link). 
There are a handful of cheap cloud providers these days, and in keeping competitive, they keep getting cheaper and better. 

For my 15 dollars a month I am getting three 1 vCore, 1G ram and 25G of storage each. I host application primarily written 
in Go and Python, and they make very efficient use of their resources.

Start with three **[Ubuntu 18.04 x64](https://amzn.to/2KLn3eE)** boxes of 1 vCore, 1G ram and 25G of storage each in Los 
Angeles (because I work in Los Angeles).

I am calling my new servers lax1, lax2 and lax3.

### Security

I don't need my hobby cluster turning into a [crypto-mining platform while I sleep](https://news.bitcoin.com/hackers-target-400000-computers-with-mining-malware/).

#### Firewall

[ufw](https://help.ubuntu.com/community/UFW) makes easy work of security. Fine-grained `Iptables` rules are nice (and 
complicated, and easy to get wrong) but `ufw` is just dead-simple, and it's production grade security since it's just 
wrapping more complicated Iptable rules.

Login to the box and setup security:
```bash
# lock down the box
ufw --force reset
ufw allow ssh
ufw allow 6443 # Kubernetes API
ufw allow 80
ufw allow 443
ufw default deny incoming
ufw enable
```

#### VPN

[WireGuard] is the VPN I use for cluster communication security. [Install WireGuard](https://www.wireguard.com/install/) 
by following their instructions for Ubuntu below:

```bash
sudo add-apt-repository ppa:wireguard/wireguard
sudo apt-get update
sudo apt-get install wireguard -y
```

Although according to the documentation it's okay to run [WireGuard] over the public interface if your host allows it 
you might as well set up a private network. On [Vultr](https://www.vultr.com/?ref=7418713) it is as simple as checking 
a box setup or clicking on "Add Private Network" in the server settings.

On the **Ubuntu 18.04** servers you need to add the new private network interface manually:

In `/etc/netplan/10-ens7.yaml` add the following lines (replace 10.99.0.200/16 with the assigned private IP and range):
```yaml
network:
  version: 2
  renderer: networkd
  ethernets:
    ens7:
      mtu: 1450
      dhcp4: no
      addresses: [10.5.96.4/20]
```

In my case, the subnet mask is 255.255.240.0 which equates to a /20. 
[Check out this cheat sheet for a quick IP range refrence](https://www.aelius.com/njh/subnet_sheet.html)

Then run the command:

```bash
netplan apply
```

You should now be able to run `ifconfig` and get a new interface like this:

```plain
ens7: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 10.5.96.3  netmask 255.255.240.0  broadcast 10.5.111.255
        inet6 fe80::5800:1ff:fe7c:d24a  prefixlen 64  scopeid 0x20<link>
        ether 5a:00:01:7c:d2:4a  txqueuelen 1000  (Ethernet)
        RX packets 7  bytes 726 (726.0 B)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 2  bytes 176 (176.0 B)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
```

You should be able to ping the private IPs of other servers on the same private network out the new interface, 
in my case **ens7**.

```bash
ping -I ens7 10.5.96.4

PING 10.5.96.4 (10.5.96.4) from 10.5.96.3 ens7: 56(84) bytes of data.
64 bytes from 10.5.96.4: icmp_seq=1 ttl=64 time=1.48 ms
64 bytes from 10.5.96.4: icmp_seq=2 ttl=64 time=0.808 ms
^C
--- 10.5.96.4 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1001ms
rtt min/avg/max/mdev = 0.808/1.144/1.481/0.338 ms
```

**Configuring [WireGuard]**

You will need a public and private key for each server. Here is a simple bash script for generating the key 
pairs all at once (thanks [Hobby Kube](https://github.com/hobby-kube/)]:

```bash
for I in 1 2 3; do
  private_key=$(wg genkey)
  public_key=$(echo $private_key | wg pubkey)
  echo "Server $i private key: $private_key"
  echo "Server $i public key:  $public_key"
done
```

Cut and paste the output somewhere safe as you will need it for configuring each server.

The [WireGuard] VPN Configuration will setup another interface, **wg0** Each server will have a configuration file similar to this:

```bash
# /etc/wireguard/wg0.conf
[Interface]
Address = 10.0.1.1
PrivateKey = <PRIVATE_KEY_KUBE1>
ListenPort = 51820

[Peer]
PublicKey = <PUBLIC_KEY_KUBE2>
AllowedIps = 10.0.1.2/32
Endpoint = 10.8.23.94:51820

[Peer]
PublicKey = <PUBLIC_KEY_KUBE3>
AllowedIps = 10.0.1.3/32
Endpoint = 10.8.23.95:51820
```

You will need to open up the port 51820 on the new private interface for each server. On my new servers, the interface 
is **ens7** as seen when we ran `ifconfig` above.

```bash
ufw allow in on ens7 to any port 51820
ufw allow in on wg0
ufw reload
```

Next ensure that ip forwarding is enabled. If running `sysctl net.ipv4.ip_forward` returns 0 then you will need to run 
the following commands:

```bash
echo "net.ipv4.ip_forward=1" >> /etc/sysctl.conf # enable ip4 forwarding
sysctl -p # apply settings from /etc/sysctl.conf
```

To enable the VPN and run on startup, execute the following commands on each server:

```bash
systemctl start wg-quick@wg0
systemctl enable wg-quick@wg0
```

## Kubernetes

### Install Docker

On each server run:

```bash
apt-get install docker.io -y
```

Ensure the proper **DOCKER_OPS** are set by creating the file
`/etc/systemd/system/docker.service.d/10-docker-opts.conf` and adding
the following line:

```plain
Environment="DOCKER_OPTS=--iptables=false --ip-masq=false"
```

You will need to restart Docker and reload daemons:

```bash
systemctl restart docker
systemctl daemon-reload
```

### Install [Etcd] (in cluster mode)

Maunally install version 3.2.13:

```bash
export ETCD_VERSION="v3.2.13"
mkdir -p /opt/etcd
curl -L https://storage.googleapis.com/etcd/${ETCD_VERSION}/etcd-${ETCD_VERSION}-linux-amd64.tar.gz \
  -o /opt/etcd-${ETCD_VERSION}-linux-amd64.tar.gz
tar xzvf /opt/etcd-${ETCD_VERSION}-linux-amd64.tar.gz -C /opt/etcd --strip-components=1
```

Creating the systemd unit file `/etc/systemd/system/etcd.service` on each server. We are configuring [Etcd] to communicate 
over our new VPN, so we don't need many of the provided security options.

On our three node cluster, the configuration for lax1 looks like this:

```bash
[Unit]
Description=etcd
After=network.target wg-quick@wg0.service

[Service]
Type=notify
ExecStart=/opt/etcd/etcd --name lax1 \
  --data-dir /var/lib/etcd \
  --listen-client-urls "http://10.0.1.1:2379,http://localhost:2379" \
  --advertise-client-urls "http://10.0.1.1:2379" \
  --listen-peer-urls "http://10.0.1.1:2380" \
  --initial-cluster "lax1=http://10.0.1.1:2380,lax2=http://10.0.1.2:2380,lax3=http://10.0.1.3:2380" \
  --initial-advertise-peer-urls "http://10.0.1.1:2380" \
  --heartbeat-interval 200 \
  --election-timeout 5000
Restart=always
RestartSec=5
TimeoutStartSec=0
StartLimitInterval=0

[Install]
WantedBy=multi-user.target
```

The config key `--initial-cluster` is just the initial cluster. You can quickly add more nodes in the future without 
modifying this value.

Enable startup and run [Etcd] on each server:

```bash
systemctl enable etcd.service # launch etcd during system boot
systemctl start etcd.service
```

Run the command `journalctl -xe` if you encounter any errors. The first time I started up [excd] it failed due to a typo.

Check the status of the new [Etcd] cluster:

```bash
/opt/etcd/etcdctl member list

83520a64ae261035: name=lax1 peerURLs=http://10.0.1.1:2380 clientURLs=http://10.0.1.1:2379 isLeader=true
920054c1ee3bca8a: name=lax3 peerURLs=http://10.0.1.3:2380 clientURLs=http://10.0.1.3:2379 isLeader=false
950feae803ed7835: name=lax2 peerURLs=http://10.0.1.2:2380 clientURLs=http://10.0.1.2:2379 isLeader=false
```

### Install Kubernetes

Run the following commands on each server:

```bash
curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add -
```

```bash
cat <<EOF > /etc/apt/sources.list.d/kubernetes.list
deb http://apt.kubernetes.io/ kubernetes-xenial-unstable main
EOF
```

```bash
apt-get update
apt-get install -y kubelet kubeadm kubectl kubernetes-cni
```

#### Initialize the master node

Create the configuration file `/tmp/master-configuration.yml` and
replace PUBLIC_IP_LAX1 with the servers public ip address:

```yaml
apiVersion: kubeadm.k8s.io/v1alpha1
kind: MasterConfiguration
api:
  advertiseAddress: 10.0.1.1
etcd:
  endpoints:
  - http://10.0.1.1:2379
  - http://10.0.1.2:2379
  - http://10.0.1.3:2379
apiServerCertSANs:
  - <PUBLIC_IP_LAX1>
```

Run the following command on lax1:

```bash
kubeadm init --config /tmp/master-configuration.yml
```

After running `kubeadm init` make sure you copy the output, specifically the `--token`, it will look something like 
this `3b1e9s.t21tgbbyx1yt7lrp`.

Next, we will use [Weave Net] to create a Pod network. [Weave Net] is excellent since it is stable, production ready 
and has no configuration.

Create a `.kube` directory for the current user (in my case root).  `kubectl` will access the local Kubernetes with a 
symlinked config file in the logged-in users home path.

```bash
[ -d $HOME/.kube ] || mkdir -p $HOME/.kube
ln -s /etc/kubernetes/admin.conf $HOME/.kube/config
```

Install [Weave Net]:

```bash
kubectl apply -f "https://cloud.weave.works/k8s/net?k8s-version=$(kubectl version | base64 | tr -d '\n')"
```

Open the firewall for weave:

```bash
ufw allow in on weave
ufw reload
```

We need [Weave Net] to route traffic over our VPN. With the following commands, we can set up a new **10.96.0.0/16** 
network for [Weave Net] to route on our new VPN interface.

On each of the servers run the following command replacing the 10.0.1.1 with .2 and .3 to match the server's VPN IP.

```
ip route add 10.96.0.0/16 dev wg0 src 10.0.1.1
``

Add the [systemd] service unit file `/etc/systemd/system/overlay-route.service` to ensure this network configuration happens on boot.

Make sure to change 10.0.1.1 to 10.0.1.2 and 10.0.1.3 for the corresponding servers.

```bash
[Unit]
Description=Overlay network route for Wireguard
After=wg-quick@wg0.service

[Service]
Type=oneshot
User=root
ExecStart=/sbin/ip route add 10.96.0.0/16 dev wg0 src 10.0.1.1

[Install]
WantedBy=multi-user.target
```

Enable the new service on each node:

```bash
systemctl enable overlay-route.service
```


### Joining the Cluster

Use the token we received after running the `kubeadm init` command in the "Initialize the master node" section above.

```bash
kubeadm join --token=<TOKEN> 10.0.1.1:6443 --discovery-token-unsafe-skip-ca-verification
```

### Permissions: RBAC (Role Based Access Control)

Setup permissive RBAC. A permissive RBAC does not affect a clusters ability to be "production grade" since security 
models can change based on the requirements of the cluster. You want a secure cluster, and you get that with the security 
setup in the steps above. What you don't need in a small cluster is a complicated security model. You can add that later.

```bash
kubectl create clusterrolebinding permissive-binding \
  --clusterrole=cluster-admin \
  --user=admin \
  --user=kubelet \
  --group=system:serviceaccounts
```

### kubectl: Remote Access

The easiest way to connect to the new cluster is to download and use its configuration file.

```bash
# if you don't have kubectl installed use homebrew (https://brew.sh/) to install it.
brew install kubectl

# on your local workstation
cd ~/.kube
scp root@lax1.example.com:./.kube/config lax1_config
```

Edit the new lax1_config file and change the yaml key **server** under the **cluster** 
section to the location of your server `server: https://lax1.example.com:6443` you may also 
want to change the context name to something more descriptive like **lax1**.

The environment variable **[KUBECONFIG]** holds paths to config files for `kubectl`. In your shell profile 
(`.bash_profile` or `.bashrc`) add:
 
 ```plain
export KUBECONFIG=$KUBECONFIG:$HOME/.kube/config:$HOME/.kube/lax1_config
 ```
 
Logging in to a new terminal on your workstation and try switching between contexts
(`kubectl config use-context lax1`):

```bash
# kubectl configuration help
kubectl config -h

# display the configs visible to kubectl
kubectl config view

# get the current context
kubectl config current-context

# use the new lax1 context
kubectl config use-context lax1

# get the list of nodes from lax
kubectl get nodes

```

### Deploy an Application

Create a file called `tcp-echo-service.yml`

<script src="https://gist.github.com/cjimti/cb051976caa20f5c53311a7a75e85487.js"></script>

kubectl can use URLs or local files for input:

```bash
# create a service
kubectl create -f https://bit.ly/tcp-echo-service

# list services
kubectl get services

NAME         TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE
kubernetes   ClusterIP   10.96.0.1       <none>        443/TCP          1d
tcp-echo     NodePort    10.109.249.93   <none>        5000:32413/TCP   3m
```

In my case, the port **32413** was assigned to the new TCP echo service. 

Create a deployment configuration called `tcp-echo-deployment.yml`:

<script src="https://gist.github.com/cjimti/f936f728b28cdaf3f0edb26b2a7b8c99.js"></script>

kubectl can use URLs or local files for input:

```bash
kubectl create -f http://bit.ly/tcp-echo-deployment

# describe the deployment
kubectl describe deployment tcp-echo

```


## Resources

- [KUBECONFIG]
- [systemd]
- [Weave Net]
- [Etcd]
- [WireGuard]
- [Hobby Kube] A fantastic write-up and how I got started.

[KUBECONFIG]: https://kubernetes.io/docs/concepts/configuration/organize-cluster-access-kubeconfig/
[systemd]: https://wiki.ubuntu.com/systemd
[WireGuard]: https://www.wireguard.io/
[Weave Net]: https://www.weave.works/oss/net/
[Etcd]: https://coreos.com/etcd/docs/latest/getting-started-with-etcd.html
[Hobby Kube]: https://github.com/hobby-kube/guide

