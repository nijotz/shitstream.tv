FROM node:8

ENV PG_HOST postgres
RUN apt-get update -yq && apt-get install -yq build-essential libav-tools python-pip
RUN pip install --upgrade youtube-dl pip

COPY . ./
RUN npm i

CMD ["./wait-for-it.sh", "postgres:5432", "--", "npm", "start"]
