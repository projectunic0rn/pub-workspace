
class MessageToMarkdown:
    def __init__(self, message):
        self.message = message
    
    def add_quote_block(self):
        self.message = f'> {self.message}'
        return self
    
    def add_author_signature(self, message_author, workspace_type):
        message_signature = f'- {message_author}, {workspace_type}'
        self.message = f'{self.message}\n{message_signature}'
        return self