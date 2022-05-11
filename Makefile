sync:
	cd ../docs/ && nbdoc_test
	rm -rf docs/
	rsync -am --include '*/' --include '*.py' --exclude '*' ../docs/docs
	git add -A; git commit -m'sync scripts'; git push --set-upstream origin main