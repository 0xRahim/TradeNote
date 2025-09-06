# TradeNote API Documentation

## Introduction

Welcome to the TradeNote API documentation. This API provides a comprehensive set of endpoints to manage your trading journal, including notes, trades, and playbooks. It uses JWT for authentication and provides a secure and modular way to interact with your data.

## Authentication

The API uses JWT (JSON Web Tokens) for authentication. To access protected endpoints, you need to obtain a token by logging in and then include it in the `Authorization` header of your requests.

### Register

*   **Endpoint**: `POST /auth/register`
*   **Description**: Registers a new user.
*   **Request Body**:
    ```json
    {
        "username": "your_username",
        "password": "your_password",
        "avatar": "base64_encoded_image_string" // Optional
    }
    ```
*   **Response**:
    *   **201 Created**:
        ```json
        {
            "message": "New user created!"
        }
        ```

### Login

*   **Endpoint**: `POST /auth/login`
*   **Description**: Logs in a user and returns a JWT token.
*   **Request**: Basic Authentication with username and password.
*   **Response**:
    *   **200 OK**:
        ```json
        {
            "token": "your_jwt_token"
        }
        ```

## Endpoints

### User

#### Get User

*   **Endpoint**: `GET /auth/user`
*   **Description**: Retrieves the authenticated user's information.
*   **Headers**: `Authorization: Bearer <token>`
*   **Response**:
    *   **200 OK**:
        ```json
        {
            "id": 1,
            "username": "testuser",
            "avatar": "SGVsbG8gV29ybGQ="
        }
        ```

#### Upload Avatar

*   **Endpoint**: `POST /auth/avatar`
*   **Description**: Uploads or updates the user's avatar.
*   **Headers**: `Authorization: Bearer <token>`
*   **Request Body**:
    ```json
    {
        "avatar": "new_base64_encoded_image_string"
    }
    ```
*   **Response**:
    *   **200 OK**:
        ```json
        {
            "message": "Avatar updated!"
        }
        ```

### Notes

#### Create Note

*   **Endpoint**: `POST /notes/`
*   **Description**: Creates a new note.
*   **Headers**: `Authorization: Bearer <token>`
*   **Request Body**:
    ```json
    {
        "title": "My Note Title",
        "content": "This is the content of my note."
    }
    ```
*   **Response**:
    *   **201 Created**:
        ```json
        {
            "message": "Note created!"
        }
        ```

#### Get All Notes

*   **Endpoint**: `GET /notes/`
*   **Description**: Retrieves all notes for the authenticated user.
*   **Headers**: `Authorization: Bearer <token>`
*   **Response**:
    *   **200 OK**:
        ```json
        {
            "notes": [
                {
                    "id": 1,
                    "title": "Test Note",
                    "content": "This is a test note."
                }
            ]
        }
        ```

#### Get Note by ID

*   **Endpoint**: `GET /notes/<note_id>`
*   **Description**: Retrieves a specific note by its ID.
*   **Headers**: `Authorization: Bearer <token>`
*   **Response**:
    *   **200 OK**:
        ```json
        {
            "id": 1,
            "title": "Test Note",
            "content": "This is a test note."
        }
        ```

#### Update Note

*   **Endpoint**: `PUT /notes/<note_id>`
*   **Description**: Updates a specific note.
*   **Headers**: `Authorization: Bearer <token>`
*   **Request Body**: A note object with the fields to update.
*   **Response**:
    *   **200 OK**:
        ```json
        {
            "message": "Note updated!"
        }
        ```

#### Delete Note

*   **Endpoint**: `DELETE /notes/<note_id>`
*   **Description**: Deletes a specific note.
*   **Headers**: `Authorization: Bearer <token>`
*   **Response**:
    *   **200 OK**:
        ```json
        {
            "message": "Note deleted!"
        }
        ```

### Trades

#### Create Trade

*   **Endpoint**: `POST /trades/`
*   **Description**: Creates a new trade with an optional screenshot.
*   **Headers**: `Authorization: Bearer <token>`
*   **Request Body**: `multipart/form-data` with the following fields:
    *   `ticker`: (string, required)
    *   `result`: (string, required)
    *   `total_pnl`: (float, required)
    *   `entry_datetime`: (string, required, ISO 8601 format)
    *   `exit_datetime`: (string, required, ISO 8601 format)
    *   `risk_reward`: (float, required)
    *   `position`: (string, required)
    *   `stoploss_pips`: (integer, required)
    *   `range`: (integer, required)
    *   `result_type`: (string, required)
    *   `entry_model`: (string, required)
    *   `trade_model`: (string, required)
    *   `setup_type`: (string, required)
    *   `confluences`: (string, required, JSON array of strings)
    *   `trade_note`: (string, optional)
    *   `roadmap`: (string, optional)
    *   `screenshot`: (file, optional)
*   **Response**:
    *   **201 Created**:
        ```json
        {
            "message": "Trade created!"
        }
        ```

#### Get All Trades

*   **Endpoint**: `GET /trades/`
*   **Description**: Retrieves all trades for the authenticated user.
*   **Headers**: `Authorization: Bearer <token>`
*   **Response**:
    *   **200 OK**:
        ```json
        {
            "trades": [
                {
                    "id": 1,
                    "ticker": "AAPL",
                    "result": "Win",
                    "total_pnl": 250.00,
                    "entry_datetime": "2025-09-01T09:30:00Z",
                    "exit_datetime": "2025-09-01T15:45:00Z",
                    "risk_reward": 2.5,
                    "position": "Long",
                    "stoploss_pips": 10,
                    "trade_range": 50,
                    "result_type": "Good Win",
                    "entry_model": "Breakout",
                    "trade_model": "Scalp",
                    "setup_type": "A+",
                    "confluences": ["Breakout", "EMA Cross"],
                    "trade_note": "Good entry on breakout.",
                    "roadmap": "Planned to take profit at 155.00.",
                    "screenshot_filename": "trade123.png"
                }
            ]
        }
        ```

#### Get Trade by ID

*   **Endpoint**: `GET /trades/<trade_id>`
*   **Description**: Retrieves a specific trade by its ID.
*   **Headers**: `Authorization: Bearer <token>`
*   **Response**:
    *   **200 OK**:
        ```json
        {
            "id": 1,
            "ticker": "AAPL",
            "result": "Win",
            "total_pnl": 250.00,
            "entry_datetime": "2025-09-01T09:30:00Z",
            "exit_datetime": "2025-09-01T15:45:00Z",
            "risk_reward": 2.5,
            "position": "Long",
            "stoploss_pips": 10,
            "trade_range": 50,
            "result_type": "Good Win",
            "entry_model": "Breakout",
            "trade_model": "Scalp",
            "setup_type": "A+",
            "confluences": ["Breakout", "EMA Cross"],
            "trade_note": "Good entry on breakout.",
            "roadmap": "Planned to take profit at 155.00.",
            "screenshot_filename": "trade123.png"
        }
        ```

#### Update Trade

*   **Endpoint**: `PUT /trades/<trade_id>`
*   **Description**: Updates a specific trade.
*   **Headers**: `Authorization: Bearer <token>`
*   **Request Body**: `multipart/form-data` with the fields to update.
*   **Response**:
    *   **200 OK**:
        ```json
        {
            "message": "Trade updated!"
        }
        ```

#### Delete Trade

*   **Endpoint**: `DELETE /trades/<trade_id>`
*   **Description**: Deletes a specific trade.
*   **Headers**: `Authorization: Bearer <token>`
*   **Response**:
    *   **200 OK**:
        ```json
        {
            "message": "Trade deleted!"
        }
        ```

#### Get Screenshot

*   **Endpoint**: `GET /trades/screenshots/<filename>`
*   **Description**: Retrieves a screenshot image.
*   **Headers**: `Authorization: Bearer <token>`
*   **Response**:
    *   **200 OK**: The image file.

### Playbooks

#### Create Playbook

*   **Endpoint**: `POST /playbooks/`
*   **Description**: Creates a new playbook.
*   **Headers**: `Authorization: Bearer <token>`
*   **Request Body**: A playbook object.
*   **Response**:
    *   **201 Created**:
        ```json
        {
            "message": "Playbook created!",
            "playbook_id": "pb_12345678"
        }
        ```

#### Get All Playbooks

*   **Endpoint**: `GET /playbooks/`
*   **Description**: Retrieves all playbooks for the authenticated user.
*   **Headers**: `Authorization: Bearer <token>`
*   **Response**:
    *   **200 OK**:
        ```json
        {
            "playbooks": [
                {
                    "playbook_id": "pb_breakout_strategy",
                    "title": "Breakout Strategy",
                    "entry_model": "Breakout",
                    "trade_model": "Intraday",
                    "setup_grade": "A+",
                    "created_at": "2025-08-15T10:00:00Z",
                    "updated_at": "2025-09-01T09:30:00Z"
                }
            ]
        }
        ```

#### Get Playbook by ID

*   **Endpoint**: `GET /playbooks/<playbook_id>`
*   **Description**: Retrieves a specific playbook by its ID.
*   **Headers**: `Authorization: Bearer <token>`
*   **Response**:
    *   **200 OK**:
        ```json
        {
            "playbook_id": "pb_breakout_strategy",
            "title": "Breakout Strategy",
            "entry_model": "Breakout",
            "trade_model": "Intraday",
            "setup_grade": "A+",
            "confluences": [
                "Volume Spike",
                "RSI Divergence"
            ],
            "rules": [
                "Enter on the first pullback to the broken resistance.",
                "Stop loss below the breakout candle.",
                "Target 2R."
            ],
            "confirmations": [
                "Price closes above resistance on H1 timeframe."
            ],
            "invalidations": [
                "False breakout with immediate rejection."
            ],
            "roadmap": [
                "Identify key level",
                "Wait for price to break and close above",
                "Enter on retest of level"
            ],
            "tags": ["strategy", "breakout", "intraday"],
            "created_at": "2025-08-15T10:00:00Z",
            "updated_at": "2025-09-01T09:30:00Z"
        }
        ```

#### Update Playbook

*   **Endpoint**: `PUT /playbooks/<playbook_id>`
*   **Description**: Updates a specific playbook.
*   **Headers**: `Authorization: Bearer <token>`
*   **Request Body**: A playbook object with the fields to update.
*   **Response**:
    *   **200 OK**:
        ```json
        {
            "message": "Playbook updated!"
        }
        ```

#### Delete Playbook

*   **Endpoint**: `DELETE /playbooks/<playbook_id>`
*   **Description**: Deletes a specific playbook.
*   **Headers**: `Authorization: Bearer <token>`
*   **Response**:
    *   **200 OK**:
        ```json
        {
            "message": "Playbook deleted!"
        }
        ```

### Events

#### Get Events

*   **Endpoint**: `GET /events`
*   **Description**: Retrieves a mock list of events.
*   **Response**:
    *   **200 OK**:
        ```json
        [
            {
                "date": "2024-07-22",
                "events": [
                    {
                        "type": "earnings",
                        "time": "BMO",
                        "symbol": "UEC",
                        "details": "UEC Uranium Energy Corp Earnings"
                    },
                    {
                        "type": "data",
                        "time": "08:30",
                        "details": "Chicago Fed National Activity Index"
                    }
                ]
            },
            {
                "date": "2024-07-23",
                "events": [
                    {
                        "type": "earnings",
                        "time": "BMO",
                        "symbol": "GE",
                        "details": "General Electric Co Earnings"
                    },
                    {
                        "type": "data",
                        "time": "09:00",
                        "details": "S&P Case-Shiller Home Price Index"
                    }
                ]
            }
        ]
        ```

## Data Models

### User

| Attribute | Type | Description |
|---|---|---|
| `id` | Integer | The unique identifier for the user. |
| `username` | String | The user's username. |
| `password` | String | The user's hashed password. |
| `avatar` | Text | A base64 encoded string of the user's avatar image. |

### Note

| Attribute | Type | Description |
|---|---|---|
| `id` | Integer | The unique identifier for the note. |
| `title` | String | The title of the note. |
| `content` | Text | The content of the note. |
| `user_id` | Integer | The ID of the user who owns the note. |

### Trade

| Attribute | Type | Description |
|---|---|---|
| `id` | Integer | The unique identifier for the trade. |
| `ticker` | String | The stock ticker symbol. |
| `result` | String | The result of the trade (e.g., "Win", "Loss"). |
| `total_pnl` | Float | The total profit or loss from the trade. |
| `entry_datetime` | DateTime | The date and time of the trade entry. |
| `exit_datetime` | DateTime | The date and time of the trade exit. |
| `risk_reward` | Float | The risk/reward ratio of the trade. |
| `position` | String | The position of the trade (e.g., "Long", "Short"). |
| `stoploss_pips` | Integer | The stop loss in pips. |
| `trade_range` | Integer | The range of the trade. |
| `result_type` | String | The type of result (e.g., "Good Win"). |
| `entry_model` | String | The entry model used for the trade. |
| `trade_model` | String | The trade model used. |
| `setup_type` | String | The setup type of the trade. |
| `confluences` | JSON | A list of confluences for the trade. |
| `trade_note` | Text | Notes about the trade. |
| `roadmap` | Text | The roadmap for the trade. |
| `screenshot_filename` | String | The filename of the uploaded screenshot. |
| `user_id` | Integer | The ID of the user who owns the trade. |

### Playbook

| Attribute | Type | Description |
|---|---|---|
| `id` | Integer | The unique identifier for the playbook. |
| `playbook_id` | String | A unique string identifier for the playbook. |
| `title` | String | The title of the playbook. |
| `entry_model` | String | The entry model for the playbook. |
| `trade_model` | String | The trade model for the playbook. |
| `setup_grade` | String | The setup grade for the playbook. |
| `confluences` | JSON | A list of confluences for the playbook. |
| `rules` | JSON | A list of rules for the playbook. |
| `confirmations` | JSON | A list of confirmations for the playbook. |
| `invalidations` | JSON | A list of invalidations for the playbook. |
| `roadmap` | JSON | A list of roadmap steps for the playbook. |
| `tags` | JSON | A list of tags for the playbook. |
| `created_at` | DateTime | The timestamp when the playbook was created. |
| `updated_at` | DateTime | The timestamp when the playbook was last updated. |
| `user_id` | Integer | The ID of the user who owns the playbook. |