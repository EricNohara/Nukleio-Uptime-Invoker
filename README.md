# Nukleio Supabase Uptime Invoker

This AWS Lambda keeps both the production and development Nukleio Supabase
projects active. On every scheduled invocation, it calls each environment's
authenticated uptime endpoint independently. A failure in one environment does
not prevent the other request from running.

## Runtime behavior

The Lambda makes one `GET` request to each configured endpoint. Its result
contains a separate entry for `prod` and `dev`. It returns HTTP status `200`
only when both requests succeed; otherwise it returns `502`, which makes a
partial outage visible in Lambda monitoring.

Each request has a 30-second timeout.

## Lambda environment variables

Configure these six values on the Lambda. Do not commit credentials to this
repository.

| Variable | Purpose |
| --- | --- |
| `PROD_API_URL` | Production `getUserData` endpoint URL. |
| `PROD_PRIVATE_API_KEY` | Production endpoint's private API key. |
| `PROD_USER_EMAIL` | Production timer-trigger user's email. |
| `DEV_API_URL` | Development `getUserData` endpoint URL. |
| `DEV_PRIVATE_API_KEY` | Development endpoint's private API key. |
| `DEV_USER_EMAIL` | Development timer-trigger user's email. |

## One-time AWS migration

AWS Lambda functions and EventBridge rules cannot be renamed. Replace the old
resources instead of modifying their names:

- Old Lambda: `PortfolioManagerSupabaseTimerTrigger`
- New Lambda: `Nukleio-Supabase-Uptime-Invoker`
- Old EventBridge rule: `PortfolioManagerSupabaseUptimeTrigger`
- Recommended new EventBridge rule: `NukleioSupabaseUptimeInvokerSchedule`

1. In AWS Lambda, open the old function's **Configuration** pages and record
   its Python runtime, architecture, execution role, memory, timeout, and any
   other settings. Also open its EventBridge trigger and record the exact
   schedule expression.
2. Create `Nukleio-Supabase-Uptime-Invoker` in `us-east-2`, selecting the same
   Python runtime, architecture, and existing execution role as the old Lambda.
   Set the handler to `lambda_function.lambda_handler`, then copy the old
   memory, timeout, and other configuration values exactly.
3. In the new function's **Configuration > Environment variables**, add the
   six variables listed above with their environment-specific values.
4. In Amazon EventBridge, create the scheduled rule
   `NukleioSupabaseUptimeInvokerSchedule`. Copy the old rule's exact schedule,
   choose `Nukleio-Supabase-Uptime-Invoker` as the target, and allow EventBridge
   to invoke it.
5. Push this repository's changes to `main`. The GitHub Actions workflow will
   deploy the Lambda package to `Nukleio-Supabase-Uptime-Invoker`.
6. Run a Lambda test invocation. Confirm both `prod` and `dev` entries show
   `success: true` and a successful status code. Then wait for one scheduled
   invocation and confirm it in CloudWatch logs.
7. Disable `PortfolioManagerSupabaseUptimeTrigger`. After the new scheduled
   invocation succeeds, delete that rule and
   `PortfolioManagerSupabaseTimerTrigger`.

## Deployment

Pushing to `main` installs `requests`, packages `src/`, and deploys the code to
`Nukleio-Supabase-Uptime-Invoker` in `us-east-2`. The GitHub Actions secrets
`AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` must retain permission to update
that replacement Lambda function.
