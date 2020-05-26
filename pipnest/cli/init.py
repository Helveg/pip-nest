from ..interfaces import Action

class InitAction(Action):
    def get_parser_args(self):
        return dict(help="Initialize your NEST module as a pipnest package.")

    def fill_parser(self, parser):
        pass

    def handle_command(self, args):
        pass
