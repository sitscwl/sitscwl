cb4_matogrosso_example:
	cwl-runner \
		--basedir ${PWD} \
		cwl/workflow.cwl \
		examples/CB4_MatoGrosso_LULC.yaml \
