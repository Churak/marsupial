#!/bin/sh -x

if [ -n "$DESTDIR" ] ; then
    case $DESTDIR in
        /*) # ok
            ;;
        *)
            /bin/echo "DESTDIR argument must be absolute... "
            /bin/echo "otherwise python's distutils will bork things."
            exit 1
    esac
    DESTDIR_ARG="--root=$DESTDIR"
fi

cd "/home/marsupial/marsupial/src/joystick_drivers/wiimote"

# Note that PYTHONPATH is pulled from the environment to support installing
# into one location when some dependencies were installed in another
# location, #123.
/usr/bin/env \
    PYTHONPATH="/home/marsupial/marsupial/install/lib/python2.7/dist-packages:/home/marsupial/marsupial/build/lib/python2.7/dist-packages:$PYTHONPATH" \
    CATKIN_BINARY_DIR="/home/marsupial/marsupial/build" \
    "/usr/bin/python" \
    "/home/marsupial/marsupial/src/joystick_drivers/wiimote/setup.py" \
    build --build-base "/home/marsupial/marsupial/build/joystick_drivers/wiimote" \
    install \
    $DESTDIR_ARG \
    --install-layout=deb --prefix="/home/marsupial/marsupial/install" --install-scripts="/home/marsupial/marsupial/install/bin"
