# Authorizer

This project contains source code and supporting files for a lambda REQUEST authorizer. The logic of this authorizer is fairly straightforward and it either allows access to ALL api methods on all resources or denies all access. The decision is made based on validity of the ID token passed in the Authorization header or in the Authorization query parameter of the method URL. The authorizer can be used for controlling access to REST or WebSockets APIs. HTTP APIs use different authorizer event format and code would need to be adopted for such a purpose.

## Environment variables
The authorizer uses following environment variables which control it's behavior:
* **SSM_PARAMETER_NAME**. Name of the SSM parameter expected to contain Cognito's JWKS endpoint's URL and application id which will be checked against token's **aud** claim. Sample value of the SSM parameter:
```
{
   "url":"https://cognito-idp.eu-west-1.amazonaws.com/eu-west-1_DexXZE63O/.well-known/jwks.json",
   "client_id":"1b7l19qgrnigbjn42q6cn6uvim"
}
```
* **LOG_LEVEL** (optional) can be one of DEBUG, WARN, INFO, ERROR. If not set, INFO is assumed as default
* **SKIP_EXPIRY_CHECK** (optional) ignores expiry of the token. **This should only be used for debugging purposes**. If not set to "True" the expiry check will be performed (default)