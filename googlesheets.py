from __future__ import print_function
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

import pandas as pd

# This part is copied from the Google Sheets API Quickstart Guide: https://developers.google.com/sheets/api/quickstart/python
SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
# If modifying scopes, delete this file
store = file.Storage('token.json')
creds = store.get()
if not creds or creds.invalid:
	flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
	creds = tools.run_flow(flow, store)
service = build('sheets', 'v4', http=creds.authorize(Http()))

# This is my code
getSheets = lambda : service.spreadsheets()
getValues = lambda : getSheets().values()
batchUpdate = lambda bookId, requests: getSheets().batchUpdate(spreadsheetId=bookId, body={'requests': [requests]}).execute()

def getSheetDict(bookId):
	sheetDict = {}
	result = getSheets().get(spreadsheetId=bookId, fields='sheets.properties').execute()
	for sheet in result.get('sheets', {}):
		properties = sheet.get('properties', {})
		sheetDict[properties['title'].lower()] = properties['sheetId']
	return sheetDict

def read(bookId, sheetName):
	result = getValues().get(spreadsheetId=bookId, range=sheetName).execute()
	df = pd.DataFrame(result.get('values', []))
	return df.rename(columns = df.iloc[0]).drop(0).reset_index(drop=True) if df.shape[0] != 0 else df

def readAll(bookId):
	return {sheetName: read(bookId, sheetName) for sheetName in getSheetDict(bookId).keys()}

def write(bookId, sheetName, df):
	if sheetName.lower() in getSheetDict(bookId):
		getValues().clear(spreadsheetId=bookId, range=sheetName, body={}).execute()
	else:
		batchUpdate(bookId, {'addSheet': {'properties': {'title': sheetName}}})
	body = {'values': [df.columns.fillna('').tolist()] + df.fillna('').values.tolist()}
	getValues().update(spreadsheetId=bookId, range=sheetName, body=body, valueInputOption='RAW').execute()

def delete(bookId, sheetName):
	sheetDict, sheetName = getSheetDict(bookId), sheetName.lower()
	if sheetName in sheetDict:
		batchUpdate(bookId, {'deleteSheet': {'sheetId': sheetDict[sheetName]}})

def deleteOthers(bookId, sheetsToKeep):
	keepSet = set([s.lower() for s in sheetsToKeep])
	for sheetName, sheetId in getSheetDict(bookId).items():
		if sheetName not in keepSet:
			batchUpdate(bookId, {'deleteSheet': {'sheetId': sheetId}})
