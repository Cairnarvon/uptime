all:
	@echo "Targets:"
	@echo "  pypi        Build distributions and upload them to PyPI."
	@echo "  uptime.zip  Build docs and zip them for manual upload to PyPI."
	@echo "  clean       Clear out temporary cruft."

.PHONY: pypi
pypi:
	python setup.py sdist upload

uptime.zip: doc/index.rst doc/conf.py
	rm -f uptime.zip
	cd doc; $(MAKE) clean html
	cd doc/_build/html; zip -r ../../../uptime.zip *

.PHONY: clean
clean:
	cd doc; $(MAKE) clean
	rm -f uptime.zip
	rm -rf build
	rm -rf src/*.pyc
