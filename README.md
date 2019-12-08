# cloud_command_line_tool
A CLI tool for retrieving important services information from a CSP's API
## User Guide
### Pre-requisites:
  1. Ensure that you have Pandas for Python3 installed. You can achieve this by copying the following command into your Linux terminal: pip3 install pandas
  2. Ensure you run the script using python3, and use your terminal with the following command: python3 CPX_Tool.py

## Future Improvements
1. As this is a command line tool that assumes an API call to the CSP, there must be keys and secrets involved, allowing users to 1. make API calls and 2. authorizing calls that can be made.
  1.1 With the above assumption, a future version should consider a configuration method that allows the user to input new      keys, update keys, etc.
  1.2 With the above assumption, existing methods should be able to return a statement such as "you are not authorized to perform this action" or the equivalent response from the API when either old, depreciated keys are used, or when valid keys do not have existing permissions to make certain API calls.
