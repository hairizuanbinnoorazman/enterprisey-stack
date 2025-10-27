# Enterprisey Stack

This repo comprises of my learnings to set up ldap + oidc in order to build out more entreprise level applications. Authentication and authorization are big challenges in bigger companies - plain old username and password aren't enough. Need to know how to ensure all the authentication is passed between systems

This whole journey started due to the need to do authentication and authorization for MCP Servers at my place of work. There is definitely no way for us to pass username and passwords around (Don't ever trust LLM to do good things with your username and passwords) - so the only way to do that is via Authorization headers. According to MCP documentation as of October 2025: https://modelcontextprotocol.io/specification/draft/basic/authorization, we can rely on OIDC approach to do all the auth/authorization stuff - so here we are...

Details for what the user info means

```
{
  "iss": "http://127.0.0.1:5556",      // Issuer = Dex
  "sub": "CgXXXXX",                    // Unique user ID
  "aud": "flask",                      // Audience = your client_id (Application A)
  "exp": 1761659508,                   // Expiration time
  "iat": 1761573108,                   // Issued-at time
  "nonce": "2mmDxKkT65dDQbbkaVrw",     // For login replay protection
  "at_hash": "JRIGwm8YZY6AlRlGK6vJ2g",
  "email": "test@test.com",
  "email_verified": true
}
```

## Current Working Prompt

I have the following in my stack:

- Openldap
- osixia/phpldapadmin:latest
- Dex

The above 3 are running in a docker compose setup

I have also have a python application (application A) that connects to dex to do authentication and authoirzation of the application.

How can i have application A call to application B (also another flask app) but application B relies on application's A authentication 

Ignore setting up openldap, phpldapadmin and dex - i have already had them running for a while. Just focus only on application B

## Quickstart

For logging into osixia/phpldapadmin:latest, use the following credentials:

cn=admin,dc=example,dc=org / admin