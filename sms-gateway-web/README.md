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
