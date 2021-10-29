#!/usr/bin/env python2
#
# Creates all the dependencies from the org-mode files

from __future__ import print_function
from glob import glob

def main():
    C_FILES               =  []
    C_O_FILES             =  []
    F_FILES               =  []
    F_O_FILES             =  []
    FH_FUNC_FILES         =  []
    FH_TYPE_FILES         =  []
    H_FUNC_FILES          =  []
    H_TYPE_FILES          =  []
    H_PRIVATE_FUNC_FILES  =  []
    H_PRIVATE_TYPE_FILES  =  []
    C_TEST_FILES          =  []
    F_TEST_FILES          =  []
    TANGLED_FILES         =  []
    ORG_FILES             =  []
    TANGLED_FILES         =  []
    EXPORTED_FILES        =  []

    DEPS       =  {}
    DEPS_ORG   =  {}
    DEPS_TEST  =  {}
    TESTS      =  {}
    HTML       =  {}
    TEXT       =  {}
    DEPS_DOC   =  {}

    for org in glob("org/*.org"):
        i         =  org.split('/')[-1].rsplit(".",1)[0]
        tangled   =  "org/."+i+".tangled"
        exported  =  "org/."+i+".exported"
        c_test_x  =  "tests/test_"+i
        c_test_o  =  "tests/test_"+i+".$(OBJEXT)"
        f_test_o  =  "tests/test_"+i+"_f.$(OBJEXT)"
        c_test    =  "tests/test_"+i+".c"
        f_test    =  "tests/test_"+i+"_f.f90"
        html      =  "share/doc/qmckl/html/"+i+".html"
        text      =  "share/doc/qmckl/text/"+i+".txt"

        i="src/"+i

        c=i+".c"
        o=i+".$(OBJEXT)"
        h_func=i+"_func.h"
        h_type=i+"_type.h"
        h_private_func=i+"_private_func.h"
        h_private_type=i+"_private_type.h"
        f90=i+"_f.f90"
        fo=i+"_f.$(OBJEXT)"
        fh_func=i+"_fh_func.f90"
        fh_type=i+"_fh_type.f90"

        ORG_FILES      += [org]
        TANGLED_FILES  += [tangled]
        EXPORTED_FILES += [exported]
        DEPS_ORG[org] = tangled
        DEPS_DOC[org] = exported
        TEXT[org]     = text
        HTML[org]     = html

        grep = open(org, "r").read()

        if "(eval c)" in grep:
           C_FILES   += [c]
           C_O_FILES += [o]

           if c in DEPS:
               DEPS[c] += [tangled]
           else:
               DEPS[c] = [tangled]

           if o in DEPS:
               DEPS[o] += [c, "$(qmckl_h)"]
           else:
               DEPS[o] = [c, "$(qmckl_h)"]

        if "(eval h_func)" in grep:
            H_FUNC_FILES += [h_func]

            if h_func in DEPS:
                DEPS[h_func] += [tangled]
            else:
                DEPS[h_func] = [tangled]

        if "(eval h_type)" in grep:
            H_TYPE_FILES +=  [h_type]

            if h_type in DEPS:
                DEPS[h_type] += [tangled]
            else:
                DEPS[h_type]  = [tangled]

        if "(eval h_private_type)" in grep:
            H_PRIVATE_TYPE_FILES += [h_private_type]

            if h_private_type in DEPS:
                DEPS[h_private_type] += [tangled]
            else:
                DEPS[h_private_type]  = [tangled]

            if o in DEPS:
                DEPS[o] += [h_private_type]
            else:
                DEPS[o]  = [h_private_type]

        if "(eval h_private_func)" in grep:
            H_PRIVATE_FUNC_FILES += [h_private_func]

            if o in DEPS:
                DEPS[o] += [h_private_func]
            else:
                DEPS[o]  = [h_private_func]

            if h_private_func in DEPS:
                DEPS[h_private_func] += [tangled]
            else:
                DEPS[h_private_func]  = [tangled]

        if "(eval f)" in grep:
            F_FILES += [f90]

            if f90 in DEPS:
                DEPS[f90] += [tangled, "$(src_qmckl_fo)"]
            else:
                DEPS[f90]  = [tangled, "$(src_qmckl_fo)"]

            if fo in DEPS:
                DEPS[fo] += [f90, "$(src_qmckl_fo)"]
            else:
                DEPS[fo]  = [f90, "$(src_qmckl_fo)"]

        if "(eval fh_func)" in grep:
            FH_FUNC_FILES += [fh_func]

            if fh_func in DEPS:
                DEPS[fh_func] += [tangled]
            else:
                DEPS[fh_func]  = [tangled]

        if "(eval fh_type)" in grep:
            FH_TYPE_FILES += [fh_type]

            if fh_type in DEPS:
                DEPS[fh_type] += [tangled]
            else:
                DEPS[fh_type]  = [tangled]


        if "(eval c_test)" in grep:
            C_TEST_FILES += [c_test]

            if c_test in DEPS_TEST:
                DEPS_TEST[c_test] = [tangled]
            else:
                DEPS_TEST[c_test] = [tangled]

            if c_test_x in TESTS:
                TESTS[c_test_x] += [c_test, "$(qmckl_h)"]
            else:
                TESTS[c_test_x]  = [c_test, "$(qmckl_h)"]

        if "(eval f_test)" in grep:
            F_TEST_FILES += [f_test]

            if f_test in DEPS:
                DEPS_TEST[f_test] += [tangled, "$(test_qmckl_fo)"]
            else:
                DEPS_TEST[f_test]  = [tangled, "$(test_qmckl_fo)"]

            if c_test_x in TESTS:
                TESTS[c_test_x] += [f_test, "$(test_qmckl_fo)"]
            else:
                TESTS[c_test_x]  = [f_test, "$(test_qmckl_fo)"]

    output = ["",
              "## Source files",
              "",
              "ORG_FILES="+" ".join(ORG_FILES),
              "TANGLED_FILES="+" ".join(TANGLED_FILES),
              "EXPORTED_FILES="+" ".join(EXPORTED_FILES),
              "C_FILES="+" ".join(C_FILES),
              "F_FILES="+" ".join(F_FILES),
              "C_O_FILES="+" ".join(C_O_FILES),
              "FH_FUNC_FILES="+" ".join(FH_FUNC_FILES),
              "FH_TYPE_FILES="+" ".join(FH_TYPE_FILES),
              "H_FUNC_FILES="+" ".join(H_FUNC_FILES),
              "H_TYPE_FILES="+" ".join(H_TYPE_FILES),
              "H_PRIVATE_FUNC_FILES="+" ".join(H_PRIVATE_FUNC_FILES),
              "H_PRIVATE_TYPE_FILES="+" ".join(H_PRIVATE_TYPE_FILES),
              "C_TEST_FILES="+" ".join(C_TEST_FILES),
              "F_TEST_FILES="+" ".join(F_TEST_FILES),
              "TESTS="+" ".join(TESTS.keys()).replace("$(srcdir)/",""),
              "HTML_FILES="+" ".join(HTML.values()),
              "TEXT_FILES="+" ".join(TEXT.values()),
              "" ]

    output+= ["",
              "## Org-mode inherited dependencies",
              "",
              "if QMCKL_DEVEL" ]
    for f in DEPS_ORG.keys():
        output += [ DEPS_ORG[f] + ": "+f,
                    "\t$(tangle_verbose)top_builddir=$(top_builddir) srcdir=$(srcdir) $(srcdir)/tools/tangle.sh "+f,
                    "" ]
    output += [ "endif",
                "" ]

    output+= ["",
              "## Source dependencies",
              "",
              "if QMCKL_DEVEL" ]
    for f in sorted(DEPS.keys()):
        if DEPS[f][-1].endswith(".tangled"):
            output += [ f + ": " + " ".join(DEPS[f]) ]
    output += [ "endif",
                "$(src_qmckl_fo): $(src_qmckl_f)" ]
    for f in sorted(DEPS.keys()):
        if not DEPS[f][-1].endswith(".tangled"):
            output += [ f + ": " + " ".join(DEPS[f]) ]

    output+= ["",
              "## Test files",
              "",
              "$(test_qmckl_fo): $(test_qmckl_f)"]
    output += ["",
                "check_PROGRAMS = $(TESTS)" ]
    for f in sorted(TESTS.keys()):
        prefix = "tests_" + f.rsplit("/",1)[-1]
        output += [ prefix + "_SOURCES = " + \
                    " ".join(TESTS[f]).replace("$(srcdir)",""),
                    prefix + "_LDADD   = src/libqmckl.la",
                    prefix + "_LDFLAGS = -no-install",
                    "" ]

    tmp = "EXTRA_DIST += "
    for dir in glob("share/qmckl/test_data/*"):
      for f in glob("%s/*"%(dir)):
        tmp += " \\\n   "+f
    tmp += "\n"
    output += tmp.split("\n")

    output+= ["",
              "## Documentation",
              "",
              "if QMCKL_DEVEL" ]

    for f in sorted(ORG_FILES):
        output += [ HTML[f] + ": " + DEPS_DOC[f],
                    TEXT[f] + ":  " + DEPS_DOC[f],
                    "" ]

    for f in sorted(DEPS_DOC.keys()):
        output += [ DEPS_DOC[f] + ": " + f + " $(htmlize_el)",
                    "\t$(export_verbose)top_builddir=$(top_builddir) srcdir=$(srcdir) $(srcdir)/tools/build_doc.sh "+f,
                    "" ]
    output += ["endif"]

    f = open("generated.mk","w")
    f.write("\n".join(output))



if __name__ == "__main__":
    main()




