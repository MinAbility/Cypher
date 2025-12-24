import pathlib
import logging
import sys

def setup_logging():
    # Create logs directory at project root
    logs_dir = pathlib.Path(__file__).resolve().parent.parent / "logs"
    logs_dir.mkdir(exist_ok=True)
    
    # Configure logging
    log_format = '%(asctime)s | %(levelname)-8s | %(name)-15s | %(message)s'
    date_format = '%Y-%m-%d %H:%M:%S'
    
    # Create formatters
    formatter = logging.Formatter(log_format, date_format)
    
    # File handler for all logs
    file_handler = logging.FileHandler(logs_dir / 'Cypher.log', encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    
    # Console handler for important logs
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)
    
    # Configure discord.py logger
    discord_logger = logging.getLogger('discord')
    discord_logger.setLevel(logging.INFO)
    
    # Bot-specific logger
    bot_logger = logging.getLogger('cypher_bot')
    bot_logger.setLevel(logging.DEBUG)
    
    return bot_logger
