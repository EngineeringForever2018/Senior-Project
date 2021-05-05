## Installation (Non-Development)

Install Docker, then run the following command in the parent directory (`avpd`) to build the container.

```bash
docker build -t avpd-backend -f backend/Dockerfile .
```

Once the container is built, you can run it at any time with:

```bash
docker run -p 8000:8000 avpd-backend
```
