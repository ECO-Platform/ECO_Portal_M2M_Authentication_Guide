# ECO Portal Machine-to-Machine (M2M) Authentication Guide

This guide explains how to obtain an access token for accessing the API of the new ECO Portal at `https://portal.eco-platform.org/`. Registration and activation of a user account is required.

## Overview

Obtaining an access token for accessing the API of the new ECO Portal requires two steps:

1. Obtain an ID token from Auth0 at `https://auth.eco-platform.org` using the Client Credentials flow with your application's client ID and client secret that have been issued to you by ECO Platform.
2. Obtain an API access token from ECO Portal at `https://portal.eco-platform.org` using the ID token obtained in step 1.

The API access token can then be used to access the ECO Portal at `https://portal.eco-platform.org/resource/` and all its member nodes.

Both steps are explained in detail below.


## Step 1: Obtain token from Identity Provider (auth0)

### Overview

This guide explains how to obtain an ID token from Auth0 using the Client Credentials flow with your application's client ID and client secret. ID tokens are JSON Web Tokens (JWTs) that contain identity information about the authenticated user.

### Prerequisites

Before you begin, ensure you have:

- **Client ID**: Your application's client identifier
- **Client Secret**: Your application's client secret

(you will find those when logging in on ECO Portal with your account).

The other parameters needed are as follows:
- **Auth0 Domain**: Your Auth0 tenant domain is `auth.eco-platform.org`.

- **Audience**: The API identifier is `https://portal.eco-platform.org`.

- **Scope**: The scope is `create:token`.

  

### Authentication Endpoint

**URL**: `https://auth.eco-platform.org/oauth/token` **Method**: `POST` **Content-Type**: `application/x-www-form-urlencoded`

## Request Parameters

| Parameter       | Type   | Required | Description                                     |
| --------------- | ------ | -------- | ----------------------------------------------- |
| `grant_type`    | string | Yes      | Must be `client_credentials`                    |
| `client_id`     | string | Yes      | Your application's client ID                    |
| `client_secret` | string | Yes      | Your application's client secret                |
| `audience`      | string | No       | The API identifier (required for access tokens) `https://portal.eco-platform.org` |
| `scope`         | string | No       | Requested scope `create:token` |

## Basic Request Example

### cURL

```bash
curl -X POST \
  https://auth.eco-platform.org/oauth/token \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'grant_type=client_credentials' \
  -d 'client_id=YOUR_CLIENT_ID' \
  -d 'client_secret=YOUR_CLIENT_SECRET' \
  -d 'audience=https://portal.eco-platform.org' \
  -d 'scope=create:token'
```

### JavaScript (Node.js)

```javascript
const axios = require('axios');

const getAccessToken = async () => {
  try {
    const response = await axios.post('https://auth.eco-platform.org/oauth/token', {
      grant_type: 'client_credentials',
      client_id: 'YOUR_CLIENT_ID',
      client_secret: 'YOUR_CLIENT_SECRET',
      audience: 'https://portal.eco-platform.org',
      scope: 'create:token'
    }, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    });
    
    return response.data;
  } catch (error) {
    console.error('Error obtaining token:', error.response.data);
    throw error;
  }
};
```

### Python

```python
import requests

def get_access_token():
    url = "https://auth.eco-platform.org/oauth/token"
    
    payload = {
        'grant_type': 'client_credentials',
        'client_id': 'YOUR_CLIENT_ID',
        'client_secret': 'YOUR_CLIENT_SECRET',
        'audience': 'https://portal.eco-platform.org',
        'scope': 'create:token'
    }
    
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    
    response = requests.post(url, data=payload, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error: {response.status_code} - {response.text}")
```

### C-Sharp

```csharp
using System;
using System.Collections.Generic;
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;
using Newtonsoft.Json;

public class Auth0TokenService
{
    private readonly HttpClient _httpClient;
    
    public Auth0TokenService()
    {
        _httpClient = new HttpClient();
    }
    
    public async Task<TokenResponse> GetAccessTokenAsync()
    {
        var url = "https://auth.eco-platform.org/oauth/token";
        
        var parameters = new List<KeyValuePair<string, string>>
        {
            new KeyValuePair<string, string>("grant_type", "client_credentials"),
            new KeyValuePair<string, string>("client_id", "YOUR_CLIENT_ID"),
            new KeyValuePair<string, string>("client_secret", "YOUR_CLIENT_SECRET"),
            new KeyValuePair<string, string>("audience", "https://portal.eco-platform.org"),
            new KeyValuePair<string, string>("scope", "create:token")
        };
        
        var content = new FormUrlEncodedContent(parameters);
        
        var response = await _httpClient.PostAsync(url, content);
        var responseContent = await response.Content.ReadAsStringAsync();
        
        if (response.IsSuccessStatusCode)
        {
            return JsonConvert.DeserializeObject<TokenResponse>(responseContent);
        }
        else
        {
            throw new Exception($"Error: {response.StatusCode} - {responseContent}");
        }
    }
}

public class TokenResponse
{
    [JsonProperty("access_token")]
    public string AccessToken { get; set; }
    
    [JsonProperty("token_type")]
    public string TokenType { get; set; }
    
    [JsonProperty("expires_in")]
    public int ExpiresIn { get; set; }
    
    [JsonProperty("scope")]
    public string Scope { get; set; }
}
```

## Response Format

### Successful Response (200 OK)

```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIs...",
  "token_type": "Bearer",
  "expires_in": 86400,
  "scope": "create:token"
}
```

### Response Fields

| Field          | Type   | Description               |
| -------------- | ------ | ------------------------- |
| `access_token` | string | The JWT access token      |
| `token_type`   | string | Always "Bearer"           |
| `expires_in`   | number | Token lifetime in seconds |
| `scope`        | string | Granted scopes            |

## Error Responses

### Invalid Client (401 Unauthorized)

```json
{
  "error": "invalid_client",
  "error_description": "Invalid client credentials"
}
```

### Invalid Grant (400 Bad Request)

```json
{
  "error": "invalid_grant",
  "error_description": "Grant type not supported"
}
```

### Invalid Scope (400 Bad Request)

```json
{
  "error": "invalid_scope",
  "error_description": "Scope is not valid"
}
```

## Using the Token

Once you have the access token, include it in the Authorization header of your API requests:

```bash
curl -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
     https://your-api.com/protected-endpoint
```

## Environment Variables Example

Create a `.env` file:

```env
AUTH0_DOMAIN=your-tenant.auth0.com
AUTH0_CLIENT_ID=your_client_id
AUTH0_CLIENT_SECRET=your_client_secret
AUTH0_AUDIENCE=https://portal.eco-platform.org
```

## Troubleshooting

### Common Issues

1. **Invalid Client Error**: Verify your client ID and secret are correct
2. **Invalid Audience**: Ensure the audience matches your API identifier exactly
3. **Scope Issues**: Check that your application has the requested scopes enabled
4. **Domain Issues**: Verify your Auth0 domain is correct (without protocol)

### Debug Tips

- Test with a tool like Postman first before implementing in code
- Ensure your application type supports the Client Credentials flow



## Step 2: Obtain API access token from ECO Portal

Using the token obtained in step 1, you can request a token for accessing the API by sending a POST request to the following end point:

```http
POST https://portal.eco-platform.org/resource/authenticate/token/exchange

{
  "subject_token": "eyJh...."
}
```



You will receive a response where your access token is in the `access_token` property:

```json
{
    "access_token": "eyJhbG...",
    "token_type": "Bearer",
    "expires_at": 1758446694254,
    "scope": null,
    "refresh_token": null
}
```



Using this token as a bearer token, you can access the ECO Portal at `https://portal.eco-platform.org/resource/` and all its member nodes.



## Security Best Practices

1. **Store Credentials Securely**: Never expose client secrets in client-side code
2. **Use Environment Variables**: Store credentials as environment variables
3. **Token Expiration**: Implement token refresh logic before expiration
4. **HTTPS Only**: Always use HTTPS for token requests
5. **Scope Limitation**: Request only the minimum required scopes
6. **Token Storage**: Store tokens securely and clear them when no longer needed



## Additional Resources

- [Auth0 Client Credentials Flow Documentation](https://auth0.com/docs/flows/client-credentials-flow)
- [Auth0 Management API](https://auth0.com/docs/api/management/v2)
- [JWT.io](https://jwt.io/) - JWT token decoder for debugging

