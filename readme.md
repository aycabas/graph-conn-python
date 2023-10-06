# Build Graph Connector using Microsoft Graph Python SDK
This app shows how to create a connector using Microsoft Graph Python SDK.

## Pre-requisites
- [Python](https://www.python.org/) and [pip](https://pip.pypa.io/en/stable/) installed on your development machine.
- Microsoft work or school account to test the connector. If you don't have a Microsoft account, you can sign up for the [Microsoft 365 Developer Program](https://developer.microsoft.com/microsoft-365/dev-program) to get a free Microsoft 365 subscription.
- `Client Id` of [an application registered in the Microsoft identity platform](https://learn.microsoft.com/en-us/azure/active-directory/develop/quickstart-register-app)

## Run the app

Install Azure Identity and Microsoft Graph SDK:
```bash
python3 -m pip install azure-identity
python3 -m pip install msgraph-sdk
```

Run the app:
```bash
python3 main.py
```
