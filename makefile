all:

clean:
	rm -rf *~ *.pyc *.ps
	rm -rf __pycache__
	rm -rf .cache
	cd gesture-recognition; make clean
