update:
	cd ../docs/ && git pull && make update

copy:
	rm -rf docs/
	rsync -a --include '*/' --include '*.py' --exclude '*' ../docs/docs .
	git add -A; git commit -m'sync scripts'; git push --set-upstream origin main

all: update copy