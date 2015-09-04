.PHONY: clean pack

clean:
	rm -f PEPs.docset/Contents/Resources/Documents/backblue.gif
	rm -f PEPs.docset/Contents/Resources/Documents/cookies.txt
	rm -f PEPs.docset/Contents/Resources/Documents/fade.gif
	rm -rf PEPs.docset/Contents/Resources/Documents/hts-cache
	rm -f PEPs.docset/Contents/Resources/Documents/hts-log.txt
	rm -f PEPs.docset/Contents/Resources/Documents/index.html

pack:
	tar -czvf PEPs.tgz PEPs.docset
