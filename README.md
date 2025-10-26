# Remote Sandbox Platform Comparison

Experimental repository for testing and comparing remote sandbox execution platforms
for AI agents, code execution, and secure computing.

## Overview

This repo serves as a testing ground for evaluating different sandbox platforms
that enable secure execution of untrusted code. Each platform will be tested,
documented, and compared based on features, performance, developer experience,
and use cases.

## Platforms Under Evaluation

### 1. Daytona

- **Type**: Secure infrastructure for running AI-generated code
- **Runtime**: Full Linux environments with Docker support
- **Key Features**:
  - Sub-90ms sandbox creation time
  - Isolated runtime protection for AI-generated code
  - Massive parallelization for concurrent workflows
  - Programmatic control via SDK (Process, File System, Git, LSP APIs)
  - Stateful by design - sandboxes run indefinitely
  - Environment snapshots for save/restore workflows
  - Multi-region deployment options
  - Computer Use sandbox (Linux, macOS, Windows)
  - Docker compatibility (Docker-in-Docker, Dockerfile support)
  - Pay-as-you-go pricing model
- **SDKs**: Python, TypeScript
- **Primary Use Cases**: AI agents, code interpreters, coding agents, data analysis, computer use automation

### 2. Cloudflare Sandbox

- **Type**: Secure code execution on Cloudflare's edge network
- **Runtime**: Full Linux environment (Amazon Linux 2023) with Node.js 22 and Python 3.13
- **Key Features**:
  - Built on Cloudflare Containers
  - Execute commands, manage files, run background processes
  - Expose services via preview URLs
  - Code execution with rich outputs (charts, tables, images)
  - Persistent state between executions
  - Real-time output streaming
  - sudo access available
  - Integrated with Cloudflare Workers
  - OIDC token authentication
- **SDKs**: TypeScript, Python
- **Primary Use Cases**: AI code execution, data analysis & notebooks, interactive development environments, CI/CD systems
- **Pricing**: Available on Workers Paid plan, based on Containers platform pricing

### 3. Vercel Sandbox

- **Type**: Ephemeral compute for running untrusted code on Vercel
- **Runtime**: Node.js 22 and Python 3.13 on Amazon Linux 2023
- **Key Features**:
  - Ephemeral sandboxes for dynamic workloads
  - Execute untrusted or user-generated code
  - Real-time workloads for AI agents
  - Port exposure for development servers
  - Resource allocation (configurable vCPUs)
  - Git repository cloning (public & private)
  - Timeout configuration (up to 5 hours Pro/Enterprise)
  - Integrated observability dashboard
  - OIDC or access token authentication
  - sudo access with preserved environment
- **SDKs**: TypeScript, Python
- **Primary Use Cases**: AI agent code execution, code generation tools, developer playgrounds, testing backend logic, running dev servers
- **Pricing**: Available in Beta on all plans

## Repository Structure

```
/
├── daytona/          # Daytona experiments and POCs
├── vercel-sdk/       # Vercel AI SDK experiments
├── cloudflare/       # Cloudflare service experiments
└── docs/             # Documentation and findings
```

## Experimentation Goals

- Test sandbox creation speed and reliability
- Evaluate API/SDK ergonomics and developer experience
- Compare pricing models and cost-effectiveness
- Assess security and isolation features
- Document limitations and edge cases
- Create sample applications demonstrating each platform's strengths

## Notes

Each platform folder will contain:

- Setup instructions
- Sample code and experiments
- Performance benchmarks
- Documentation of findings
- Pros/cons analysis
