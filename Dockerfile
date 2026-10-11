# syntax=docker/dockerfile:1
# Use Python 3.14 slim (Debian-based) to avoid musl/glibc compatibility issues
FROM python:3.14-slim AS builder

# Install uv for efficient dependency management
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Copy workspace configuration and server pyproject
COPY pyproject.toml uv.lock ./
COPY server/pyproject.toml server/pyproject.toml
COPY server/src server/src

# Install dependencies into a virtual environment in /app/.venv
# Install the server package and its deps (--no-dev excludes dev dependencies)
# Use --no-editable to install as a normal package, not an editable link
RUN uv sync --frozen --no-dev --project server --no-editable

# --- Final Stage ---
FROM python:3.14-slim

# Create a non-root user for security
RUN groupadd -r agenthq && useradd -r -g agenthq agenthq

# Set the working directory
WORKDIR /home/agenthq/app

# Copy the virtual environment from the builder stage
COPY --from=builder /app/.venv /home/agenthq/app/.venv

# Ensure the non-root user owns the app directory
RUN chown -R agenthq:agenthq /home/agenthq/app

# Set environment variables
ENV PATH="/home/agenthq/app/.venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1
ENV AGENT_HQ_LOG_LEVEL=INFO

# Switch to the non-root user
USER agenthq

# Expose HTTP port for MCP communication
EXPOSE 3000

# Use python -m to invoke the module directly to avoid shebang issues
# Run in HTTP mode for production deployment
ENTRYPOINT ["/home/agenthq/app/.venv/bin/python", "-m", "agent_hq_server.__main__"]
CMD ["--http", "--host", "0.0.0.0", "--port", "3000"]

