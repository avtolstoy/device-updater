

class CompositeProgress:
	def __init__(self, spans, target):
		self.spans = spans
		self.target = target
		for s in self.spans:
			spans.onChange += self.update

	def update(self):
		total = 0
		current = 0
		for s in self.spans:
			total += s.max-s.min
			current += s.current-s.min
		self.set(current, total)

	def set(self, current, total)
		self.target.max = total
		self.target.update(total)


class ProgressSpan:
	# span, currrent
	# posts events when current is changed
	def __init__(self,max,min=0,name):
		self.max = max
		self.min = min
		self.name = name
		self.current = min
		self.onChange = EventHandler()

	def update(current):
		if current!=self.current:
			self.current = current
			self.onChange.fire(self)
