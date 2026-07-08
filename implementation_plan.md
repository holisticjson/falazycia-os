# Implementation Plan - Resolving Vertex AI and AWS Bedrock Model Issues

In order to resolve the issues with GCP Vertex AI (Gemini 3.5/3.1 models returning 403 or 404, depending on the endpoint used) and AWS Bedrock ("ThrottlingException: Too many tokens per day"), we need to adjust the configuration and run comprehensive verification tests.

## User Review Required

> [!WARNING]
> The AWS Bedrock error `ThrottlingException - {"message":"Too many tokens per day..."}` is a strict quota enforcement from AWS. Even though they sent confirmation emails about increasing limits, the actual limit change in the AWS console is either still propagating, or was applied to the base models only (e.g. `anthropic.claude-sonnet-4-6` in `us-east-1` directly) rather than the cross-region inference profiles (e.g. `eu.anthropic.claude-sonnet-4-6`).
> We have successfully tested `gemini-2.5-flash` and `gemini-2.5-pro` via Vertex AI and they work perfectly.
>
> To use `gemini-3.5-flash` or `gemini-3.1-pro` via the Google AI Studio (generativelanguage) endpoint, you need to enable the **Gemini API** on your Google Cloud Console for the project.

## Open Questions

- *None at this moment.* The technical realities are clear: the Gemini API (`generativelanguage.googleapis.com`) needs to be enabled for your project to use Google AI Studio endpoints. For AWS Bedrock, the daily token limit is being enforced by AWS, and we should check if they can be contacted or if we can use native models (if only those were updated).

## Proposed Changes

We will configure `litellm_config.yaml` to include appropriate backups and direct mappings. We will also update the configuration file on the remote server and make sure the `pm2` process starts up and runs without crashing.

### Configurations

#### [MODIFY] [litellm_config.yaml](file:///c:/Aplikacje%20MVP/Holistic%20Jason/litellm_config.yaml)
We will define the following models:
1. `hermes-fast` mapped to `vertex_ai/gemini-2.5-flash` (Active, fast, works, low cost).
2. `hermes-think` mapped to `vertex_ai/gemini-2.5-pro` (Active, smart, works).
3. `gemini-3.5-flash` mapped to `gemini/gemini-3.5-flash` (using the Developer API key).
4. `gemini-3.1-pro` mapped to `gemini/gemini-3.1-pro` (using the Developer API key).
5. `bedrock/anthropic.claude-sonnet-4-6` mapped to `bedrock/eu.anthropic.claude-sonnet-4-6` (with `bedrock/anthropic.claude-sonnet-4-6` as a fallback or vice-versa).
We will also provide a fallbacks block so that if Bedrock fails due to throttling (which is currently the case), it falls back to `hermes-think` or `hermes-fast` rather than crashing or returning a raw 400/429 error.

#### [MODIFY] [Remote configuration files](file:///home/holisticjson/litellm/config.yaml)
We will upload/write the new configuration on the remote machine `HermesGCP` and verify the PM2 process.

## Verification Plan

### Automated Tests
1. Run local query tests:
   `ssh HermesGCP "python3 /home/holisticjson/query_fast.py"`
2. Verify that querying a model that currently fails (like Bedrock or 3.5) falls back gracefully if configured, or that we receive the correct error message.
