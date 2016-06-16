from __future__ import print_function
import httplib2
import os
import time
from ISStreamer.Streamer import Streamer

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/sheets.googleapis.com-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Sheets API Python Quickstart'

# Initialize the Initial State Streamer
streamer = Streamer(bucket_key="rsvp", access_key="Your_Access_Key")

def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'sheets.googleapis.com-python-quickstart.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def main():
    while True:
        """Shows basic usage of the Sheets API.

        Creates a Sheets API service object and prints data from 3 different
        cells in our spreadsheet:
        https://docs.google.com/spreadsheets/d/Your_Spreadsheet_Id/edit
        """
        credentials = get_credentials()
        http = credentials.authorize(httplib2.Http())
        discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                        'version=v4')
        service = discovery.build('sheets', 'v4', http=http,
                                  discoveryServiceUrl=discoveryUrl)

        spreadsheetId = 'Your_Spreadsheet_Id_from_Sheet_URL'
        # Sheet name and cells you want data from
        rangeName = 'Sheet4!A2:C2'
        result = service.spreadsheets().values().get(
            spreadsheetId=spreadsheetId, range=rangeName).execute()
        values = result.get('values', [])

        if not values:
            print('No data found.')
        else:
            print('Attending, Not Attending, Responded:')
            for row in values:
                # Print columns A, B and C, which correspond to indices 0, 1 and 2.
                print('%s, %s, %s' % (row[0], row[1], row[2]))
                streamer.log("Attending",str(row[0]))
                print("Attending",str(row[0]))
                streamer.log("Not Attending",str(row[1]))
                print("Not Attending",str(row[1]))
                streamer.log("Responded",str(row[2]))
                print("Responded",str(row[2]))
                streamer.flush()
        time.sleep(900)

if __name__ == '__main__':
    main()
