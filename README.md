# Review Analyzer

A work-in-progress that helps business owners efficiently analyze reviews to identify strong and weak points.

## Steps to Use

Once the software is running and open in your browser, do the following:
- Go to your product's review page
- Copy a long review and paste it into the text box
- Hit the "Analyze Review" button
- You will see the review score (an estimated rating based on the text content) as well as the review text. Aspects of your product that the reviewer liked is highlighted in green and parts that were disliked is highlighted in red.

## Steps to Run

- [Install Python 3.9 or above](https://www.python.org/downloads/)
- Run `pip install -U -r requirements.txt` in order to install project dependencies
- Open `serve.py` in a text editor. Paste in your OpenAI API key in the spot where it says `PASTE_YOUR_API_KEY_HERE`. Keep the quotes around the api key.
- Run `python -m flask --app serve run`
- Navigate to `127.0.0.1:5000` or the url displayed in your console to view the review analyzer in action!
