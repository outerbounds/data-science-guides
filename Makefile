sync:
	cd ../docs/ && nbdoc_test
	pwd

copy:
	rm -rf docs/
	rsync -a --include '*/' --include '*.py' --exclude '*' ../docs/docs .
	# git add -A; git commit -m'sync scripts'; git push --set-upstream origin main
