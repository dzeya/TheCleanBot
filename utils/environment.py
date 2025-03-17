import os
import logging
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

def load_environment():
    """
    Load environment variables based on ENVIRONMENT variable.
    If ENVIRONMENT is 'development', load from .env.development
    If ENVIRONMENT is 'test' or 'staging', load from .env.test
    Otherwise, load from .env (production)
    """
    env = os.getenv("ENVIRONMENT", "production")
    logger.info(f"Detected environment: {env}")
    
    if env == "development":
        # Load development environment variables
        env_file = ".env.development"
    elif env in ["test", "staging"]:
        # Load test environment variables
        env_file = ".env.test"
    else:
        # Load production environment variables
        env_file = ".env"
    
    # Check if the file exists
    file_exists = os.path.isfile(env_file)
    logger.info(f"Looking for environment file: {env_file} (exists: {file_exists})")
    
    # Try to load the environment file
    if file_exists:
        # Load the appropriate .env file
        load_dotenv(dotenv_path=env_file)
        logger.info(f"Loaded environment from {env_file} (Environment: {env})")
    else:
        # If file doesn't exist, log a warning but continue
        logger.warning(f"Environment file {env_file} not found. Using existing environment variables.")
        
        # If we're in Vercel, environment variables should be set in the Vercel dashboard
        if "VERCEL" in os.environ:
            logger.info("Running in Vercel environment, using Vercel environment variables")
    
    # Check if critical variables are loaded
    token = os.getenv("TELEGRAM_TOKEN")
    webhook_url = os.getenv("WEBHOOK_URL")
    
    if not token:
        logger.error("TELEGRAM_TOKEN is missing or empty!")
    else:
        logger.info(f"TELEGRAM_TOKEN is set: {token[:4]}...{token[-4:]}")
        
    if not webhook_url:
        logger.error("WEBHOOK_URL is missing or empty!")
    else:
        logger.info(f"WEBHOOK_URL is set: {webhook_url}")
    
    return env 