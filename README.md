# Firelens log loss

Demonstrates how Fireles loses logs when app terminates while producing a high number of logs per second.

## Setup

You need to have an ECS cluster up and running. For these tests `ECS_CONTAINER_STOP_TIMEOUT` was set to 2 minutes. For the nodes in the clusters both AMIs were tested: `/aws/service/ecs/optimized-ami/amazon-linux-2/recommended/image_id` and `/aws/service/ecs/optimized-ami/amazon-linux-2023/recommended/image_id`.

The ECS task definition used for the tests looks as follows:
```yaml
TaskDefinition:
Type: AWS::ECS::TaskDefinition
Properties:
  ExecutionRoleArn: !GetAtt ECSRole.Arn
  Family: poc
  NetworkMode: <your-network-mode>
  RequiresCompatibilities:
    - EC2
  Memory: 4096
  ContainerDefinitions:
    - Name: logger
      Essential: true
      Image: <ecr-registry>/poc/logger:local
      Command:
        - 10000
        - 0
        - 1
      # Using awslogs driver flushes all logs
      # LogConfiguration:
      #   LogDriver: awslogs
      #   Options:
      #     awslogs-group: firelens-load-test
      #     awslogs-region: !Ref AWS::Region
      LogConfiguration:
        LogDriver: awsfirelens
        Options:
          Name: cloudwatch_logs
          region: eu-west-1
          log_group_name: firelens-load-test
          auto_create_group: true
          log_stream_prefix: logger
          # Similar log lost when writing to stdout
          # Name: stdout

    - Name: log_router
      Essential: true
      Image: fluent/fluent-bit:2.2.2
      # Used for testing delayed SIGTERM
      # Image: <ecr-registry>/poc/fluent-bit:local
      FirelensConfiguration:
        Type: fluentbit
        Options:
          enable-ecs-log-metadata: true
          config-file-type: s3
          config-file-value: arn:aws:s3:::<poc-id>-firelens-config/fluentbit-extra.conf
      PortMappings:
        - ContainerPort: 2020
      # Enable Fluent Bit debug logs
      # Environment:
      #   - Name: FLB_LOG_LEVEL
      #     Value: debug
      LogConfiguration:
        LogDriver: awslogs
        Options:
          awslogs-group: firelens-container
          awslogs-region: eu-west-1
          awslogs-create-group: true
          awslogs-stream-prefix: firelens
```

Fluent Bit configuration file `fluentbit-extra.conf`:
```yaml
[SERVICE]
    Grace        30
    Flush        1
    Daemon       Off
    HTTP_Server  On
    HTTP_Listen  0.0.0.0
    HTTP_PORT    2020
``` 
