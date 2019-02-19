#this function receives an string and looks for an IP address inside the string
def ip(input_str):

	#importing the regular expression module
	from re import compile
	
	#this is the pattern to match an ip
	#the ip can be formated with dots, commas or any combination of the two
	# xxx.xxx.xxx.xxx or xxx,xxx,xxx,xxx or xxx.xxx,xxx,xxx
	#I'm using this pattern because i find it very clever although it is not very readable
	#is the same as using r'\d{1,3}[,.]\d{1,3}[,.]\d{1,3}[,.]\d{1,3}' 
	pattern = compile(r'([0-9]{1,3})([.,]([0-9]{1,3})){3}')
	
	#finditer finds all matchings in the string
	matches = pattern.finditer(input_str) # this is a list
		
	for match in matches:
		#this returns only the IP and not the whole object
		#as we're garanteed we only have one match we can retrun rigth away
		return match.group(0)
