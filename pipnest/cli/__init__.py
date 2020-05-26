from .plugins import discover
from .init import InitAction
import argparse


def _construct_parser():
    """
        Construct the fully populated argument parser.
    """
    # Parser
    parser = argparse.ArgumentParser()
    # Set all global arguments on the root parser
    _apply_global_arguments(parser)
    parser.add_argument(
        "-v", "--version", action="store_true", help="Show version",
    )
    parser.set_defaults(handler=base_command)
    # Subparsers
    subparsers = parser.add_subparsers(
        title="Actions", description="All available actions to perform.", dest="action",
    )
    # Collect the `actions` plugins, they need to return an object that implements the
    # pipnest.interfaces.Action interface.
    for plugin in discover("actions"):
        # Create the subparser with the plugin defined arguments and name.
        plugin_parser = subparsers.add_parser(plugin.__name__, **plugin.get_parser_args())
        # Fill the parser object with its arguments etc.
        plugin.fill_parser(plugin_parser)
        # Set all global arguments on the plugin parser.
        _apply_global_arguments(plugin_parser)
        # Set the `handler` argument to the command handler
        plugin_parser.set_defaults(handler=plugin.handle_command)

    return parser


class GlobalArgument:
    """
        A global argument can be given at any position in the CLI command.

        For example using a global argument '-x'::

          pipnest -x test

        Is equivalent to::

          pipnest test -x
    """

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def add_to(self, parser):
        """
            Add the global argument to a parser. A global argument should be added to
            each parser in order to function in each position.
        """
        parser.add_argument(*self.args, **self.kwargs)


# A list of global arguments
_global_arguments = [
    # GlobalArgument('-t','--test',help="Test arg")
]


def _apply_global_arguments(parser):
    """
        Apply the global arguments to a parser.
    """
    for arg in _global_arguments:
        arg.add_to(parser)


def handle_command():
    """
        Handle CLI command. Collect all available actions, use
        ``argparse`` to parse the arguments and then execute the action's handler.
    """
    # Get the fully populated argparser
    parser = _construct_parser()
    # Parse the arguments
    args = parser.parse_args()
    # Execute the handler. Every subparser has handler so either it is set or the
    # ArgumentParser informs the user that the given command does not exist and this code
    # isn't reached.
    args.handler(args)


def base_command(args):
    """
        The handler for the ``pipnest`` command withot any specified action.
    """
    if args.version:
        from .. import __version__

        print(__version__)
