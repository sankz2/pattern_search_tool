## Usage
<b>File Upload and Extraction</b>

* In the "Upload and Extract Files" section, click the "Browse" button.
* A file dialog will appear. Select a .tar.gz or .zip file containing the log files from your system.
* The selected file path will appear in the input field next to the "Browse" button.
* Click the "Upload and Extract" button.
* The file will be uploaded and extracted automatically. If the archive contains nested archives, those will also be extracted.
* The extracted files will be saved in the ~/extracted directory, and a success message will be displayed.
* After extraction, click the "Download Extracted Files" button.
* Choose a destination folder to save the extracted files. The files will be copied to the selected location. 

<b>Error Detection</b>
* In the "Error Detection" section, click the "Browse" button next to the "Choose error detection folder" input field.
* A directory selection dialog will appear. Choose the folder containing the log files you want to analyse. 

&emsp;<b>Uploading the Error Detection Folder</b>

* After selecting the folder, click the "Upload for Detection" button.
* The selected folder path will appear in the input field, and a success message will be displayed. 

&emsp;<b>Entering Connection Name (Optional)</b>

* If you want to search for errors related to a specific connection, enter the connection name in the "Enter the connection name" field. 

&emsp;<b>Entering Error Patterns</b>

* In the "Enter patterns" field, type the keywords or patterns you want to search for in the log files. Separate multiple patterns with spaces.
* The patterns will automatically appear in the list below the input field. 

&emsp;<b>Adding Preset Patterns</b>

* Click the "Add Presets" button to quickly add common error patterns like "Exception," "Error," and "Failed." 

&emsp;<b>Deleting a Pattern</b>

* Select the pattern from the list and click the "Delete Selected Pattern" button to remove it. 

&emsp;<b>Starting Error Detection:</b>

* Click the "Start Detection" button to begin scanning the log files for the specified patterns.
* The application will generate an output file for each log file, containing only the lines that match the patterns.
* A success message will be displayed once detection is complete, and the "Download Result" button will be enabled. 

&emsp;<b>Downloading Detection Results</b> 

* Click the "Download Result" button.
* Choose a destination folder to save the results. The output files will be copied to the selected location.
