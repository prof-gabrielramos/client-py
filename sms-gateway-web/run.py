import argparse
import os
import sys

# Add the parent directory to the path so we can import from app
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app  # noqa: E402

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the SMS Gateway Web Client")
    parser.add_argument("--host", default="0.0.0.0", help="Host to run the server on")
    parser.add_argument(
        "--port", type=int, default=5000, help="Port to run the server on"
    )
    parser.add_argument("--debug", action="store_true", help="Run in debug mode")
    args = parser.parse_args()

    app.run(host=args.host, port=args.port, debug=args.debug)
