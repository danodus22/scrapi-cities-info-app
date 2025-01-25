import yaml

def load_config(file_path):
    """
    Loads a YAML configuration file from the given path.
    Args:
        file_path (str): Path to the configuration file.
    Returns:
        dict: Configuration data.
    """
    try:
        with open(file_path, 'r') as file:
            config = yaml.safe_load(file)
        return config
    except FileNotFoundError:
        print(f"Die Datei {file_path} wurde nicht gefunden.")
        return None
    except yaml.YAMLError as e:
        print(f"Fehler beim Lesen der YAML-Datei: {e}")
        return None
