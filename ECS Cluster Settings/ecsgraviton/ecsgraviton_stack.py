# The code that defines your stack goes here
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from aws_cdk import (
    core as cdk,
    aws_ec2 as ec2,
    aws_ecs as ecs,
    aws_ecr as ecr,
    aws_autoscaling as autoscaling
)

class EcsGravitonStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create a VPC
        vpc = ec2.Vpc(
            self, "Vpc",
            max_azs=2
        )

        # Create an ECS cluster
        clustergraviton = ecs.Cluster(self, "ClusterGraviton",
            vpc=vpc
        )
        # Create an ECS cluster
        clusterec2 = ecs.Cluster(self, "ClusterEc2",
            vpc=vpc
        )
        
        # Or add customized capacity. Be sure to start the Amazon ECS-optimized AMI.
        auto_scaling_group = autoscaling.AutoScalingGroup(self, "ASG",
            vpc=vpc,
            instance_type=ec2.InstanceType("c5.large"),
            machine_image=ecs.EcsOptimizedImage.amazon_linux(),
            # Or use Amazon ECS-Optimized Amazon Linux 2 AMI
            # machineImage: EcsOptimizedImage.amazonLinux2(),
            desired_capacity=1
        )
        
        clusterec2.add_auto_scaling_group(auto_scaling_group)
        
        
        clustergraviton.add_capacity("graviton-cluster",
            min_capacity=1,
            instance_type=ec2.InstanceType("c6g.large"),
            machine_image=ecs.EcsOptimizedImage.amazon_linux2(ecs.AmiHardwareType.ARM)
        )
        
        # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
        ec2_task_definition = ecs.Ec2TaskDefinition(self, "TaskDefEc2",
            network_mode=ecs.NetworkMode.BRIDGE
        )# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
        graviton_task_definition = ecs.Ec2TaskDefinition(self, "TaskDefGraviton",
            network_mode=ecs.NetworkMode.BRIDGE
        )
        
        # ec2_task_definition_correto = ecs.Ec2TaskDefinition(self, "TaskDefEc2Correto",
        #     network_mode=ecs.NetworkMode.BRIDGE
        # )
        
        #Get the repos
        repository = ecr.Repository.from_repository_arn(self,"graviton-test", "arn:aws:ecr:us-east-1:366522364779:repository/myrepo")
        #Create a Repo the repos
        #repository = ecr.Repository(self, "graviton-test")
        # add permisions to clusterec2 and clustergraviton to pull images from repository
        
        
        
        containergraviton = graviton_task_definition.add_container("CPUEater-correto",
            # Use an image from DockerHub
            image=ecs.ContainerImage.from_ecr_repository(repository,"correto"),
            memory_limit_mib=1024,
            logging=ecs.LogDrivers.aws_logs(stream_prefix="correto")
        )
        
        
        # containerec2correto = ec2_task_definition_correto.add_container("CPUEater-correto",
        #     # Use an image from DockerHub
        #     image=ecs.ContainerImage.from_ecr_repository(repository,"correto"),
        #     memory_limit_mib=1024,
        #     logging=ecs.LogDrivers.aws_logs(stream_prefix="corretoec2")
        # )
        
        containerec2 = ec2_task_definition.add_container("CPUEater-jdk",
            # Use an image from DockerHub
            image=ecs.ContainerImage.from_ecr_repository(repository,"openjdk"),
            memory_limit_mib=1024,
            logging=ecs.LogDrivers.aws_logs(stream_prefix="openjdk")
        )
        
        # Instantiate an Amazon ECS Service
        ecs_service_ec2 = ecs.Ec2Service(self, "ServiceEC2",
            cluster=clusterec2,
            task_definition=ec2_task_definition
        )
        
        
        # Instantiate an Amazon ECS Service
        ecs_service_graviton = ecs.Ec2Service(self, "ServiceGraviton",
            cluster=clustergraviton,
            task_definition=graviton_task_definition
        )
        
        
        # Instantiate an Amazon ECS Service
        # ecs_service_ec2_correto = ecs.Ec2Service(self, "ServiceEC2Correto",
        #     cluster=clusterec2,
        #     task_definition=ec2_task_definition_correto
        # )
        # ecs_service_ec2.add_placement_strategies(ecs.PlacementStrategy.spread_across_instances())
        # ecs_service_ec2_correto.add_placement_strategies(ecs.PlacementStrategy.spread_across_instances())