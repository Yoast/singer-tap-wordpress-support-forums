"""Cleaner functions."""
# -*- coding: utf-8 -*-

from types import MappingProxyType
from typing import Any, Optional
import re
from tap_wordpress_support_forums.streams import STREAMS


class ConvertionError(ValueError):
    """Failed to convert value."""


def to_type_or_null(
    input_value: Any,
    data_type: Optional[Any] = None,
    nullable: bool = True,
) -> Optional[Any]:
    """Convert the input_value to the data_type.

    The input_value can be anything. This function attempts to convert the
    input_value to the data_type. The data_type can be a data type such as str,
    int or Decimal or it can be a function. If nullable is True, the value is
    converted to None in cases where the input_value == None. For example:
    a '' == None, {} == None and [] == None.

    Arguments:
        input_value {Any} -- Input value

    Keyword Arguments:
        data_type {Optional[Any]} -- Data type to convert to (default: {None})
        nullable {bool} -- Whether to convert empty to None (default: {True})

    Returns:
        Optional[Any] -- The converted value
    """
    # If the input_value is not equal to None and a data_type input exists
    if input_value and data_type:
        # Convert the input value to the data_type
        try:
            return data_type(input_value)
        except ValueError as err:
            raise ConvertionError(
                f'Could not convert {input_value} to {data_type}: {err}',
            )

    # If the input_value is equal to None and Nullable is True
    elif not input_value and nullable:
        # Convert '', {}, [] to None
        return None

    # If the input_value is equal to None, but nullable is False
    # Return the original value
    return input_value


def clean_row(row: dict, mapping: dict) -> dict:
    """Clean the row according to the mapping.

    The mapping is a dictionary with optional keys:
    - map: The name of the new key/column
    - type: A data type or function to apply to the value of the key
    - nullable: Whether to convert empty values, such as '', {} or [] to None

    Arguments:
        row {dict} -- Input row
        mapping {dict} -- Input mapping

    Returns:
        dict -- Cleaned row
    """
    cleaned: dict = {}

    key: str
    key_mapping: dict

    # For every key and value in the mapping
    for key, key_mapping in mapping.items():

        # Retrieve the new mapping or use the original
        new_mapping: str = key_mapping.get('map') or key

        # Convert the value
        cleaned[new_mapping] = to_type_or_null(
            row[key],
            key_mapping.get('type'),
            key_mapping.get('null', True),
        )

    return cleaned


def cleanhtml(raw_html):
    """Removes html from string.

    Arguments:
        raw_html {str} -- Input string

    Returns:
        string -- String without HTML Tags
    """
    cleanr = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext


def clean_support_requests(row: dict) -> dict:
    """Clean active versions.

    Arguments:
        row {dict} -- Input row

    Returns:
        dict -- Cleaned row
    """
    mapping: dict = STREAMS['support_requests'].get('mapping', {})

    # Remove URL from ID
    row['id'] = row['id'].replace('https://wordpress.org/support/topic/', '')
    row['id'] = row['id'].replace('/', '')

    # Remove URL around plugin name
    row['plugin'] = row['plugin'].replace('/support/plugin/', '')
    row['plugin'] = row['plugin'].replace('/feed', '')

    # Remove HTML code and Tags from the description/title
    row['description'] = cleanhtml(row['description'])
    row['title'] = cleanhtml(row['title'])

    # Remove Newlines and Tabs
    row['description'] = row['description'].replace('\n', ' ')
    row['description'] = row['description'].replace('\t', '')

    return clean_row(row, mapping)


CLEANERS: MappingProxyType = MappingProxyType({
    'support_requests': clean_support_requests,
})
