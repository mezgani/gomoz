clean:
	find . -iname \*\.pyc | xargs rm -fr 
	find . -iname  *~ | xargs rm -fr 
