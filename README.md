# arnie

This has the source code for the different files that you will need to create the monolith application. The code runs on an ec2 t2.small instance 

# Here are the files that are included 

1. orders.py - this has the main logic of the monolith code. You will need to change the database host name, database name, username and password. You will have to make 5 such changes so that you can connect to the database 

2. convert_api.py - This is flask wrapper that converts the code in orders.py to services that can be called through other programs 

3. database_Create_scripts - This hsa the create statement for the three tables that you will need in the database (RDS mysql). I used a micro but suggest that you use a small. I had a lot of errors with no more connections available with the micro size

For running it without a container, upgrade to python3 on your ec2 instance, install the required libraries as per the requirement.txt file, make changes to the orders.py (database changes).

# Install New Relic APM (python agent) and infra on your ec2 instance. Refer to New Relic Documentation for the same. 

# To run the program, run the following command from your ec2 instance. 
NEW_RELIC_CONFIG_FILE=newrelic.ini newrelic-admin run-program python3 convert_api.py

# Some additional files that you really don't need to run this as a monolith. They convert the entire monolith to a container managed through K8 (EKS)

a. Dockerfile - self explanatory 
b. requirement.txt - has all the dependencies that you will need
c. deployment.yaml - has the deployment file to be used for creating a cluster using kubectl 
d. cluster.yaml - configuration file for creating a eks cluster using eksctl 

You would have to first create a docker container with the necessary changes to your orders.py (database related changes), upload that to your docker repository and update the image tag in your deployment.yaml before you can run it in containers. 


# How to generate Load with the application

I used Jmeter to Load test the application. Download Jemeter on your laptop and create the following tests. 

Find Customers 
<your aws machine ip>/get_customer_details?num=<customer_id>
  
Find orders 
<your aws machine ip>/get_order_details?num2=<order_id>

Create customers 
<your aws machine ip>/create_customer?customer_name=<name>&customer_add=<address>&customer_phone=<phone>

create orders 
<your aws machine ip>/create_order?cust_id=<customer_id>&order_item=<order Item>&order_value=<Value of order>&shipper=<shipper_name>
  Note the your should put the customer_id with an id that already exists in your database 
 
