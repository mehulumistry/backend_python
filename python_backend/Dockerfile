FROM alpine:3.1

# Update
RUN apk add --update python py-pip

# Install app dependencies

RUN pip install -r requirements.txt

# Bundle app source
COPY WebAPI.py /src/WebAPI.py

EXPOSE  3000
CMD ["python", "/src/WebAPI.py", "-p 3000"]