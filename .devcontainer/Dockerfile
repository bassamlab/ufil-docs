# in your Dockerfile
FROM sphinxdoc/sphinx

ENV LC_ALL=C.UTF-8

# Install additional OS packages.
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
  && apt-get -y install --no-install-recommends \
  git openssh-client

# Setup terminal sessions
COPY .bashrc /root/.bashrc

# Setup workspace
WORKDIR /docs

# Add pyhton requirements
ADD requirements.txt /docs
RUN pip3 install -r requirements.txt