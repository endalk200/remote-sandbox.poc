# Vercel Sandbox (BETA)

> ⚠️ Vercel Sandbox is currently in beta and this POC is done on beta version as Oct 26th 2026

[Official Documentation](https://vercel.com/docs/vercel-sandbox)

Vercel Sandbox is an ephemeral compute primitive designed to safely run untrusted or user-generated code on Vercel.
It supports dynamic, real-time workloads for AI agents, code generation, and developer experimentation.

With Vercel Sandbox, you can:

- Execute untrusted or third-party code: When you need to run code that has not been reviewed, such as AI agent output or user uploads, without exposing your production systems.
- Build dynamic, interactive experiences: If you are creating tools that generate or modify code on the fly, such as AI-powered UI builders or developer sandboxes such as language playgrounds.
- Test backend logic in isolation: Preview how user-submitted or agent-generated code behaves in a self-contained environment with access to logs, file edits, and live previews.
- Run a development server to test your application.

## [Authentication](#authentication)

### [Vercel OIDC token](#vercel-oidc-token)

The SDK uses Vercel OIDC tokens to authenticate whenever available. This is the most straightforward and recommended way to authenticate.

When developing locally, you can download a development token to `.env.local` using `vercel env pull`. After 12 hours the development token expires, meaning you will have to call `vercel env pull` again.

In production, Vercel manages token expiration for you.

### [Using access tokens](#using-access-tokens)

If you want to use the SDK from an environment where `VERCEL_OIDC_TOKEN` is unavailable, you can also authenticate using an access token. You will need

- your [Vercel team ID](https://vercel.com/docs/accounts#find-your-team-id)
- your [Vercel project ID](https://vercel.com/docs/project-configuration/general-settings#project-id)
- a [Vercel access token](https://vercel.com/docs/rest-api/reference/welcome#creating-an-access-token) with access to the above team

Set your team ID, project ID, and token to the environment variables `VERCEL_TEAM_ID`, `VERCEL_PROJECT_ID`, and `VERCEL_TOKEN`. Then pass these to the `create` method:

TypeScript

```typescript
const sandbox = await Sandbox.create({
  teamId: process.env.VERCEL_TEAM_ID!,
  projectId: process.env.VERCEL_PROJECT_ID!,
  token: process.env.VERCEL_TOKEN!,
  ...
});
```

Python

```python
import os
from vercel.sandbox import AsyncSandbox as Sandbox

async def create_with_access_tokens():
    sandbox = await Sandbox.create(
        team_id=os.environ["VERCEL_TEAM_ID"],
        project_id=os.environ["VERCEL_PROJECT_ID"],
        token=os.environ["VERCEL_TOKEN"],
        ...
    )
```

## [System specifications](#system-specifications)

Sandbox includes a `node22` and `python3.13` image. In both of these images:

- User code is executed as the `vercel-sandbox` user.
- The default working directory is `/vercel/sandbox`.
- `sudo` access is available.

|              | Runtime                   | Package managers |
| ------------ | ------------------------- | ---------------- |
| `node22`     | `/vercel/runtimes/node22` | `npm`, `pnpm`    |
| `python3.13` | `/vercel/runtimes/python` | `pip`, `uv`      |

### Available packages

The base system is Amazon Linux 2023 with the following additional packages:

`bind-utils bzip2 findutils git gzip iputils libicu libjpeg libpng ncurses-libs openssl openssl-libs procps tar unzip which whois zstd`

Users can install additional packages using the `dnf` package manager:

TypeScript

```typescript
import { Sandbox } from "@vercel/sandbox";

const sandbox = await Sandbox.create();
await sandbox.runCommand({
  cmd: "dnf",
  args: ["install", "-y", "golang"],
  sudo: true,
});
```

You can find the [list of available packages](https://docs.aws.amazon.com/linux/al2023/release-notes/all-packages-AL2023.7.html) on the Amazon Linux documentation.

### Sudo config

The sandbox sudo configuration is designed to be easy to use:

- `HOME` is set to `/root`. Commands executed with sudo will source root's configuration files (e.g. `.gitconfig`, `.bashrc`, etc).
- `PATH` is left unchanged. Local or project-specific binaries will still be available when running with elevated privileges.
- The executed command inherits all other environment variables that were set.
