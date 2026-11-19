# Urban Routes — End-to-End Test Automation

Automated UI tests for **Urban Routes**, a taxi-ordering web app, written in Python with Selenium WebDriver and Pytest. Built as the final automation project of the TripleTen QA program.

The suite covers the full ordering flow: setting a route, choosing a tariff, verifying a phone number by SMS code, adding a payment card, leaving a comment for the driver, ordering extras and confirming the order.

## Tech stack

- Python 3
- Selenium WebDriver 4.25
- Pytest 8.3
- Google Chrome + ChromeDriver

## Project structure

| File | Purpose |
|---|---|
| `main.py` | Test class `TestUrbanRoutes` with the 8 test cases |
| `pages.py` | Page Object `UrbanRoutesPage`: locators and page actions |
| `data.py` | Server URL and test data (addresses, phone, card, comment) |
| `helpers.py` | Helpers to check that the server is reachable and to read the SMS code |
| `requirements.txt` | Project dependencies |

## Test cases

| # | Test | What it checks |
|---|---|---|
| 1 | `test_set_route` | "From" and "To" addresses are filled in correctly |
| 2 | `test_select_plan` | The Comfort tariff is selected |
| 3 | `test_fill_phone_number` | Phone number is added and confirmed with the SMS code |
| 4 | `test_fill_card` | A card is added and shown as the payment method |
| 5 | `test_comment_for_driver` | The comment for the driver is saved |
| 6 | `test_order_blanket_and_handkerchiefs` | The blanket and handkerchiefs option is switched on |
| 7 | `test_order_2_ice_creams` | The ice cream counter shows 2 |
| 8 | `test_car_search_model_appears` | After ordering, the car search window appears |

## Design decisions

- **Page Object Model.** All locators (ID, class name, CSS and XPath) and page actions live in `pages.py`, so the tests in `main.py` only describe the scenario. If the UI changes, only the page object needs updating.
- **Explicit waits, no fixed sleeps.** Every interaction waits for the element to be visible or clickable with `WebDriverWait`, which keeps the tests fast and stable.
- **SMS code from the browser logs.** Chrome performance logging is enabled so the confirmation code can be read from the network response in Chrome DevTools logs, without a real phone.
- **Independent tests.** Each test opens the page and sets the route again, so tests can run alone or in any order.

## How to run

1. Clone the repository:
   ```bash
   git clone https://github.com/surfgtho-tech/urban-routes-selenium-automation.git
   cd urban-routes-selenium-automation
   ```
2. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Start a new Urban Routes server and paste its URL into `URBAN_ROUTES_URL` in `data.py`.
4. Run the tests:
   ```bash
   pytest main.py -v
   ```

> Note: the Urban Routes server is a temporary test environment provided by TripleTen, so the URL in `data.py` has to be updated each time a new server is started.

## Author

**William Cunha** — Junior QA Tester
[LinkedIn](https://www.linkedin.com/in/william-cunha-429359348/) · [GitHub](https://github.com/surfgtho-tech)

Como colar:

No repositório, abra o README.md e clique no ícone de lápis (✏️).
Apague tudo (Ctrl+A, Delete) e cole o texto.
Clique em Commit changes... e use uma mensagem como docs: update README with project overview.
Clique em Commit changes de novo pra confirmar.
