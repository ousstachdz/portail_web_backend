# Installation Steps

## 1. Install Docker

Make sure Docker is installed on your system. You can download and install Docker from the official website: [https://www.docker.com](https://www.docker.com).

## 2. Build the Docker Image

Run the following command to build the Docker image for Odoo:

```bash
sudo docker build -t odoo_ocr .
```

## 3. Configure docker-compose.yml

Rename the `docker-compose.YOU_OS.yaml` to `docker-compose.yaml` file according to your operating system:

- For Windows: Rename `docker-compose.windows.yaml` to `docker-compose.yaml`
- For Linux/Mac: Rename `docker-compose.linux.yaml` to `docker-compose.yaml`

## 4. Start the Services

Run the following command to start the Odoo and PostgreSQL services:

```bash
docker-compose up
```

## 5. Enable Watch Mode

Once the services are running, press the `w` key on your keyboard to enable watch mode. This will automatically restart the server whenever changes are detected in the code.

## Additional Notes

- Ensure that Docker Desktop (for Windows/Mac) or Docker Engine (for Linux) is running before executing the commands.
- If you encounter permission issues, try running the commands with `sudo` (Linux/Mac) or as an administrator (Windows)."
# portail_web_backend
