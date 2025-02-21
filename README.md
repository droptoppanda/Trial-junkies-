# Trial-junkies-

## Documentation

### Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/Trial-junkies-.git
    ```
2. Navigate to the project directory:
    ```sh
    cd Trial-junkies-
    ```
3. Install dependencies:
    ```sh
    npm install
    ```

### Configuration

Before running the application, you may need to configure some settings. Create a `.env` file in the root directory and add the necessary environment variables. For example:
```sh
API_KEY=your_api_key_here
DATABASE_URL=your_database_url_here
```

## Environment Variables

The following environment variables need to be set in the `.env` file:

- `RAPIDAPI_KEY`: Your RapidAPI key.
- `WALLET_KEYPAIR`: Your wallet keypair.
- `SOLANA_ENDPOINT`: The Solana endpoint URL.
- `DISCORD_BOT_TOKEN`: Your Discord bot token.
- `GEMINI_API_KEY`: Your Gemini API key.

### Usage

To start the application, run:
```sh
npm start
```

### Using the Bot

1. **Invite the Bot to Your Server**: Use the OAuth2 URL to invite the bot to your Discord server.
2. **Bot Commands**: The bot supports the following commands:
    - `!help`: Displays a list of available commands.
    - `!balance`: Shows the current balance of the wallet.
    - `!price [symbol]`: Fetches the current price of the specified cryptocurrency.
    - `!transfer [amount] [address]`: Transfers the specified amount to the given address.

### Running Tests

To run tests, use:
```sh
npm test
```

To run tests using Python, use:
```sh
python -m unittest discover -s tests
```

### Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -m 'Add some feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Open a pull request.

### License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.