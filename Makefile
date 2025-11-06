VERSION ?= 0.1.1
CHART_VERSION ?= 0.1.1
DATE := $(shell date +%Y-%m-%d)

update-version:
	# Update the chart versions (cross-platform compatible sed)
	sed -i.bak -e 's/^version:.*/version: $(CHART_VERSION)/' \
		-e 's/^appVersion:.*/appVersion: "$(VERSION)"/' ./deployments/charts/canchat-role-change/Chart.yaml && rm -f ./deployments/charts/canchat-role-change/Chart.yaml.bak

	# Add changelog entry if not already done
	grep "$(CHART_VERSION)" ./deployments/charts/canchat-role-change/CHANGELOG.md || \
		{ echo "## [$(CHART_VERSION)] - $(DATE)\n\n" | cat - ./deployments/charts/canchat-role-change/CHANGELOG.md > temp && mv temp ./deployments/charts/canchat-role-change/CHANGELOG.md; }
	grep "$(VERSION)" ./CHANGELOG.md || \
		{ echo "## [$(VERSION)] - $(DATE)\n\n" | cat - ./CHANGELOG.md > temp && mv temp ./CHANGELOG.md; }