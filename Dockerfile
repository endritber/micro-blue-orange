FROM python:3.9.6

# Setup ENV variables
ENV DOCKERIZE_VERSION v0.6.1
ENV PYTHONUNBUFFERED 1
ENV PATH $PATH:/usr/src/.local/bin

# Set workspace
WORKDIR /usr/src/app

# Install dockerize
RUN wget https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
  && tar -C /usr/local/bin -xzvf dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
  && rm dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz

# Copy code and install app dependencies
COPY . /usr/src/app

# Install dependencies
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

RUN mkdir -p /vol/web/media/uploads/product
COPY media/test-product.jpg /vol/web/media/uploads/product/
RUN mkdir -p /vol/web/static
RUN adduser user
RUN chown -R user:user /vol
RUN chmod -R 755 /vol/web
USER user