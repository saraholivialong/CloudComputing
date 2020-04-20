Student Name: Sarah Long
Student ID: 120314058

Data retrieval from API:-

1) The EC2 instance was built based on lab work and the instance launched in Putty

2) The file API_query.py was created, by the command nano (See contents in: API_query.py)

3) The python file was run, and the results were obtained from the browser in json form, then converted to csv

4) The csv file was uploaded to github and used in the next segment

Instructions for setup of Cassandra/flask for miniproject:-

1) Build EC2 instance based on lab work and launch instance in Putty

2) Set up the environment by running the following commands where cassandra-CW-A is the container name:

	sudo apt update
	sudo apt install docker.io
	sudo docker pull cassandra:latest
	sudo docker run --name cassandra-CW-a -p 9042:9042 -d cassandra:latest

3) Download the dataset and copy the data from github into the container by running the commands:

	wget -O EUcapitals.csv https://raw.githubusercontent.com/saraholivialong/CloudComputing/master/EUcapitals.csv
	sudo docker cp EUcapitals.csv cassandra-CW-d:/home/EUcapitals.csv

4) Launch the cassandra shell:

	sudo docker exec -it cassandra-CW-a cqlsh

5) Create keyspace for data to be inserted, then create table:

	CREATE KEYSPACE eucities WITH REPLICATION = {'class' : 'SimpleStrategy', 'replication_factor' : 1};
	CREATE TABLE eucities.stats (capital text PRIMARY KEY, alpha2Code text, name text, population int, region text, subregion text);

6) Copy the data into the table:

	COPY eucities.stats (capital, alpha2Code, name, population, region, subregion)
	FROM '/home/EUcapitals.csv'
	WITH DELIMITER=',' AND HEADER=TRUE;

7) Check data by querying, for example:

	SELECT * from eucities.stats WHERE capital = 'London' ALLOW FILTERING;

8) Exit the shell to connect flask to cassandra in the next steps

9) Create requirements.txt file, by the command nano (See contents in: requirements.txt)

10) Create Dockerfile, by the command nano (See contents in: Dockerfile.txt)

11) Inspect the container to check IP Address using the command:

	sudo docker inspect cassandra-CW-a

12) Create coursework.py, by the nano command (See contents in: coursework.py)

13) Ensure the IP address for contact_points matches the one in step (11)

14) Check the cassandra container is running:

	sudo docker ps

15) Build and run the image using the following commands:

	sudo docker build . --tag=cassandrarest:v1
	sudo docker run -p 80:80 cassandrarest:v1

16) Once running, check the functionality of GET, DELETE, POST requests using the below:
	*Make sure to check the IP address of the AWS instance

	Check GET
	GET: http://IPaddress/eucities/Zagreb

	Check DELETE - run DELETE command in another terminal
	DELETE: curl -X "DELETE" http://IPaddress/eucities/Zagreb
	GET: http://IPaddress/eucities/Zagreb

	Check POST - run POST command in another terminal
	POST: curl -X "POST" http://IPaddress/eucities/Metropolis
	GET: http://IPaddress/eucities/Metropolis

	Check PUT - run PUT command in another terminal
	POST: curl -X "PUT" http://IPaddress/eucities/Metropolis
	GET: http://IPaddress/eucities/Metropolis
