# Slack App
## Summary 
Project Unicorn slack workspace app written with Python on Flask.

## Python version
- Python 3.x.x

## Quick Start
```bash
# navigate to slack directory
$ cd src/slack

# Install dependencies
$ pip3 install -r requirements.txt

# Run development server
$ export FLASK_APP=app.py
$ python3 -m flask run

# Run tests
$ pytest

# If new dependency installed, update requirements.txt
$ pip3 freeze > requirements.txt
```

## Testing
Reference pytest [documentation](https://docs.pytest.org/en/5.4.3/index.html) for testing.
