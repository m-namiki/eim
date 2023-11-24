FROM python:3.11

WORKDIR /workspace/eim

RUN curl -sSf https://rye-up.com/get | RYE_INSTALL_OPTION="--yes" bash \
  && echo 'source "$HOME/.rye/env"' >> ~/.bashrc

# install nodejs
ENV NODE_MAJOR=20
RUN mkdir -p /etc/apt/keyrings \
  && curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg \
  && echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_$NODE_MAJOR.x nodistro main" | tee /etc/apt/sources.list.d/nodesource.list \
  && apt-get update \
  && apt-get install -y nodejs \
  && rm -rf /var/lib/apt/lists/*

# install typescrpit and aws-cdk
RUN npm install --prefix ./provisioning typescript aws-cdk-lib --save-dev
