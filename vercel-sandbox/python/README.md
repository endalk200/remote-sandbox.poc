## Getting Started

Install dependencies

```bash
uv install
```

Login to Vercel using vercel cli

```bash
vercel login
```

Create a new project or link to an existing project

`vercel link`

Then pull the project's environment variables:

`vercel pull env`

This pulls a Vercel OIDC token into your `.env.local` file that the SDK will use to authenticate with.
