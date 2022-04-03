
DESTDIR=""

MANDIR=$DESTDIR/usr/share/man/man1
BINDIR=$DESTDIR/usr/bin

PKGNAME="icalc.py" 
SCRIPT="icalc.py"
MANPAGE=$PKGNAME.1.gz

case $1 in 
  uninstall)
    rm $MANDIR/$MANPAGE $BINDIR/$PKGNAME
    ;;
  *)
    # help2man -n 'A calculator script written in python. The syntax is meant to be quick to write, minimising the necessity of parenthesis.'  \
    #    ./$SCRIPT | gzip - > $MANPAGE

    # TODO: install mods/


    mkdir -p $BINDIR
    chmod 644 $MANPAGE
    chmod 755 $SCRIPT
    cp $MANPAGE $MANDIR/$MANPAGE
    cp $SCRIPT $BINDIR/$PKGNAME
    ;;
esac;

