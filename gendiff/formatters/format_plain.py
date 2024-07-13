
def _format_value(value) -> str:
    """ Format the given value to be included in the output """
    special_values = {
        False: "false",
        True: "true",
        None: "null",
    }
    if isinstance(value, dict):
        return "[complex value]"
    elif isinstance(value, bool) or value is None:
        return special_values[value]
    elif isinstance(value, str):
        return f"'{value}'"
    return value


def format_plain(data: dict) -> str:
    """ Produce formatted data as a string

    Args:
        data: difference between two files
    Return:
        formatted difference, i.e.
            Property 'common.follow' was added with value: false
            Property 'common.setting2' was removed
            Property 'common.setting3' was updated. From true to null
    """

    def _inner(data, path: str = ""):
        """ Assume that data is a dictionary """
        formatted_list = []
        for k, v in sorted(data.items()):
            key, flag = k
            if not path:
                cur_path = key
            else:
                cur_path = path + "." + key

            if flag == -1 and (key, 1) not in data.keys():
                value = f"Property '{cur_path}' was removed"
                formatted_list.append(value)
            elif flag == 1 and (key, -1) not in data.keys():
                formatted_value = _format_value(v)
                value = f"Property '{cur_path}' was added with value: {formatted_value}"
                formatted_list.append(value)
            elif flag == -1 and (key, 1) in data.keys():
                value_from = _format_value(v)
                value_to = _format_value(data[(key, 1)])
                value = f"Property '{cur_path}' was updated. From {value_from} to {value_to}"
                formatted_list.append(value)
            elif flag == 0 and not isinstance(v, dict):
                continue
            elif flag == 0 and isinstance(v, dict):
                formatted_list += _inner(v, cur_path)

        return formatted_list
    return "\n".join(_inner(data))
