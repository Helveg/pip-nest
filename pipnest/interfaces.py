"""
    This module contains all public interfaces that you can use to create plugins.
"""

import abc


class Action(abc.ABC):
    """
        An action registers a subcommand in the pipnest command.

        To register an action in your plugin add an ``pipnest.action`` entry point in the
        setup::

            setup(
                # ...
                entry_points={
                    "pipnest.action" = "my_subcommand = module.my_action"
                }
            )

        If ``module.my_action`` is a class that implements the Action interface then a
        parser for the ``pipnest my_subcommand`` CLI command is registered.
    """

    @abc.abstractmethod
    def get_parser_args(self):
        """
            This method should a dictionary of keyword arguments that are sent to the
            :class:`argparse.ArgumentParser` constructor.
        """
        pass

    @abc.abstractmethod
    def fill_parser(self, parser):
        """
            This method receives an argparse subparser for your command. Here you can add
            all your arguments and so on.
        """
        pass

    @abc.abstractmethod
    def handle_command(self, args):
        """
            This method receives the parsed arguments and should execute the command.
        """
        pass
