#!/usr/bin/env python3

def brackets(sequence):
	seqlen = len(sequence)

	if seqlen == 0 :
		return True
	elif seqlen % 2 != 0:
		return False

	oc_count = 0
	for val in sequence:
		if val == "[" : oc_count += 1
		elif val == "]" : oc_count -= 1
		if oc_count < 0 : return False
	
	if oc_count == 0 :  return True
	else : return False


sequence = input()
print(brackets(sequence))
