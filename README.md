# Credence Backend
## Preparing the Setup
First, clone this repository to your laptop then install the following tools below.
### UV tool installation (for Python)
Credence backend requires uv for virtual environment.
#### uv standalone installer (for MacOS/Linux)
Use `curl` to download the script and execute it with `sh`:

```curl -LsSf https://astral.sh/uv/install.sh | sh ```

If your system doesn't have curl, you can use wget:

```wget -qO- https://astral.sh/uv/install.sh | sh ```

Request a specific version by including it in the URL:

```curl -LsSf https://astral.sh/uv/0.13.1/install.sh | sh ```

#### uv standalone installer (for Windows)

Use `irm` to download the script and execute it with `iex`:

```powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex```

Request a specific version by including it in the URL:

```powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/0.13.1/install.ps1 | iex```
### Updating UV

When uv is installed via the standalone installer, it can update itself on-demand:

``` uv self update```

## Running the Setup

1. Run the virtual environment: source ./venv/scripts/Activate
2. Run the backend server: uv run python manage.py runserver 0.0.0.0:8000

