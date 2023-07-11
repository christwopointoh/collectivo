"""Utility functions of the collectivo app."""
import os

import yaml


def string_to_list(string: str):
    """Convert a string with items seperated by comma to a list."""
    if string == "" or string is None:
        return []
    else:
        return string.replace(" ", "").split(",")


def get_env_bool(key, default=None):
    """Take the name of an environment variable and return a boolean."""
    options = {
        None: False,
        "": False,
        "false": False,
        "False": False,
        0: False,
        "0": False,
        "true": True,
        "True": True,
        "1": True,
        1: True,
    }
    value = os.environ.get(key, default)
    if isinstance(value, bool):
        return value
    elif value in options:
        return options[value]
    else:
        raise AttributeError(
            f"Environment variable {key} must be 'true' or 'false'."
        )


def load_collectivo_settings() -> dict:
    """Load custom settings from collectivo.yml."""
    config = {}
    try:
        with open("collectivo.yml", "r") as stream:
            config = yaml.safe_load(stream) or {}
            config = expand_vars(config)
            config["extensions"] = set_extensions(config)
            config["authentication_classes"] = get_auth_classes(config)
    except FileNotFoundError:
        print("No collectivo.yml found. Using default settings.")
    except Exception as e:
        print("Error while loading collectivo.yml: %s", e)
    config["allowed_hosts"] = set_allowed_hosts(config)
    config["allowed_origins"] = set_allowed_origins(config)
    return config


def set_allowed_origins(config: dict):
    """Correct configuration of allowed origins from collectivo.yml."""
    if config.get("allowed_origins"):
        return string_to_list(config.get("allowed_origins"))
    else:
        print("'allowed_origins' not defined in collectivo.yml.")
        return []


def set_allowed_hosts(config: dict) -> list[str]:
    """Correct configuration of allowed hosts from collectivo.yml."""
    allowed_hosts = []
    if "allowed_hosts" in config:
        for host in string_to_list(config["allowed_hosts"]):
            host = host.replace("https://", "")
            host = host.replace("http://", "")
            host = host.split(":")[0]  # Remove port
            allowed_hosts.append(host)
    if "development" in config and config["development"]:
        allowed_hosts += [
            "*",
            "0.0.0.0",  # noqa: S104
            "127.0.0.1",
            "localhost",
        ]
    if not allowed_hosts:
        print("No 'allowed_hosts' have been defined.")
    return allowed_hosts


BOOLEANS = {
    "false": False,
    "False": False,
    "true": True,
    "True": True,
}


def expand_vars(input):
    """Expand environment variables recursively for the whole object."""
    match input:
        case str():
            var = os.path.expandvars(input)
            return BOOLEANS.get(var, var)
        case list():
            return [expand_vars(item) for item in input]
        case dict():
            return {key: expand_vars(value) for key, value in input.items()}
        case _:
            return input


def set_extensions(config: dict):
    """
    Create a dictionary of extension configs.

    Configurations are taken from the raw yaml input
    of both collectivo.yml and each extensions' extension.yml.

    Deals with the fact that yaml entries are converted to different data
    types. Tries to capture common cases to ensure that the resulting
    extension configs are nested dictionaries.

    Extensions that do not exist as python modules are removed.
    """
    extensions = {}
    extensions_raw = config.get("extensions")
    if extensions_raw is None:
        return extensions
    if not isinstance(extensions_raw, list):
        print("Error reading collectivo.yml.")
        return extensions
    for ext_config in extensions_raw:
        if isinstance(ext_config, str):
            extensions[ext_config] = {}
            continue
        elif not isinstance(ext_config, dict):
            print("Error reading collectivo.yml.")
            continue
        for ext_name, ext_conf in ext_config.items():
            if isinstance(ext_conf, str):
                extensions[ext_name] = {ext_conf: True}
                continue
            if isinstance(ext_conf, dict):
                extensions[ext_name] = ext_conf
                continue
            elif not isinstance(ext_conf, list):
                continue
            extensions[ext_name] = {}
            for conf_item in ext_conf:
                if isinstance(conf_item, str):
                    extensions[ext_name][conf_item] = True
                    continue
                elif not isinstance(conf_item, dict):
                    print("Error reading collectivo.yml.")
                    continue
                for key, value in conf_item.items():
                    extensions[ext_name][key] = value

    # Check if python modules exist for extensions
    for ext_name in extensions.keys():
        try:
            __import__(ext_config)
        except ImportError:
            print(f"No python module found for extension '{ext_config}'.")
            del extensions[ext_name]

    # Extend extension config based on extension.yml
    for ext_name, ext_config in extensions.items():
        try:
            path = ext_name.replace(".", "/")
            with open(path + "/extension.yml", "r") as ext_stream:
                default_ext_config = yaml.safe_load(ext_stream) or {}
                default_ext_config = expand_vars(default_ext_config)
                for k, v in default_ext_config.items():
                    if k not in ext_config:
                        ext_config[k] = v
        except FileNotFoundError:
            pass

    return extensions


def get_auth_classes(config):
    """Get authentication classes from the extension configs."""
    auth_classes = config.get("authentication_classes") or []
    for ext_name, ext_config in config["extensions"].items():
        if "authentication_classes" in ext_config:
            ext_auth_classes = ext_config["authentication_classes"]
            if isinstance(ext_auth_classes, str):
                auth_classes.append(ext_auth_classes)
            elif isinstance(ext_auth_classes, list):
                for auth_class in ext_auth_classes:
                    auth_classes.append(auth_class)
            else:
                print(f"authentication_classes in {ext_name} invalid")
    return auth_classes
