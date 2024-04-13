# Nuvolaris MastroGPT

Build easily AI applications with MastroGPT!

# Setup

You can run Nuvolaris Starter: 
- Online with Codespace 
- Locally with Docker

## Online Setup 

- Get a GitHub account
- Fork this repo in your own account
- Start it with Codespaces (you have 60 free hours)
- See below for setup.

## Local Setup 

- Install Docker and VScode in your machine
- Clone this repo
- Open it in VSCode
- Press F1  and the "Reopen in Container"

# Environments and Secrets

- Copy the `.env.example` in `.env`
- Add your secrets there (do not commit them - it is in .gitignore)
- Add non secrets envirornment variables in packages/.env
- Pass secrets and environments to your function with `#--param ARGUMENT "$VARIABLE"`
- Read the secrets as function arguments

# Development

Use the Nuvolaris Icon to execute the functions, or use the following commands from the terminal:

- `devel` (or `nuv ide devel` to run a local development environment
- `deploy` (or `nuv ide deploy`) to deploy everything in cloud
- `login` (or `nuv ide login`) to login again

Check `nuv ide` subcommand for more options.
