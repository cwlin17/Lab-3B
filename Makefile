# NAME: Don Le, Carol Lin
# EMAIL: donle22599@g.ucla.edu, carol9gmail@yahoo.com
# ID: 804971410, 804984337

default: run.sh
	rm -f lab3b
	ln run.sh lab3b
	chmod +x lab3b

dist:
	tar -czvf lab3b-804984337.tar.gz README Makefile lab3b.py run.sh

clean:
	rm -f lab3b-804984337.tar.gz lab3b
