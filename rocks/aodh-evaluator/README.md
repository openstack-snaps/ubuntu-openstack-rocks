# aodh-evaluator ROCK

This is a ROCK OCI image for aodh-evaluator.

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
> skopeo --insecure-policy copy oci-archive:aodh-evaluator_2023.1_amd64.rock docker-daemon:aodh-evaluator:2023.1
```

If you are interested in giving it a go in Microk8s, you can
export the image from your docker registry and then into the
microk8s registry:

```bash
> docker save aodh-evaluator:2023.1 > ./aodh-evaluator_2023.1.tar
> microk8s ctr image import ./aodh-evaluator_2023.1.tar
# Try with sunbeam
> juju attach-resource aodh-k8s aodh-evaluator-image=aodh-evaluator:2023.1
```
