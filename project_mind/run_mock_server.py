"""Script to run the mock API server"""
from mock_apis import start_server

if __name__ == "__main__":
    start_server(host="0.0.0.0", port=8000)