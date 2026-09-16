# Django Backend

### Built With

* [Docker](https://www.docker.com/)
* [Django](https://www.djangoproject.com/)

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple example steps:

### Prerequisites

* Docker Installation - Download apporpirate Docker installtion file for your OS: https://docs.docker.com/get-docker/

### Installation and setup

1. Once docker is installed, clone the repo on you local folder:

   ```sh
   git clone https://github.com/stjude-biohackathon/KIDS23-Team11.git
   ```
2. Copy LLM model into `backend/models/` folder. The folder structure can be similar to the following:

   ```sh
   backend/models/biogpt_finetuned/
   	config.json
   	merges.txt
   	pytorch_model.bin
   	special_tokens_map.json
   	tokenizer_config.json
   	training_args.bin
   	vocab.json
   ```
2. Go to the repo root and run this docker commands to build image (will take few minute for first time, should be faster on sunsequent run): 

   ```sh
   docker compose build
   ```

3. Start database container first using following command:

   ```sh
   docker compose up db
   ```
   Once you see following LOG in terminal, go to next step:

   ```sh
	pubgpt-db-1  | LOG:  database system is ready to accept connections
   ```
4. Open new terminal tab and start Django app container using following command:

   ```sh 
   docker compose up backend
   ```
   It should take sometime to load the app as it's downloading LLM models and preparing the apps.
   Once you see following LOG in terminal, the app is ready!
   ```sh
   pubgpt-backend-1  | Starting development server at http://0.0.0.0:8000/
   pubgpt-backend-1  | Quit the server with CONTROL-C.
   ```

<p align="right">(<a href="#top">back to top</a>)</p>


<!-- USAGE EXAMPLES -->
## Usage

To test the app, go to the homepage: http://localhost:8000/
When app is launched for the first time, it will load sample database from GPCRdb Protein family query and sample CSV file from `/raw_data/` folder.
Explore REST api queires at following page: http://localhost:8000/api/

To query the LLM models, use the following API endpoint:
http://localhost:8000/api/biogpt_finetuned/ OR
http://localhost:8000/api/biogpt_original/

The API endpoint accepts data as POST query, and the content of payload should be like this:
```json
{
	"text": "What is the function of BRAF gene?",
}

``` 

To post new data, go to database use the following API endpoint:
http://localhost:8000/api/post_question_answer/

The JSON object for post must following this format:
```json
{
	"text": "What is the meaning of life?",
	"type": "general",
	"answers": [
		{
			"type": "ChatGPT",
			"text": "Menaing of life is to be happy.",
			"score": "positive"
		},
		{
			"type": "BioGPT",
			"text": "Meaning of life is to achieve your goals.",
			"score": "neutral"
		},
		{
			"type": "AI21",
			"text": "Meaning of life is to not die.",
			"score": "negative"
		},
		{
			"type": "OpenAssistant",
			"text": "Meaning of life is to be always learning.",
			"score": "positive"
		}
	]
}
```

<p align="right">(<a href="#top">back to top</a>)</p>