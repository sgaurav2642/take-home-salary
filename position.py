from fivepaisa_client import get_client
import pandas as pd










def position_status(client):
    positions = client.positions()


    if positions['Status'] == 'Success':
        return positions


    else:
        print("Failed to fetch positions:", positions['Message'])
        return "failed to fetch positions"

















