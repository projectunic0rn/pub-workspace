# Documentation

## Summary
This repo contains the pub workspace apps. A workspace app is an app that lives on a real-time communication platform (e.g. Slack, Discord etc.) so I use the term *workspace* to refer to any of these real-time communication platforms. The apps take the form of a bot installable through a special link shared with project owners. The goal of the pub workspace apps is to provide project owners with a utility app that's useful throughout their project.

# Events of Interests
Workspaces emit events based on actions that occur. These are the events that all workspace apps currently listen to or intend to listen to.

### Currently
- Bot/App installed
- Message posted to channel

### Future
- Bot/App deleted
- Message posted via thread
- Message updated on channel
- Reaction added to message
- Reaction updated on message
- Message deleted
- Channel topic changed
- Typing occuring on channel

