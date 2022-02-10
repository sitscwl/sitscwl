#
# This file is part of sitscwl
# Copyright (C) 2022 INPE.
#
# sitscwl is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

FROM brazildatacube/sits:0.16.0
# DIGEST:sha256:785ce40c030a3bf299a37a79dc3720269d5ba0646ff71a21506499aaac523e58

#
# Installing the SITS 0.15.1-1
#
RUN Rscript -e "devtools::install_github('e-sensing/sits@v0.15.1-1')" \
	&& Rscript -e "devtools::install_version('tidyr', version='1.2.0', repos = c('https://vps.fmvz.usp.br/CRAN/'))" \
	&& Rscript -e "devtools::install_version('terra', version = '1.4.22', repos = c('https://vps.fmvz.usp.br/CRAN/'))"
