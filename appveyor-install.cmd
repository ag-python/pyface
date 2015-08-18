"%sdkverpath%" -q -version:"%sdkver%"
call setenv /x64

rem install python packages
pip install --cache-dir c:/temp nose
pip install --cache-dir c:/temp nose-exclude
pip install --cache-dir c:/temp mock
pip install --cache-dir c:/temp pyside
pip install --cache-dir c:/temp pygments
pip install --cache-dir c:/temp git+http://github.com/enthought/traits.git#egg=traits
pip install --cache-dir c:/temp git+http://github.com/enthought/traitsui.git@feature/python3#egg=traitsui
pip install --cache-dir c:/temp traits_enaml
pip install --cache-dir c:/temp enaml
pip install --cache-dir c:/temp coverage

rem install pyface
python setup.py develop
