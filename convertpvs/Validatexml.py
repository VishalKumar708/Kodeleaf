import logging

logger = logging.getLogger()


def validate_xml(temp_path, log_path, logger):
    try:
        # ........
        logger.info("XML validation successful1. Temp path: %s, Log path: %s", temp_path, log_path)
        return True
    except Exception as e:
        logger.error("XML validation failed.Error: %s, Temp path: %s, Log path: %s",e, temp_path, log_path)
        return False