docker build -t local-prometheus . --no-cache
docker tag local-prometheus claudiapreda2307/statistics:latest
docker push claudiapreda2307/statistics:latest