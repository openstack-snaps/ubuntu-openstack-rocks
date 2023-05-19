# Monolithic repo for OpenStack Rocks

To generate a rock definition from a cookie cutter template:

```bash
> ./rock-init.sh glance-api
> rock_name [glance-api]: 
> packages [sudo nfs-common qemu-utils  glance python3-boto3 python3-os-brick python3-oslo.vmware python3-rados python3-rbd apache2 libapache2-mod-wsgi-py3 openssl]:
```

The output will be in the rocks directory:

```bash
> ls -l rocks/glance-api
> total 20
> -rw-rw-r-- 1 liam liam 10765 May 19 16:59 LICENSE
> -rw-rw-r-- 1 liam liam   913 May 19 16:59 README.md
> -rw-rw-r-- 1 liam liam  1270 May 19 16:59 rockcraft.yaml
```
