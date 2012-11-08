import re 

def separate_sections(transaction):
	SECTION_SEPARATOR = "_" * 72
	sections = transaction.split(SECTION_SEPARATOR)

	for i in range(len(sections)):
		sections[i] = sections[i]
	return sections


def split_section_in_lines(section):
	return section.split('\n')

	
def get_transaction_number(sections):
	return sections[0].strip()


def get_origins(sections):
	section = sections[1].strip()
	lines = section.split('\n')

	recipient = lines[2][:31].strip()
	sender = lines[2][31:].strip()

	origins = {
			"Recipient": recipient,
			"Sender": sender}
	return origins

def get_short_text(sections):
	return sections[2].split('Short Text')[1].strip()

	
def get_system(sections):
	system_section = sections[3]

	regex = re.compile('Client|Release|System')
	splits = re.split(regex, system_section)

	# First split is 'System', ignoring it
	client = splits[1].strip()
	release = splits[2].strip()
	system = splits[3].strip()

	system_info = {
				'Client':client, 
				'Release':release, 
				'System':system}

	return system_info

	
def get_message_attributes(sections):
	message_section = sections[4]

	regex = re.compile('Processor|Priority|Language|Status|Component')
	splits = re.split(regex, message_section)

	# First split is 'Message Attributes', ignoring it
	processor = splits[1].strip()
	priority = splits[2].strip()
	language = splits[3].strip()
	status = splits[4].strip()
	component = splits[5].strip()

	message_attributes = {
						'Processor': processor, 
						'Priority': priority, 
						'Language': language,
						'Status': status,
						'Component': component}

	return message_attributes


def get_description(sections):
	return sections[5].strip()

def get_messages(transaction):

	regex = re.compile('_{72}[\r\n]{2,4}(Memo|Reply)[\r\n]{2,4}')
	splits = re.split(regex, transaction)
	# Poping the first one because it's what is before the first message
	splits.pop(0)

	# Fetch the types that were used for the regex
	types = [splits[i] for i in range(len(splits)) if i % 2 == 0]
	bodies = [splits[i] for i in range(len(splits)) if i % 2 == 1]

	# Fetch the messages details
	messages = []
	for i in range(len(bodies)):
		components = get_message_components(bodies[i])
		components['Type'] = types[i].strip()
		messages.append(components)

	return messages

def get_message_components(message):
	lines = message.split('\r\n')
	author = lines[0][0:31].strip()
	date = lines[0][31:].strip()
	body = '\r\n'.join(lines[1:])

	message_components = {
						"Author": author,
						"Date": date,
						"Body": body}

	return message_components
