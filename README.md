# CAA RESTful API


## I - What is it?
- It is a RESTful API for a CAA management.
- It uses many technologies: Python, Flask, Swagger, Docker, ...
- It uses docker for containerization

## II - Access the API
- Access the root URL of the API on AWS at [TO BE FILLED]()
- Access it on your machine with docker at [localhost:5000](localhost:5000)
- The root URL uses **Swagger** to show a descriptive list of all available RESTful calls such as `POST`, `DELETE`, `PUT` and `GET`.

## III - Obtain the source code and minimum requirements
1. Download the project
  - Without git
    - Download the ZIP file by clicking [here](https://github.com/CAA-dev/CAABack/archive/master.zip).
    - Extract the ZIP file.
  - With git (recommended)
    - Install git if you don't have it from [git-scm.com](https://git-scm.com/downloads) or use `apt-get install git`.
    - Open a terminal and enter `git clone git@github.com:CAA-dev/CAABack.git`
2. Go to the project directory with a terminal with `cd CAABack`

## IV - Run it on your machine directly
1. run `pip3 install -r requirements.txt`
2. run `python3 src/caa/server.py --config src/caa/config --mode service --log ./log --loglevel DEBUG`

## V - Run it on your machine with docker(NEED TO BE EDITED)
1. Make sure to follow the steps of **III - Obtain the source code and minimum requirements**. 
2. Enter `vagrant up && vagrant ssh` (this will install the box, docker etc.)
3. Enter `python /vagrant/server.py` (in the virtual machine you just logged in)
4. Access the Python Flask server with your browser at [localhost:5000](localhost:5000). You can then make API calls with Swagger.
5. You can also use the Chrome extension `Postman` for example to send RESTful requests such as `POST`. Install it [here](https://chrome.google.com/webstore/detail/postman/fhbjgbiflinjbdggehcddcbncdddomop?hl=en).
6. To update Swagger, refer to the information in the [Github `static` directory]().

## VI - Run it on AWS(NEED TO BE EDITED)


## VII - Run it on a Docker container
1. Cd into project directory
2. Enter `docker build -t caa-back .`
3. Enter `docker run -d -p 5000:5000 caa-back`
    If you want to see the logs, run it without `-d` flag

## VIII - Test driven development and PyUnit
1. If not on Vagrant, install **pip** and enter `pip install nose rednose coverage`
2. Run the server tests and find the test coverage with `nosetests --rednose -v --with-coverage --cover-package=server`
3. Or you can use `coverage run server_test.py && coverage report -m --include=server.py`

## - Behavior driven development and behave
1. Turn vagrant on with `vagrant up && vagrant ssh`
2. Enter `cd /vagrant && behave` and check all the tests pass


