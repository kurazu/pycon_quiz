import io

START = u'<div data-load="'
END = u'"></div>'

with io.open('index.html', 'r', encoding='utf-8') as input:
	content = input.read()

def load_file(filename):
	print u'Inserting', filename
	with io.open(u'../solutions/official/%s' % filename, 'r', encoding='utf-8') as f:
		return f.read()

output = []
while START in content:
	output.append(content[:content.index(START)])
	content = content[content.index(START) + len(START):]
	end_idx = content.find(END)
	filename = content[:end_idx]
	output.append(load_file(filename))
	content = content[end_idx + len(END):]
output.append(content)

with io.open('compiled.html', 'w', encoding='utf-8') as out:
	out.write(u''.join(output))
