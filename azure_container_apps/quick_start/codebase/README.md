# Containerizing the API

This guide will walk you through the steps to run and containerize the microservice created in `step10_microserice_db`.

## Prerequisites

- Ensure you have Python and [Poetry](https://python-poetry.org/docs/#installation) installed.
- Ensure you have Docker installed and running on your machine.

## Running the App without Docker

### Update `pyproject.toml`

Use the following as a base for your `pyproject.toml` file:
[Full Stack FastAPI Template - `pyproject.toml`](https://github.com/tiangolo/full-stack-fastapi-template/blob/master/backend/pyproject.toml)

Review each dependency in the `toml` file to understand the different libraries used in development.

### Install Dependencies

Install the project dependencies using Poetry:

<div>
  <button onclick="copyToClipboard('#install-command')">Copy</button>
  <pre id="install-command"><code>poetry install</code></pre>
</div>

###  Run the Project

Run the project in the Poetry environment to see if it is running outside a container:

<div>
  <button onclick="copyToClipboard('#run-command')">Copy</button>
  <pre id="run-command"><code>poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000</code></pre>
</div>

###  Open in Browser

- [API Root](http://0.0.0.0:8000/)
- [API Documentation](http://0.0.0.0:8000/docs)
- [OpenAPI JSON](http://0.0.0.0:8000/openapi.json)

### Run Tests

Run tests to ensure everything is working correctly:

<div>
  <button onclick="copyToClipboard('#test-command')">Copy</button>
  <pre id="test-command"><code>poetry run pytest</code></pre>
</div>

##  Containerizing the App

Follow the FastAPI Docker deployment guide: [FastAPI Deployment - Docker](https://fastapi.tiangolo.com/deployment/docker/)

###  Check Docker Installation

Ensure Docker is installed and running:

<div>
  <button onclick="copyToClipboard('#docker-version-command')">Copy</button>
  <pre id="docker-version-command"><code>docker version</code></pre>
</div>

###  Build the Docker Image for Development

Build the Docker image using the `Dockerfile.dev`:

<div>
  <button onclick="copyToClipboard('#docker-build-command')">Copy</button>
  <pre id="docker-build-command"><code>docker build -f Dockerfile.dev -t my-dev-image .</code></pre>
</div>

###  Check Docker Images

List Docker images to verify the new image:

<div>
  <button onclick="copyToClipboard('#docker-images-command')">Copy</button>
  <pre id="docker-images-command"><code>docker images</code></pre>
</div>

###  Verify Docker Image Configuration

Inspect the Docker image configuration:

<div>
  <button onclick="copyToClipboard('#docker-inspect-command')">Copy</button>
  <pre id="docker-inspect-command"><code>docker inspect my-dev-image</code></pre>
</div>

###  Run the Docker Container for Development

Run the container in detached mode and map the port:

<div>
  <button onclick="copyToClipboard('#docker-run-command')">Copy</button>
  <pre id="docker-run-command"><code>docker run -d --name dev-cont1 -p 8000:8000 my-dev-image</code></pre>
</div>

###  Check in Browser

- [API Root](http://localhost:8000)

###  Container Logs

View container logs:

<div>
  <button onclick="copyToClipboard('#docker-logs-command')">Copy</button>
  <pre id="docker-logs-command"><code>docker logs dev-cont1</code></pre>
</div>

###  Test the Container

Run tests inside the container:

<div>
  <button onclick="copyToClipboard('#docker-test-command')">Copy</button>
  <pre id="docker-test-command"><code>docker run -it --rm my-dev-image /bin/bash -c "poetry run pytest"</code></pre>
</div>

###  List Running Containers

List currently running containers:

<div>
  <button onclick="copyToClipboard('#docker-ps-command')">Copy</button>
  <pre id="docker-ps-command"><code>docker ps</code></pre>
</div>

###  List All Containers

List all containers, including stopped ones:

<div>
  <button onclick="copyToClipboard('#docker-ps-a-command')">Copy</button>
  <pre id="docker-ps-a-command"><code>docker ps -a</code></pre>
</div>

###  Interact with the Container

Access the container shell:

<div>
  <button onclick="copyToClipboard('#docker-exec-command')">Copy</button>
  <pre id="docker-exec-command"><code>docker exec -it dev-cont1 /bin/bash</code></pre>
</div>

###  Exit from the Container Shell

Exit from the container shell:

<div>
  <button onclick="copyToClipboard('#exit-command')">Copy</button>
  <pre id="exit-command"><code>exit</code></pre>
</div>

