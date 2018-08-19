from distutils.core import setup

DISTNAME = 'sfgad'
DESCRIPTION = 'A statistical framework for graph anomaly detection'
MAINTAINER = 'Simon Sudrich'
MAINTAINER_EMAIL = 'uzcyg@student.kit.edu'
URL = 'https://github.com/sudrich/sf-gad'
DOWNLOAD_URL = 'https://github.com/sudrich/sf-gad/archive/0.1.tar.gz'
LICENSE = 'GPL-3.0'

import sfgad

VERSION = sfgad.__version__

SCIPY_MIN_VERSION = '0.13.3'
NUMPY_MIN_VERSION = '1.8.2'
PANDAS_MIN_VERSION = '0.22.0'
NETWORKX_MIN_VERSION = '1.11.0'
JOBLIB_MIN_VERSION = '0.12.2'
MYSQL_CONNECTOR_MIN_VERSION = '8.0.12'


def setup_package():
    metadata = dict(name=DISTNAME,
                    maintainer=MAINTAINER,
                    maintainer_email=MAINTAINER_EMAIL,
                    description=DESCRIPTION,
                    license=LICENSE,
                    url=URL,
                    download_url=DOWNLOAD_URL,
                    version=VERSION,
                    classifiers=[],
                    install_requires=[
                        'numpy>={0}'.format(NUMPY_MIN_VERSION),
                        'pandas>={0}'.format(PANDAS_MIN_VERSION),
                        'scipy>={0}'.format(SCIPY_MIN_VERSION),
                        'networkx>={0}'.format(NETWORKX_MIN_VERSION),
                        'joblib=={0}'.format(JOBLIB_MIN_VERSION),
                        'mysql-connector-python>={0}'.format(MYSQL_CONNECTOR_MIN_VERSION)
                    ],
                    )

    setup(**metadata)


if __name__ == "__main__":
    setup_package()
