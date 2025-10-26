import asyncio
import contextlib
import os
import webbrowser

from dotenv import load_dotenv
from vercel.sandbox import AsyncSandbox as Sandbox

load_dotenv(".env.local") or load_dotenv()


async def main() -> None:
    # Timeout in milliseconds: 10 minutes = 600000ms
    # Defaults to 5 minutes. Max is 5 hours for Pro/Enterprise, 45 minutes for Hobby.
    print("Creating sandbox...")
    sandbox = await Sandbox.create(
        source={
            "url": "https://github.com/vercel/sandbox-example-next.git",
            "type": "git",
        },
        resources={"vcpus": 4},
        timeout=600_000,  # 10 minutes
        ports=[3000],
        runtime="node22",
    )

    print("Installing dependencies...")
    install_cmd = await sandbox.run_command_detached(
        "npm",
        ["install", "--loglevel", "info"],
    )

    # Stream installation logs to console
    async for line in install_cmd.logs():
        print(line.data, end="")

    # Wait for installation to complete and check exit code
    install_result = await install_cmd.wait()
    if install_result.exit_code != 0:
        print("installing packages failed")
        return

    print("Starting the development server...")
    dev_cmd = await sandbox.run_command_detached(
        "npm",
        ["run", "dev"],
    )

    # Stream server logs and detect when it's ready
    ready = asyncio.Event()

    async def stream_logs():
        async for line in dev_cmd.logs():
            print(line.data, end="")
            # Detect when Next.js dev server is ready
            if not ready.is_set() and (
                "ready" in line.data.lower() or "started server" in line.data.lower()
            ):
                ready.set()

    logs_task = asyncio.create_task(stream_logs())
    try:
        await asyncio.wait_for(ready.wait(), timeout=60)  # 60 seconds
    except asyncio.TimeoutError:
        print("Warning: Server readiness detection timed out")

    # Once the server is ready, get the sandbox URL and open it in browser
    url = sandbox.domain(3000)
    print(f"Opening browser at: {url}")
    with contextlib.suppress(Exception):
        webbrowser.open(url)

    print("Server is running. Press Ctrl+C to stop...")
    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down...")

    # Graceful shutdown
    logs_task.cancel()
    with contextlib.suppress(asyncio.CancelledError):
        await logs_task
    await dev_cmd.kill()
    await sandbox.stop()
    await sandbox.client.aclose()


if __name__ == "__main__":
    asyncio.run(main())
