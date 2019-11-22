#!/bin/sh
PATH=.:$PATH;export PATH
if [ -f UPDATE_RELEASE_NUMBER ]
then
cvs update
if [ ! -f release.h ]
then
BUILD=1
else
BUILD=`grep BUILD release.h |cut -f3 -d' '`
BUILD=`expr $BUILD + 1`
fi
cat > release.h << __EOF__
/*
 * \$Id: update_release.sh,v 1.1.1.1 2007/03/14 15:01:09 olteanu Exp $
 */
#define VERSION $1
#define RELEASE $2
#define PATCH $3
#define BUILD $BUILD
__EOF__
cvs commit -m "update release number" release.h
fi
