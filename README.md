# Crawler Project

## Overview
This project is an asynchronous web crawler that fetches and processes data from web pages using `aiohttp`. It supports retries, proxy usage, and random headers for requests.

## Features
- **Asynchronous Requests**: Uses `aiohttp` for non-blocking HTTP requests.
- **Retry Mechanism**: Retries failed requests up to a specified limit.
- **Proxy Support**: Uses a random proxy from a provided list.
- **Random Headers**: Rotates user agents and headers for each request.
- **Error Handling**: Catches and logs network-related errors.

## Installation

### Prerequisites
- Python 3.10+
- `pip` (Python package manager)

### Install Dependencies
```sh
pip install -r requirements.txt
```

## Usage

### Running the Crawler
```sh
python main.py
```

## Configuration
You can customize the crawler by modifying the `Crawler` class parameters:
- `keywords`: A list of search terms.
- `search_type`: Type of search (e.g., `repositories`, `issues`, `wikis`).

## Testing
The project includes unit tests using `pytest`.

### Run Tests
```sh
pytest tests/
```
