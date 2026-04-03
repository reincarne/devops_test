## Dockerfile
I have changed the base image in Dockerfiles because of this reason:
In general the Ubuntu and uv builds seem to be 10-17% faster than the python Docker images provided by Docker, and are also faster than OracleLinux. Reference: https://pythonspeed.com/articles/base-image-python-docker-images/

## Entrypoint
To my mind entrypoint.sh is an additional dependency which should be maintained, it increases complexity and can cause problems in debugging.

## Container networking
containers are communicating by redis celery task
the app is exposed to the external network while redis is available only inside the network. Worker doesn't need any network access except redis.

## Worker
Using celery to listen tasks from redis
worker logs are streamed to logs/worker.log file;


# CI
When code is pushed to main it will ran CI workflow which consists of 3 jobs:
1. **Semver**
    - using Gitversion to generate semantic version based on previous jobs
2. **Build**
    - Using Buildah to build docker images
    - pushes images to ghcr
    - saves the image tar archive
3. **Release**
    - pushes release tag to registry

