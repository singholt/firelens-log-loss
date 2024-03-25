LOGGER_MAKEFILE := $(word $(words $(MAKEFILE_LIST)),$(MAKEFILE_LIST))
LOGGER_DIRECTORY := $(realpath $(dir $(LOGGER_MAKEFILE)))

CI_COMMIT_SHORT_SHA ?= local
AWS_DEFAULT_REGION ?= eu-west-1

.PHONY: docker_deploy_logger
docker_deploy_logger: docker_build_logger docker_upload_logger

.PHONY: docker_build_logger
docker_build_logger:
	docker build -t poc/logger:${CI_COMMIT_SHORT_SHA} ${LOGGER_DIRECTORY}/.

.PHONY: docker_upload_logger
docker_upload_logger:
	ecs-cli push --region ${AWS_DEFAULT_REGION} poc/logger:${CI_COMMIT_SHORT_SHA}

.PHONY: docker_delete_logger
docker_delete_logger:
	aws ecr delete-repository --region ${AWS_DEFAULT_REGION} --force --repository-name poc/logger

.PHONE: docker_run_logger
docker_run_logger:
	aws ecs run-task --cli-input-json file://${LOGGER_DIRECTORY}/run_task.json --region ${AWS_DEFAULT_REGION} >> runtask_results.txt
