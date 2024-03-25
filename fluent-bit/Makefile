DOCKER_MAKEFILE := $(word $(words $(MAKEFILE_LIST)),$(MAKEFILE_LIST))
DOCKER_DIRECTORY := $(realpath $(dir $(DOCKER_MAKEFILE)))

CI_COMMIT_SHORT_SHA ?= local
AWS_DEFAULT_REGION ?= eu-west-1

.PHONY: docker_deploy_fluent-bit
docker_deploy_fluent-bit: docker_build_fluent-bit docker_upload_fluent-bit

.PHONY: docker_fluent-bit_images
docker_build_fluent-bit:
	docker build -t poc/fluent-bit:${CI_COMMIT_SHORT_SHA} ${DOCKER_DIRECTORY}/.

.PHONY: docker_upload_fluent-bit
docker_upload_fluent-bit:
	ecs-cli push --region ${AWS_DEFAULT_REGION} poc/fluent-bit:${CI_COMMIT_SHORT_SHA}

.PHONY: docker_delete_fluent-bit
docker_delete_fluent-bit:
	aws ecr delete-repository --region ${AWS_DEFAULT_REGION} --force --repository-name poc/fluent-bit
