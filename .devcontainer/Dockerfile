FROM ubuntu:22.04

# Setup workspace directory
RUN mkdir /workspace
WORKDIR /workspace

# Install useful system utilities
ENV TZ=America/New_York
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update \
	&& apt-get install --yes \
        apt-transport-https \
        build-essential \
        ca-certificates \
	    curl \
        debian-keyring \
        debian-archive-keyring \
	    git \
        gnupg \
        locales \
        postgresql-client \
        software-properties-common \
        sudo \
        tzdata \
        wget \
        zsh \
    && rm -rf /var/lib/apt/lists/*

# Install Caddy web server
RUN curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/gpg.key' | gpg --dearmor -o /usr/share/keyrings/caddy-stable-archive-keyring.gpg \
    && curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/debian.deb.txt' | tee /etc/apt/sources.list.d/caddy-stable.list \
    && apt update \
    && apt install caddy

# Install Node.js 22 from https://github.com/nodesource
ENV NODE_MAJOR 22
RUN mkdir -p /etc/apt/keyrings \ 
    && curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg \
    && echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_$NODE_MAJOR.x nodistro main" | sudo tee /etc/apt/sources.list.d/nodesource.list \
    && apt-get update \
    && apt-get install nodejs -y \
    && npm install -g npm@latest \
    && rm -rf /var/lib/apt/lists/*

# Install Angular CLI Globally
RUN npm install -g @angular/cli

# Install Python 3.12
RUN add-apt-repository ppa:deadsnakes/ppa \
    && apt update \
    && apt install --yes \
        python3.12 \
        libpq-dev \
        python3.12-venv \
        python3.12-dev \
    && rm -rf /var/lib/apt/lists* \
    && unlink /usr/bin/python3 \
    && ln -s /usr/bin/python3.12 /usr/bin/python3

RUN apt-get update && apt-get install --yes texlive-latex-base

# Use a non-root user per https://code.visualstudio.com/remote/advancedcontainers/add-nonroot-user
ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID

# Add non-root user and add to sudoers
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME -s /usr/bin/zsh \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME

# Set code to default git commit editor
RUN git config --system core.editor "code --wait"
# Set Safe Directory
RUN git config --system safe.directory '/workspace'

# Make frontend node_modules
RUN mkdir -p /workspace/frontend/node_modules && chown $USERNAME /workspace/frontend/node_modules
VOLUME /workspace/frontend/node_modules

# Configure zsh
USER $USERNAME
ENV HOME /home/$USERNAME

# Add zsh theme with niceties
RUN curl https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh | bash - \
    && sed -i 's/robbyrussell/kennethreitz/g' ~/.zshrc \
    && echo 'source <(ng completion script)' >>~/.zshrc \
    && echo 'export PATH=$PATH:$HOME/.local/bin' >>~/.zshrc

# Set Locale for Functional Autocompletion in zsh
RUN sudo locale-gen en_US.UTF-8

# Add `oc` OpenShift Client to DevContainer
RUN arch="$(arch)"; \
    case "$arch" in \
        x86_64) export TARGET='' ;; \
        aarch64) export TARGET='arm64-' ;; \
    esac; \
    wget -O /tmp/oc.tgz "https://github.com/okd-project/okd/releases/download/4.15.0-0.okd-2024-03-10-010116/openshift-client-linux-${TARGET}4.15.0-0.okd-2024-03-10-010116.tar.gz" && \
    cd /tmp && \
    tar -xvzf oc.tgz && \
    sudo mv oc /usr/bin/oc && \
    rm kubectl oc.tgz README.md

# Install Database Dependencies
COPY backend/requirements.txt /workspace/backend/requirements.txt
WORKDIR /workspace/backend
RUN python3 -m ensurepip
RUN python3 -m pip install -r requirements.txt


# Expose server ports
EXPOSE 1560 1561 1562