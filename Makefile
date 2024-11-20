# Variables
IMAGE_NAME = tvp-pipeline
CONTAINER_NAME = tvp-pipeline-container
TAG = latest
DOCKERFILE = Dockerfile
APP_ENV = config/app.env
OUTPUT_DIR = $(PWD)/output

# Default target
.PHONY: help
help:
	@echo "Usage:"
	@echo "  make build        Build the Docker image."
	@echo "  make run          Run the container with mounted volumes and environment variables."
	@echo "  make clean        Stop and remove the container."
	@echo "  make logs         Show logs from the running container."
	@echo "  make shell        Open a shell inside the running container."

# Build the Docker image
.PHONY: build
build:
	docker build -t $(IMAGE_NAME):$(TAG) -f $(DOCKERFILE) .

# Run the container
.PHONY: run
run:
	docker run --rm \
		--name $(CONTAINER_NAME) \
		--env-file $(APP_ENV) \
		-v $(OUTPUT_DIR):/app/output \
		$(IMAGE_NAME):$(TAG)

# Stop and remove the container
.PHONY: clean
clean:
	-docker stop $(CONTAINER_NAME) || true
	-docker rm $(CONTAINER_NAME) || true

# View logs from the container
.PHONY: logs
logs:
	docker logs $(CONTAINER_NAME)
