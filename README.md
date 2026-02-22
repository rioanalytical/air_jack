# Air Jack

## Description
Air Jack is a FastAPI-based application designed to manage and analyze air quality data efficiently. It provides a RESTful API that enables users to retrieve and manipulate air quality measurements.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Configuration](#configuration)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

## Installation
To install Air Jack, clone the repository and install the dependencies:

```bash
git clone https://github.com/rioanalytical/air_jack.git
cd air_jack
pip install -r requirements.txt
```

## Usage
Run the application with the following command:

```bash
uvicorn main:app --reload
```
The API will be available at `http://127.0.0.1:8000`.

### Example Request
To fetch air quality data, send a GET request to:
```
GET /api/air-quality
```

## API Endpoints
### `GET /api/air-quality`
- **Description**: Retrieve all air quality records.
- **Response**:
    - Status 200: Success
    - Body: List of air quality records.

### `POST /api/air-quality`
- **Description**: Create a new air quality record.
- **Request Body**: 
    ```json
    {
      "location": "string",
      "pm10": "number",
      "pm2_5": "number",
      "ozone": "number",
      "timestamp": "string"
    }
    ```
- **Response**:
    - Status 201: Created
    - Body: Created air quality record.

## Configuration
Make sure to set the following environment variables:
- `DATABASE_URL`: Connection URL for the database.

## Testing
To run tests for the application, use the following command:

```bash
pytest
```

## Contributing
Contributions are welcome! Please read the [CONTRIBUTING.md](CONTRIBUTING.md) file for details on our code of conduct, and the process for submitting pull requests.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
