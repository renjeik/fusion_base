# Fusionbase RESTful API using Flask

## Quick Start

Clone the repo:

```bash
git clone --depth 1 https://github.com/renjeik/fusion_base.git
```

## (Optional) Anaconda setup

If you need multiple python version in your local machine, you can setup a virtual environment for each version.

The enviroment that we are going to use throughout this project is Anaconda.

Download and install it conda, from https://www.anaconda.com/.

Open Anaconda Prompt/Terminal and create an environment using the command:

```bash
conda create --name <NAME OF ENVIRONMENT> python=3.11.4 -y
```

Next, activate the environment using the command:

```bash
conda activate <NAME OF ENVIRONMENT>
```

You will notice that the name of the current activated name is shown in the command line, like:

```bash
(<NAME OF ENVIRONMENT>) current/working/directory>
```

Make sure to check the name of the environment everytime you run a command in a terminal.

Within the terminal, direct yourself to fusion_base's folder and continue with installation of requirements.

```bash
pip install -r requirements.txt
```

To run an app, simply run:

```bash
python app.py
```

Open the browser and call the HTTP GET request to:

```bash
http://localhost:5000/search?query=<TITLE OF THE BOOK>
```

OR

```bash
http://127.0.0.1:5000/search?query=<TITLE OF THE BOOK>
```
