# CNS Final

## docker-mininet

### Docker Build Command

```bash
cd docker-mininet
docker build -t mininet .
```

### Docker Run Command

```bash
docker run -it --rm --privileged -e DISPLAY \
           -P -v /lib/modules:/lib/modules \
           mininet
```

