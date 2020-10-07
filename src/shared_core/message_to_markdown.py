"""Convert a workspace message to markdown"""
class MessageToMarkdown:
    """Convert a workspace message to markdown"""
    def __init__(self, message):
        self.message = message

    def add_quote_block(self):
        """Prepend '>' character to message"""
        self.message = f'> {self.message}'
        self.message = self.message.replace("\n", "\n> ")
        return self

    def add_author_signature(self, message_author, workspace_type):
        """Append author signature to message in format '- name, workspace_type'"""
        message_signature = f'- {message_author}, {workspace_type}'
        self.message = f'{self.message}\n{message_signature}'
        return self
