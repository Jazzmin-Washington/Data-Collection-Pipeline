from setuptools import setup, find_packages

setup= (name = 'ASOS_data',
        version = 1.0,
        packages = find_packages(),
        install_requires = [
            beautifulsoup4==4.11.1,
                boto3==1.24.2,
                botocore==1.27.2,
                jsonschema==4.6.0,
                pandas==1.4.2,
                pip==22.2.2,
                prometheus_client==0.14.1,
                psycopg2==2.8.6,
                requests==2.28.0,
                s3transfer==0.6.0,
                selenium==4.3.0
                sqlalchemy==1.4.32,
                tqdm==4.64.0,
                urllib3==1.26.9,
                webdriver-manager==3.7.1,
                argparse-prompt])