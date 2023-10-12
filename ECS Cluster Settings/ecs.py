# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from aws_cdk import (
    core as cdk,
    aws_ec2 as ec2,
    aws_ecs as ecs,
)

class SurveillanceAwsStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create a VPC
        vpc = ec2.Vpc(
            self, "Vpc",
            max_azs=2
        )

        # Create an ECS cluster
        cluster = ecs.Cluster(self, "Cluster",
            vpc=vpc
        )
        
        # Or add customized capacity. Be sure to start the Amazon ECS-optimized AMI.
        auto_scaling_group = autoscaling.AutoScalingGroup(self, "ASG",
            vpc=vpc,
            instance_type=ec2.InstanceType("t2.large"),
            machine_image=EcsOptimizedImage.amazon_linux(),
            # Or use Amazon ECS-Optimized Amazon Linux 2 AMI
            # machineImage: EcsOptimizedImage.amazonLinux2(),
            desired_capacity=1
        )
        
        cluster.add_auto_scaling_group(auto_scaling_group)
        
        cluster.add_capacity("graviton-cluster",
            min_capacity=1,
            instance_type=ec2.InstanceType("c6g.large"),
            machine_image=ecs.EcsOptimizedImage.amazon_linux2(ecs.AmiHardwareType.ARM)
        )
        
        # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
        ec2_task_definition = ecs.Ec2TaskDefinition(self, "TaskDef",
            network_mode=NetworkMode.BRIDGE
        )
        
        container = ec2_task_definition.add_container("WebContainer",
            # Use an image from DockerHub
            image=ecs.ContainerImage.from_registry("amazon/amazon-ecs-sample"),
            memory_limit_mi_b=1024
        )
        
        # Instantiate an Amazon ECS Service
        ecs_service = ecs.Ec2Service(self, "Service",
            cluster=cluster,
            task_definition=ec2_task_definition
        )