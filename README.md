# Nukleio-Uptime-Trigger

## Author: Eric Nohara-LeClair

This project contains an AWS Lambda function that calls the `getUserData` endpoint daily to keep the Supabase free tier project active. This Supabase project is the BAAS for my Portfolio Website Manager project, used to power my Managed Portfolio Website.

## Table of Contents

- [Overview](#overview)
- [How It Works](#how-it-works)
- [Deployment](#deployment)
- [Environment Variables](#environment-variables)
- [Usage](#usage)

## Overview

Supabase free tier projects can become inactive if not accessed regularly. If this happens, my portfolio website will fail to retrieve my user information from the Portfolio Manager. This Lambda function is scheduled to run every day and make a request to the `getUserData` endpoint, ensuring the project remains active even during a long period of nobody accessing my Portfolio site or the Portfolio Manager.

## How It Works

- The Lambda function uses Python and the `requests` library.
- It retrieves configuration (API URL, API key, user email) from environment variables.
- On execution, it sends a GET request to the specified endpoint with the required headers.
- It uses credentials for a special Timer Trigger user who exists only for this function.

## Deployment

Deployment is automated using GitHub Actions. On every push to the `main` branch:

- Dependencies are installed.
- The function and dependencies are zipped.
- The package is deployed to AWS Lambda using the AWS CLI.

## Environment Variables

Set the following environment variables in your Lambda function configuration:

- `NEXT_PUBLIC_PORTFOLIO_API_URL`: The URL of the `getUserData` endpoint.
- `PORTFOLIO_PRIVATE_API_KEY`: The API key for authentication.
- `USER_EMAIL`: The user email for the request header.

## Usage

No manual action is required after deployment. The Lambda function will run on its schedule and keep your Supabase project active.
