# Project 05 — Weather App with Live OpenWeather API

**Language:** Python 3.10+  
**Interface:** Command-line application  
**API:** OpenWeather Current Weather and 5-day / 3-hour Forecast

## Features
- Calls the OpenWeather REST API using `requests`
- Reads the API key from `.env` with `python-dotenv`
- Uses `params` and `timeout=10` for API requests
- Parses JSON responses
- Displays city, temperature (°C), humidity, weather description, and wind speed
- Fetches the 5-day forecast and selects one entry per date
- Handles unknown cities (404), invalid/inactive keys (401), other API errors, network failures, and invalid JSON
- Uses `.get()` for safer access to nested JSON fields
- Caches each endpoint/city result for five minutes to reduce repeated API requests
- Exits when the user submits an empty city name

## Project files
- `main.py` — application source
- `requirements.txt` — Python dependencies
- `.env.example` — API-key configuration template (contains no real key)
- `.gitignore` — excludes `.env`, virtual environments, and Python cache files
- `README.md` — setup and usage instructions
- `submission_description.txt` — suggested submission notes

## 1. Create an OpenWeather API key
1. Create a free account at https://openweathermap.org/
2. Open your API keys page and copy your key.
3. New keys can take some time (sometimes a couple of hours) to become active.

## 2. Configure your secret key
Copy `.env.example` and rename the copy to `.env`. Open `.env` and replace the placeholder:

```env
OPENWEATHER_KEY=your_actual_api_key
```

Do not add quotes unless the provider specifically instructs you to. Never paste your key into `main.py`, README, screenshots, or GitHub.

## 3. Install dependencies

```bash
python -m venv .venv
```

Windows:
```bash
.venv\Scripts\activate
```

macOS/Linux:
```bash
source .venv/bin/activate
```

Install packages:
```bash
pip install -r requirements.txt
```

## 4. Run the app

```bash
python main.py
```

Enter a city such as `Kolkata`, `London`, or `Tokyo`. Press Enter on an empty city prompt to quit. The app displays current conditions and a compact forecast table.

## API endpoints
- Current weather: `https://api.openweathermap.org/data/2.5/weather`
- 5-day forecast: `https://api.openweathermap.org/data/2.5/forecast`

Both requests use `q`, `appid`, and `units=metric` parameters. The request timeout is 10 seconds.

## Security: protecting the API key
- Keep the real key only in your local `.env` file.
- `.gitignore` contains `.env`, so Git should not track it.
- Upload `.env.example`, not `.env`.
- Before pushing, run `git status` and confirm `.env` is not listed.
- Never share the key in screenshots or submission notes.
- If a key is exposed, revoke it in your OpenWeather account and create a replacement.

## Test checklist
Test with at least five different cities, for example:
- Kolkata
- London
- Tokyo
- New York
- Mumbai

Also test:
- An unknown city name (should show a city-not-found message).
- A missing or invalid API key (should show a clear 401/key message).
- Network disconnection (should show a network error rather than crash).
- Blank city input (should exit).
- Re-entering the same city within five minutes (should use cached data).

A real API result and forecast require a working personal OpenWeather API key and internet access. The package does not include or fabricate live weather results.

## Submission checklist
According to the InternCircle Project 05 guide, submit:
1. A link to your code and README, without your API key.
2. A screenshot of the app showing a real result.
3. A note describing how you protect the API key.

The guide also asks you to test at least five cities and include a forecast for several days. Run the app with your own key before submitting.
