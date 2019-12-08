# cloud_command_line_tool
A CLI tool for retrieving important services information from a CSP's API
## User Guide
### Pre-requisites & installations:
1. Ensure that you have Pandas for Python3 installed. You can achieve this by copying the following command into your Linux terminal: pip3 install pandas
2. Ensure you run the script using python3, and use your Bash terminal with the following command: python3 CPX_Tool.py

## Assumptions
1. When calculating the status of an instance/service, I have use CPU as the sole factor and flagged an "unhealthy" instance where CPU usage is equal to or greater than 80%
2. Another assumption made here is that the number of instances running a given service is random - some additional testing may need ot be conducted around method 3, which flags services with less than 2 healthy instance. I have tested this by increasing the number, and the method seems to work appropriately given an increase in the number in line 102 of the source code. 
3. **Please also note that in order to prevent a printout overload when calling method 4 - which has the ability to track and print CPU/Memory of all instances of a given service over time (until the command is stopped, e.g. ctrl + c), I have built in a 10 second sleep time to cool off the loop. 

## Future Improvements
1. As this is a command line tool that assumes an API call to the CSP, there must be keys and secrets involved, allowing users to 1. make API calls and 2. authorizing calls that can be made.
 -1.1 With the above assumption, a future version should consider a configuration method that allows the user to input new      keys, update keys, etc.
 -1.2 With the above assumption, existing methods should be able to return a statement such as "you are not authorized to --perform this action" or the equivalent response from the API when either old, depreciated keys are used, or when valid keys do not have existing permissions to make certain API calls.
2. There are improvements to be made to the first function, that provides a write out of all services and hardware statistics across all IP addresses. Firstly I have not yet set the "Status" feature, which involves writing a function that takes CPU usage as an int, and returns a string based on the int, which will then get inserted into the dataframe. Secondly, I a second iteration should seek to slim down the number of data structures. Lastly, the code needs to be tidied up and a little more sophistication used when formatting strings of data piped in. In addition, some additional stripping must be done before passing the strings into the dataframe.
3. A further improvement is the overall efficiency of the code. Currently the code relies on several big data structures. I have tried to minimise this by abstracting a lot of the heavy lifting away to  `   running_services()  `  - but future improvements to the code should look at further reducing the number of data structures. 
4. Another furutre improvement would be to have the successful or unsuccessful execution of a function - after  `   main() `    loop back to main again, or ask if the user would like to quit the program.
5. A final future improvement is that currently, due to the piping to and from the shell, there are a number of printout statements prior to the final print out of information that covers the deliverables. I would look to remove these in a future version.

