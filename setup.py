from distutils.core import setup

setup(name='mtagtfs',
      version='1.0',
      description='Collecting real-time data from the MTA Developer API to compute subway delays at each station',
      author='Junjie Cai & Abdullah Kurkcu',
      author_email='jc9033@nyu.edu',
      url='https://github.com/ak4728/MTA-Subway-Delay',
      py_modules=['mtagtfs'],
      install_requires=['requests',
                    'datetime',
                    'pandas',
                    'gtfs-realtime-bindings'
                  ]
     )