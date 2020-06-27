class WorkspaceMessage:
    def __init__(self, message, author, channel_id, workspace_type):
        self.message = message
        self.author = author
        self.channel_id = channel_id
        self.workspace_type = workspace_type
