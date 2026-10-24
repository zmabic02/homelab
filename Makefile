KUBE_PROMETHEUS_STACK_VERSION := 91.8.2

.PHONY: \
	cluster-install \
	cluster-up \
	cluster-down \
	cluster-restart \
	cluster-status \
	observability-install \
	observability-uninstall

cluster-install:
	./scripts/install-k3s.sh

cluster-up:
	sudo systemctl start k3s

cluster-down:
	sudo systemctl stop k3s

cluster-restart:
	sudo systemctl restart k3s

cluster-status:
	sudo systemctl status k3s
