# Portfolio Management RESTful API
*The project was developed for the DevOps course of New York University (CSCI-GA.3033-014).*

[![Build Status](https://travis-ci.org/qdm12/Devops_RESTful.svg?branch=master)](https://travis-ci.org/qdm12/Devops_RESTful)
[![Code Climate](https://codeclimate.com/github/qdm12/Devops_RESTful/badges/gpa.svg)](https://codeclimate.com/github/qdm12/Devops_RESTful)
[![Test Coverage](https://codeclimate.com/github/qdm12/Devops_RESTful/badges/coverage.svg)](https://codeclimate.com/github/qdm12/Devops_RESTful/coverage)
[![Issue Count](https://codeclimate.com/github/qdm12/Devops_RESTful/badges/issue_count.svg)](https://codeclimate.com/github/qdm12/Devops_RESTful)

**Bluemix at https://portfoliomgmt.mybluemix.net**

[![Bluemix](https://img.shields.io/website-up-down-green-red/http/shields.io.svg)](https://portfoliomgmt.mybluemix.net)

**Bluemix container at https://portfoliocontainer.mybluemix.net**

[![Bluemix container](https://img.shields.io/website-up-down-green-red/http/shields.io.svg)](https://portfoliocontainer.mybluemix.net)

**Github page and Swagger (Bluemix)**
Access it at [https://qdm12.github.io/Devops_RESTful/index.html](https://qdm12.github.io/Devops_RESTful/index.html).

## I - What is it?
- It is a RESTful API for a CAA management.
- It uses many technologies: Python, Flask, Swagger, Docker, ...
- It uses docker for containerization

## II - Access the API
- Access the root URL of the API on AWS at [TO BE FILLED](https://portfoliomgmt.mybluemix.net)
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
6. To update Swagger, refer to the information in the [Github `static` directory](https://github.com/qdm12/Devops_RESTful/tree/master/static).

## VI - Run it on AWS(NEED TO BE EDITED)
1. Make sure to follow the steps of **III - Obtain the source code and minimum requirements** although you don't need Vagrant.
2. Login to Bluemix as follows:
  - `cf login https://api.ng.bluemix.net -u username -o organization -s "Portfolio Management"`
  - Enter the API endpoint as `https://api.ng.bluemix.net`
  - Enter your password
3. Enter `cf push PortfolioMgmt`
4. You can then access it at [https://portfoliomgmt.mybluemix.net](https://portfoliomgmt.mybluemix.net)


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

## For ongoing work, please refer to this page:
[https://github.com/rofrano/nyu-homework-2](https://github.com/rofrano/nyu-homework-2)
- PART 1: Deploy the service in Docker Containers on Bluemix (submit URL of service on Bluemix)
- PART 2: BDD and TDD Automated Testing (Good testing coverage required)
- PART 3: Add an automated CI/CD DevOps Pipeline

