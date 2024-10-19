# Nuvolaris MastroGPT

Build AI applications easily with MastroGPT!

## Setup

You can set up the project in two main ways:

1. **Online** with Nuvolaris and Codespaces (recommended if you have a nuvolaris.dev account)
2. **Locally** (frontend only) using npm

**Please note that chatbot and articles functions will not be available in this repository.**

### 1. Online Setup (RECOMMENDED)

To use the full project, including Nuvolaris integration, follow these steps:

- Create a GitHub account
- Log into your account on [nuvolaris.dev](https://nuvolaris.dev). If you don't have an account, request one by contacting the Nuvolaris team on [Telegram](https://t.me/+EOZM_0Pj-dI3YjBk)
  
- In the `Starters` section on the sidebar, click `Connect` to link the MastroGPT app and install the Nuvolaris GitHub app into your GitHub account.
- In the same section, select the **Fantacalcio Project** and click `OPEN IN CODESPACE`.
  - **Note**: You can also manually fork this repo into your GitHub account and start a Codespace from there.
- A Codespace with a `devcontainer` file will launch and install all dependencies in a VSCode remote environment.


  1. Edit the `src/lib/store/store.ts` file: modify the `getApiHost` function by replacing `fantatest` with your namespace. This will connect you to your own database provided by Nuvolaris.
  2. To view the database connection string, open the VSCode remote terminal and run the command `nuv -config -d`. This will show all Nuvolaris variables (these variables are also available in the backend using `#--param {chooseYourName} ${variableName}`).
     

- **Note**: By default, you'll be connected to the **fantatest.nuvolaris.dev** environment, which is why you can see all articles, player info, and stats. If you want to connect to your own database (even if you don't need it, because will be empty and for fantacalcio project you'll have all data provided by fantatest.nuvolaris.dev):
---

## Development

Use the Nuvolaris icon in the interface or run the following commands from the terminal to manage development and deployment:

- **`login`** (`nuv ide login`): Log in using your Nuvolaris account credentials
- **`devel`** (`nuv ide devel`): Start a local development environment
- **`deploy`** (`nuv ide deploy`): Deploy the project to your custom domain `{username}.nuvolaris.dev`

You can explore more options by running `nuv ide` to see additional subcommands.

### 2. Local Setup (Frontend Only)

To work only on the frontend without the Nuvolaris backend integration, follow these steps:

- Install VSCode or your preferred IDE
- Clone this repo
- Open it in VSCode
- Copy the `.env` file from the `packages` folder to the `src` folder
- Run `npm install` and then `npm run dev` to start the local environment

**Note:** This setup connects you to the **fantatest account** on Nuvolaris, and you will only be able to modify the frontend side of the project.
