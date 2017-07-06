class UnknownCmdError(Exception):
    def __init__(self, cmd):
        self.message = 'Unknown command type: %s' % cmd

    def __str__(self):
        return self.message
