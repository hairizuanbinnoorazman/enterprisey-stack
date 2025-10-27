# Enterprisey Stack

This repo comprises of my learnings to set up ldap + oidc in order to build out more entreprise level applications. Authentication and authorization are big challenges in bigger companies - plain old username and password aren't enough. Need to know how to ensure all the authentication is passed between systems

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