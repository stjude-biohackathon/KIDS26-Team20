# MyGPT Backend Setup Guide

This guide will walk you through the steps to set up the MyGPT backend on your local machine.
Following instructions are for MacOS only, other OS users may need to adapt the steps accordingly.

## Requirements

To Run the MyGPT pipeline, we will need the following minimum specifications for your system:

*   8 CPUs
*   8 GB Memory (16 GB or more for better response time)
*   10 GB hard-drive storage

We will also need several tools to run the pipeline:

*   Brew
*   Git
*   Docker
*   Ollama

## Requirements installation

We will install these required tools in the following steps:

1. **Brew installation**

	Check if you have `brew` installed on your system by running following command.

	```
	brew --version
	```

	If you get error that `brew not found`, you can install brew by folliwng command from the new terminal window (similar to Jupyter installation but open new tab for terminal without closing existing window that's running Jupyter). For more details about brew check this [page](https://brew.sh/)

	```
	/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
	```

2.  **Brew packages installation**

	We will install Brew packages by running following commands:

	```
	brew install git
	```

3. **Docker installation**

	To run MyGPT with CPUs-only, the entire pipeline will run as a single unit from Docker.
	Check if you have `docker` installed on your system by running following command.

	```
	docker --version
	```

	If you get an error that `docker not found`, go to the official Docker installation page for Mac and install the appropriate Docker on your system: https://docs.docker.com/desktop/install/mac-install/

	You can change Docker setting to match requirements for MyGPT:
	<img src="./MyGPT_backend/installation/images/docker_resources.png?raw=true" width="700px">


4. **Ollama installation**

	Finally, download and install Ollama by following instructions from this offical [Ollama site](https://ollama.ai/)

	You can check if Ollama is running by visiting http://localhost:11434/ in your default browser.

> [!CAUTION]
> After installing Ollama, close any open Terminal/Command Prompt before you pull the nomic embedding model, which is best performing embedding model for MyGPT pipeline, by running following command:

```
ollama pull nomic-embed-text
```

## MyGPT backend installation

### Build docker images from source code

1. **Get copy of source code for this repository**

	If you don not have the source code for this GitHub repository, we will first get the source code by running following command. It will create `KIDS-Team20` folder on your Desktop.

	```
	git clone https://github.com/stjude-biohackathon/KIDS26-Team20.git
	```

2. **Build docker images**

	We will run following script to build docker images:

	```
	cd KIDS26-Team20
	bash MyGPT_backend/installation/macOS/build_docker.sh
	```

	Before starting containers, replace all placeholders in `.env_backend` if you have different configuration requirements.

3. **Run docker containers**

	We will run following script to run docker containers:

	```
	bash MyGPT_backend/installation/macOS/run_docker.sh
	```

	This script should take around 5-10 minutes to run.
	While above script is running, it will open several pages in your default browser. 
	You can see status of different components of MyGPT pipeline on these pages.
	* backend: http://localhost:8000/

		<img src="./MyGPT_backend/installation/images/backend_server.png?raw=true" width="500px">

## Test the running MyGPT backend

After the containers are running and the backend is available at
http://localhost:8000/, open a new terminal in the repository root and run the
live context endpoint test:

```bash
python scripts/test_mygpt_backend.py
```
