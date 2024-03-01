export FLASK_APP=index.py
export FLASK_DEBUG=1

run:
	# fuser -k 5000/tcp
	# pipreqs > requirements.txt --force
	# raml2html doc.raml > templates/doc.html
	flask run
