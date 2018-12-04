This module adds a few extra useful functions to Google's sheets API, to allow you to read from and write to Google spreadsheets using Pandas dataframes. Before using this module, please read the Google Quickstart: https://developers.google.com/sheets/api/quickstart/python

Here are the descriptions of the different methods: 

- read(bookId, sheetName) - returns a dataframe containing all the cells in sheet *sheetName* in spreadsheet *bookId*, with the first row as the column names. 
- readAll(bookId) - returns a dictionary of {sheetName: DataFrame} for each sheet in spreadsheet *bookId*. 
- write(bookId, sheetName, df) - writes dataframe *df* to sheet *sheetName* in spreadsheet *bookId*. Clears existing data if sheet already exists. 
- delete(bookId, sheetName) - deletes sheet *sheetName* from spreadsheet *bookId*. 
- deleteOthers(bookId, sheetsToKeep) - delets all sheets in spreadsheet *bookId* except the ones listed in *sheetsToKeep*. 
