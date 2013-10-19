array = []
for d in range(1, 60):
	array.append((d * 192 + 1) % 59)
print sorted(array)