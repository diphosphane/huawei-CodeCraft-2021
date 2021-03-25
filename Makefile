CodeCraft-2021.zip: *.py
	rm SDK/SDK_python/CodeCraft-2021/src/*
	cp *.py SDK/SDK_python/CodeCraft-2021/src/
	cd SDK/SDK_python/; bash CodeCraft_zip.sh
	cp SDK/SDK_python/CodeCraft-2021.zip .