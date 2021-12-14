# bookworm

For our project, we have created a book track keeper service in AWS and have used the RDS Aurora Database accessible via Amazon EC2 and have linked it to MySQL. MySQL has been further linked to Python Flask to make our website connected with AWS. 

The architectural design of the project is as follows - 

The first component is the VPC. VPC is a Virtual Private cloud, which is a logically isolated section of AWS cloud where we can launch AWS resources. All the resources are launched in the VPC that we have created. We have made the VPC accessible from Internet using Internet gateway. We have further divided the VPC into subnets. The route table is used to direct incoming or outgoing traffic. Network ACLs are used to allow or deny traffic to subnets. We have created an EC2 instance here, and the security groups are used to allow or deny traffic to an EC2 instance. We also have Amazon Aurora, which is a database in AWS. 

In short, we performed the following steps to create our project. First, we created the VPC and attached an Internet gateway to it to make our VPC accessible from the internet. We then created one Public and two Private subnets. Then, we created an EC2 instance in the public subnet which can be accessible from outside the VPC. Further, we created an RDS Aurora cluster in Private subnets to ensure that the database is not accessible from outside our VPC. So, our RDS Aurora is accessible from outside VPC only via the EC2 instance in the public subnet. We connected this to our database using MySQL workbench. 

