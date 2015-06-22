import sys
import os
import argparse
import pyperclip
import re
from match import PhoneMatch, EmailMatch

''' main entry point for cppy '''

__version__ = '0.0.1'

PHONE_REGEX = r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})'
EMAIL_REGEX = r'\w+[.|\w]\w+@\w+[.]\w+[.|\w+]\w+'

def main():
	parser = argparse.ArgumentParser(prog= 'Copy Parse', description='Parse emails and phone numbers from copied text')
	args = parser.parse_args()

	text = str(pyperclip.paste())
	if text:
		matches = []
		email_re = re.compile(EMAIL_REGEX)
		phone_re = re.compile(PHONE_REGEX)

		if len(email_re.findall(text)) > 0:
			for g in email_re.findall(text):
				match = EmailMatch(g)
				try:
					match.log()
				except Exception as ex:
					print str(ex)

		if len(phone_re.findall(text)) > 0:
			for g in phone_re.findall(text):
				match = PhoneMatch(g)
				try:
					match.log()
				except Exception as ex:
					print str(ex)
		

