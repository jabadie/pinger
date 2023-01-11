
build:
	docker build -t pinger -f docker/Dockerfile.local  .

start:
	docker run -d --rm --name pinger --publish 8080:8080  pinger:latest

stop:
	docker stop pinger

clean:
	docker image prune -a -f 

test:
	cd source/pinger
	python3 -m unittest discover source/pinger
