
def get_transactions(file_name):
	transactions = open(file_name).read().split("R/3 Internal Message: ")

	index_to_pop = []
	for i in range(len(transactions)):
		# Arbitrary length to discard the non transaction split
		if (len(transactions[i]) < 10) :
			index_to_pop.append(i)

	# When splitting, it's possible to have undisirable  items. Remove them here
	for i in range(len(index_to_pop) - 1, -1, -1):
		transactions.pop(i)

	return transactions

	
def separate_sections(transaction):
	SECTION_SEPARATOR = "_" * 72
	sections = transaction.split(SECTION_SEPARATOR)

	for i in range(len(sections)):
		#sections[i] = trim_text(sections[i])
		sections[i] = sections[i].strip()
	return sections


def split_section_in_lines(section):
	return section.split('\n')

# Function can be deleted. Does exactly the same thing as strip()
def trim_text(section):
	lines_to_pop = []
	lines = section.split('\n')
	
	# Check the empty lines from the start
	line_number = 0
	while (len(lines[line_number]) <= 1):
		
		lines_to_pop.append(line_number)
		line_number += 1
	
	# Check the empty lines from the end
	line_number = len(lines) - 1
	while (len(lines[line_number]) <= 1):
		lines_to_pop.append(line_number)
		line_number -= 1

	# Order and reverse the lines to pop, starting from the end to pop
	# will have no bad results
	lines_to_pop.sort()
	lines_to_pop.reverse()
	
	# Pop the empty lines
	for i in lines_to_pop:
		lines.pop(i)

	return '\n'.join(lines)
	

def get_transaction_number(sections):
	return sections[0].strip()
	
def get_short_text(sections):
	return sections[2].split('Short Text')[1].strip()

def get_system(sections):
	system = sections[3]
	
	# Split every part of the section from the previous split
	client_split = system.split('Client')
	release_split = client_split[1].split('Release')
	system_split = release_split[1].split('System')
	
	client = release_split[0].strip()
	release = system_split[0].strip()
	system = system_split[1].strip()
	
	system_info = {
				'Client':client, 
				'Release':release, 
				'System':system}
	
	return system_info

def get_message_attributes(sections):
	message_section = sections[4]
	
	# Split every part of the section from the previous split
	processor_split = message_section.split('Processor')
	priority_split = processor_split[1].split('Priority')
	language_split = priority_split[1].split('Language')
	status_split = language_split[1].split('Status')
	component_split = status_split[1].split('Component')
	
	processor = priority_split[0].strip()
	priority = language_split[0].strip()
	language = status_split[0].strip()
	status = component_split[0].strip()
	component = component_split[1].strip()
	
	message_attributes = {
						'Processor': processor, 
						'Priority': priority, 
						'Language': language,
						'Status': status,
						'Component': component}
	
	return message_attributes


def get_description(sections):
	return sections[5].strip()
	
def get_messages(sections):

	messages = []
	for message in sections[6:]:
		messages.append(get_message_components(message))
	
	return messages
	
def get_message_components(message):
	lines = message.split('\r\n')
	type = lines[0]
	name = lines[2][0:31].strip()
	time = lines[2][31:].strip()
	message = '\r\n'.join(lines[3:])
	
	message_components = {
						"Type": type,
						"Name": name,
						"Time": time,
						"Message": message}
	
	return message_components
	
