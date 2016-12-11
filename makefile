all:
	
clean:
	rm -f *~ *.pyc *.ps

cleaner: clean
	rm -rf __pycache__
	rm -rf .cache
