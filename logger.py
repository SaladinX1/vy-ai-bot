# import logging

# logging.basicConfig(filename='logs/system.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# def log_action(action, status="OK"):
#     logging.info(f"Action: {action} | Status: {status}")





import logging

logging.basicConfig(filename='logs/system.log', level=logging.INFO, format='%(asctime)s - %(message)s')

def log_action(action, status="OK"):
    logging.info(f"Action: {action} | Status: {status}")
