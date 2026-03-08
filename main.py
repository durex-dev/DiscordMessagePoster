from client import d_client
from common.utils.config_reader import Config


if __name__ == "__main__":
    config = Config() # type: ignore
    d_client.run(config.client_token)
