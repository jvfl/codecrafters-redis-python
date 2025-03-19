import importlib
import glob

from os.path import dirname, basename, isfile, join

from ._command_handler_factory import CommandHandlerFactory


# Loads all modules inside this folder dynamically so all commands get registered
modules = glob.glob(join(dirname(__file__), "*.py"))

for f in modules:
    if isfile(f) and not f.endswith("__init__.py"):
        importlib.import_module(f".{basename(f)[:-3]}", package="app.commands")

__all__ = ["CommandHandlerFactory"]
