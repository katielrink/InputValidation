# Input Validation
## Project Description:
  This project creates a command-line driven telephone listing program, which can store the full names of the users, as well as their telephone numbers. Each input of the name and the telephone number is validated against a preset RegEx to prevent invalid data from being entered into the database. The information is then stored in a simplified method to enable easier searching access later.<br>
  The initial information is read in from a CSV file, where the first column contains the names of the users, and the second column contains their corresponding phone number’s. From which, the user is prompted with the options to add a new user, delete a user by their name, delete a user by their phone number, or print a list of all users stored in the database.
## Compilation Methods:
  The program is written in Python and reads from a CSV file. The program is run via the command line and takes an input argument of the name of the input file. To run the provided test data run the following command from within the folder containing both the file and the python program.<br>
  ```python3 InputValidation.py TestData.csv```

	
Once the program is running, it will prompt you for the information it needs, which you can continue to enter via the terminal window. <br>
## Input Validation Methodology:
### Name Validation
The goal was to allow as many different versions of names as possible. Given that in some countries there is more than a first, middle, and last name [1], I wanted to allow as many names as could reasonably fit. However, I did not want the input to extend past a reasonable limit and cause the program to be unable to handle it, so a limit was used to have a maximum of 90 characters. Further, given that in many countries it is common to hyphenate last names [2], I wanted to allow the last name to be hyphenated as many times as necessary. Further, many foreign names are spelled utilizing letters and symbols unfamiliar to the standard English language [3], such as the ñ, in which removing the added features would entirely change the name. Not to mention names written in entirely other languages, which I did not wish to block as they are valid names. Therefore I settled on the following regex expression. <br>
```^[\w'\-,.][^0-9_!¡?÷?¿/\\+=@#$%ˆ&*(){}|~<>;:[\]]{1,150}$```

  It initially begins matching at the start of the string, as we do not want any part left out. I then create a character set which matches any word, apostrophe, dash, comma, or period characters. <br>
  I then create a negated set to not allow any of the remaining special characters and numbers, which I could not find common usage for in naming conventions, which would mean any use of them was either a malicious attack or simply an incorrect input. Note that, without the characters listed above, it is impossible to my knowledge to create a cross-site scripting attack, or a SQL injection attack within the data input. 
Finally, I required that any character set of the allowed characters without the invalid ones, be within the length of 2-90 characters. Given that certain names written in foreign languages only result in one character letter [4], whereas I could not find any commonly used names that exceeded 150 characters long even with included family names [5].  <br>

**Criteria : Between 1-15 of the allowed standard characters**

### Phone Number Validation
  The goal was to allow as many international numbers, and as many different number formatting means as possible. The formatting came based on common practice methods, so any method of writing numbers that is not common practice will most likely not be accepted.<br>
	The country code is always preceded by a +, which indicates it’s an international number. The country code can be anywhere from 1-3 digits long. However some niche codes may contain a 1- to begin with, but most of the codes can be found under a larger country code, so they are not as important to include as a possibility [6]. <br>
	This is then followed by the area code, which can be anywhere from 2-4 digits long. It is sometimes separated out by spaces or parentheses, but it can just be left interconnected with the rest of the numbers [7]. The numbers of the area code can be anywhere from 0-9 and be leading with a 0.<br>
	Following the area code is the local phone number. As far as my research showed, the maximum number of digits that any local telephone code could ave was 10, whereas there must always be a minimum of 5 additional numbers. Granted these vary widely based on region, and ideally you would compare the area code to the number of digits following, however given that the digit length is within the valid range it is more likely than not it falls into one of the valid phone numbers in existence [9].<br> 
	The final section of the phone number the standard practice is to follow the phone number with a comma, and then lead into the abbreviation ext followed by the extension number. It has been written by some, however, without the comma, and occasionally without the space when the entire number is simply formatted together. As far as I can tell there is no limit on the possible length of the phone number extension, so a cap at 20 characters reasonably allows all possible extensions without overloading the program [10].<br>
  ```
    #country code
    reg = "([+][1-9]{1,3})?[-\s\.]{0,1}"
    #area code
    reg += "([(]{0,1}\d{2,4}[)]{0,1})\s{0,1}"
    #additional identifying numbers
    reg += "[-\s\.0-6]{1}[-\s\.0-9]{4,9}"
    #extension
    reg += "([,]?[\\s]?ext[\\s]?\\d{1,20})?$"
```
    
  The above allows for an initial, optional country code to demonstrate an international number. If one exists it must first have a plus sign to indicate its existence, followed by 1-3 numbers in the range of 1-9. It then indicates the optional existence of either a dash, a space, or a period.<br>
	Following which, I check for the area code, which are all required to exist. An optional parenthese exists on either side of the statement, where there can either be one or none. It then must contain any three digits form 0-9. It is then followed by an optional whitespace character. <br>
	After the area code comes the additional identifiers, which vary from location to location. It must at least have one additional digit, or a dash, period, or space, to indicate more digits are to come. Then at minimum you must follow by 4-9 additional numbers, which can be separated by a space, dash, period, or nothing.<br>
	The final part of the phone number is the phone extension, which is optional. There can be at maximum one comma following the main phone number, and then optionally one space. There then must be the expression ext followed by an optional space. It should then include one or more digits to indicate the extension number. <br>

**Criteria : Optional Country Code, 2-4 Digit Area Code, 5-10 digit local phone number, optional extension following ‘ext’**
## Evaluation of Results
### Name Validation
In testing, when a cross-site scripting or a SQL injection attack was attempted, the result was caught as invalid and not processed. When processed against a list of randomly generated names, all of the names proved to pass as valid, including many foreign and accented names. However, due to the way unicode was read in, certain random characters would not be processed. Overall, the validation process is flawed for universal names, but does accomplish its goals.<br>

**Pros:**
- Allow Names with Various Symbols<br>
- Allow diverse/foreign names<br>
- No restrictions on family names<br>
- No restrictions on ordering<br>
**Cons:**<br>
- Errors with Unicode processing<br>
- Vague enough to allow some unknown malicious content to be injected<br>


### Phone Number Validation
  In testing, all obviously incorrect phone numbers, such as those without numbers, too few numbers, and too many numbers showed up as incorrect. As more precise testing was done, the program proved to be able to handle most common uses of splitting up the numbers, such as parentheses, dashes, spaces, and periods. However, when these characters are more sporadically placed, thus abandoning common practice, the program can only read them as invalid numbers. Additionally, the program cannot recognize invalid area codes, or whether the area code corresponds correctly to the country. It can only work on vague principles. However, assuming the numbers themselves are written correctly, the program can handle most different valid and invalid number formats. <br>

**Pros:**
- A wide variety of country’s phone numbers can be accepted<br>
- Extensions and different countries are accepted<br>
- Commonly used formats are accepted<br>
**Cons:**<br>
- Invalid area and country codes will not be detected<br>
- Doesn’t recognize number combinations that do not exist<br>
- Can’t distinguish between the same number but with different seperations<br>

## Test Data : 

### Valid Data:
Bruce Schneier : (212)456-7891<br>
Schneier, Bruce : 212-456-7891<br>
O’Malley, John F. : (212)-456-7893<br>
John O’Malley-Smith : 212.456.7894<br>
Ron O’Henry-Smith-Barnes : 2124567895<br>
Brad Everett Samuel Smith : +12124567896<br>
アイヌ イタク : +12124567897<br>
Čeština: +1 212.456.7898<br>
Mooring Böökingharde : (703) 123-1234 ext 204<br>
LùGáànda : +1-212-456-7900<br>
Русский язык : +44-7911 123456<br>
你好 : 0473 36 29 65<br>
### Invalid Name:
L33t Hacker : ,+8618980642709<br>
<Script>alert(“XSS”)</Script> : 123-1234<br>
select * from users; : 011 123 123 1234<br>
k@tielkazzo : 011 1 703 111 1234<br>
xxx@xxx.xxx’ OR 1 = 1 LIMIT 1 — ‘ ] : +212-456-7899<br>
## Invalid Phone Number
Juan García Reyes : 123<br>
Rodriguez y Calderón, Carla : <script>alert(“XSS”)</script><br>
Marc-André ter Stegen : +01 (703) 123-1234<br>
Kagawa, Shinji : 123456789ext<br>
あいこあけみ : +1234 (201) 123-1234<br>
Katie Rink : (703) 123-1234 e 204<br>

## References
[1] https://en.wikipedia.org/wiki/Spanish_naming_customs<br>
[2]https://en.wikipedia.org/wiki/Double-barrelled_name#:~:text=A%20double%2Dbarrelled%20name%20is,Mandela%20and%20Sacha%20Baron%20Cohen.<br>
[3] https://languagelog.ldc.upenn.edu/nll/?p=18769<br>
[4] https://digitalcommons.butler.edu/cgi/viewcontent.cgi?article=5327&context=wordways<br>
[5] https://www.historyrundown.com/top-5-people-with-the-longest-names/<br>
[6] https://countrycode.org/<br>
[7] https://support.twilio.com/hc/en-us/articles/223183008-Formatting-International-Phone-Numbers<br>
[8] https://en.wikipedia.org/wiki/National_conventions_for_writing_telephone_numbers<br>
[9]https://www.stylemanual.gov.au/grammar-punctuation-and-conventions/numbers-and-measurements/telephone-numbers<br>
[10] https://bizfluent.com/how-8493758-abbreviate-phone-extension.html<br>


