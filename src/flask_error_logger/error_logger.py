import os
from typing import Sequence, Union

from flask import Flask
from peewee import Model


class ErrorLogger:
    """
    Class for holding state for logging.
    """

    def __init__(self,
                 app: Flask,
                 error_types: Sequence[str] = ("5xx",),
                 error_templates: Union["dict[str,str]", bool] = None,
                 ):
        if not isinstance(app, Flask):
            raise TypeError("app must be a Flask instance")
        self.app = app
        self.error_types, self.all_4xx, self.all_5xx = self.create_error_list(
            error_types)
        self.show_templates, self.error_templates = self.create_templates_mapping(
            error_templates)

    def create_error_list(self, error_seq: Sequence):
        """
        Create a list of errors for a given error sequence.
        If 4xx or 5xx in error_seq, no 4xx or 5xx series codes will be in returned list. Instead, all_4xx or all_5xx will be True.
        Args:
            error_seq(Sequence): The error sequence.

        Returns:
            tuple[`error_list(list)`, `all_4xx`, `all_5xx`]

        """
        error_list = []
        all_4xx = False
        all_5xx = False
        error_seq_lower_case = [str(error).lower() for error in error_seq]
        # check for 4xx and 5xx
        if "4xx" in error_seq_lower_case:
            all_4xx = True
        if "5xx" in error_seq_lower_case:
            all_5xx = True
        # get errors if not 4xx or 5xx
        if all_4xx:
            for error in error_seq_lower_case:
                if error.startswith("5") and not error.endswith("x"):
                    error_list.append(error)
        if all_5xx:
            for error in error_seq_lower_case:
                if error.startswith("4") and not error.endswith("x"):
                    error_list.append(error)

        return error_list, all_4xx, all_5xx

    def create_templates_mapping(self, error_templates):
        """Create a mapping for error types with templates

        Args:
            error_templates (dict|bool|None): error templates received at initialisation.

        Returns:
            show_templates(bool), error_templates(dict) 
        """
        show_templates = False
        template_dict = {}
        if error_templates == True or isinstance(error_templates, dict):
            show_templates = True
        if isinstance(error_templates, dict):
            for key, value in error_templates.items():
                template_dict[str(key)] = value
        return show_templates, template_dict
