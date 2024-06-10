import tomllib

version = "0.1.0"

def get_user_agent(nation: str):
    user_agent = f"GreenDumper {version} "
    f"/ Developed by nation:TheSapphire "
    f"/ Operated by nation:{nation}"
    return user_agent

def get_config():
    with open("config.toml", "rb") as f:
        config = tomllib.load(f)
    return config