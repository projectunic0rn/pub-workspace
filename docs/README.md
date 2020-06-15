# Documentation

## Summary
This repo contains the pub workspaces apps. In the context of this repo a workspace app is an app that lives on a real-time communication platform (e.g. Slack, Discord etc.). This repo uses the term *workspace* to refer to any of these real-time communication platforms. The apps takes the form of a bot installable through a marketplace or special link. The goal of the pub workspace apps is to provide project owners with a utility app that's useful throughout their project.

## System
self note: add overall system design description - whats this system suppose to do and how is it going to do it?

# Events of Interests
Workspaces emit events that are triggered based on actions that occur on the workspaces. These are the following events that all workspace apps listen to.
- Bot/App deleted
- Bot/App installed
- Message posted to channel
- Message posted via thread
- Message updated on channel
- Reaction added to message
- Reaction updated on message
- Message deleted
- Channel topic changed
- Typing occuring on channel
