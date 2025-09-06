# TradeNote

A powerful and personal trading journal to track your trades, analyze your performance, and refine your strategies.

## Screenshots

| Dashboard | Trades | Add Trade |
| :---: | :---: | :---: |
| ![Dashboard Screenshot](https://raw.githubusercontent.com/0xRahim/TradeNote/refs/heads/master/screenshots/dashboard.png)| ![Trades](https://raw.githubusercontent.com/0xRahim/TradeNote/refs/heads/master/screenshots/trades.png) | ![Add Trade](https://raw.githubusercontent.com/0xRahim/TradeNote/refs/heads/master/screenshots/add-trades.png) |
| **Playbook** | **Notebook** | **Events** |
| ![Playbook](https://raw.githubusercontent.com/0xRahim/TradeNote/refs/heads/master/screenshots/playbook.png) | ![Notebook](https://raw.githubusercontent.com/0xRahim/TradeNote/refs/heads/master/screenshots/notebook.png) | ![Events](https://raw.githubusercontent.com/0xRahim/TradeNote/refs/heads/master/screenshots/events.png) |

## Features

*   **Trade Logging**: Log detailed information about each trade, including ticker, P&L, entry/exit times, risk/reward, position, and more.
*   **Screenshot Uploads**: Attach screenshots to your trades for visual analysis.
*   **Playbook Creation**: Define and manage your trading strategies with detailed rules, confluences, and roadmaps.
*   **Note Taking**: A simple notebook to jot down ideas, market observations, or anything else.
*   **Economic Calendar**: Keep track of important economic events (yet to be implemented).
*   **User Authentication**: Secure your journal with JWT-based authentication.

## Tech Stack

*   **Frontend**: HTML, CSS, JavaScript
*   **Backend**: Python, Flask, Flask-SQLAlchemy, Flask-Cors, PyJWT

## Getting Started

### Prerequisites

*   Python 3

### Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/your-username/TradeNoteV3.git
    cd TradeNoteV3
    ```
2.  Run the setup script to install dependencies:
    ```bash
    ./setup.sh
    ```

## Usage

1.  Run the application:
    ```bash
    ./tradenote.sh
    ```
2.  Access the application in your browser at `http://localhost:1111/index.html`.

## Project Structure

The project is divided into two main parts:

*   `frontend/`: Contains all the static files for the user interface (HTML, CSS, JS).
*   `backend/`: Contains the Flask API server, database models, and business logic.

## API Documentation

For detailed information about the API endpoints, see the [API Documentation](docs/api_documentation.md).

## Contributing

Contributions are welcome! Please feel free to submit a pull request.

1.  Fork the Project
2.  Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3.  Commit your Changes (`git commit -m '''Add some AmazingFeature'''`)
4.  Push to the Branch (`git push origin feature/AmazingFeature`)
5.  Open a Pull Request

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
