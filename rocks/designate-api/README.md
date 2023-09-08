# designate-api ROCK

This is a ROCK OCI image for designate-api.

More information is coming.

For now, if you want to play with it:

```bash
> sudo snap install rockcraft --edge --classic
> rockcraft pack
```

Now that you have created the ROCK, you can import it into
your local docker repository. Using skopeo is a good idea as
it will help ensure that all layers of the image are imported
into docker (this is just the top layer).

```bash
> skopeo --insecure-policy copy oci-archive:designate-api_2023.1_amd64.rock docker-daemon:designate-api:2023.1
```

If you are interested in giving it a go in Microk8s, you can
export the image from your docker registry and then into the
microk8s registry:

```bash
> docker save designate-api:2023.1 > ./designate-api_2023.1.tar
> microk8s ctr image import ./designate-api_2023.1.tar
# Try with sunbeam
> juju attach-resource designate-api designate-api-image=designate-api:2023.1
```
