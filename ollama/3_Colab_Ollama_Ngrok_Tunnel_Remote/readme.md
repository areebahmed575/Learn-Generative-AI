# Exposing Local Ollama Instance on Google Colab using Ngrok

This guide explains how to expose a local Ollama instance running on Google Colab to the internet using Ngrok. This setup allows you to leverage Colab's computational power and access the Ollama server from your local machine.

## Prerequisites

1. Obtain an Ngrok authentication token.
2. Ensure you have a Google Colab environment with GPU support enabled.

## Steps to Set Up and Access Ollama on Colab

### Step 1: Obtain Ngrok Token

First, acquire your Ngrok authentication token by creating an account at [Ngrok](https://ngrok.com/) and copying your personal authentication token.

### Step 2: Configure Colab Runtime

Navigate to `Runtime -> Change runtime type` in Colab and select **T4 GPU** to utilize GPU acceleration.

### Step 3: Set Up Secret Token in Colab

Set the secret token in Colab using the variable name `NGROK_AUTH_TOKEN`.

### Step 4: Execute the Colab Code Across Four Cells

#### Cell 1: Install Ollama

```python
# Download and run the Ollama Linux install script
!curl -fsSL https://ollama.com/install.sh | sh
```

#### Cell 2: Retrieve Ngrok Token

```python
# Get Ngrok authentication token from Colab secrets environment
from google.colab import userdata
NGROK_AUTH_TOKEN = userdata.get('NGROK_AUTH_TOKEN')
```

#### Cell 3: Install Dependencies and Set Up Environment

```python
# Install necessary packages: aiohttp for async subprocess execution and pyngrok for Ngrok integration
!pip install aiohttp pyngrok

import asyncio
import os

# Set LD_LIBRARY_PATH to prioritize system NVIDIA libraries over built-in ones
os.environ.update({'LD_LIBRARY_PATH': '/usr/lib64-nvidia'})

# Define an async helper function to run commands asynchronously
async def run(cmd):
    print('>>> starting', *cmd)
    p = await asyncio.subprocess.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )

    # Asynchronously process and print the output and error streams
    async def pipe(lines):
        async for line in lines:
            print(line.strip().decode('utf-8'))

    await asyncio.gather(
        pipe(p.stdout),
        pipe(p.stderr),
    )

# Authenticate with Ngrok using the token
await run(['ngrok', 'config', 'add-authtoken', NGROK_AUTH_TOKEN])
```

#### Cell 4: Start Ollama Server and Ngrok Tunnel

```python
# Run multiple tasks concurrently:
# 1. Start the Ollama server.
# 2. Start Ngrok to forward HTTP traffic from the local Ollama API running on localhost:11434.
await asyncio.gather(
    run(['ollama', 'serve']),
    run(['ngrok', 'http', '--log', 'stderr', '11434', '--host-header', 'localhost:11434']),
    # Uncomment the next line and replace with your Ngrok domain if using a static URL
    # run(['ngrok', 'http', '--log', 'stderr', '11434', '--host-header', 'localhost:11434', '--domain', 'insert-your-static-ngrok-domain-here']),
)
```

### Step 5: Extract the Ngrok URL

After running the code in the last cell, the Ngrok app link will be displayed in the output. Example:

```
2024-09-02T08:43:05+0000 lvl=info msg="started tunnel" obj=tunnels name=command_line addr=http://localhost:11434 url=https://c46f-34-125-8-152.ngrok-free.app
```

Copy the Ngrok app link from the output. This link will be used to access the Ollama instance from your local machine.

## Accessing the Ollama Instance from Your Local Computer

### Step 1: Set Up Your Local Environment

- **Download the Ollama CLI Tool**
  - For macOS: `brew install ollama`
  - For Windows, download from [here](https://ollama.com/download).

- **Set the Ngrok app URL for Local Terminal Connection**
  - For macOS/Linux: 
    ```sh
    export OLLAMA_HOST="[ngrok app url]"
    ```
  - For Windows:
    1. Edit Environment Variables.
    2. Add a new variable with the name `OLLAMA_HOST` and the value as the Ngrok app URL.

- Verify the environment variable by running:

  ```sh
  echo %OLLAMA_HOST%
  ```

### Step 2: Run Ollama Commands

- **List Available Models**

  ```sh
  ollama list
  ```

- **Run a Specific Model**

  ```sh
  ollama run llama3
  ```

## Connecting a Local Jupyter Notebook to the Ollama Server on Colab

You can connect your local Jupyter notebook to the Colab server using the following code:

```python
import requests
import json

# Replace this URL with your Ngrok URL
ollama_url = "https://c46f-34-125-8-152.ngrok-free.app"

def query_ollama(prompt, model="llama3"):
    headers = {
        "ngrok-skip-browser-warning": "true"  # This header bypasses the Ngrok browser warning
    }
    data = {
        "prompt": prompt,
        "model": model
    }
    
    # Stream the request to handle the sequence of JSON objects
    response = requests.post(f"{ollama_url}/api/generate", json=data, headers=headers, stream=True)
    
    results = []
    
    # Process each line in the response as a separate JSON object
    for line in response.iter_lines():
        if line:
            try:
                json_response = json.loads(line.decode('utf-8'))
                results.append(json_response)
            except json.JSONDecodeError as e:
                print(f"Failed to decode JSON: {e}")
                continue
    
    return results

# Test the connection with a specific model
response = query_ollama("What is Ollama?", model="llama3")
result = ""
for r in response:
    result += r['response']

print(result)
```

## Conclusion

By following this guide, you have successfully set up Ollama on Google Colab, exposed it via Ngrok, and accessed it from your local machine or Jupyter notebook. You can now leverage Colab's resources for your Ollama projects seamlessly.
