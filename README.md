<div align="center">
<h1 align="center">AWS Graviton Comparison with Java Corretto vs Java OpenJDK</h1>
</div>




<img src="https://d2908q01vomqb2.cloudfront.net/f1f836cb4ea6efb2a0b1b99f41ad8b103eff4b59/2021/04/10/Site-Merch_Graviton_SocialMedia_2.jpg" width="100%">


### [Contributions are Welcome]

## Description

This implementation is ment to show the difference in performance between a Graviton instance and a T2 running the same Java application. The key difference for this comparison to work is ussing Java Correto for the Graviton instances and plain OpenJDK for the T2 instances.



## How Deploy

### Build the images

- **Build** the graviton image located in the Graviton2 folder, to do so, you either need to have Docker with extensions(experimental) ennabled or install it, you might follow this instructions: [Quickly build ARM docker images](https://aws.amazon.com/blogs/compute/how-to-quickly-setup-an-experimental-environment-to-run-containers-on-x86-and-aws-graviton2-based-amazon-ec2-instances-effort-to-port-a-container-based-application-from-x86-to-graviton2)
- **Build** the plain java application
- **Push** both images to an existing repository with the openjdk and correto tags respectively `:openjdk` `:correto`
- **Deploy** the CDK, remember to change the repository location in the `ecsgraviton_stack.py` file then just do the `cdk deploy`
- Note: You might want to include or run any other Java application for comparison of your specific usecase, just add the application to the Dockerfile and overwrite the entrypoint

<div align="center">
  
[Deployment](https://github.com/gasamoma/Ec2vsGraviton/assets/14201087/cc9145c0-b1d2-4745-837a-049391aa041b)

</div>

## About the project.

### Performance comparison
<div align="center">

[Media_performance_comparison.webm](https://github.com/gasamoma/Ec2vsGraviton/assets/14201087/acf90acf-b144-4f14-8fde-cd4e517078a6)

</div>


- The main idea is to create a fast way to create Java application comparison for customers that are currently running ECS with EC2 or Fargate, and want to get the improvements of using Graviton2.
- The use of this code is completely free, if you are sharing thi with a cusomer ensure to clarify that AWS does not offer support on the current build, tho I'll do my best to keep it up to date


## Buildx setup

```
export DOCKER_BUILDKIT=1
docker build --platform=local -o . git://github.com/docker/buildx
mkdir -p ~/.docker/cli-plugins
mv buildx ~/.docker/cli-plugins/docker-buildx
chmod a+x ~/.docker/cli-plugins/docker-buildx
docker run --privileged --rm tonistiigi/binfmt --install all 
docker buildx create --name mybuild --use 
docker buildx inspect --bootstrap 
docker buildx build --platform linux/amd64,linux/arm64 --tag ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/myrepo:latest --push .
```

If you are using new docker versions you only need to login and build
```
aws ecr create-repository --repository-name myrepo --region=us-east-1
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com
cd Graviton2
docker buildx build --platform linux/amd64,linux/arm64 --tag ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/myrepo:openjdk --push .
cd ../PlainJava
docker buildx build --platform linux/amd64,linux/arm64 --tag ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/myrepo:correto --push .
```

## Cleanup
<div align="center">

[Media_destroy.webm](https://github.com/gasamoma/Ec2vsGraviton/assets/14201087/2091915b-4224-44ab-9031-e781799648b3)

</div>

## Future scope

- Add MVN to the example 

## Support on Beerpay

Hey if you find this usefull share me your story @gasamoma or with a couple of  :beers:! :)
