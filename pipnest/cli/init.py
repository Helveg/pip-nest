from ..interfaces import Action
from ..project import ProjectMetadata, _project_meta, ProjectProposal

def validate_meta(meta, v):
    if meta.choices and v not in meta.choices:
        print("Please select one of the given choices.")
        return False
    return v != ""


def input_meta(meta):
    choices = "" if meta.choices is None else " ({})".format("/".join(meta.choices))
    default = "" if meta.default is None else " [{}]".format(meta.default)
    response = ""
    while True:
        response = input(meta.label + choices + default + ": ")
        if not response and meta.default is not None:
            return meta.default
        if validate_meta(meta, response) is True:
            break

    return response


def get_meta_parser_kwargs(meta):
    kwargs = {}
    if meta.choices is not None:
        kwargs["nargs"] = "?"
        kwargs["choices"] = meta.choices
    return kwargs


class InitAction(Action):
    def get_parser_args(self):
        return dict(help="Initialize your NEST module as a pipnest package.")

    def fill_parser(self, parser):
        parser.add_argument("directory", nargs="?", default=".", help="Path to create the project in")
        parser.add_argument("-f", "--force", action="store_true", help="Force overwrite of existing project")
        # Add an argument per project metadata.
        for arg in _project_meta:
            kwargs = get_meta_parser_kwargs(arg)
            parser.add_argument("--" + arg.name, help=arg.help, **kwargs)

    def fill_meta(self, args):
        # Check which metadata was not provided as argument in the CLI command.
        missing_args = [m for m in _project_meta if args.__dict__[m.name] is None]
        # Ask for the missing metadata as user input.
        for m in missing_args:
            # Update the args namespace with the validated user input.
            args.__dict__[m.name] = input_meta(m)

    def handle_command(self, args):
        # Fill in the missing metadata
        self.fill_meta(args)
        # Create a proposal from the arguments.
        p = ProjectProposal.from_args(args)
        try:
            # Execute the proposal to create the project.
            p.create()
        except FileExistsError as f:
            print(f)
