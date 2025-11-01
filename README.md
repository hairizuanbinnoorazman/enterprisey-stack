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

## Learnings

- Do not use RFC-9068 unless absolutely needed. It seems like the usual authentication servers don't properly support it in the first place - so could be possible that this is a standard that's not really followed. This is the version that has `jti` requirements + headers `typ` would be `at+jwt` instead of usual `JWT`
- Some Important RFC to take note of (because the end goal is to get this whole enterprisey stack working with MCP Clients + Servers)
  - RFC 7591 - Oauth 2.0 Dynamic Client Registration Protocol
  - RFC 8414 - Oauth 2.0 Authorization Server Metadata
  - RFC 8707 - Resource Indicators for Oauth 2.0
  - RFC 9068 - JWT Profile for Oauth 2.0 Access Tokens
  - RFC 9728 - Oauth 2.0 Protected Resource Metadata

## Current Working Prompt

I have the following in my stack:

- Openldap
- osixia/phpldapadmin:latest
- Dex

The above 3 are running in a docker compose setup

I have also have a python application (application A) that connects to dex to do authentication and authoirzation of the application.

How can i have application A call to application B (also another flask app) but application B relies on application's A authentication 

Ignore setting up openldap, phpldapadmin and dex - i have already had them running for a while. Just focus only on application B

## Quickstart for phpldapadmin

For logging into osixia/phpldapadmin:latest, use the following credentials:

cn=admin,dc=example,dc=org / admin

The following container has capability to alter ldap entries

## Quickstart for Dex

There is nothing we need to do here, we simply need set it up with the dex configuration

## Quickstart for authentik

Most bigger companies rely on LDAP. So let's assume to go with the direction of not needing to setup authentication. Authentik is so much harder to use - there is way more things to set up

To setup LDAP Source:  
Directory -> Federation and Social Login -> Create -> LDAP Source

Configurations:

- Server URI: ldap://ldap:389
- Sync Users: True
- Sync Group: False (for easier setup)
- Bind CN: cn=admin,dc=example,dc=org
- Bind Password: admin
- Base DN: ou=users,dc=example,dc=org
- LDAP User Mapping:
  - LDAP Mapping: mail
  - LDAP Mapping: uid

After setting up LDAP Source, it syncs users into a particular user group set

We then need to setup the following:

- Providers (Set up Oauth provider)
  - Redirect URLs: .*
  - Access Token: 1hr? So that it'll be easier to debug?
  - Scopes: email, offline_access, profile, openid
  - This generates a client ID and client secret that can be injected into our plain old python applications (main.py and ultimate.py)
- Application
  - Point the provider to the one we created above
