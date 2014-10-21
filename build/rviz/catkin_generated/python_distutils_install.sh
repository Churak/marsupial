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

cd "/home/jared/marsupial/src/rviz"

# Note that PYTHONPATH is pulled from the environment to support installing
# into one location when some dependencies were installed in another
# location, #123.
/usr/bin/env \
    PYTHONPATH="/home/jared/marsupial/install/lib/python2.7/dist-packages:/home/jared/marsupial/build/lib/python2.7/dist-packages:$PYTHONPATH" \
    CATKIN_BINARY_DIR="/home/jared/marsupial/build" \
    "/usr/bin/python" \
    "/home/jared/marsupial/src/rviz/setup.py" \
    build --build-base "/home/jared/marsupial/build/rviz" \
    install \
    $DESTDIR_ARG \
    --install-layout=deb --prefix="/home/jared/marsupial/install" --install-scripts="/home/jared/marsupial/install/bin"
