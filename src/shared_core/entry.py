"""Entrypoint for apps into shared core module"""
class Entry: # pylint: disable=too-few-public-methods
    """Entry follows facade pattern - acts as boundary
       between apps and shared code. Includes data object
       mapping and request forwarding.
    """
    def __init__(self):
        pass

    def process_app_installed_event(self):
        """Message processor, map and forward data."""
        raise NotImplementedError

    def process_app_uninstalled_event(self):
        """Message processor, map and forward data."""
        raise NotImplementedError

    def process_message_posted_event(self):
        """Message processor, map and forward data."""
        raise NotImplementedError

    def process_message_updated_event(self):
        """Message processor, map and forward data."""
        raise NotImplementedError

    def process_message_deleted_event(self):
        """Message processor, map and forward data."""
        raise NotImplementedError

    def process_reaction_added_event(self):
        """Message processor, map and forward data."""
        raise NotImplementedError

    def process_reaction_removed_event(self):
        """Message processor, map and forward data."""
        raise NotImplementedError

    def process_channel_topic_change_event(self):
        """Message processor, map and forward data."""
        raise NotImplementedError
    