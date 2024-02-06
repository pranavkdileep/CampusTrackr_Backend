

<p align="center">
 <img width="100px" src="https://github.com/pranavkdileep/CampusTrackr_Backend/blob/main/Docs/icon%20(2).png?raw=true" align="center" alt=":package: Deploy CampusTrackr_Backend" />
 <h2 align="center">:package: Deploy CampusTrackr_Backend</h2>
 <p align="center">This document provides a step-by-step guide on how to deploy the CampusTrackr_Backend, a cloud-based software platform for the education domain1. The CampusTrackr_Backend is a GitHub repository that contains the source code and configuration files for the backend services of CampusTrack2. By following this guide, you will be able to set up and run the CampusTrackr_Backend on your own server or cloud provider.</p>
</p>

  <p align="center">
    <a href="https://github.com/pranavkdileep/CampusTrackr_Backend/issues">
      <img alt="Issues" src="https://img.shields.io/github/issues/pranavkdileep/CampusTrackr_Backend?style=flat&color=336791" />
    </a>
    <a href="https://github.com/pranavkdileep/CampusTrackr_Backend/pulls">
      <img alt="GitHub pull requests" src="https://img.shields.io/github/issues-pr/pranavkdileep/CampusTrackr_Backend?style=flat&color=336791" />
    </a>
    <br />
  <a href="https://github.com/pranavkdileep/CampusTrackr_Backend/issues/new/choose">Report Bug</a>
  <a href="https://github.com/pranavkdileep/CampusTrackr_Backend/issues/new/choose">Request Feature</a>
  </p>
  <h3 align="center">Systems on which it has been tested.</h3>
 <p align="center">
  <a href="https://ubuntu.com/download">
      <img alt="Ubuntu" src="https://img.shields.io/badge/Ubuntu-E95420?style=flat&logo=ubuntu&logoColor=white" />
    </a>
  <a href="https://www.microsoft.com/pt-br/software-download/windows10">
      <img alt="Windows" src="https://img.shields.io/badge/Windows-0078D6?style=flat&logo=windows&logoColor=white" />
    </a>
  </p>


<p align="center"><strong></strong>✨</p>

# Getting started
 [<img width="300px" src="https://github.com/pranavkdileep/CampusTrackr_Backend/blob/main/Docs/Download%20Android%20APK%20Badge.png?raw=true" align="center" />](https://github.com/pranavkdileep/CampusTracker-Cloud-ANDROID/releases/download/1.0/app-release.apk)

## Demo

URL : https://pranavkd-campus.hf.space/ 

KEY : 12345678

ADMIN ID : 0

ADMIN PASSWORD : 12345678


## How it Works

This project is a backend server that provides APIs for a mobile application that interacts with a college database. It is built using FastAPI, a modern and fast web framework for Python.

The following diagram illustrates the architecture and the workflow of the project:

    +-----------------+      +-----------------+      +-----------------+
    |                 |      |                 |      |                 |
    |  Mobile App     | <--> |  Backend Server | <--> |  MySql Server |
    |                 |      |                 |      |                 |
    +-----------------+      +-----------------+      +-----------------+

## Running On Server
Tutorial Video

<video src="https://github.com/pranavkdileep/CampusTrackr_Backend/raw/main/Docs/Screencast%20from%202024-02-06%2011-04-39.webm"></video>

ENV Example :

    DB_HOST=aws.connect.psdb.cloud
    DB_USERNAME=6k6cemv23561hs4rmkmf
    DB_PASSWORD=pscale_pw_CcYwSoG4zi16pJ5laqRd
    DB_NAME=student
    DB_PORT=3306
    SSL_MODE=false
    TOKEN=12345678
    ADMIN_PASSWORD=12345678
For Setup Database Go To The Url Once `https://{server ip:8000 or domain}/setupDatabase`

For Setup Easypanel on Your Cloud Server Watch The Video Click Here


## Running Locally

### With Docker Compose

```bash
docker-compose up
```

### With Docker

```bash
# Build the Docker image
docker build -t CampusTrackr_Backend .

# Run the Docker container
docker run -p 8000:8000 CampusTrackr_Backend

```

### With uvicorn

#### Install dependencies

```bash
pip install -r requirements.txt
```

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

Your Bakend Url Will be  `http://localhost:8000/`. or `http://{server ip or domain}/`


## 🤝 Contributing

Contributions, issues and feature requests are welcome!<br />Feel free to check [issues page](issues).

## Show your support

Give a ⭐️ if this project helped you!

Or buy me a coffee 🙌🏾

<a href="https://www.buymeacoffee.com/pranavkdileep">
    <img src="https://img.buymeacoffee.com/button-api/?text=Buy me a coffee&emoji=&slug=hebertcisco&button_colour=FFDD00&font_colour=000000&font_family=Inter&outline_colour=000000&coffee_colour=ffffff" />
</a>

## 📝 License

Copyright © 2024 [PRANAV K DILEEP](https://github.com/pranavkdileep).<br />
This project is [MIT](LICENSE) licensed.
