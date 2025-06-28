# SMS Gateway Web Client

A web-based interface for the Android SMS Gateway, replicating the functionality of the Python client for sending and managing SMS messages through a clean dashboard.

## Features

- Send SMS messages to individual or multiple recipients
- View message history and delivery status
- Manage SMS gateway connection settings
- Simple contact management for frequent recipients
- Webhook support for event notifications

## Installation

1. **Clone the Repository** (if applicable) or ensure all files are in the `sms-gateway-web` directory.

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application**:
   ```bash
   python run.py
   ```
   You can specify host and port if needed:
   ```bash
   python run.py --host 0.0.0.0 --port 5000
   ```

4. **Access the Web Interface**:
   Open your browser and navigate to `http://localhost:5000` (or the host/port you specified).

## Running with Docker (Recommended for Local Development & Deployment)

This web interface is designed to be run with Docker and Docker Compose for ease of deployment and consistent environments.

1.  **Ensure Docker and Docker Compose are installed.**

2.  **Navigate to the `sms-gateway-web` directory** (this directory).

3.  **Build and run the container using Docker Compose**:
    ```bash
    docker-compose up --build
    ```
    This command will build the Docker image if it doesn't exist and start the service. The web interface will be accessible at `http://localhost:5000`.

    To run in detached mode (in the background):
    ```bash
    docker-compose up --build -d
    ```

4.  **To stop the application**:
    ```bash
    docker-compose down
    ```
    This will stop and remove the containers defined in the `docker-compose.yml` file.

### Docker Configuration Details
-   **Dockerfile**: The `Dockerfile` in this directory defines the image for the web application. It uses a Python base image, installs dependencies, and copies the application code.
-   **docker-compose.yml**: The `docker-compose.yml` file orchestrates the `web` service.
    -   It builds the image using the local `Dockerfile`.
    -   It maps port `5000` of the host to port `5000` of the container.
    -   **Persistent Configuration**: It mounts a local directory `./config` to `/root/.sms-gateway-web` inside the container. This ensures that your configuration (`config.json`) and the local SQLite database (`sms_gateway.db`) persist even if the container is stopped or restarted.
    -   Sets `FLASK_ENV=production` for the Flask application.
    -   `restart: unless-stopped` ensures the service restarts automatically unless manually stopped.

## Deployment

For deploying this application, using the provided Docker setup is highly recommended.

### General Docker Deployment
You can adapt the `docker-compose.yml` for your production server. Ensure you manage secrets and potentially use a reverse proxy like Nginx or Traefik for SSL termination and domain routing.

### Deploying to Coolify
1.  Push your repository (including the `sms-gateway-web` directory with its `Dockerfile` and `docker-compose.yml`) to a Git provider (GitHub, GitLab, etc.).
2.  In Coolify, create a new "Application" or "Service" based on your Git repository.
3.  Point Coolify to the `sms-gateway-web` directory and specify that it should use Docker Compose.
    *   **Build Pack**: Select Docker Compose.
    *   **Docker Compose File**: `sms-gateway-web/docker-compose.yml` (or adjust path if deploying from root).
4.  **Persistent Storage**: Configure a persistent volume in Coolify that maps to `/root/.sms-gateway-web` in the container, similar to the local Docker Compose setup. This ensures your settings and data are saved.
5.  **Environment Variables**: Set any necessary environment variables through the Coolify interface (e.g., `FLASK_ENV`).
6.  **Port**: Ensure Coolify exposes port `5000` or configure it as needed.
7.  Deploy. Coolify will handle building the image and running the container.

### Deploying to a VPS with Portainer + Traefik
1.  **Prerequisites**:
    *   A VPS with Docker and Docker Compose installed.
    *   Portainer installed and running.
    *   Traefik installed and configured as a reverse proxy (typically in its own Docker container, handling SSL via Let's Encrypt).

2.  **Clone the Repository**:
    Clone this repository onto your VPS:
    ```bash
    git clone <your-repo-url>
    cd <your-repo-name>/sms-gateway-web
    ```

3.  **Modify `docker-compose.yml` for Traefik (Optional but Recommended)**:
    Add labels to the `web` service in `sms-gateway-web/docker-compose.yml` so Traefik can discover and route to it.
    ```yaml
    version: '3.8'

    services:
      web:
        build: .
        image: sms-gateway-web:latest # Consider using a tagged version for production
        container_name: sms-gateway-web
        # Remove direct port mapping if Traefik is handling it
        # ports:
        #   - "5000:5000"
        volumes:
          # Ensure this path is correct and accessible on your VPS for persistent storage
          - ./config:/root/.sms-gateway-web
          # Or use a Docker named volume:
          # - sms_gateway_web_data:/root/.sms-gateway-web
        environment:
          - FLASK_ENV=production
          # Add any other production specific environment variables
        restart: unless-stopped
        labels:
          - "traefik.enable=true"
          - "traefik.http.routers.sms-gateway-web.rule=Host(`your-domain.com`)" # Replace with your domain
          - "traefik.http.routers.sms-gateway-web.entrypoints=websecure"
          - "traefik.http.services.sms-gateway-web.loadbalancer.server.port=5000"
          - "traefik.http.routers.sms-gateway-web.tls.certresolver=myresolver" # Replace with your Traefik cert resolver

    # If using a Docker named volume for data persistence:
    # volumes:
    #   sms_gateway_web_data:
    ```
    **Note**: Ensure the Traefik network is correctly configured and the `sms-gateway-web` service is attached to it if necessary (often via `networks` directive in `docker-compose.yml`).

4.  **Deploy using Portainer Stacks**:
    *   In Portainer, go to "Stacks".
    *   Click "Add stack".
    *   Give it a name (e.g., `sms-gateway`).
    *   Choose "Git Repository" as the build method, point to your repository and branch, and set the Compose path to `sms-gateway-web/docker-compose.yml`.
    *   Alternatively, choose "Web editor" and paste the content of your (potentially modified) `docker-compose.yml`.
    *   Deploy the stack. Portainer will pull the image (or build it if specified and not found) and run the containers.

5.  **DNS**: Ensure your domain (`your-domain.com`) points to your VPS IP address. Traefik will then handle SSL and route traffic to the `sms-gateway-web` container.

## Configuration

- The first time you run the application, a configuration directory will be created at `~/.sms-gateway-web/` with a `config.json` file and a local database.
- You can configure the gateway connection settings, authentication requirements, and other preferences through the web interface under "Settings".

## Usage

- **Dashboard**: View recent messages and statistics.
- **Send SMS**: Compose and send messages to one or more recipients.
- **Messages**: Browse message history with status information.
- **Contacts**: Manage frequently used recipient information.
- **Webhooks**: Configure webhooks for event notifications (message sent, delivered, failed, etc.).
- **Settings**: Configure gateway connection and application preferences.

## Security

- Authentication can be enabled in the settings to protect access to the web interface.
- Configuration data and local message history are stored in `~/.sms-gateway-web/`.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

If you encounter any issues or have feature requests, please file an issue on the GitHub repository or contact the maintainers.
