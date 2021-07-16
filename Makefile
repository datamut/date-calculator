all:
	/bin/false

build_api:
	docker build -t calculator_api -f api.Dockerfile .

run_api:
	docker run -it -p 8089:8089 calculator_api

build_shell:
	docker build -t calculator_shell -f shell.Dockerfile .

run_shell:
	docker run -it calculator_shell

test_scidate:
	DOCKER_BUILDKIT=0 docker build -t scidate_test -f test.scidate.Dockerfile .
	docker run -it scidate_test
