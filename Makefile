CI_COMMIT_SHORT_SHA ?= local
AWS_DEFAULT_REGION ?= eu-west-1
CI_COMMIT_SHORT_SHA ?= local
STACK_NAME ?= ${STACK_PREFIX}-poc
STACK_PREFIX ?= prefix

include logger/Makefile
include fluent-bit/Makefile
