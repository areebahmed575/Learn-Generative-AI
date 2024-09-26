# Deploy to Azure Container Apps with GitHub Actions

GitHub Actions is a powerful and flexible automation tool integrated into GitHub, designed to help you build, test, and deploy your code directly from your GitHub repository. Here are some key features and benefits of GitHub Actions:

## Key Features and Benefits

### Automation and CI/CD
GitHub Actions enables continuous integration and continuous deployment (CI/CD) workflows. You can automate the process of testing and deploying your applications whenever code changes are pushed to your repository.

### Custom Workflows
You can create custom workflows using YAML files. These workflows define the steps to be taken when certain events occur in your repository, such as code pushes, pull requests, or issues.

### Pre-built Actions and Reusable Workflows
GitHub Actions provides a marketplace with thousands of pre-built actions created by the community and GitHub. These actions can be used to perform common tasks like setting up environments, deploying to cloud services, or running specific tests.

### Integration with GitHub Ecosystem
As it is built into GitHub, Actions integrates seamlessly with other GitHub features like pull requests, issues, and the GitHub API. This integration simplifies automation and provides better visibility and management of your CI/CD pipelines.

### Matrix Builds
You can run tests across multiple operating systems and versions of runtime environments. This is useful for ensuring that your code works correctly across different setups.

### Self-hosted Runners
Besides using GitHub's hosted runners, you can run jobs on your own infrastructure, giving you more control over the environment in which your workflows run.

### Security and Permissions
GitHub Actions supports secure access controls, allowing you to define who can trigger workflows and what secrets and environment variables are available to your workflows.

### Cost Management
GitHub provides a certain amount of free usage for GitHub Actions, with detailed billing for additional usage, making it easier to manage costs associated with CI/CD pipelines.

# Steps to Deploy Azure Container App with GitHub Actions
## Prerequisites

- **Azure Subscription**: Ensure you have an Azure account. If not, create one [here](https://azure.microsoft.com/en-us/free/).
- **Azure CLI**: Install Azure CLI from [here](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli).
- **GitHub Repository**: Have a repository with your container app code.

## 1. Set Up Azure Environment

### Login to Azure
<div>
  <button onclick="copyToClipboard('#login-azure')">Copy</button>
  <pre id="login-azure"><code>az login</code></pre>
</div>

### Create Resource Group
<div>
  <button onclick="copyToClipboard('#create-resource-group')">Copy</button>
  <pre id="create-resource-group"><code>az group create --name myresourcegroup --location eastus</code></pre>
</div>

### Create Container App Environment
<div>
  <button onclick="copyToClipboard('#create-container-app-env')">Copy</button>
  <pre id="create-container-app-env"><code>az containerapp env create --name mycontainerappenv --resource-group myresourcegroup --location eastus</code></pre>
</div>

### Create the Service Principal
<div>
  <button onclick="copyToClipboard('#create-service-principal')">Copy</button>
  <pre id="create-service-principal"><code>az ad sp create-for-rbac --name "myServicePrincipal" --role contributor --scopes /subscriptions/{subscription-id} --sdk-auth</code></pre>
</div>

This command will output a JSON object containing your Azure credentials. Save these credentials as they will be used later.

## 2. Create Docker Image

### Build Docker Image
<div>
  <button onclick="copyToClipboard('#build-docker-image')">Copy</button>
  <pre id="build-docker-image"><code>docker build -t your-dockerhub-username/myapp:latest .</code></pre>
</div>

### Push Docker Image to Docker Hub

#### Login to Docker Hub
<div>
  <button onclick="copyToClipboard('#login-docker-hub')">Copy</button>
  <pre id="login-docker-hub"><code>docker login --username your-dockerhub-username</code></pre>
</div>

#### Tag and Push Image
<div>
  <button onclick="copyToClipboard('#tag-push-image')">Copy</button>
  <pre id="tag-push-image"><code>docker tag myapp:latest your-dockerhub-username/myapp:latest
docker push your-dockerhub-username/myapp:latest</code></pre>
</div>

## 3. Configure GitHub Secrets

Go to your GitHub repository. Navigate to `Settings` > `Secrets and variables` > `Actions`. Add the following secrets:

- **DOCKER_HUB_USERNAME**: Your Docker Hub username.
- **DOCKER_HUB_ACCESS_TOKEN**: Your Docker Hub access token (You can create an access token from Docker Hub instead of using your password).
- **AZURE_CREDENTIALS**: Your Azure credentials in JSON format.

The JSON format for `AZURE_CREDENTIALS` should look like this:
<div>
  <button onclick="copyToClipboard('#azure-credentials')">Copy</button>
  <pre id="azure-credentials"><code>{
  "clientId": "e7f8c3bd-fe7c-484d-bd022a-2892edf151e5",
  "clientSecret": "xas8Q~t4Kb4tlQ-eh222o~Esr_z2kAMkM6ybcsgGag_",
  "subscriptionId": "06ddb3b9-9f0ba-4e1b-9e0e-1190ba64ff07",
  "tenantId": "e5d64a62-32ec6e-4a87-84fa-d64cda031416",
  "activeDirectoryEndpointUrl": "https://login.microsoftonline.com",
  "resourceManagerEndpointUrl": "https://management.azure.com/",
  "activeDirectoryGraphResourceId": "https://graph.windows.net/",
  "sqlManagementEndpointUrl": "https://management.core.windows.net:8443/",
  "galleryEndpointUrl": "https://gallery.azure.com/",
  "managementEndpointUrl": "https://management.core.windows.net/"
}</code></pre>
</div>

## 4. Create GitHub Action Workflow

In your GitHub repository, create a `.github/workflows/deploy.yml` file with the following content:
<div>
  <button onclick="copyToClipboard('#github-action-workflow')">Copy</button>
  <pre id="github-action-workflow"><code>name: Deploy to Azure Container Apps

on:
  push:
    branches:
      - main

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v2

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v1

      - name: Log in to Docker Hub
        run: |
          echo ${{ secrets.DOCKER_HUB_ACCESS_TOKEN }} | docker login -u ${{ secrets.DOCKER_HUB_USERNAME }} --password-stdin

      - name: Build and push Docker image
        run: |
          docker build -t ${{ secrets.DOCKER_HUB_USERNAME }}/myapp:latest .
          docker push ${{ secrets.DOCKER_HUB_USERNAME }}/myapp:latest

      - name: Azure Login
        uses: azure/login@v1
        with:
          creds: ${{ secrets.AZURE_CREDENTIALS }}

      - name: Deploy to Azure Container Apps
        run: |
          az containerapp create \
            --name mycontainerapp \
            --resource-group myresourcegroup \
            --environment mycontainerappenv \
            --image ${{ secrets.DOCKER_HUB_USERNAME }}/myapp:latest \
            --target-port 8000 \
            --ingress 'external' \
            --env-vars 'APP_SETTING=my-setting'</code></pre>
</div>

Replace placeholders (e.g., `your-dockerhub-username`, `myapp`, `myresourcegroup`, `mycontainerapp`, `mycontainerappenv`) with your actual values, ensuring they are all in lowercase.

## 5. Run GitHub Action

Push your code to the `main` branch, and the GitHub Actions workflow will trigger automatically, building and deploying your container app to Azure.

## Additional Tips

- **Testing Locally**: Before deploying, ensure your Docker container works as expected locally.
- **Monitoring**: Use Azure Portal to monitor your container app’s health and logs.