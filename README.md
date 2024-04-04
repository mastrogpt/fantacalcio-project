# smart-ai-secretary

An intelligent secretary for showcase site, which notifies you when someone wants to contact you or is interested in your products. 

## Before starting
Please, before starting, make a copy of the `.env.example` file, insert your environment variables there, and then rename that file as `.env`.

You need a backend server with secrets saved, such as google certificate to handle oauth, open ai key and slack hoos to send message.

To handle this complexity, use this repo: 
`https://github.com/AntonioPiga/smart-ai-secretary-backend`
## Developing

Once you've created a project and installed dependencies with `npm install` (or `pnpm install` or `yarn`), start a development server:

```bash
npm run dev

# or start the server and open the app in a new browser tab
npm run dev -- --open
```

## Building

To create a production version of your app:

```bash
npm run build
```

You can preview the production build with `npm run preview`.

> To deploy your app, you may need to install an [adapter](https://kit.svelte.dev/docs/adapters) for your target environment.
