# make fake ctm
# CBL317-00498-XXXXXXXX-SE0004-en 1 aggregate 0.000 20.400 the common of problems there are all there are all those people follow through the best decreased are in a good position to offer them billion
{
    nitems = NF - 5;
    if ($5 > 0) {
        timeshift = ($5 - 0.1) / nitems;
        st = 0;
        en = timeshift;
        for (i=1;i<=nitems;i++) {            
            printf "%s 1 %.3f %.3f %s 0.500000\n", $1, st, timeshift, $(i+5);
            st = en;
            en += timeshift;
        }
    } else {
        printf "DEBUG: ERROR: %s\n", $0;
    }
}
