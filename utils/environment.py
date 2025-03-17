import os
from dotenv import load_dotenv

def load_environment():
    """
    Load environment variables based on ENVIRONMENT variable.
    If ENVIRONMENT is 'test' or 'staging', load from .env.test
    Otherwise, load from .env (production)
    """
    env = os.getenv("ENVIRONMENT", "production")
    
    if env in ["test", "staging"]:
        # Load test environment variables
        env_file = ".env.test"
    else:
        # Load production environment variables
        env_file = ".env"
    
    # Load the appropriate .env file
    load_dotenv(dotenv_path=env_file)
    
    # Log which environment we're using
    print(f"Loaded environment from {env_file} (Environment: {env})")
    
    return env 