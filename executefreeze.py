import dhansdk


# Set up logging configuration file
import logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
logger.file_handler = logging.FileHandler('executefreeze.log')
logger.file_handler.setLevel(logging.DEBUG)
from dotenv import load_dotenv

load_dotenv()

import os


def trackfreeze(dhansdk_instance,accountnumber, access_token, loss_threshold):
    
    try:
        print("Tracking freeze conditions...")
        totalrealised,totalunrealised,fin_data,errordetail = dhansdk_instance.getposition()
        print("Tracking freeze conditions...completed")
        
        if totalrealised and ( totalrealised< loss_threshold ) : 
            return {
                "freeze": True,
                "reason": "Significant Losses",
                "total_realised_loss": totalrealised,
                "details": fin_data,
                'error': errordetail
            }
        else:
            return {
                "freeze": False,
                "total_realised_loss": totalrealised,
                "details": fin_data,
                'error': errordetail
            }
        
       
    except Exception as e:
        logger.error(f"Error tracking freeze conditions: {e}")
        return {"error": str(e)}


def freeze_account(accountnumber, access_token, loss_threshold):
    dhansdk_instance = dhansdk.HTTP(accountnumber, access_token)
    trackfreeze_data = trackfreeze(dhansdk_instance,accountnumber, access_token, loss_threshold)
    if  trackfreeze_data.get("freeze"):
        try:
            response = dhansdk_instance.killswitch('ACTIVATE')
            return {
                "freeze_response": response,
                "trackfreeze_data": True
            }
        except Exception as e:
            logger.error(f"Error freezing account: {e}")
            return {"error": str(e)}


def main(accountnumber, access_token, loss_threshold):
    while True:
        try:


            freeze_response = freeze_account(accountnumber, access_token, loss_threshold)
            if freeze_response and freeze_response.get("trackfreeze_data"):
                logger.info(f"Account frozen due to losses: {freeze_response}")
                break  # Exit loop after freezing account
            

        
        except Exception as e:
            logger.error(f"Error in main loop: {e}")




   
if __name__ == "__main__":
    accountnumber = os.environ.get("Dhan_USER_ID")
    access_token = os.environ.get("Dhan_ACCESS_TOKEN")
    loss = os.environ.get("LOSS_THRESHOLD")
    print("Starting freeze execution...")
    print('loss threshold:',loss)
    main(accountnumber, access_token, loss)

